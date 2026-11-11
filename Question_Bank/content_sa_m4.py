"""Answers to the five Module 4 sample questions (Spark, Breeze, Saddle, exception handling)."""
from dsl import B, CODE, H3, H4, NOTE, OUT, P, T, TIP, WARN

QUESTIONS = []


def question(qid, title, image, blocks):
    QUESTIONS.append(dict(id=qid, module=4, title=title, image=image, blocks=blocks))


# ------------------------------------------------------------------------------------------------ Q1
question("M4-Q1", "Large-Scale Student Performance Analytics using Spark and Breeze", "6278527581963359885.jpg", [
    H3("Answer, point by point"),
    NOTE("The screenshot of this question is cut off after the fifth bullet. The five visible bullets are answered; the fifth one is the last line that can be read (\"Justify why Spark is preferred over traditional data-processing systems\")."),
    H4("1. How would Spark's architecture help process millions of records efficiently?"),
    B(["<b>Partitioning</b>: the 5 million rows are cut into partitions and every partition is processed by its own task, in parallel on the executors. In the demo, `spark.range(5000000)` is split into 4 partitions, so 4 tasks run at once.",
       "<b>Two-phase aggregation</b>: each task first aggregates its own partition (`partial_avg` in the physical plan) and only the small partial results travel through the one shuffle (`Exchange`) to the final aggregate. Little data moves.",
       "<b>Lazy evaluation and the DAG</b>: transformations only build a plan; the optimiser (Catalyst) rewrites the whole plan before anything runs; an action starts the job.",
       "<b>In-memory processing and caching</b> of reused data, <b>data locality</b> (tasks go to the node that holds the data), and <b>scale-out</b>: more executors, same code.",
       "<b>Fault tolerance</b>: a lost partition is recomputed from its lineage."]),
    H4("2. Which Spark components (Driver, Executor, Cluster Manager) are involved?"),
    T(["Component", "What it does", "In this demo"], [
        ["<b>Driver</b>", "runs `main()`, owns the SparkSession, turns the code into a DAG of stages and tasks, schedules the tasks and collects the results", "the JVM of the program"],
        ["<b>Cluster manager</b>", "decides which worker nodes give resources, starts the executors (Standalone, YARN, Kubernetes)", "local mode: simulated inside one JVM (`master local[4]`)"],
        ["<b>Executors</b>", "JVM processes on the worker nodes that run the tasks, keep cached partitions in memory and report back", "4 task slots"]], [0.18, 0.54, 0.28]),
    H4("3. How can Breeze be used for statistical computations on the dataset?"),
    P("Breeze is a numerical library for <b>one JVM</b>: dense vectors and matrices, `mean`, `stddev`, `variance`, `dot`, element-wise operators (`/:/`), linear algebra. It is not distributed. The sensible split is: <b>Spark reduces the 5 million rows</b> to something small (aggregates, a sample, sufficient statistics), and <b>Breeze does the local numerical work</b> on that result. Collecting all 5 million rows into the driver just to use Breeze would defeat the purpose. In the code, three vectors (attendance, CGPA, placed 0/1) give mean CGPA 7.57, standard deviation 1.48, the correlations attendance~CGPA 0.952, CGPA~placed 0.955, attendance~placed 0.935, and z-scores of CGPA."),
    H4("4. Propose methods to identify factors influencing placements"),
    B(["<b>Compare groups</b>: placed students average CGPA 8.8 and attendance 90, not placed 6.35 and 70 (`groupBy(\"Placed\")`).",
       "<b>Correlation</b> of each factor with the outcome (Breeze above, or `df.stat.corr` in Spark).",
       "<b>Model-based</b>: Spark MLlib `LogisticRegression` (coefficients: attendance 0.087, CGPA 0.764 on standardised features, both push towards \"placed\"), or `RandomForestClassifier` feature importances; `ChiSqSelector` for categorical factors.",
       "At 5 million rows: train/test split, cross-validation, handle class imbalance, and watch for leakage (a column that is only known after the placement).",
       "<b>Association is not cause</b>: CGPA and attendance may both reflect motivation or the campus. Four rows are a demonstration, not evidence."]),
    H4("5. Justify why Spark is preferred over traditional data-processing systems"),
    T(["", "Traditional (single-machine tools, RDBMS, MapReduce)", "Spark"], [
        ["Scale", "limited by one machine's memory and disk (vertical scaling)", "add machines (horizontal scaling)"],
        ["Speed", "MapReduce writes every intermediate result to disk", "keeps intermediate data in memory and plans the whole DAG"],
        ["Variety of work", "separate systems for SQL, streaming, ML, graphs", "one engine: Spark SQL, Streaming, MLlib, GraphX"],
        ["Failures", "re-run by hand or restart the job", "recompute lost partitions from the lineage automatically"],
        ["Programming", "low-level or tool specific", "Scala, Java, Python, R and SQL APIs"]], [0.16, 0.42, 0.42]),
    P("Honest limit: for data that fits one machine, plain pandas or a database is simpler and faster than starting a cluster."),
    H3("Code, run on the dataset of the question (Spark + Breeze)"),
    CODE("sa_m4_q1.scala", "Code: code/sa_m4_q1.scala"),
    OUT("sa_m4_q1.out.txt", "Real output", maxlines=60),
])

