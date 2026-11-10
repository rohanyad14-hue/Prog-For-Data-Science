//> using scala 2.13.12
//> using dep org.apache.spark::spark-sql:3.5.1
//> using javaOpt --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.net=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/sun.nio.cs=ALL-UNNAMED --add-opens=java.base/sun.security.action=ALL-UNNAMED --add-opens=java.base/sun.util.calendar=ALL-UNNAMED
// Notes M4: Spark behaviours that exams like to probe (local mode, Spark 3.5.1)
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

case class Sale(region: String, product: String, amount: Double)

object N4Spark {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder().appName("notes").master("local[4]").config("spark.ui.enabled", "false")
      .config("spark.driver.bindAddress", "127.0.0.1").config("spark.driver.host", "127.0.0.1").getOrCreate()
    val sc = spark.sparkContext
    sc.setLogLevel("ERROR")
    import spark.implicits._

    println("--- partitions: the unit of parallelism ---")
    val nums = sc.parallelize(1 to 12, 4)
    println("glom shows the contents of each partition: " + nums.glom().collect().map(_.toList).toList)
    println("defaultParallelism (cores in local[4]) = " + sc.defaultParallelism + " | spark.sql.shuffle.partitions = " + spark.conf.get("spark.sql.shuffle.partitions"))
    println("repartition(2) -> " + nums.repartition(2).getNumPartitions + " (full shuffle, can increase) | coalesce(2) -> " + nums.coalesce(2).getNumPartitions + " (no shuffle, only decreases)")
    println("coalesce(8) cannot increase: " + nums.coalesce(8).getNumPartitions)

    println("\n--- narrow vs wide: look for the shuffle in the lineage ---")
    val pairs = sc.parallelize(Seq("a" -> 1, "b" -> 2, "a" -> 3, "b" -> 4, "a" -> 5), 2)
    println("map/filter chain (narrow):\n" + pairs.map(x => x).filter(_._2 > 1).toDebugString)
    println("reduceByKey (wide):\n" + pairs.reduceByKey(_ + _).toDebugString)
    println("reduceByKey = " + pairs.reduceByKey(_ + _).collect().toList.sorted + " | groupByKey.mapValues(sum) = " + pairs.groupByKey().mapValues(_.sum).collect().toList.sorted
      + "  (same answer; reduceByKey combines inside each partition first, so it shuffles less)")

    println("\n--- laziness: nothing runs until an action ---")
    val acc = sc.longAccumulator("seen")
    val mapped = sc.parallelize(1 to 100, 4).map { x => acc.add(1); x * 2 }
    println("after map: accumulator = " + acc.value)
    println("count() action: " + mapped.count() + " | accumulator now = " + acc.value)
    mapped.count()
    println("second action recomputes the lineage: accumulator = " + acc.value + " (200 = 2 x 100)")
    val cached = sc.parallelize(1 to 100, 4).map { x => acc.add(1); x * 2 }.cache()
    acc.reset(); cached.count(); cached.count()
    println("with cache(): two actions but only 100 map calls: accumulator = " + acc.value + " | storage level: " + cached.getStorageLevel.description)

    println("\n--- closures and shared variables ---")
    var counter = 0
    sc.parallelize(1 to 10, 2).foreach(x => counter += x)
    println("driver variable updated inside foreach: counter = " + counter + " (executors modified private copies; use an accumulator)")
    val sumAcc = sc.longAccumulator("sum")
    sc.parallelize(1 to 10, 2).foreach(x => sumAcc.add(x))
    println("accumulator gives the right total: " + sumAcc.value)
    val lookup = sc.broadcast(Map("a" -> "Alpha", "b" -> "Beta"))
    println("broadcast variable (read-only copy per executor): " + pairs.map { case (k, v) => (lookup.value(k), v) }.reduceByKey(_ + _).collect().toList.sorted)

    println("\n--- actions that bring data to the driver ---")
    val big = sc.parallelize(1 to 1000000, 8)
    println("count = " + big.count() + " | take(3) = " + big.take(3).toList + " | takeOrdered(3, desc) = " + big.takeOrdered(3)(Ordering[Int].reverse).toList + " | first = " + big.first())
    println("collect() would copy all 1,000,000 elements into the driver's memory - avoid on large data")
    println("sum of 1..1,000,000 with Int reduce = " + big.reduce(_ + _) + " (overflowed!) | with Long = " + big.map(_.toLong).reduce(_ + _) + " | max = " + big.max() + " | distinct count of x % 7 = " + big.map(_ % 7).distinct().count())

    println("\n--- DataFrame API vs SQL: same plan ---")
    val df = Seq(Sale("S", "pen", 10), Sale("S", "book", 40), Sale("N", "pen", 15), Sale("N", "pen", 5), Sale("W", "book", 25)).toDF()
    val viaApi = df.filter($"amount" >= 10).groupBy("region").agg(sum("amount").as("total"), count("*").as("n")).orderBy("region")
    df.createOrReplaceTempView("sales")
    val viaSql = spark.sql("SELECT region, SUM(amount) AS total, COUNT(*) AS n FROM sales WHERE amount >= 10 GROUP BY region ORDER BY region")
    println("API   : " + viaApi.collect().map(_.toSeq.mkString("/")).toList)
    println("SQL   : " + viaSql.collect().map(_.toSeq.mkString("/")).toList)
    println("same optimised plan: " + (viaApi.queryExecution.optimizedPlan.toString.replaceAll("#\\d+L?", "") == viaSql.queryExecution.optimizedPlan.toString.replaceAll("#\\d+L?", "")))
    println("schema: " + df.schema.fields.map(f => s"${f.name}:${f.dataType.simpleString}").mkString(", "))
    val ds = df.as[Sale]
    println("Dataset[Sale] is typed: " + ds.filter(_.amount > 20).map(_.product).collect().toList + " | a typo like _.amout fails at compile time, while $\"amout\" fails only at run time")
    val regions = Seq(("S", "South"), ("N", "North")).toDF("region", "label")
    println("join: " + df.join(regions, Seq("region"), "left").select("region", "label").distinct().orderBy("region").collect().map(_.toSeq.mkString("/")).toList + " | W has no match -> null label")
    println("broadcast join hint is applied by Catalyst for small tables: " + df.join(broadcast(regions), "region").queryExecution.executedPlan.toString.contains("BroadcastHashJoin"))

    println("\n--- RDD word count with sorting, and what a shuffle does to partition counts ---")
    val words = sc.parallelize(Seq("spark is fast", "spark is lazy", "scala runs spark", "fast is good"), 3).flatMap(_.split(" "))
    val wc = words.map((_, 1)).reduceByKey(_ + _)
    println("word count: " + wc.sortBy(r => (-r._2, r._1)).collect().toList + " | partitions before/after reduceByKey: " + words.getNumPartitions + "/" + wc.getNumPartitions)
    spark.stop()
  }
}
