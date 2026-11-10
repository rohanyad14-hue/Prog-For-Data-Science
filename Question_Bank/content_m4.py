from dsl import *


def short_javaopt(text):
    out = []
    for ln in text.split("\n"):
        if ln.startswith("//> using javaOpt"):
            ln = "//> using javaOpt --add-opens=java.base/java.lang=ALL-UNNAMED ... (13 flags that let Spark 3.5 run on Java 17; see the file)"
        out.append(ln)
    return "\n".join(out)


def drop_noise(text):
    return "\n".join(l for l in text.split("\n") if not l.startswith(("trying to return java", "return java")))


def before_result(text):
    return text.split("\nresult:")[0]


def from_result(text):
    return "result:" + text.split("\nresult:", 1)[1]


def between(start, end):
    def f(text):
        lines = text.split("\n")
        a = next(i for i, l in enumerate(lines) if start in l)
        b = next(i for i, l in enumerate(lines) if end in l and i >= a)
        return "\n".join(lines[a:b + 1])
    return f


mcqs = [
    MCQ("Which Spark process builds the DAG of stages and schedules tasks on executors?",
        ["Executor", "Driver", "Worker disk", "Cluster manager only"], 1,
        "The driver runs your `main()`, holds the SparkSession, builds the DAG and sends tasks to executors. The cluster manager only allocates resources."),
    MCQ("Which of these is an action?", ["`map`", "`filter`", "`reduceByKey`", "`count`"], 3,
        "`count`, `collect`, `take`, `reduce` and `saveAsTextFile` trigger execution; the others only extend the lineage."),
    MCQ("RDD stands for:", ["Random Data Directory", "Resilient Distributed Dataset", "Relational Data Document", "Remote Data Driver"], 1,
        "Resilient (recoverable), Distributed (partitioned over nodes), Dataset (collection of records); also immutable."),
    MCQ("After an executor fails, a lost RDD partition is recovered by:",
        ["restoring a replica from HDFS always", "recomputing it from its lineage (the DAG of transformations)",
         "restarting the whole application", "asking the user"], 1,
        "Spark remembers how each RDD was derived, so only the lost partitions are recomputed."),
    MCQ("What does `Try(\"4x2\".toInt)` evaluate to?",
        ["`Success(4)`", "`Failure(NumberFormatException)`", "`None`", "an uncaught exception"], 1,
        "`Try` captures the exception inside a `Failure` value instead of throwing."),
    MCQ("Which Spark component provides DataFrames, SQL and the Catalyst optimiser?",
        ["Spark Core", "Spark SQL", "MLlib", "GraphX"], 1, "Spark SQL (with the DataFrame/Dataset API)."),
    MCQ("\"Lazy evaluation\" in Spark means:",
        ["data is loaded slowly", "transformations are only recorded; computation starts when an action is called",
         "actions are queued for the next day", "executors start late"], 1,
        "Laziness lets Spark see the whole plan, pipeline narrow steps and skip unused work."),
    MCQ("In Breeze, `a *:* b` for two `DenseVector[Double]` computes:",
        ["the dot product", "the element-wise product", "the cross product", "the outer product"], 1,
        "`*:*` is element-wise; `dot` gives the inner product and `*` on matrices is matrix multiplication."),
    MCQ("`Option[T]` is mainly used to:",
        ["loop over a collection", "represent a value that may be absent as `Some(x)` or `None`, avoiding null",
         "declare a mutable value", "catch exceptions with a message"], 1, "It makes absence explicit in the type, so the compiler makes you handle it."),
    MCQ("Which operation normally causes a shuffle (wide dependency)?",
        ["`map`", "`filter`", "`reduceByKey`", "`flatMap`"], 2,
        "`reduceByKey` must bring equal keys together from different partitions. `map`, `filter`, `flatMap` work inside each partition (narrow)."),
    MCQ("Spark can run under which cluster managers?",
        ["only its own standalone manager", "Standalone, YARN and Kubernetes", "only YARN", "only Kubernetes"], 1,
        "The application code is the same; the cluster manager only changes how resources are obtained."),
]