# ------------------------------------------------------------------------------------------------ Q2
question("M4-Q2", "Smart Healthcare Data Processing with Saddle and Spark", "6278527581963359888.jpg", [
    H3("Answer, point by point"),
    H4("1. How can Saddle Series and Frames be used to organise the data?"),
    B(["A <b>Series</b> is one labelled column: the index holds the PatientID, the values the blood pressures (`Series(bp, ids)`).",
       "A <b>Frame</b> is a table of such columns with row labels (patients) and column labels (Age, BP, Diabetes). It is typed: all columns of a Frame share one element type, so Diabetes is stored as 1.0 / 0.0 (or kept in a separate Series[String]).",
       "Index alignment, filtering (`bpSeries.filter(_ >= 140)` keeps the patient labels), sorting (`sorted`), missing-value handling (`fillNA`), column arithmetic and `Vec` statistics are available. A Series has no `mean`: use `.values.mean` (128.3).",
       "Saddle is the \"small pandas\" of Scala: one machine, in memory."]),
    H4("2. Which Spark component would distribute processing across hospital servers?"),
    P("The work is distributed by <b>Spark Core's scheduler</b>: the DataFrame / Spark SQL layer splits the data into partitions, the cluster manager provides <b>executors</b> on the worker servers, and the driver sends one task per partition to them. In the code `repartition(2, col(\"Diabetes\"))` shows rows spread over two partitions (P101 and P103 in partition 1, P102 and P104 in partition 0), each of which would be processed on some executor of a real cluster."),
    H4("3. How would you detect abnormal patient records?"),
    B(["<b>Clinical rules</b> (American Heart Association blood-pressure categories, treating the single BP number as systolic): below 120 normal, 120-129 elevated, 130-139 stage 1, 140 and above stage 2. Result: P104 normal, P102 elevated, P101 stage 1, P103 stage 2.",
       "<b>Combined rule</b>: diabetes and BP >= 130 marks P101 and P103 as high risk. Mean BP is 137.5 with diabetes and 119.0 without.",
       "<b>Statistical rule</b>: z-score or IQR. Here the largest z-score is 1.57, so no record is a statistical outlier although P103 is clinically abnormal: rules and statistics find different things, use both.",
       "<b>Validity checks</b>: impossible values (BP 0 or 400), missing fields, duplicate patient ids. On large data add an unsupervised detector (isolation forest, k-means distance)."]),
    H4("4. How can large-scale healthcare analytics benefit from distributed computing?"),
    B(["Millions of records from many cities are processed in minutes, because partitions are handled in parallel.",
       "Data can be processed where it is stored (data locality), and a failed node does not lose the job (lineage recomputation).",
       "Model training and cohort queries scale by adding servers.",
       "Patient data is sensitive: anonymise or pseudonymise identifiers, control access and encrypt in transit and at rest."]),
    H4("5. Compare the roles of Saddle and Spark"),
    T(["", "Saddle", "Spark"], [
        ["Where it runs", "one JVM, data in local memory", "a cluster of executors, data in partitions"],
        ["Data size", "what fits in one machine", "far larger than one machine"],
        ["Strength", "labelled, aligned Series / Frame manipulation, quick exploration", "parallel SQL, ETL, machine learning, streaming"],
        ["Typical role here", "organise and inspect a hospital's summary or a sample", "read, clean, aggregate and score all hospitals' records"],
        ["Together", "Spark produces the aggregated result, Saddle (or Breeze) analyses it locally", ""]], [0.2, 0.4, 0.4]),
    H3("Code 1: Saddle"),
    CODE("sa_m4_q2_saddle.scala", "Code: code/sa_m4_q2_saddle.scala"),
    OUT("sa_m4_q2_saddle.out.txt", "Real output"),
    H3("Code 2: Spark"),
    CODE("sa_m4_q2_spark.scala", "Code: code/sa_m4_q2_spark.scala"),
    OUT("sa_m4_q2_spark.out.txt", "Real output", maxlines=60),
])

