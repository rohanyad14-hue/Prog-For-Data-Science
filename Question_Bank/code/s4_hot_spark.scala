//> using scala 2.13.12
//> using dep org.apache.spark::spark-sql:3.5.1
//> using dep org.apache.spark::spark-mllib:3.5.1
//> using dep org.scalanlp::breeze:2.1.0
//> using javaOpt --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.net=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/sun.nio.cs=ALL-UNNAMED --add-opens=java.base/sun.security.action=ALL-UNNAMED --add-opens=java.base/sun.util.calendar=ALL-UNNAMED
// Sample HOT questions, Module 4: Spark + Breeze answers (local mode, Spark 3.5.1)
import breeze.linalg.{DenseVector, norm}
import breeze.stats.{mean => bmean, stddev => bstd}
import org.apache.spark.TaskContext
import org.apache.spark.ml.classification.LogisticRegression
import org.apache.spark.ml.feature.VectorAssembler
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions._
import scala.util.{Failure, Success, Try}

case class Rec(StudentID: String, Attendance: Int, CGPA: Double, Placed: String)
case class Patient(PatientID: String, Age: Int, BP: Int, Diabetes: String)
case class Txn(customer: String, product: String, amount: Int)
case class Post(UserID: String, PostType: String, Likes: Int)
case class Loan(CustomerID: String, Income: Double, Loan: Double, Status: String)

object S4HotSpark {
  def pearson(x: DenseVector[Double], y: DenseVector[Double]): Double = {
    val xm = x - bmean(x); val ym = y - bmean(y)
    (xm dot ym) / (norm(xm) * norm(ym))
  }

  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder().appName("hot4").master("local[4,4]").config("spark.ui.enabled", "false")
      .config("spark.driver.bindAddress", "127.0.0.1").config("spark.driver.host", "127.0.0.1").getOrCreate()
    val sc = spark.sparkContext
    sc.setLogLevel("ERROR")
    import spark.implicits._

    println("--- Q1 step 1: the four sample rows with Spark SQL ---")
    val s = Seq(Rec("S101", 92, 8.5, "Yes"), Rec("S102", 75, 6.8, "No"), Rec("S103", 88, 9.1, "Yes"), Rec("S104", 65, 5.9, "No")).toDF()
    s.groupBy("Placed").agg(count("*").as("n"), round(avg("CGPA"), 2).as("avg_cgpa"), round(avg("Attendance"), 1).as("avg_attendance")).orderBy("Placed").show()
    println("Spark correlation(Attendance, CGPA) = " + "%.4f".format(s.stat.corr("Attendance", "CGPA")))

    println("--- Q1 step 2: Breeze statistics on the same columns ---")
    val att = DenseVector(92.0, 75.0, 88.0, 65.0); val cgpa = DenseVector(8.5, 6.8, 9.1, 5.9); val placed = DenseVector(1.0, 0.0, 1.0, 0.0)
    println(f"mean CGPA ${bmean(cgpa)}%.3f, std CGPA ${bstd(cgpa)}%.3f, mean attendance ${bmean(att)}%.2f")
    println(f"Pearson(att, cgpa) = ${pearson(att, cgpa)}%.4f | point-biserial(cgpa, placed) = ${pearson(cgpa, placed)}%.4f | (att, placed) = ${pearson(att, placed)}%.4f")
    val z = (cgpa - bmean(cgpa)) / bstd(cgpa)
    println("z-scores of CGPA: " + z.toArray.map(v => f"$v%.2f").mkString(", "))

    println("--- Q1 step 3: MLlib logistic regression (code path only: 4 rows cannot support conclusions) ---")
    val feats = new VectorAssembler().setInputCols(Array("Attendance", "CGPA")).setOutputCol("features").transform(s.withColumn("label", when($"Placed" === "Yes", 1.0).otherwise(0.0)))
    val lrm = new LogisticRegression().setMaxIter(50).setRegParam(0.1).fit(feats)
    println("coefficients (Attendance, CGPA): " + lrm.coefficients.toArray.map(v => f"$v%.3f").mkString(", ") + " | predictions: " + lrm.transform(feats).select("prediction").as[Double].collect().toList)