shorts = [
    SHORT("How does exception handling in Scala differ from Java? Show `try / catch / finally`.", 5, [
        B(["`try` is an <i>expression</i>: it has a value (the last expression of the try or the matching catch).",
           "`catch` takes <b>pattern-matching</b> cases: `case e: ArithmeticException => ...`.",
           "There are no <i>checked</i> exceptions: the compiler never forces you to declare or catch them.",
           "`finally` always runs. `throw` is an expression of type `Nothing`."]),
        SNIP("val r = try { 10 / d } catch {\n  case _: ArithmeticException => 0\n  case e: Exception           => -1\n} finally println(\"done\")", lang="scala")]),
    SHORT("Differentiate `Option`, `Try` and `Either`.", 5, [
        T(["Type", "Cases", "Use when", "Example"], [
            ["`Option[A]`", "`Some(a)` / `None`", "a value may simply be absent", "`map.get(\"k\")`"],
            ["`Try[A]`", "`Success(a)` / `Failure(ex)`", "wrapping code that may throw", "`Try(s.toInt)`"],
            ["`Either[E, A]`", "`Left(error)` / `Right(a)`", "you want your own error value", "`safeSqrt(-4)` -> `Left(\"...\")`"]],
          [0.17, 0.25, 0.3, 0.28]),
        P("All three work with `map`, `flatMap`, `for` comprehensions and pattern matching, so failures propagate without nested `if` or `try`.")]),
    SHORT("Compare Breeze, Saddle and Spire.", 3, [
        T(["Library", "Purpose", "Main types"], [
            ["Breeze", "numerical computing and linear algebra, statistics, optimisation", "`DenseVector`, `DenseMatrix`, `*:*`, `\\`, `.t`"],
            ["Saddle", "data manipulation with labelled, indexed data and NA handling (like a small pandas)", "`Vec`, `Series`, `Frame`, `Index`"],
            ["Spire", "exact and generic numerics", "`Rational`, `Algebraic`, `Complex`, typeclasses `Field`, `Ring`"]], [0.14, 0.52, 0.34])]),
    SHORT("Name the main parts of the Spark architecture and the role of each.", 5, [
        T(["Part", "Role"], [
            ["Driver", "runs `main()`, creates the SparkSession, turns actions into a DAG of stages and tasks, schedules them, collects results"],
            ["Cluster manager", "allocates resources: Standalone, YARN or Kubernetes"],
            ["Worker node / Executor", "executor is a JVM process that runs tasks and caches partitions in memory or on disk"],
            ["Task", "the smallest unit of work: one stage applied to one partition"],
            ["Partition", "a slice of an RDD or DataFrame; the unit of parallelism"]], [0.25, 0.75])]),
    SHORT("State the four properties of an RDD and explain lineage.", 3, [
        P("<b>Resilient</b> (recoverable through lineage), <b>Distributed</b> (split in partitions across nodes), <b>Dataset</b> (typed records), "
          "<b>Immutable</b> (transformations create new RDDs). <b>Lineage</b> is the recorded chain of transformations that produced an RDD, "
          "shown by `rdd.toDebugString`. A lost partition is rebuilt by replaying only the needed part of that chain, so no data replication is required.")]),
    SHORT("Give three transformations and three actions of Spark, and explain why laziness helps.", 3, [
        P("Transformations: `map`, `filter`, `reduceByKey` (also `flatMap`, `groupByKey`, `join`). Actions: `count`, `collect`, `saveAsTextFile` (also `take`, `reduce`, `first`)."),
        P("Because nothing runs until an action, Spark sees the whole plan first. It can pipeline several narrow steps into one pass over the data, "
          "avoid materialising intermediate results, and (for DataFrames) let Catalyst reorder and prune work.")]),
    SHORT("Explain narrow and wide transformations, and what a shuffle is.", 3, [
        P("<b>Narrow</b>: each output partition depends on one input partition (`map`, `filter`, `flatMap`); pipelined in one stage. "
          "<b>Wide</b>: an output partition needs data from many input partitions (`reduceByKey`, `groupByKey`, `join`); Spark must <b>shuffle</b> "
          "(redistribute data by key across the network and disk), which ends a stage. Shuffles are the main cost in Spark jobs, so reduce them "
          "(prefer `reduceByKey` over `groupByKey`).")]),
    SHORT("List the Spark ecosystem components and one use of each.", 5, [
        T(["Component", "Use"], [
            ["Spark Core", "RDD API, task scheduling, memory management, fault recovery"],
            ["Spark SQL", "structured data with DataFrames, Datasets and SQL; Catalyst optimiser"],
            ["Structured Streaming", "process live data (Kafka, sockets, files) with the same DataFrame API"],
            ["MLlib", "scalable machine learning: pipelines, regression, classification, clustering"],
            ["GraphX", "graph computation (PageRank, connected components)"]], [0.25, 0.75])]),
    SHORT("Why is Spark often preferred over Hadoop MapReduce?", 3, [
        B(["MapReduce writes intermediate results to disk between every map and reduce step. Spark plans a DAG and keeps intermediate data in memory where possible.",
           "One engine for batch, SQL, streaming, ML and graphs; rich APIs in Scala, Python, Java, R and SQL.",
           "Iterative algorithms (ML) reuse cached datasets instead of re-reading from disk each iteration."])]),
    SHORT("RDD versus DataFrame.", 3, [
        P("An RDD is a low-level distributed collection of objects with no schema, so Spark cannot optimise it. A DataFrame is a distributed table with named, "
          "typed columns; Catalyst optimises its plan and Tungsten stores it compactly. The Spark quick-start recommends switching to Datasets/DataFrames "
          "for better performance, and keeping RDDs for low-level control.")]),
    SHORT("Briefly describe the characteristics of big data (the V's).", 2, [
        P("Volume (size), Velocity (speed of arrival), Variety (structured, semi-structured, unstructured), commonly extended with Veracity (quality) "
          "and Value. Spark is built to process data that is too large or too fast for a single machine.")]),
]