# ------------------------------------------------------------------------------------------------ Q3
question("M4-Q3", "E-Commerce Recommendation System with Exception Handling and Spark", "6278527581963359900.jpg", [
    H3("Answer, point by point"),
    H4("1. How can Spark process millions of transactions in parallel?"),
    P("The transaction file is read as partitions (for a file in HDFS or S3 roughly one per block). Each partition becomes one task; tasks run in parallel on the executors. Parsing, filtering and the partial aggregation (`groupBy(\"Product\")`) happen inside the tasks, and only the small partial results are shuffled to compute the totals. Adding executors adds parallelism without changing the code."),
    H4("2. What exceptions may occur during loading and processing?"),
    T(["Stage", "Problem", "Example in the code"], [
        ["Loading", "missing or unreadable input", "`AnalysisException` with error class `PATH_NOT_FOUND`"],
        ["Loading", "corrupted or malformed lines", "`C105,Phone,abc` (text in a number column), `C106,Laptop` (a column missing)"],
        ["Processing", "bad values", "`NumberFormatException`, null customer id, negative amount"],
        ["Processing", "skewed or oversized data", "one product with most of the rows, `OutOfMemoryError`"],
        ["Cluster", "task, executor, node or shuffle-fetch failure", "simulated in section 4 of the code"]], [0.14, 0.38, 0.48]),
    H4("3. Propose an exception-handling strategy for missing or corrupted records"),
    B(["<b>Read with an explicit schema</b> and choose the parse mode: `PERMISSIVE` (default; bad rows become nulls and, with a `_corrupt_record` column, the raw line is kept), `DROPMALFORMED` (silently drops) or `FAILFAST` (stops the job at the first bad line). The code uses `PERMISSIVE` with the corrupt-record column and puts the two unparsable lines in a <b>dead-letter list</b> for later inspection; a third row fails a business rule (no customer id).",
       "<b>Validate</b> business rules after parsing (customer id present, amount greater than 0). 4 clean rows remain.",
       "<b>At record level</b> wrap the parsing in `Try` and count failures with an <b>accumulator</b> (3 bad records skipped), so one bad line never kills the job.",
       "<b>Fail fast where it should</b>: missing input path or schema errors stop the job with a clear message; but if the share of bad records is above a threshold, fail the job too, because the data source is broken.",
       "Catch exceptions at the driver around the action, log, alert, and `spark.stop()` in `finally`."]),
    WARN("`count()` can hide bad data. It needs no column values, so Spark prunes the columns and never parses the bad fields: the code shows `count()` returning all 7 lines while `collect()` (which parses everything) applies the parse mode."),
    H4("4. How does Spark's fault-tolerance mechanism improve reliability?"),
    B(["<b>Lineage</b>: Spark remembers how every partition was computed from the input. If a task or executor fails, only the lost partitions are recomputed.",
       "<b>Task retries</b>: a failed task is re-run (default up to 4 attempts, `spark.task.maxFailures`). Demonstrated: one task throws on its first attempt, Spark runs it again, and the job result is correct (360.0).",
       "Also: stage re-execution after a lost shuffle output, optional speculative execution of slow tasks, <b>checkpointing</b> to cut a very long lineage (and for streaming state), restart of the driver in cluster mode, replicated storage such as HDFS."]),
    H4("5. Suggest business insights from the processed data"),
    B(["<b>Laptops</b> bring Rs. 135,000 of the Rs. 178,000 revenue of the clean rows (76%) from 2 of 4 buyers; mobiles 25,000 and tablets 18,000.",
       "<b>Next-best-product recommendation</b>: for every customer, take the products they have not bought and rank them by popularity (buyers, then revenue). Result: C101 and C103 (laptop buyers) get Mobile, C102 and C104 get Laptop.",
       "Next steps with more data: collaborative filtering with `ALS` from Spark MLlib, co-purchase rules (\"people who bought a laptop also bought ...\"), segmentation by spend.",
       "Data quality is itself an insight: 3 of 7 lines (43%) were damaged, so the source system needs fixing."]),
    H3("Code, run on the dataset of the question"),
    CODE("sa_m4_q3.scala", "Code: code/sa_m4_q3.scala"),
    OUT("sa_m4_q3.out.txt", "Real output", maxlines=70),
])