    println("--- Q1 step 4: the same code on 5,000,000 synthetic students ---")
    val big = spark.range(5000000L).select(($"id" % 10000).cast("string").as("sid"), (lit(50) + rand(1) * 50).as("Attendance"), (lit(5) + rand(2) * 5).as("CGPA"))
      .withColumn("Placed", when(rand(3) < ($"CGPA" - 5) / 5, 1.0).otherwise(0.0))
    println("partitions: " + big.rdd.getNumPartitions + " | rows: " + big.count())
    big.groupBy("Placed").agg(round(avg("CGPA"), 3).as("avg_cgpa"), round(avg("Attendance"), 2).as("avg_att"), count("*").as("n")).orderBy("Placed").show()
    println("correlation(CGPA, Placed) over 5M rows = " + "%.3f".format(big.stat.corr("CGPA", "Placed")) + " | correlation(Attendance, Placed) = " + "%.3f".format(big.stat.corr("Attendance", "Placed")) + "   (synthetic data: placement was generated from CGPA only)")

    println("--- Q2 Spark part: abnormal patient records ---")
    val p = Seq(Patient("P101", 45, 130, "Yes"), Patient("P102", 32, 120, "No"), Patient("P103", 58, 145, "Yes"), Patient("P104", 29, 118, "No")).toDF()
    p.createOrReplaceTempView("patients")
    spark.sql("SELECT PatientID, Age, BP FROM patients WHERE BP >= 140 OR Age >= 55 ORDER BY BP DESC").show()
    p.groupBy("Diabetes").agg(count("*").as("n"), round(avg("BP"), 1).as("avg_bp"), round(avg("Age"), 1).as("avg_age")).orderBy("Diabetes").show()
    println("partitions used: " + p.rdd.getNumPartitions + " (each partition would sit on a different hospital server in a cluster)")

    println("--- Q3 step 1: parsing raw lines with Either, counting good and bad records ---")
    val raw = sc.parallelize(Seq("C101,Laptop,65000", "C102,Mobile,25000", "C103,Laptop,70000", "C104,Tablet,18000", "C105,Mobile,abc", "C106,,5000", "broken line", "C107,Laptop,-100"), 3)
    def parse(line: String): Either[String, Txn] = line.split(",", -1).map(_.trim) match {
      case Array(c, pr, a) if pr.nonEmpty => Try(a.toInt).toEither.left.map(_ => s"non-numeric amount in '$line'").flatMap(v => if (v > 0) Right(Txn(c, pr, v)) else Left(s"non-positive amount in '$line'"))
      case Array(_, _, _)                  => Left(s"missing product in '$line'")
      case _                               => Left(s"wrong number of fields in '$line'")
    }
    val parsed = raw.map(parse).cache()
    val good = parsed.collect { case Right(t) => t }
    val bad = parsed.collect { case Left(e) => e }.collect().toList
    println(s"good records: ${good.count()} | rejected: ${bad.size}")
    bad.foreach(b => println("  rejected -> " + b))
    println("revenue by product (good records only): " + good.map(t => (t.product, t.amount)).reduceByKey(_ + _).collect().toList.sorted)

    println("--- Q3 step 2: item co-purchase counts for a simple recommender (illustrative baskets) ---")
    val baskets = sc.parallelize(Seq("C101" -> List("Laptop", "Mouse"), "C102" -> List("Mobile", "Earbuds"), "C103" -> List("Laptop", "Mouse", "Bag"), "C104" -> List("Tablet", "Cover"), "C105" -> List("Mobile", "Earbuds", "Cover")))
    val pairs = baskets.flatMap { case (_, items) => for (a <- items; b <- items if a != b) yield ((a, b), 1) }.reduceByKey(_ + _)
    val rec = pairs.map { case ((a, b), n) => (a, (b, n)) }.groupByKey().mapValues(_.toList.sortBy(x => (-x._2, x._1)).take(2)).collect().toMap
    println("also bought with Laptop: " + rec("Laptop") + " | with Mobile: " + rec("Mobile") + " | with Cover: " + rec("Cover"))