# ------------------------------------------------------------------------------------------ longs
c1_prompt = [
    P("Explain exception handling in Scala. Write a program that shows `try / catch / finally`, a custom exception, `Option`, `Try` (with `recover`) and "
      "`Either`. Explain why functional error handling is preferred to throwing exceptions."),
]
c1_answer = [
    B(["<b>Throwing and catching</b>: `throw new X(msg)`; `catch { case e: X => ... }` uses pattern matching; `finally` always runs. "
       "`try` returns a value, so `val r = try ... catch ...` is idiomatic.",
       "<b>Custom exception</b>: `class InsufficientFundsException(msg: String) extends Exception(msg)`.",
       "<b>Functional alternatives</b> keep errors in the type so callers cannot ignore them: `Option` (absence), `Try` (captured exception, with "
       "`recover`, `map`, `getOrElse`, `toOption`), `Either` (a typed error in `Left`).",
       "In a `for` comprehension the first `Left` or `Failure` stops the chain, which replaces nested `try` blocks."]),
    CODE("m4_q1_exceptions.scala"),
    OUT("m4_q1_exceptions.out.txt"),
    TIP("In the output the line printed by `finally` appears before `divide(10, 2) = 5`: the `finally` block runs before the function hands its value back to the caller's `println`."),
]

c2_prompt = [
    P("(Lab experiments 18 to 20) Use Breeze to compute total revenue per fruit (price times quantity) and solve a linear system; use Saddle to load a small dataset, "
      "filter apples and compute their average price; use Spire for exact arithmetic. Say what role each library plays, and how charts are added (Vegas, Plotly.Scala)."),
]
c2_answer = [
    T(["Library", "Lab", "What the code shows"], [
        ["Breeze", "19", "`DenseVector`, element-wise `*:*`, `sum`, `mean`, `variance` (sample variance, divides by n-1), `DenseMatrix`, `\\` solve, `dot`"],
        ["Saddle", "18, 20", "`Vec` with a boolean mask, `Series` with an `Index`, `Frame` of aligned columns, NA handling in `mean`"],
        ["Spire", "20", "`Rational(1,10) + Rational(2,10)` equals exactly 3/10, while `0.1 + 0.2` in `Double` is `0.30000000000000004`"],
        ["Vegas / Plotly.Scala", "18, 19", "declarative charts (grammar of graphics) built from data; need a notebook or a browser to view"]], [0.18, 0.08, 0.74]),
    CODE("m4_q2_breeze.scala"),
    OUT("m4_q2_breeze.out.txt", transform=drop_noise),
    CODE("m4_q3_saddle.scala"),
    OUT("m4_q3_saddle.out.txt"),
    NOTE("Breeze printed two start-up messages about the Java version of its native-library loader; they are omitted above. "
         "Saddle: the original `org.scala-saddle` artifacts on Maven Central stop at Scala 2.11, so this program uses the maintained fork "
         "`io.github.pityka::saddle-core:4.0.0-M14` (a milestone release) on Scala 2.13. In that version `Frame.firstCol(name)` returns a Series and "
         "operators need `import org.saddle.ops.BinOps._`; your lab file uses the older `frame.col(...)` style, so check the API of the version you load."),
]