# ------------------------------------------------------------------------------------------------ Q4
question("M4-Q4", "Social Media Sentiment Analysis using Spark Big Data Architecture", "6278527581963359907.jpg", [
    H3("Answer, point by point"),
    H4("1. How do Spark's Driver Program and Executors coordinate processing?"),
    T(["Step", "Who", "What happens"], [
        ["1", "Driver", "your program creates the SparkSession / SparkContext and builds the logical plan from the transformations"],
        ["2", "DAG scheduler (in the driver)", "cuts the plan into <b>stages</b> at every shuffle (wide transformation)"],
        ["3", "Task scheduler + cluster manager", "asks for executors, then sends one <b>task</b> per partition of a stage to them"],
        ["4", "Executors", "run the tasks on their partitions, keep cached blocks, send heartbeats and task results back"],
        ["5", "Driver", "collects the results (`collect`, `show`, `write`), the next stage starts when the previous one is complete"]], [0.08, 0.30, 0.62]),
    P("The code asks the scheduler for its own report: one aggregation job was split into 2 stages (map side with 2 tasks, reduce side with 4 tasks), and the RDD version of the same aggregation shows the `ShuffledRDD` that marks the stage boundary."),
    H4("2. Which Spark components are responsible for task scheduling and execution?"),
    B(["<b>DAGScheduler</b> (stages), <b>TaskScheduler</b> with its scheduler backend (tasks to executors), the <b>cluster manager</b> (resources: Standalone, YARN, Kubernetes) and the <b>executors</b> (execution, caching through the block manager).",
       "At component level (the five Spark libraries): Spark Core does the scheduling and execution; Spark SQL, Structured Streaming, MLlib and GraphX are built on top of it."]),
    H4("3. How would Spark manage increasing volumes of social-media data?"),
    B(["<b>Scale out</b>: more executors; dynamic allocation adds and removes them with the load.",
       "<b>Partitioning</b> by key and a sensible partition count. The demo aggregates 2 million rows with 1 partition and with 4 partitions and gets the same 4 groups: only the parallelism changes, not the code.",
       "<b>Efficient formats</b> (Parquet, columnar, compressed), caching of reused data, <b>broadcast joins</b> for small tables, salting to handle skewed keys.",
       "<b>Ingest continuously</b> with Structured Streaming (Kafka or files) instead of nightly batches."]),
    H4("4. Identify possible system failures and explain how exception handling improves robustness"),
    B(["Failures: input file missing, malformed records, executor or node loss, network or shuffle timeouts, out-of-memory, driver failure.",
       "In the code a missing input file (`posts_day1.csv`) is caught as an `AnalysisException` with error class `PATH_NOT_FOUND`; the job reports it and continues with the other sources. Unparsable like counts (\"n/a\" and an empty string) are skipped and counted with an accumulator (2 skipped, valid counts 520, 310, 750).",
       "Task failures are retried by Spark itself; a long lineage is shortened with checkpoints; alerts fire when the bad-record ratio is too high."]),
    H4("5. Recommend metrics that help identify trending topics"),
    T(["Metric", "Meaning", "On this data"], [
        ["Total and average likes per post type", "which topics get most reactions", "Technology 1,160 (2 posts, 580 average), Education 750, Sports 310"],
        ["Mentions per time window", "growth of a hashtag hour by hour", "#scala 0 to 2, #spark 1 to 2, #cricket 1 to 0 (invented posts)"],
        ["Engagement rate", "likes + comments + shares divided by impressions", "needs impressions"],
        ["Velocity / spike score", "z-score of today's count against its history", "needs history"],
        ["Sentiment mix", "share of positive, neutral, negative posts per topic", "3 positive, 2 negative (lexicon rule, invented posts)"]], [0.28, 0.36, 0.36]),
    NOTE("The table of the question has no text, so the hashtag and sentiment parts use five invented posts to show the technique. A real sentiment system would use a trained model (Tokenizer, TF-IDF and logistic regression in Spark ML) instead of a word list."),
    H3("Code, run on the dataset of the question"),
    CODE("sa_m4_q4.scala", "Code: code/sa_m4_q4.scala"),
    OUT("sa_m4_q4.out.txt", "Real output", maxlines=70),
])

