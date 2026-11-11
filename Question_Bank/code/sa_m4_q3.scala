//> using scala 2.13.12
//> using dep org.apache.spark::spark-sql:3.5.1
//> using javaOpt --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.net=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/sun.nio.cs=ALL-UNNAMED --add-opens=java.base/sun.security.action=ALL-UNNAMED --add-opens=java.base/sun.util.calendar=ALL-UNNAMED
// Sample answer M4-Q3: a recommendation pipeline in Spark with exception handling and fault tolerance
import java.nio.file.{Files, Paths}
import java.util.concurrent.atomic.AtomicInteger

import scala.util.{Failure, Success, Try}

import org.apache.spark.{SparkException, TaskContext}
import org.apache.spark.scheduler.{SparkListener, SparkListenerTaskEnd}
import org.apache.spark.sql.{AnalysisException, SparkSession}
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._

object Recommender {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder().appName("recommender").master("local[2,3]")      // 2 threads; a task may fail 3 times before the job fails
      .config("spark.ui.enabled", "false").config("spark.driver.bindAddress", "127.0.0.1").config("spark.driver.host", "127.0.0.1")
      .config("spark.sql.shuffle.partitions", "4").getOrCreate()
    val sc = spark.sparkContext
    sc.setLogLevel("ERROR")
    import spark.implicits._

    val lines = Seq("CustomerID,Product,Amount", "C101,Laptop,65000", "C102,Mobile,25000", "C103,Laptop,70000", "C104,Tablet,18000",
                    "C105,Phone,abc", ",Tablet,100", "C106,Laptop")                         // the last three lines are damaged
    Files.write(Paths.get("transactions.csv"), lines.mkString("\n").getBytes("UTF-8"))

    println("--- 1. loading: a missing input is an exception at once ---")
    try spark.read.option("header", "true").csv("no_such_file.csv")
    catch { case e: AnalysisException => println("AnalysisException, error class " + e.getErrorClass) }

    println("\n--- 2. corrupted records: three parse modes ---")
    val schema = StructType(Seq(StructField("CustomerID", StringType), StructField("Product", StringType), StructField("Amount", DoubleType)))
    def read(mode: String, s: StructType = schema) = spark.read.option("header", "true").option("mode", mode).schema(s).csv("transactions.csv")
    println("count() only needs the row count, so Spark prunes the columns and never parses the bad values: " + read("DROPMALFORMED").count() + " rows")
    println("collect() parses everything: DROPMALFORMED keeps " + read("DROPMALFORMED").collect().length + " rows, PERMISSIVE keeps " + read("PERMISSIVE").collect().length + " rows")
    try read("FAILFAST").collect()
    catch { case e: SparkException => println("FAILFAST stops the job: " + e.getClass.getSimpleName) }

    val parsed = read("PERMISSIVE", StructType(schema.fields :+ StructField("_corrupt_record", StringType))).cache()
    val corrupt = parsed.filter(col("_corrupt_record").isNotNull)
    val good = parsed.filter(col("_corrupt_record").isNull && col("CustomerID").isNotNull && col("Amount") > 0).drop("_corrupt_record")
    println("dead-letter lines (unparsable): " + corrupt.select("_corrupt_record").as[String].collect().toList)
    println("rows failing a business rule (no customer id): " + parsed.filter(col("_corrupt_record").isNull && col("CustomerID").isNull).count())
    println("clean rows used for the model: " + good.count())

    println("\n--- 3. the same cleaning at RDD level with Try and an accumulator ---")
    val badCount = sc.longAccumulator("bad lines")
    val cleaned = sc.textFile("transactions.csv").filter(!_.startsWith("CustomerID")).flatMap { line =>
      Try { val Array(id, product, amount) = line.split(",", -1); (id, product, amount.toDouble) } match {
        case Success(t) if t._1.nonEmpty => Some(t)
        case _ => badCount.add(1); None
      }
    }
    println("good records: " + cleaned.count() + ", bad records skipped: " + badCount.value)

    println("\n--- 4. fault tolerance: one task fails on its first attempt, Spark re-runs it ---")
    val failedTasks = new AtomicInteger(0)
    sc.addSparkListener(new SparkListener {
      override def onTaskEnd(end: SparkListenerTaskEnd): Unit = if (end.taskInfo.failed) failedTasks.incrementAndGet()
    })
    val total = sc.parallelize(1 to 8, 4).map { x =>
      val ctx = TaskContext.get()
      if (ctx.partitionId() == 1 && ctx.attemptNumber() == 0) throw new RuntimeException("simulated executor failure")
      x * 10
    }.sum()
    Thread.sleep(1000)                                                                       // let the listener thread catch up
    println("result " + total + " (expected 360.0) after " + failedTasks.get() + " failed task attempt, re-run automatically from the lineage")

    println("\n--- 5. business insight and a first recommender ---")
    val popularity = good.groupBy("Product").agg(count("*").as("buyers"), sum("Amount").as("revenue"))
    popularity.orderBy(desc("revenue")).show()
    val candidates = good.select("CustomerID").distinct().crossJoin(popularity)
      .join(good.select("CustomerID", "Product"), Seq("CustomerID", "Product"), "left_anti")          // products the customer has not bought yet
    val rank = Window.partitionBy("CustomerID").orderBy(col("buyers").desc, col("revenue").desc)
    candidates.withColumn("rank", row_number().over(rank)).filter(col("rank") === 1)
      .select(col("CustomerID"), col("Product").as("recommended")).orderBy("CustomerID").show()
    spark.stop()
  }
}