c3_prompt = [
    P("Draw and explain the Apache Spark architecture. Describe how a Spark application is turned into jobs, stages and tasks, "
      "using a word-count program as the example."),
]
c3_answer = [
    DIAGRAM("spark", "Spark cluster architecture: the driver talks to the cluster manager, executors run tasks and cache data."),
    H3("Component roles"),
    B(["<b>Driver</b>: your `main()`, the SparkSession, DAG scheduler and task scheduler. It must stay alive for the whole application.",
       "<b>Cluster manager</b>: grants executors (Standalone, YARN, Kubernetes).",
       "<b>Executors</b>: JVMs on worker nodes; run tasks in threads, keep cached partitions, report results back to the driver."]),
    H3("From code to tasks"),
    FLOW(["Application", "Job (one per action)", "Stages (cut at shuffles)", "Tasks (one per partition)"],
         "Execution hierarchy."),
    B(["<b>Job</b>: created each time an action (`collect`, `count`, `save`) is called.",
       "<b>Stage</b>: a group of narrow transformations that can run without moving data. A wide transformation (`reduceByKey`) starts a new stage.",
       "<b>Task</b>: one stage on one partition. With 2 partitions, each stage has 2 tasks."]),
    P("In the word count below, `flatMap` and `map` form stage 0; `reduceByKey` needs a shuffle, so the reduce side is stage 1. "
      "The `(2)` in `toDebugString` is the number of partitions, and the `+-` marks the shuffle boundary."),
    CODE("m4_q4_spark.scala", "Code: m4_q4_spark.scala (first part: session and word count)", transform=short_javaopt, maxlines=21),
    OUT("m4_q4_spark.out.txt", "Output (first part: partitions and lineage)", transform=lambda t: before_result(t)),
    NOTE("Run in local mode (`local[2]`, two worker threads in one JVM) with Spark 3.5.1 on Java 17, so the \"cluster\" is simulated. "
         "The architecture and the stage/task logic are the same on a real cluster."),
]

c4_prompt = [
    P("(FAT high-frequency questions 3 and 4) What is an RDD? Define its four properties and explain how DAG lineage gives fault tolerance without replication. "
      "List three transformations and three actions, and show with a program that transformations are lazy."),
]
c4_answer = [
    T(["Property", "Meaning"], [
        ["Resilient", "lost partitions are recomputed from lineage"],
        ["Distributed", "data is split into partitions spread over executors"],
        ["Dataset", "collection of typed records"],
        ["Immutable", "never modified; every transformation produces a new RDD"]], [0.2, 0.8]),
    H3("Lineage and fault tolerance"),
    P("Every RDD stores a reference to its parents and the function applied. If an executor dies, the driver reschedules only the lost partitions on "
      "other executors, which re-read the source data and replay the transformations. Nothing was copied in advance, so there is no replication overhead "
      "during normal running; the price is recomputation time after a failure. `persist`/`cache` avoid recomputing an RDD that is used again, "
      "and checkpointing writes it to reliable storage so a very long lineage can be cut."),
    H3("Transformations (lazy) versus actions (eager)"),
    T(["", "Transformations", "Actions"], [
        ["Returns", "a new RDD", "a value to the driver, or writes to storage"],
        ["Executes", "no, only extends the lineage", "yes, triggers a job"],
        ["Examples", "`map`, `filter`, `flatMap`, `reduceByKey`", "`count`, `collect`, `take`, `reduce`, `saveAsTextFile`"]], [0.16, 0.42, 0.42]),
    P("Proof of laziness in the output below: after calling `map`, the accumulator that counts executions of the function still reads 0; "
      "after the action `reduce`, it reads 10."),
    CODE("m4_q4_spark.scala", "Excerpt from m4_q4_spark.scala (laziness demo)", transform=between("---- Laziness", "after reduce()")),
    OUT("m4_q4_spark.out.txt", "Relevant lines of the output of m4_q4_spark.scala (listed in the previous question)",
        transform=lambda t: "\n".join(l for l in before_result(t).split("\n") if l.startswith(("word counts", "after map", "after reduce")))),
]

