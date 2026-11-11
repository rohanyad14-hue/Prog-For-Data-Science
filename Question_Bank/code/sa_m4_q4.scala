//> using scala 2.13.12
//> using dep org.apache.spark::spark-sql:3.5.1
//> using javaOpt --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.net=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/sun.nio.cs=ALL-UNNAMED --add-opens=java.base/sun.security.action=ALL-UNNAMED --add-opens=java.base/sun.util.calendar=ALL-UNNAMED
// Sample answer M4-Q4: social-media analytics: how the driver, DAG scheduler and executors work, robustness, trending metrics
import scala.collection.mutable.ListBuffer
import scala.util.{Failure, Success, Try}

import org.apache.spark.scheduler.{SparkListener, SparkListenerStageCompleted}
import org.apache.spark.sql.{AnalysisException, DataFrame, SparkSession}
import org.apache.spark.sql.functions._

case class Post(UserID: String, PostType: String, Likes: Int)

object SocialMedia {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder().appName("social").master("local[2]")
      .config("spark.ui.enabled", "false").config("spark.driver.bindAddress", "127.0.0.1").config("spark.driver.host", "127.0.0.1")
      .config("spark.sql.shuffle.partitions", "4").config("spark.sql.adaptive.enabled", "false")
      .config("spark.sql.session.timeZone", "UTC").getOrCreate()
    val sc = spark.sparkContext
    sc.setLogLevel("ERROR")
    import spark.implicits._

    val stages = ListBuffer[String]()                                                        // what the scheduler reports
    sc.addSparkListener(new SparkListener {
      override def onStageCompleted(e: SparkListenerStageCompleted): Unit = stages.synchronized { stages += s"${e.stageInfo.numTasks} tasks" }
    })

    println("--- 1. the driver plans, the executors run the tasks ---")
    val posts = Seq(Post("U101", "Technology", 520), Post("U102", "Sports", 310), Post("U103", "Education", 750), Post("U104", "Technology", 640)).toDF()
    val byType = posts.groupBy("PostType").agg(count("*").as("posts"), sum("Likes").as("total_likes"), round(avg("Likes"), 1).as("avg_likes"), max("Likes").as("top_post"))
    stages.clear()
    byType.collect()                                                                         // one action = one job
    Thread.sleep(500)
    println("the scheduler split that job into " + stages.size + " stages, tasks per stage: " + stages.mkString(", ") + " (map side, then reduce side)")
    byType.orderBy(desc("total_likes")).show()
    println("the same aggregation as an RDD: the ShuffledRDD marks the stage boundary")
    println(posts.rdd.map(r => (r.getString(1), r.getInt(2))).reduceByKey(_ + _).toDebugString.linesIterator.map("  " + _).mkString("\n"))

    println("\n--- 2. growth in volume: more partitions, more parallel tasks, no code change ---")
    val big = spark.range(2000000L).select((col("id") % 4).as("bucket"), (rand(7) * 1000).cast("int").as("Likes"))
    for (parts <- Seq(1, 4)) println(parts + " partition(s): " + big.repartition(parts).groupBy("bucket").agg(sum("Likes")).orderBy("bucket").collect().length + " groups from " + big.count() + " rows")

    println("\n--- 3. failures and exception handling ---")
    def load(path: String): Option[DataFrame] = Try(spark.read.option("header", "true").csv(path)) match {
      case Success(df) => Some(df)
      case Failure(e: AnalysisException) => println("input " + path + " missing (" + e.getErrorClass + "): skip this source, keep the job alive"); None
      case Failure(e) => throw e
    }
    println("load result: " + load("posts_day1.csv").map(_.count()))
    val badLikes = sc.longAccumulator("unparsable likes")
    val likes = sc.parallelize(Seq("520", "310", "n/a", "750", "")).flatMap(s => Try(s.toInt).toOption.orElse { badLikes.add(1); None })
    println("valid like counts: " + likes.collect().toList + ", skipped: " + badLikes.value)

    println("\n--- 4. trending topics from (invented) timestamped posts ---")
    val feed = Seq(("U101", "2026-11-10 09:05:00", "Loving the new #spark release, great speed"),
                   ("U102", "2026-11-10 09:40:00", "Terrible match, bad refereeing #cricket"),
                   ("U103", "2026-11-10 10:10:00", "Great course on #spark and #scala"),
                   ("U104", "2026-11-10 10:30:00", "#spark job failed again, awful error"),
                   ("U101", "2026-11-10 10:50:00", "Happy with #scala great docs")).toDF("UserID", "time", "text")
    val tags = feed.withColumn("ts", to_timestamp(col("time")))
      .withColumn("tag", explode(expr("filter(split(lower(text), ' '), w -> w like '#%')")))
      .groupBy(window(col("ts"), "1 hour").getField("start").as("hour"), col("tag")).count()
    tags.orderBy("hour", "tag").show(false)
    val positive = Set("loving", "great", "happy", "good")
    val negative = Set("terrible", "bad", "awful", "failed")
    val sentiment = udf((t: String) => { val w = t.toLowerCase.split("\\W+"); w.count(positive) - w.count(negative) })
    feed.withColumn("score", sentiment(col("text"))).withColumn("label", when(col("score") > 0, "positive").when(col("score") < 0, "negative").otherwise("neutral"))
      .groupBy("label").count().orderBy("label").show()
    spark.stop()
  }
}
