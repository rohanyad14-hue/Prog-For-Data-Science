from dsl import *
from notes_util import NOISE, between, pick

# =====================================================================================================
sub_4_1 = SUB("4.1", "Breeze (numerical computing)", [
    B(["Breeze (`org.scalanlp::breeze`) is Scala's numerical library: `DenseVector`, `DenseMatrix`, linear algebra (`inv`, `det`, `eigSym`, `svd`, solve with `\\`), statistics (`breeze.stats.mean/variance`) and optimisation.",
       "Operators: `+ -` element-wise; <b>`*:*` element-wise product</b>; `*` is the <b>matrix product</b> for matrices (and scalar scaling for vectors); `dot` inner product; `.t` transpose; `A \\ b` solves A x = b.",
       "Indexing is 0-based with parentheses: `v(0 to 1)`, `m(::, 0)` (a column), `m(1, ::)` (a row). Broadcasting uses `*`: `m(*, ::) - rowVector`.",
       "`variance` is the <b>sample</b> variance (divides by n - 1), like `np.var(ddof=1)`.",
       "Dependency (sbt): `\"org.scalanlp\" %% \"breeze\" % \"2.1.0\"` (tested version)."]),
    OUT("n4_try_breeze.out.txt", "Verified output", transform=pick("Breeze:")),
    OUT("m4_q2_breeze.out.txt", "Lab 19 revenue calculation (question bank M4-C2)", transform=lambda t: "\n".join(l for l in t.split("\n") if not l.startswith(NOISE))),
    QA("Compute the total revenue per fruit with Breeze (price times quantity).", [
        SNIP("val revenue = price *:* qty        // element-wise product\nsum(revenue)", lang="scala", caption="Lab 19, run in the question bank: Apple 375.00 ... Orange 400.00, total 1840.00")], "3 marks"),
    QA("Difference between `*:*` and `*` in Breeze.", [P("`*:*` multiplies element by element (matrix `m *:* m` gives 1, 4, 9, 16 in the output); `*` on two matrices is the matrix product (7, 10, 15, 22). `dot` on vectors gives the scalar inner product.")], "tricky"),
    QA("Solve 2x + y = 3, x + 3y = 5 with Breeze.", [P("`DenseMatrix((2.0, 1.0), (1.0, 3.0)) \\ DenseVector(3.0, 5.0)` gives x = 0.8, y = 1.4 (Lab 19 run).")], "3 marks"),
    QA("How do you do PCA in Breeze?", [P("Centre the columns, form the covariance `(Xc.t * Xc) / (n - 1.0)`, and call `eigSym`. The output reproduces the Python result: eigenvalues 0.8783 and 5.6217 (ascending order in Breeze), largest-variance ratio 0.8649. "
                                          "Breeze returns eigenvalues in ascending order, NumPy's `eigh` too, so reverse them before reading PC1.")], "tricky"),
])

sub_4_2 = SUB("4.2", "Saddle (data frames) and Spire (exact numerics)", [
    B(["Saddle gives indexed, array-backed data structures: `Vec` (1-D), `Index` (labels), `Series` (Vec + Index), `Frame` (columns of aligned Series), with automatic alignment on labels and NA handling (NaN for Double). It is Scala's small pandas.",
       "Workflow of Lab 18: build a Frame, filter rows with a boolean mask, take the column, compute `mean`; charts with Vegas are declarative (data + encodings + mark) and need a notebook/browser.",
       "The original `org.scala-saddle` artifacts on Maven Central stop at Scala 2.11; the tested program uses the maintained fork `io.github.pityka::saddle-core:4.0.0-M14` on Scala 2.13 (needs `import org.saddle.ops.BinOps._` for `Vec * Vec`).",
       "<b>Spire</b> provides generic and exact numeric types: `Rational`, `Algebraic`, `Complex`, and type classes. Use it when floating-point error is unacceptable."]),
    OUT("m4_q3_saddle.out.txt", "Verified output (Saddle)"),
    OUT("m4_q2_breeze.out.txt", "Verified output (last line: Spire)", transform=lambda t: t.split("\n")[-1]),
    QA("Filter the apple rows and compute the average apple price in Saddle.", [P("Build a boolean `Vec` with `fruit.map(_ == \"Apple\")`, take its positions with `find(identity)`, then `price.take(positions).mean`. Output: prices 2.4, 2.65, 2.5, 3.1; average 2.6625.")], "5 marks"),
    QA("How does Saddle treat missing values?", [P("As NA (NaN for doubles). Statistics skip them: the mean of `Vec(2.0, NaN, 4.0)` is 3.0 and the count is 2 (output).")], "2 marks"),
    QA("Why use Spire's `Rational` instead of `Double`?", [P("`0.1 + 0.2` in `Double` is `0.30000000000000004`; `Rational(1,10) + Rational(2,10)` equals exactly `3/10` (output). Rationals are exact but slower.")], "3 marks"),
    QA("Compare Breeze, Saddle and Spire.", [T(["", "Breeze", "Saddle", "Spire"], [["Purpose", "linear algebra, statistics", "labelled data tables, NA handling", "exact, generic numbers"], ["Main types", "`DenseVector`, `DenseMatrix`", "`Vec`, `Series`, `Frame`", "`Rational`, `Algebraic`"],
                                                                                    ["Python analogue", "NumPy/SciPy", "pandas", "`fractions`, `decimal`"]], [0.2, 0.27, 0.27, 0.26])], "3 marks"),
])