c5_prompt = [
    P("(FAT high-frequency question 10) Describe the components of the Spark ecosystem. Explain how Spark SQL's Catalyst optimiser improves a query through "
      "logical optimisation, physical planning and code generation, and show an example."),
]
c5_answer = [
    T(["Component", "Purpose"], [
        ["Spark Core", "RDDs, scheduling, memory, fault tolerance"],
        ["Spark SQL", "DataFrames/Datasets, SQL, Catalyst"],
        ["Structured Streaming", "incremental processing of live data with the DataFrame API"],
        ["MLlib", "machine learning algorithms and pipelines"],
        ["GraphX", "graph processing"]], [0.25, 0.75]),
    H3("Catalyst"),
    FLOW(["SQL / DataFrame code", "Analysis: resolve names and types", "Logical optimisation (rules)", "Physical planning (cost model)",
          "Code generation (bytecode)"], "Phases of Catalyst."),
    N(["<b>Analysis</b>: unresolved column and table names are resolved against the catalog; types are checked.",
       "<b>Logical optimisation</b>: rule-based rewrites such as predicate pushdown, column pruning, constant folding and combining filters.",
       "<b>Physical planning</b>: one or more physical plans are generated (for example broadcast hash join versus sort-merge join) and the cheapest is chosen.",
       "<b>Code generation</b>: whole-stage code generation compiles the chosen plan into Java bytecode that avoids virtual calls and per-row overhead."]),
    P("In the second query the code has two separate `filter` calls and a multiplication by a literal. After Catalyst, the two filters are merged into one "
      "`(id > 10) AND (id < 50)` and `cast(5 as bigint)` has been folded into the literal `5`. The first query, on a small in-memory table, shows no `Filter` node "
      "in its optimised plan although the code filters `salary > 68000`; the result still excludes Kabir (65000), so Catalyst applied the predicate to the local "
      "data while optimising."),
    CODE("m4_q4_spark.scala", "Excerpt from m4_q4_spark.scala (DataFrame and Catalyst demo)", transform=between("---- DataFrame", "rows kept")),
    OUT("m4_q4_spark.out.txt", "Plans printed by m4_q4_spark.scala", transform=from_result),
    TIP("Catalyst is written in Scala and relies on pattern matching over tree nodes, which is one reason Scala features in this course."),
]

longs = [
    LONG("Exception handling in Scala", 10, c1_prompt, c1_answer,
         "try/catch/finally 3, custom exception 1, Option/Try/Either 4, explanation of preference 2."),
    LONG("Scala libraries: Breeze, Saddle and Spire", 10, c2_prompt, c2_answer,
         "Breeze 3, Saddle 3, Spire 2, charts and role comparison 2."),
    LONG("Apache Spark architecture", 10, c3_prompt, c3_answer,
         "diagram 3, component roles 3, job-stage-task 3, example 1."),
    LONG("RDDs, lineage, transformations and actions", 10, c4_prompt, c4_answer,
         "four properties 2, lineage 3, transformations vs actions with examples 3, laziness demo 2."),
    LONG("Spark components and the Catalyst optimiser", 10, c5_prompt, c5_answer,
         "components 3, Catalyst phases 4, example 3."),
]

MODULE_4 = MODULE(
    4, "Scala libraries and Spark basics", "8 hours",
    "Scala libraries: Breeze and Saddle; exception handling; Apache Spark architecture; Spark and big data; Apache Spark components.",
    [P("Labs 18 to 20 (Saddle, Vegas, Breeze, Plotly.Scala, Spire) belong here. Spark is not in the lab list, so expect theory and short code in the FAT.")],
    mcqs, shorts, longs,
    exam_notes=[TIP("Draw the Spark architecture diagram in every Spark answer: driver, cluster manager, workers with executors and tasks. It is cheap marks."),
                WARN("Do not say Spark \"stores\" data. It computes on data held in external storage; executors only cache partitions temporarily.")],
)
