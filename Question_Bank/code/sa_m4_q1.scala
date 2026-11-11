//> using scala 2.13.12
//> using dep org.apache.spark::spark-sql:3.5.1
//> using dep org.apache.spark::spark-mllib:3.5.1
//> using dep org.scalanlp::breeze:2.1.0
//> using javaOpt --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.net=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/sun.nio.cs=ALL-UNNAMED --add-opens=java.base/sun.security.action=ALL-UNNAMED --add-opens=java.base/sun.util.calendar=ALL-UNNAMED
// Sample answer M4-Q1: placement analytics with Spark (distributed work) and Breeze (local numerics)
import breeze.linalg.DenseVector
import breeze.stats.{mean, stddev}
import org.apache.spark.ml.classification.LogisticRegression
import org.apache.spark.ml.feature.VectorAssembler
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

object PlacementAnalytics {
  // Pearson correlation written with Breeze vector operations
  def pearson(a: DenseVector[Double], b: DenseVector[Double]): Double = {
    val ac = a - mean(a)
    val bc = b - mean(b)
    (ac dot bc) / math.sqrt((ac dot ac) * (bc dot bc))
  }

  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder().appName("placements").master("local[4]")
      .config("spark.ui.enabled", "false").config("spark.driver.bindAddress", "127.0.0.1").config("spark.driver.host", "127.0.0.1")
      .config("spark.sql.shuffle.partitions", "4").getOrCreate()
    val sc = spark.sparkContext
    sc.setLogLevel("ERROR")
    import spark.implicits._

    println("--- 1. architecture: the same code scales from 4 rows to 5 million rows ---")
    println("driver master: " + sc.master + " (a cluster manager URL such as yarn or k8s in production)")
    val big = spark.range(5000000L).select(col("id").as("StudentID"), (rand(1) * 40 + 60).as("Attendance"), (rand(2) * 5 + 5).as("CGPA"))
    println("5,000,000 synthetic students split into " + big.rdd.getNumPartitions + " partitions, one task per partition")
    val summary = big.agg(count("*"), round(avg("Attendance"), 1), round(avg("CGPA"), 1), round(corr("Attendance", "CGPA"), 3)).first()
    println("count, mean attendance, mean CGPA, correlation (independent random columns, so about 0): " + summary.toSeq.mkString(", "))
    println("physical plan of the aggregation (note the partial and final aggregate around one shuffle):")
    println(big.agg(avg("CGPA")).queryExecution.executedPlan.toString.linesIterator.map("  " + _).mkString("\n"))

    println("\n--- 2. the four rows of the question ---")
    val students = Seq(("S101", 92, 8.5, "Yes"), ("S102", 75, 6.8, "No"), ("S103", 88, 9.1, "Yes"), ("S104", 65, 5.9, "No"))
      .toDF("StudentID", "Attendance", "CGPA", "Placed")
    students.groupBy("Placed").agg(count("*").as("students"), avg("Attendance").as("avg_attendance"), avg("CGPA").as("avg_cgpa")).orderBy("Placed").show()

    println("--- 3. Breeze on the small aggregated result (single JVM, no cluster) ---")
    val rows = students.select("Attendance", "CGPA", "Placed").collect()          // only OK because the result is small
    val att = DenseVector(rows.map(_.getInt(0).toDouble))
    val cgpa = DenseVector(rows.map(_.getDouble(1)))
    val placed = DenseVector(rows.map(r => if (r.getString(2) == "Yes") 1.0 else 0.0))
    println(f"CGPA: mean ${mean(cgpa)}%.2f, std dev ${stddev(cgpa)}%.2f")
    println(f"correlation attendance~CGPA ${pearson(att, cgpa)}%.3f, CGPA~placed ${pearson(cgpa, placed)}%.3f, attendance~placed ${pearson(att, placed)}%.3f")
    println("z-scores of CGPA: " + ((cgpa - mean(cgpa)) /:/ stddev(cgpa)).toArray.map(z => f"$z%.2f").mkString(", "))

    println("\n--- 4. which factors influence placement? a model on the Spark side ---")
    val prepared = new VectorAssembler().setInputCols(Array("Attendance", "CGPA")).setOutputCol("features").transform(
      students.withColumn("label", when(col("Placed") === "Yes", 1.0).otherwise(0.0)))
    val model = new LogisticRegression().setRegParam(0.1).setStandardization(true).fit(prepared)
    println("coefficients (Attendance, CGPA): " + model.coefficients.toArray.map(c => f"$c%.3f").mkString(", ") + " | both positive, so both push towards 'placed'")
    model.transform(prepared).select("StudentID", "label", "prediction").show()
    spark.stop()
  }
}