sub_4_3 = SUB("4.3", "Exception handling in Scala", [
    B(["`try { ... } catch { case e: IOException => ... } finally { ... }`. `try` is an <b>expression</b> with a value; `catch` takes pattern-matching cases; the first matching case wins; <b>no checked exceptions</b>.",
       "Custom exception: `class MyEx(msg: String) extends Exception(msg)`; `throw new MyEx(\"...\")` has type `Nothing`.",
       "Functional style: `Option` (absence), `Try` (`Success`/`Failure`, wraps code that may throw; `map`, `flatMap`, `recover`, `recoverWith`, `getOrElse`, `toOption`), `Either` (`Left` = error, `Right` = value; the error can carry information).",
       "`scala.util.control.NonFatal` matches ordinary exceptions but not fatal ones (`OutOfMemoryError`, `StackOverflowError`); never swallow fatal errors. `Try` does not catch them.",
       "`scala.util.Using` closes resources automatically (like Java try-with-resources or Python `with`)."]),
    OUT("n4_try_breeze.out.txt", "Verified output", transform=pick("try/catch", "catch order", "Try:", "Either", "Using")),
    OUT("m4_q1_exceptions.out.txt", "Question bank M4-C1 program output"),
    QA("What is printed first for `f(2)`: the `finally` message or the returned value, and what does `f(0)` return?", [P("The `finally` message prints first, then the caller prints `f(2) = 5`; `f(0)` catches `ArithmeticException` and returns -1 (output). `finally` runs before the value is handed back.")], "predict the output"),
    QA("`NumberFormatException` is a subclass of `IllegalArgumentException`. In which order should the cases be written?", [P("Most specific first. If `case e: IllegalArgumentException` comes before `case e: NumberFormatException` the latter is unreachable (the output shows `\"x\"` handled by the first handler).")], "tricky"),
    QA("Differentiate `Option`, `Try` and `Either`.", [T(["", "Cases", "Use"], [["`Option`", "`Some` / `None`", "absence only"], ["`Try`", "`Success` / `Failure(ex)`", "code that may throw"], ["`Either`", "`Right(v)` / `Left(err)`", "typed, informative errors"]], [0.2, 0.4, 0.4])], "5 marks"),
    QA("What does a for-comprehension over `Try` do when the second step fails?", [P("It stops and returns that `Failure`; later steps do not run (output: `Failure(NumberFormatException: For input string: \"oops\")`).")], "3 marks"),
    QA("Does `Try(parse(\"x\").get)` throw?", [P("`parse(\"x\")` is only a `Failure` value; calling `.get` on a `Failure` re-throws the stored exception, and the outer `Try` captures it (a `NumberFormatException`). Avoid `.get`; use `getOrElse`, `fold`, `recover`.")], "tricky"),
    QA("Why is catching `Throwable` or `Exception` blindly a bad idea?", [P("It hides programming errors and (for Throwable) fatal JVM errors. Catch specific exceptions or use `NonFatal`; `NonFatal(StackOverflowError)` is false (output).")], "3 marks"),
])

