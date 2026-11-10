from dsl import *
from notes_util import pick

sub_5_1 = SUB("5.1", "The language-selection criteria", [
    P("The syllabus names these criteria. Your FAT notes group them into 13 (IDE and diagnostics together). For each one, know the <b>question to ask</b> and an example of how it can tip the decision."),
    T(["Criterion", "Question to ask", "Typical lean"], [
        ["Size of the deployment (data, resource, load)", "how much data, how many users or events per second, what hardware?", "large and concurrent: Scala/Java on a cluster; small and exploratory: Python"],
        ["Security", "authentication, encryption, input validation, memory safety, dependency vetting?", "mature enterprise stacks on the JVM; any language needs secure design and patched dependencies"],
        ["Skill set", "what does the team already know; who can we hire?", "Python has the largest data-science pool; Scala engineers are fewer and specialised"],
        ["The targeted platform", "where will it run: JVM cluster, cloud, notebook, browser, device?", "Spark/JVM: Scala, Java (or PySpark); embedded devices: C/C++"],
        ["Elasticity of a language", "can it serve a script, a service and a distributed pipeline, and adapt as needs change?", "Scala and Python stretch widely; R is mostly analysis"],
        ["Time to production", "how fast can we deliver a working version?", "Python for prototypes"],
        ["Performance", "CPU-bound speed, latency, throughput?", "JIT-compiled JVM code is faster than CPython; Python is fast only through C libraries (NumPy)"],
        ["Support and community", "libraries, documentation, answers, long-term maintenance?", "PyPI and Maven are huge; check that the key libraries are actively maintained"],
        ["Purpose", "ML, ETL, streaming, web, statistics?", "ML: Python; Spark jobs: Scala; statistics: R"],
        ["Programmer experience", "readability, REPL/notebooks, learning curve?", "Python is gentle; Scala is expressive but steeper"],
        ["Ease of development and maintenance", "refactoring safety, testing, typing?", "static typing (Scala, Java) helps large code bases; Python needs tests and type hints"],
        ["Efficiency", "memory, CPU and energy cost per result?", "JVM tuning vs Python per-object overhead"],
        ["Availability of an IDE", "debugger, profiler, completion, refactoring tools?", "IntelliJ IDEA (Scala/Java), PyCharm/VS Code (Python), RStudio (R)"],
        ["Error checking and diagnosis", "are errors found at compile time or run time; how good are stack traces and debuggers?", "static languages catch type errors before running; dynamic ones need tests and linters"]], [0.24, 0.38, 0.38]),
    QA("Explain 'size of the deployment: data, resource and load'.", [P("Data: gigabytes in pandas versus terabytes on Spark. Resource: memory, CPU and budget (a JVM service needs heap sizing). Load: concurrent users or events per second; high concurrency favours the JVM and its concurrency libraries.")], "3 marks"),
    QA("Why can a language that is fast for development be slow in production, and what can be done?", [P("CPython interprets bytecode and has per-object overhead; heavy loops are slow unless the work is vectorised (NumPy) or moved to compiled code. Remedies: vectorise, use PySpark DataFrames (they run in the JVM), rewrite hot paths in Scala/Java/C, profile first.")], "3 marks"),
    QA("Explain the 'elasticity of a language'.", [P("How well the same language covers small scripts through to large systems, and adapts to changing requirements. Scala (concise scripts to large typed systems) and Python (with packaging and type hints) score well.")], "2 marks"),
    QA("Static versus dynamic typing for maintenance.", [T(["", "Static (Scala, Java)", "Dynamic (Python, R)"], [["Type errors", "compile time", "run time"], ["Refactoring large code", "compiler guides you", "needs good tests"], ["Writing speed", "more annotations (inference reduces them)", "faster to write"]], [0.25, 0.375, 0.375])], "3 marks"),
])

