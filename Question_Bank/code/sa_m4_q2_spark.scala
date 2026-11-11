//> using scala 2.13.12
//> using dep org.apache.spark::spark-sql:3.5.1
//> using javaOpt --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.net=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/sun.nio.cs=ALL-UNNAMED --add-opens=java.base/sun.security.action=ALL-UNNAMED --add-opens=java.base/sun.util.calendar=ALL-UNNAMED
// Sample answer M4-Q2 (Spark part): the same patient data processed in parallel
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

object HospitalSpark {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder().appName("hospital").master("local[2]")
      .config("spark.ui.enabled", "false").config("spark.driver.bindAddress", "127.0.0.1").config("spark.driver.host", "127.0.0.1")
      .config("spark.sql.shuffle.partitions", "4").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    import spark.implicits._

    val patients = Seq(("P101", 45, 130, "Yes"), ("P102", 32, 120, "No"), ("P103", 58, 145, "Yes"), ("P104", 29, 118, "No"))
      .toDF("PatientID", "Age", "BloodPressure", "Diabetes")

    println("--- the DataFrame is split into partitions; each executor processes its partitions in parallel ---")
    val spread = patients.repartition(2, col("Diabetes"))                    // rows with the same key travel to the same partition
    spread.withColumn("partition", spark_partition_id()).orderBy("PatientID").show()

    println("--- abnormal records: rules and a statistical check ---")
    val flagged = patients
      .withColumn("bp_stage", when(col("BloodPressure") >= 140, "stage 2").when(col("BloodPressure") >= 130, "stage 1")
        .when(col("BloodPressure") >= 120, "elevated").otherwise("normal"))
      .withColumn("high_risk", col("Diabetes") === "Yes" && col("BloodPressure") >= 130)
    flagged.orderBy("PatientID").show()
    val stats = patients.agg(avg("BloodPressure").as("mean"), stddev_pop("BloodPressure").as("sd")).first()
    val (mu, sd) = (stats.getDouble(0), stats.getDouble(1))
    println(f"z-score of each BP (mean $mu%.1f, sd $sd%.1f): " + patients.orderBy("PatientID").select("BloodPressure").as[Int].collect().map(v => f"${(v - mu) / sd}%.2f").mkString(", "))

    println("--- the SQL view of the same question ---")
    patients.createOrReplaceTempView("patients")
    spark.sql("SELECT Diabetes, COUNT(*) AS patients, ROUND(AVG(BloodPressure), 1) AS avg_bp FROM patients GROUP BY Diabetes ORDER BY Diabetes").show()
    spark.stop()
  }
}