    println("--- Q3 step 3: fault tolerance, a task that fails on its first attempt is re-run ---")
    val flaky = sc.parallelize(1 to 8, 4).mapPartitionsWithIndex { (idx, it) =>
      val ctx = TaskContext.get()
      if (idx == 2 && ctx.attemptNumber() == 0) throw new RuntimeException("simulated executor failure")      // partition 2 fails on its first attempt
      Iterator((idx, ctx.attemptNumber(), it.map(_ * 10).toList))
    }
    val res = flaky.collect().toList.sortBy(_._1)
    println("(partition, attempt that succeeded, values): " + res.mkString(" "))
    println("every partition is present, and partition 2 succeeded on attempt 1 (its second try); master local[4,4] allows 4 attempts per task, spark.task.maxFailures = " + sc.getConf.get("spark.task.maxFailures", "4"))

    println("--- Q4 step 1: engagement by post type ---")
    val posts = Seq(Post("U101", "Technology", 520), Post("U102", "Sports", 310), Post("U103", "Education", 750), Post("U104", "Technology", 640)).toDF()
    posts.groupBy("PostType").agg(count("*").as("posts"), sum("Likes").as("total_likes"), round(avg("Likes"), 1).as("avg_likes")).orderBy(desc("total_likes")).show()
    println("--- Q4 step 2: lexicon-based sentiment of post text (illustrative texts) ---")
    val texts = Seq(("U101", "Technology", "love the new phone great battery"), ("U102", "Sports", "terrible match boring and slow"), ("U103", "Education", "great course love the teacher"), ("U104", "Technology", "slow app bad update")).toDF("UserID", "PostType", "text")
    val lex = Seq(("love", 1), ("great", 1), ("terrible", -1), ("boring", -1), ("slow", -1), ("bad", -1)).toDF("word", "score")
    val senti = texts.withColumn("word", explode(split($"text", " "))).join(lex, "word").groupBy("UserID", "PostType").agg(sum("score").as("sentiment"))
    senti.orderBy("UserID").show()
    senti.groupBy("PostType").agg(round(avg("sentiment"), 2).as("avg_sentiment")).orderBy(desc("avg_sentiment")).show()
    println("--- Q4 step 3: trending = growth between time windows, not the biggest total (illustrative hourly counts) ---")
    val hourly = Seq(("Technology", 1, 100), ("Technology", 2, 130), ("Sports", 1, 40), ("Sports", 2, 160), ("Education", 1, 90), ("Education", 2, 95)).toDF("topic", "hour", "mentions")
    val w = Window.partitionBy("topic").orderBy("hour")
    hourly.withColumn("prev", lag("mentions", 1).over(w)).where($"prev".isNotNull).withColumn("growth_%", round(($"mentions" - $"prev") / $"prev" * 100, 1)).select("topic", "prev", "mentions", "growth_%").orderBy(desc("growth_%")).show()

    println("--- Q5 step 1: loan-to-income ratio in Spark and Breeze ---")
    val loans = Seq(Loan("L101", 650000, 300000, "Approved"), Loan("L102", 350000, 400000, "Rejected"), Loan("L103", 800000, 500000, "Approved"), Loan("L104", 250000, 350000, "Rejected")).toDF()
    val withR = loans.withColumn("LTI", round($"Loan" / $"Income", 3))
    withR.select("CustomerID", "LTI", "Status").show()
    withR.groupBy("Status").agg(round(avg("LTI"), 3).as("avg_LTI"), round(avg("Income"), 0).as("avg_income"), count("*").as("n")).orderBy("Status").show()
    val inc = DenseVector(650000.0, 350000.0, 800000.0, 250000.0); val ln = DenseVector(300000.0, 400000.0, 500000.0, 350000.0)
    val lti = ln /:/ inc
    println("Breeze element-wise ratio: " + lti.toArray.map(v => f"$v%.3f").mkString(", ") + f" | mean ${bmean(lti)}%.3f | std ${bstd(lti)}%.3f | corr(income, loan) = ${pearson(inc, ln)}%.3f")
    withR.createOrReplaceTempView("loans")
    spark.sql("SELECT CustomerID, CASE WHEN LTI > 1.0 THEN 'HIGH' WHEN LTI > 0.5 THEN 'MEDIUM' ELSE 'LOW' END AS risk FROM loans ORDER BY CustomerID").show()
    spark.stop()
  }
}