# ------------------------------------------------------------------------------------------------ Q5
question("M4-Q5", "Financial Risk Analysis using Breeze, Saddle and Spark", "6278527581963359908.jpg", [
    H3("Answer, point by point"),
    NOTE("The screenshot ends after the third bullet; if the original question has more bullets they could not be read. The three visible bullets are answered."),
    H4("1. How can Saddle be used to structure and preprocess the data?"),
    B(["Put the numbers in a labelled <b>Frame</b> (`Income`, `Loan` per CustomerID); keep the text column `Status` in a separate `Vec[String]` because a Frame holds one element type.",
       "<b>Preprocess</b>: fill a missing income (`fillNA(_ => mean)` turns the NaN into 566,667 in the demo), derive new columns with element-wise arithmetic (`loan / income` gives the loan-to-income ratio), filter by condition, sort (riskiest first: L104, L102, L103, L101).",
       "<b>Group statistics</b> with index positions: mean ratio 0.543 for approved loans and 1.271 for rejected loans."]),
    H4("2. Which Breeze functions help compute statistical measures and risk indicators?"),
    T(["Need", "Breeze", "Result"], [
        ["Centre and spread", "`mean`, `stddev`, `variance` on a `DenseVector`", "income: mean 512,500, standard deviation 256,174"],
        ["Loan-to-income ratio", "`ln /:/ inc` (element-wise division)", "0.462, 1.143, 0.625, 1.400"],
        ["Income left after the loan", "`inc - ln` (vector subtraction)", "350,000; -50,000; 300,000; -100,000"],
        ["Correlation, covariance", "`dot` on centred vectors", "correlation income~loan 0.429"],
        ["Standardised income", "`(inc - mean(inc)) /:/ stddev(inc)`", "0.54, -0.63, 1.12, -1.02"],
        ["Rule-based flag", "comparison on the ratio", "ratio above 1.0 means the loan exceeds the income: L102 and L104 (both rejected)"]], [0.26, 0.42, 0.32]),
    P("The ratio separates the two groups cleanly in this sample (approved: 0.46 and 0.63; rejected: 1.14 and 1.40), which is why it is a useful risk indicator. Four loans cannot prove a rule; in practice add the debt-to-income ratio, credit history and employment data."),
    H4("3. How can Spark distribute the loan-analysis tasks across a cluster?"),
    B(["Load the loan table as a DataFrame (from HDFS, S3 or a database) and <b>repartition</b> by a suitable key (customer id range, branch, region). Each partition is one task: the code shows L101 and L104 in partition 0, L102 and L103 in partition 1.",
       "Row-wise work (the ratio, the risk band) runs inside the tasks on all partitions at once; aggregations (`groupBy(\"Status\")`) first aggregate per partition and then combine, so little data is shuffled.",
       "A small shared value such as the risk threshold is sent once to every executor with a <b>broadcast variable</b>.",
       "Model training with <b>MLlib</b> `LogisticRegression`: the coefficient of the loan-to-income ratio is -2.536, the coefficient of income is about 0 once the ratio is in the model. A heavier loan lowers the chance of approval.",
       "The driver then gets only the small result (summary table, coefficients), possibly for Saddle or Breeze to analyse further."]),
    H3("Code 1: Saddle and Breeze"),
    CODE("sa_m4_q5_saddle_breeze.scala", "Code: code/sa_m4_q5_saddle_breeze.scala"),
    OUT("sa_m4_q5_saddle_breeze.out.txt", "Real output", maxlines=60),
    H3("Code 2: Spark"),
    CODE("sa_m4_q5_spark.scala", "Code: code/sa_m4_q5_spark.scala"),
    OUT("sa_m4_q5_spark.out.txt", "Real output", maxlines=60),
])