sub_4_4 = SUB("4.4", "Big data and Apache Spark: why Spark", [
    B(["Big data: characterised by volume, velocity, variety (and veracity, value). One machine cannot store or process it fast enough, so work is split over a cluster.",
       "<b>Hadoop MapReduce</b> writes intermediate results to disk between map and reduce steps. <b>Spark</b> plans a DAG of operations and keeps intermediate data in memory where possible; it also unifies batch, SQL, streaming, machine learning and graphs.",
       "Spark is written in Scala and runs on the JVM; APIs exist for Scala, Java, Python (PySpark), R and SQL. Main abstractions: RDD (low level), DataFrame/Dataset (structured, optimised).",
       "Modes: local (one JVM, used for the tests in these notes), standalone, YARN, Kubernetes. The current Spark release line is 4.x; the labs and textbooks use 3.x, and the concepts here are the same."]),
    QA("Why is Spark often faster than Hadoop MapReduce?", [P("It avoids writing intermediate data to disk by caching in memory, optimises the whole job as a DAG, and reuses datasets in iterative algorithms (machine learning) instead of re-reading from disk each pass.")], "3 marks"),
    QA("What are the V's of big data?", [P("Volume (size), Velocity (arrival speed), Variety (structured, semi-structured, unstructured); often Veracity (quality) and Value.")], "2 marks"),
    QA("Why is Scala a natural fit for Spark?", [P("Spark itself is written in Scala, the Scala API is the most complete and has no cross-language serialisation overhead; Dataset typed operations and Catalyst use Scala features such as case classes and pattern matching.")], "2 marks"),
])

sub_4_5 = SUB("4.5", "Spark architecture", [
    DIAGRAM("spark", "Driver, cluster manager and executors."),
    B(["<b>Driver</b>: runs your `main`, holds the `SparkSession`/`SparkContext`, converts actions into jobs, stages and tasks (DAG scheduler), schedules tasks, collects results. It must stay alive for the whole application.",
       "<b>Cluster manager</b>: allocates resources (Standalone, YARN, Kubernetes). <b>Worker nodes</b> run <b>executors</b> (JVM processes) that execute tasks and cache partitions.",
       "<b>Application > job > stage > task</b>: each action creates a job; a job is cut into stages at shuffle boundaries; a stage has one task per partition.",
       "<b>Partition</b> = slice of a dataset, the unit of parallelism. A task processes one partition."]),
    OUT("n4_spark_traps.out.txt", "Verified output (local[4])", transform=pick("partitions: the unit")),
    QA("Draw and explain Spark's architecture.", [P("The diagram above: the driver talks to the cluster manager to obtain executors, then sends tasks directly to the executors and receives results. Executors hold cached data. Explain each box in one sentence and mention the DAG scheduler.")], "10 marks"),
    QA("What is the difference between a job, a stage and a task?", [P("Job: triggered by one action. Stage: a set of operations that run without a shuffle. Task: one stage on one partition; with 4 partitions a stage runs 4 tasks (the output shows `parallelize(1 to 12, 4)` split into four partitions of three numbers).")], "3 marks"),
    QA("`repartition(2)` versus `coalesce(2)`; can `coalesce(8)` increase partitions?", [P("`repartition` does a full shuffle and can increase or decrease the count; `coalesce` merges partitions without a full shuffle and can only decrease. `coalesce(8)` on 4 partitions stays 4 (output).")], "tricky"),
    QA("What does `spark.sql.shuffle.partitions = 200` mean?", [P("After a shuffle in the DataFrame API (join, groupBy) the result has 200 partitions by default, even for tiny data; tune it, or let Adaptive Query Execution merge small partitions.")], "3 marks"),
    QA("Client mode versus cluster mode.", [P("In client mode the driver runs on the machine that submitted the application (convenient for interactive work); in cluster mode the driver runs inside the cluster (survives the client disconnecting, used in production).")], "3 marks"),
])