sub_5_2 = SUB("5.2", "Python, Scala, Java and R compared", [
    T(["", "Python", "Scala", "Java", "R"], [
        ["Typing", "dynamic (hints optional)", "static, inferred", "static, verbose", "dynamic"],
        ["Runs on", "CPython interpreter", "JVM", "JVM", "R interpreter"],
        ["Strength", "ML ecosystem, readability, notebooks", "Spark, streaming, functional + OO", "enterprise services, huge ecosystem", "statistics, graphics, reports"],
        ["Weakness", "slow in pure loops; GIL limits threads", "steeper learning, slower compile, fewer people", "verbose", "weaker for production services"],
        ["Typical use", "analysis, ML, prototypes, glue", "big-data pipelines, high-throughput jobs", "back-end systems, integration", "statistical modelling"]], [0.14, 0.22, 0.24, 0.2, 0.2]),
    B(["<b>PySpark versus Scala Spark</b>: DataFrame operations run in the JVM engine either way, so speed is similar; Python UDFs and RDD lambdas run in Python worker processes and pay serialisation cost. Scala gives typed Datasets and first access to new APIs.",
       "The 'best' language depends on the project: tie every recommendation to criteria and facts of the scenario."]),
    QA("Compare Python and Scala across the selection criteria.", [P("Use the 14-row table in 5.1 plus: Python wins on time to production, skills and ML ecosystem; Scala wins on performance, load, platform fit with Spark, and maintainability of large code. Close with a recommendation for a stated scenario.")], "10 marks"),
    QA("When would you choose R?", [P("For statistical analysis, specialist CRAN packages, and publication-quality graphics or reports (R Markdown, Shiny), usually by statisticians and for small to medium data; less often for production services.")], "2 marks"),
    QA("Is PySpark slower than Scala Spark?", [P("For DataFrame/SQL code it is about the same because the plan runs in the JVM. It is slower when Python functions run per row (UDFs, `rdd.map(lambda ...)`), because rows are serialised between the JVM and Python workers.")], "tricky"),
])

sub_5_3 = SUB("5.3", "Weighted decision matrix (worked example)", [
    B(["Method: list the criteria that matter; give each a weight (weights sum to 1); score each language 1 to 5 on each criterion; multiply, add, compare; sanity-check the winner against the scenario.",
       "The scores are judgements; the method makes the reasoning explicit and lets stakeholders change a weight and see the effect."]),
    CODE("m5_decision_matrix.py", "Code (tested)"),
    OUT("m5_decision_matrix.out.txt", "Verified output"),
    QA("Case A: fraud detection at 5 TB/day on Spark with eight JVM engineers. Case B: a three-person start-up ML prototype in six weeks. Which language for each?", [
        P("Case A: Scala (4.55, Java 4.45, Python 3.20) because throughput, load, Spark fit and maintainability dominate. Case B: Python (4.45, Java 4.00, Scala 3.45) because time to production, skills and ecosystem dominate. If Case B later reaches terabytes, change the weights and decide again.")], "10 marks"),
    QA("Compute Scala's weighted score for Case A: scores 5, 5, 3, 2, 4, 5, 5 with weights 0.25, 0.20, 0.05, 0.10, 0.05, 0.15, 0.20.", [P("1.25 + 1.00 + 0.15 + 0.20 + 0.20 + 0.75 + 1.00 = 4.55.")], "tricky"),
    QA("What are the weaknesses of a weighted decision matrix?", [P("Subjective scores and weights, false precision, criteria that overlap and double count, and neglect of one deal-breaker (for example a mandatory platform). Use it to structure the discussion, not to replace it.")], "3 marks"),
])

NOTES_5 = NMODULE(
    5, "Programming language selection criteria", "6 hours",
    "size of the deployment (data, resource and load); security; skill set; targeted platform; elasticity of a language; time to production; performance; support and community; purpose; programmer experience; ease of development and maintenance; efficiency; availability of an IDE; error checking and diagnosis.",
    [("All fourteen criteria", "5.1"), ("Comparing languages (Python, Scala, Java, R)", "5.2"), ("Applying the criteria to a case study", "5.3")],
    [sub_5_1, sub_5_2, sub_5_3],
)
