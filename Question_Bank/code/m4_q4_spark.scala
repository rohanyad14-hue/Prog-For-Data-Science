//> using scala 2.13.12
//> using dep org.apache.spark::spark-sql:3.5.1
//> using javaOpt --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.net=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/sun.nio.cs=ALL-UNNAMED --add-opens=java.base/sun.security.action=ALL-UNNAMED --add-opens=java.base/sun.util.calendar=ALL-UNNAMED
// M4-Q4  Spark in local mode: RDD, lazy transformations vs actions, lineage, DataFrame + Catalyst plan
import org.apache.spark.sql.SparkSession

case class Emp(name: String, dept: String, salary: Double)

object M4Q4 {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder().appName("pds-demo").master("local[2]")
      .config("spark.ui.enabled", "false").config("spark.driver.bindAddress", "127.0.0.1")
      .config("spark.driver.host", "127.0.0.1").getOrCreate()
    val sc = spark.sparkContext
    sc.setLogLevel("ERROR")
    import spark.implicits._

    // ---- RDD word count: transformations build a DAG, the action runs it ----
    val lines = sc.parallelize(Seq("spark is fast", "spark is lazy", "scala runs spark"), 2)
    val counts = lines.flatMap(_.split(" ")).map(w => (w, 1)).reduceByKey(_ + _)
    println("partitions       : " + lines.getNumPartitions)
    println("lineage (DAG)    :\n" + counts.toDebugString)
    println("word counts      : " + counts.collect().sortBy(r => (-r._2, r._1)).toList)

    // ---- Laziness: an accumulator counts how often the map function really runs ----
    val calls = sc.longAccumulator("map calls")
    val doubled = sc.parallelize(1 to 10).map { x => calls.add(1); x * 2 }     // transformation only
    println("after map()      : map ran " + calls.value + " times   (nothing computed yet)")
    val total = doubled.reduce(_ + _)                                          // action
    println("after reduce()   : map ran " + calls.value + " times, result = " + total)

    // ---- DataFrame + Catalyst: look at the plans ----
    val df = Seq(Emp("Asha", "AI", 90000), Emp("Ravi", "DB", 70000),
                 Emp("Meena", "AI", 110000), Emp("Kabir", "DB", 65000)).toDF()
    val q = df.filter($"salary" > 68000).groupBy("dept").avg("salary").orderBy("dept")
    println("\nresult:")
    q.show()
    println("optimised logical plan and physical plan (excerpt):")
    val plan = q.queryExecution
    println(plan.optimizedPlan.toString.linesIterator.map("  " + _).mkString("\n"))
    println(plan.executedPlan.toString.linesIterator.map("  " + _).mkString("\n"))

    // ---- Catalyst rules visible: two Filters merge into one; cast(5 as bigint) folds to 5 ----
    val r = spark.range(100).filter($"id" > 10).filter($"id" < 50).select(($"id" * (2 + 3)).as("x"))
    val show = (s: String) => s.linesIterator.map("  " + _).mkString("\n")
    println("\nanalysed plan (as written):\n" + show(r.queryExecution.analyzed.toString))
    println("optimised plan (after Catalyst):\n" + show(r.queryExecution.optimizedPlan.toString))
    println("rows kept: " + r.count())
    spark.stop()
  }
}