sub_4_6 = SUB("4.6", "RDDs, transformations, actions and lazy evaluation (tricky topic)", [
    B(["<b>RDD</b> = Resilient Distributed Dataset: partitioned across the cluster, <b>immutable</b>, typed, recoverable. Created by `sc.parallelize(...)`, `sc.textFile(...)` or by transforming another RDD.",
       "<b>Transformations</b> (lazy; return a new RDD): `map`, `filter`, `flatMap`, `distinct`, `union`, `reduceByKey`, `groupByKey`, `join`, `sortBy`. <b>Actions</b> (eager; return a value or write data): `count`, `collect`, `take`, `first`, `reduce`, `foreach`, `saveAsTextFile`.",
       "<b>Lazy evaluation</b>: transformations only extend the <b>lineage</b> (the DAG); an action triggers computation. Each new action recomputes the lineage unless the RDD is `cache()`d/`persist()`ed.",
       "<b>Fault tolerance</b>: a lost partition is recomputed from its lineage, so no data replication is needed. `toDebugString` shows the lineage.",
       "<b>Narrow</b> dependencies (map, filter, flatMap): each output partition depends on one input partition, pipelined in one stage. <b>Wide</b> (reduceByKey, groupByKey, join, distinct, repartition): data is shuffled across the network, which starts a new stage and is the main cost."]),
    OUT("n4_spark_traps.out.txt", "Verified output", transform=pick("narrow vs wide", "laziness")),
    QA("An accumulator is incremented inside `map`. What does it read after `map`, after `count()`, and after a second `count()`?", [
        P("0, 100, 200. `map` did nothing (lazy); the first action ran the function for 100 elements; the second action recomputed the whole lineage. With `cache()` two actions gave only 100 calls (output).")], "tricky"),
    QA("Why does `reduceByKey` shuffle less than `groupByKey` for the same answer?", [P("`reduceByKey` first combines values inside each partition (map-side combine) so only partial sums cross the network; `groupByKey` ships every value. Both returned `(a,9), (b,6)` in the output.")], "tricky"),
    QA("Define RDD and its four properties; explain how lineage gives fault tolerance.", [P("Resilient, Distributed, Dataset, Immutable. Each RDD records its parent and the function applied; if an executor fails, only the lost partitions are rebuilt by re-running those steps from the source data, with no replication cost during normal running.")], "5 marks"),
    QA("Name three transformations and three actions and say why laziness helps.", [P("Transformations: `map`, `filter`, `reduceByKey`. Actions: `count`, `collect`, `saveAsTextFile`. Because nothing runs before an action, Spark sees the whole plan, pipelines narrow steps into one pass, avoids storing intermediate results and can skip unused work.")], "5 marks"),
    QA("Why can `collect()` crash the driver?", [P("It copies the entire dataset into the driver's memory. Use `take(n)`, `takeOrdered`, aggregations, or write results to storage. The output uses `take(3)` on a 1,000,000-element RDD.")], "3 marks"),
    QA("What does `glom()` show, and how many partitions does a shuffle produce?", [P("`glom()` turns each partition into an array so you can see how data is split: `List(1,2,3), List(4,5,6), ...`. For RDDs a shuffle such as `reduceByKey` keeps the parent partition count unless you pass `numPartitions` (3 before and after in the output). For DataFrames it is `spark.sql.shuffle.partitions` (200).")], "3 marks"),
    QA("What does persisting an RDD do and what is its default storage level?", [P("`cache()` keeps the computed partitions in memory (`MEMORY_ONLY`, shown as 'Memory Deserialized 1x Replicated') so later actions skip recomputation; use `persist(StorageLevel.MEMORY_AND_DISK)` for data that may not fit.")], "3 marks"),
])

sub_4_7 = SUB("4.7", "Shared variables and closures (tricky topic)", [
    B(["Code inside `foreach`/`map` runs on executors in separate JVMs. The closure (including captured variables) is <b>serialised and copied</b> to each task, so modifying a driver variable from there does not update the driver's copy.",
       "<b>Accumulators</b>: write-only-from-tasks counters that the driver can read (`sc.longAccumulator`). Reliable only when updated inside actions; updates inside transformations may repeat if a stage re-runs.",
       "<b>Broadcast variables</b>: a read-only value sent once to each executor (lookup tables) instead of shipping it with every task."]),
    OUT("n4_spark_traps.out.txt", "Verified output", transform=pick("closures")),
    QA("`var counter = 0; rdd.foreach(x => counter += x)`: what is `counter` on the driver afterwards?", [P("0 (output). Each task incremented its own deserialised copy. Use an accumulator: `sc.longAccumulator(\"sum\")` gave 55 for 1 to 10. Spark's guide warns that behaviour of such code is undefined; in local mode it may even appear to work in some set-ups, so never rely on it.")], "tricky"),
    QA("When do you use a broadcast variable?", [P("For a medium-sized read-only table used by many tasks (country codes, a lookup map). It is shipped once per executor rather than once per task. The output maps keys to names with `lookup.value(k)`.")], "3 marks"),
    QA("Why can accumulator values be wrong when used inside transformations?", [P("A task may be re-executed (failure, speculation, or recomputation without cache), applying the update again. In the output the second `count()` doubled the value to 200.")], "tricky"),
])

sub_4_8 = SUB("4.8", "Spark SQL, DataFrames, Datasets and Catalyst", [
    B(["A <b>DataFrame</b> is a distributed table with a schema; a <b>Dataset[T]</b> adds compile-time types (case classes). Both are optimised by <b>Catalyst</b> and executed with Tungsten (compact binary memory and generated code). The Spark quick-start recommends them over raw RDDs.",
       "DataFrame API and SQL (`createOrReplaceTempView` + `spark.sql`) compile to the <b>same plan</b>. Actions: `show`, `collect`, `count`, `write`.",
       "<b>Catalyst phases</b>: analysis (resolve names and types) > logical optimisation (predicate pushdown, column pruning, constant folding, combine filters) > physical planning (choose strategies, e.g. broadcast join) > code generation.",
       "`explain(true)` prints the parsed, analysed, optimised and physical plans. Adaptive Query Execution (`AdaptiveSparkPlan`) can re-optimise at run time."]),
    OUT("n4_spark_traps.out.txt", "Verified output", transform=pick("DataFrame API")),
    OUT("m4_q4_spark.out.txt", "Catalyst plans (question bank M4-C5)", transform=lambda t: "result:" + t.split("\nresult:", 1)[1]),
    QA("Explain Catalyst's four phases with an example.", [P("In the second query the two `filter` calls were merged into `(id > 10) AND (id < 50)` and `cast(5 as bigint)` was folded to the literal `5` (logical optimisation, output). Analysis resolved `id`, physical planning chose `Range`/`Project`/`Filter` operators, and whole-stage code generation compiled them to bytecode.")], "10 marks"),
    QA("DataFrame versus Dataset versus RDD.", [T(["", "RDD", "DataFrame", "Dataset[T]"], [["Schema", "no", "yes (untyped Rows)", "yes (typed)"], ["Optimiser", "none", "Catalyst", "Catalyst"], ["Type safety", "compile-time", "run time", "compile-time"],
                                                                                       ["Use", "low-level control", "SQL-style analytics", "typed pipelines in Scala/Java"]], [0.2, 0.27, 0.27, 0.26])], "5 marks"),
    QA("Is the DataFrame result the same via the API and via SQL? Why?", [P("Yes: both returned `N/15.0/1, S/50.0/2, W/25.0/1` and the optimised plans were identical (output `same optimised plan: true`), because both are parsed into the same logical plan before Catalyst runs.")], "3 marks"),
    QA("Why does a typo in `ds.filter(_.amout > 20)` fail earlier than `df.filter($\"amout\" > 20)`?", [P("The typed Dataset lambda is checked by the Scala compiler; the DataFrame column name is a string resolved at run time during analysis (`AnalysisException`).")], "tricky"),
    QA("What does a broadcast join do and when is it chosen?", [P("The small table is sent to every executor so the large table need not be shuffled. Catalyst picks it automatically when one side is below `spark.sql.autoBroadcastJoinThreshold` or when you add `broadcast(df)` (the plan contained `BroadcastHashJoin`).")], "3 marks"),
])

sub_4_9 = SUB("4.9", "Spark components: Core, SQL, Streaming, MLlib, GraphX", [
    T(["Component", "Purpose", "Notes"], [
        ["Spark Core", "RDD API, scheduling, memory management, fault recovery", "foundation of everything else"],
        ["Spark SQL", "structured data: DataFrames, Datasets, SQL, Catalyst", "read/write Parquet, JSON, CSV, JDBC"],
        ["Structured Streaming", "live data processed as an unbounded table with the DataFrame API", "micro-batches; exactly-once with suitable sources/sinks; older RDD-based DStreams are legacy"],
        ["MLlib", "scalable machine learning: pipelines, regression, classification, clustering, recommendation", "`DataFrame`-based API is the main one"],
        ["GraphX", "graph computation: PageRank, connected components", "RDD-based; Pregel API"]], [0.2, 0.45, 0.35]),
    QA("List the Spark ecosystem components and one use of each.", [P("Spark Core (task scheduling and RDDs), Spark SQL (analytics on tables), Structured Streaming (real-time data), MLlib (distributed machine learning), GraphX (graph analytics).")], "5 marks"),
    QA("How does Structured Streaming treat a stream?", [P("As an unbounded table to which new rows keep being appended; your query (the same as for batch) is run incrementally on each micro-batch and updates the result.")], "3 marks"),
    QA("What is an MLlib Pipeline?", [P("A sequence of stages (transformers such as feature encoders and estimators such as logistic regression) fitted together, the Spark analogue of scikit-learn's `Pipeline`.")], "2 marks"),
])

NOTES_4 = NMODULE(
    4, "Scala libraries and Spark basics", "8 hours",
    "Scala libraries: Breeze, Saddle; exception handling; Apache Spark architecture; Spark and big data; Apache Spark components.",
    [("Breeze", "4.1"), ("Saddle (and Spire from the labs)", "4.2"), ("Exception handling", "4.3"), ("Spark big data", "4.4"), ("Apache Spark architecture", "4.5"),
     ("RDDs, transformations, actions (core of Spark)", "4.6, 4.7"), ("DataFrames, Datasets, Catalyst", "4.8"), ("Apache Spark components", "4.9")],
    [sub_4_1, sub_4_2, sub_4_3, sub_4_4, sub_4_5, sub_4_6, sub_4_7, sub_4_8, sub_4_9],
)
