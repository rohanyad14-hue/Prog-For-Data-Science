from dsl import *

mcqs = [
    MCQ("A team of data scientists who already know Python must deliver an ML prototype in four weeks. Which criteria weigh most?",
        ["performance and security only", "time to production and skill set", "IDE availability only", "elasticity only"], 1,
        "Short deadline plus existing skills favour the language the team already knows, with a rich ML ecosystem (Python)."),
    MCQ("Static typing mainly helps a large codebase because:",
        ["it makes programs shorter", "many type errors are caught at compile time and refactoring is safer",
         "it removes the need for tests", "it makes the program run on any platform"], 1,
        "Compile-time checking supports maintenance and error diagnosis. It does not replace tests."),
    MCQ("Apache Spark itself is mainly written in:", ["Python", "R", "Scala", "C#"], 2,
        "Scala (running on the JVM). Python, R, Java and SQL are language APIs on top."),
    MCQ("\"Elasticity of a language\" refers to:",
        ["how quickly it compiles", "how well it covers small scripts up to large systems and adapts to changing needs",
         "the price of the licence", "the number of keywords"], 1, "Can the same language serve a quick script, a service and a distributed pipeline?"),
    MCQ("For a pure CPU-bound loop written in the language itself, which is typically fastest?",
        ["CPython", "R", "Scala/Java on the JVM (JIT compiled)", "a shell script"], 2,
        "JIT-compiled JVM code beats the CPython interpreter. Python code is fast only when it calls compiled libraries such as NumPy."),
    MCQ("A weighted decision matrix is used to:",
        ["measure code coverage", "score each option against weighted criteria and compare totals", "choose a database index", "estimate cloud cost exactly"], 1,
        "Weights reflect the project's priorities; the highest weighted total wins, and the result should be sanity-checked."),
    MCQ("Which tool is the usual IDE choice for Scala development?",
        ["RStudio", "IntelliJ IDEA with the Scala plugin", "Xcode only", "Notepad only"], 1, "VS Code with Metals is the other common option."),
    MCQ("Python numerical code is fast mostly because:",
        ["the interpreter is the fastest", "heavy work runs in compiled C/C++/Fortran libraries (NumPy, SciPy)", "it has no garbage collection", "it is statically typed"], 1,
        "Vectorised calls move the loop out of the interpreter."),
]

shorts = [
    SHORT("Explain \"size of the deployment\": data, resource and load.", 3, [
        B(["<b>Data</b>: gigabytes on a laptop (pandas) versus terabytes across a cluster (Spark).",
           "<b>Resource</b>: memory, CPU and budget available; a JVM service needs heap tuning, a script may need none.",
           "<b>Load</b>: number of concurrent users or events per second; high concurrency favours the JVM (Scala, Java) and its mature concurrency libraries."])]),
    SHORT("Why is security a language-selection criterion?", 3, [
        P("It decides how easily you can meet requirements such as authentication, encryption, input validation and audit. Look at the maturity of security libraries, "
          "memory safety, how dependencies are vetted (supply-chain risk), patch frequency and available expertise. Static typing and sandboxing help, "
          "but the application design matters more than the language alone.")]),
    SHORT("How do skill set and community support influence the choice?", 3, [
        P("A language the team already knows shortens delivery and reduces defects. A large community means more libraries, documentation, answered questions, "
          "and easier hiring (Python has the largest data-science pool; Scala has fewer but specialised data engineers). Check also how actively the key libraries are maintained.")]),
    SHORT("Discuss the trade-off between time to production and performance.", 3, [
        P("Python gets a working version out quickly, which matters while requirements are uncertain. Scala/Java need more up-front effort but run faster and "
          "scale better on a JVM cluster. A common strategy: prototype in Python, then move the performance-critical path to Scala/Java (or use PySpark DataFrames, "
          "which execute in the JVM engine, and avoid slow Python UDFs).")]),
    SHORT("What is meant by the elasticity of a language?", 2, [
        P("Its ability to stretch from a short exploratory script to a large, long-lived production system, and to adapt as requirements change. "
          "Scala (concise scripts to large typed systems) and Python (with typing and packaging tools) score well; a language only good for one-off analysis scores lower.")]),
    SHORT("Explain the importance of IDE availability and error checking or diagnosis.", 3, [
        B(["IDE: code completion, refactoring, debugging, profiling and test integration raise productivity (IntelliJ IDEA, PyCharm, VS Code, RStudio).",
           "Error checking: compile-time checks (Scala, Java) catch type errors before running; dynamic languages find them at run time, so they need tests, linters and type hints.",
           "Diagnosis: quality of stack traces, debuggers and logging decides how fast production incidents are fixed."])]),
    SHORT("Compare static and dynamic typing for maintenance.", 3, [
        T(["", "Static (Scala, Java)", "Dynamic (Python, R)"], [
            ["Type errors found", "at compile time", "at run time"],
            ["Refactoring large code", "safer, compiler guides you", "needs good tests"],
            ["Speed of writing", "more annotations (less in Scala via inference)", "faster to write"],
            ["Tooling", "precise completion and navigation", "good with type hints, weaker without"]], [0.24, 0.38, 0.38])]),
    SHORT("List five criteria that favour Python and five that favour Scala.", 5, [
        T(["Favours Python", "Favours Scala"], [
            ["Time to production", "Performance on CPU-bound work"],
            ["Large talent pool", "Big-data deployment size and load"],
            ["ML and data-science ecosystem", "Native fit with Spark and the JVM"],
            ["Gentle learning curve and REPL/notebooks", "Static typing for maintenance of large code"],
            ["Huge community (PyPI)", "Concurrency and streaming pipelines"]], [0.5, 0.5])]),
]

# ------------------------------------------------------------------------------------------ longs
c1_prompt = [
    P("(FAT high-frequency question 7) Compare Python, Scala, Java and R across the language-selection criteria in the syllabus and give an architectural "
      "justification for when to use each."),
]
c1_answer = [
    P("Judgements below are typical, not absolute; always tie your answer to a stated project."),
    T(["Criterion", "What you ask", "Python", "Scala", "Java", "R"], [
        ["Size of deployment (data, resource, load)", "how much data, how many users, what hardware", "small to medium; scales via Spark/Dask", "very large, high concurrency", "very large, high concurrency", "memory-bound, small to medium"],
        ["Security", "libraries, memory safety, vetting", "good; vet dependencies", "JVM security stack", "mature enterprise stack", "limited for services"],
        ["Skill set", "what the team knows", "largest pool", "smaller, specialised", "large pool", "statisticians"],
        ["Targeted platform", "where it runs", "anywhere, notebooks, cloud", "JVM, Spark clusters", "JVM everywhere", "analysis workstation, Shiny"],
        ["Elasticity", "script to large system", "good", "very good", "good, verbose", "mostly analysis"],
        ["Time to production", "delivery speed", "fastest", "slower", "slower", "fast for analysis"],
        ["Performance", "CPU-bound speed", "slow alone, fast via C libraries", "fast (JIT)", "fast (JIT)", "slow alone"],
        ["Support and community", "libraries, answers", "PyPI, huge", "smaller, strong in data engineering", "Maven, huge", "CRAN, strong in statistics"],
        ["Purpose", "ML, ETL, web, stats", "ML, analysis, glue", "Spark jobs, streaming", "enterprise services", "statistical modelling, reports"],
        ["Programmer experience", "readability, REPL", "very good", "expressive, steeper", "verbose", "good for statisticians"],
        ["Ease of maintenance", "refactoring, typing", "needs tests/type hints", "strong typing", "strong typing", "weaker"],
        ["Efficiency", "memory, CPU", "overhead per object", "JVM tuned", "JVM tuned", "copies data often"],
        ["IDE availability", "tooling", "PyCharm, VS Code, notebooks", "IntelliJ, Metals", "IntelliJ, Eclipse", "RStudio"],
        ["Error checking and diagnosis", "compile vs run time", "run time, linters", "compile time", "compile time", "run time"]],
      [0.17, 0.17, 0.17, 0.17, 0.16, 0.16]),
    H3("When to use each"),
    B(["<b>Python</b>: exploratory analysis, machine learning, quick prototypes, glue code, teams with mixed backgrounds.",
       "<b>Scala</b>: Spark jobs, streaming and batch pipelines, high-throughput data services, large codebases that need strong typing and functional style.",
       "<b>Java</b>: enterprise back-ends and integration with existing JVM systems; broad hiring pool.",
       "<b>R</b>: statistical modelling, publication-quality graphics, reports in domains with strong R packages."]),
]

c2_prompt = [
    P("<b>Case A.</b> A bank needs a real-time fraud-detection pipeline that processes about 5 TB of transactions per day on a Spark cluster. The team has eight "
      "experienced JVM engineers. <b>Case B.</b> A start-up with three data scientists must deliver an ML prototype in six weeks using small CSV and Parquet files. "
      "For each case choose a language and justify it with a weighted decision matrix."),
]
c2_answer = [
    P("Method: (1) list the criteria that matter, (2) give each a weight so that weights add up to 1, (3) score each candidate from 1 to 5, "
      "(4) multiply and add, (5) compare totals and sanity-check the winner against the case facts."),
    T(["Criterion", "Python", "Scala", "Java", "R", "Weight A", "Weight B"], [
        ["Deployment size / load", "3", "5", "5", "2", "0.25", "0.05"],
        ["Performance", "2", "5", "5", "2", "0.20", "0.05"],
        ["Time to production", "5", "3", "3", "4", "0.05", "0.30"],
        ["Skill set available", "5", "2", "4", "2", "0.10", "0.25"],
        ["Ecosystem / community", "5", "4", "5", "3", "0.05", "0.20"],
        ["Maintainability", "3", "5", "4", "2", "0.15", "0.05"],
        ["Platform fit (Spark/JVM)", "3", "5", "4", "1", "0.20", "0.10"]], [0.28, 0.1, 0.1, 0.1, 0.1, 0.16, 0.16]),
    P("Example calculation, Case A, Scala: 0.25x5 + 0.20x5 + 0.05x3 + 0.10x2 + 0.05x4 + 0.15x5 + 0.20x5 = 1.25 + 1.00 + 0.15 + 0.20 + 0.20 + 0.75 + 1.00 = <b>4.55</b>."),
    CODE("m5_decision_matrix.py"),
    OUT("m5_decision_matrix.out.txt"),
    H3("Conclusions"),
    B(["<b>Case A -> Scala</b> (4.55; Java is close at 4.45). Throughput, concurrency, native Spark integration and strong typing dominate, and the team already knows the JVM, "
       "so Scala or Java is justified; Python scores 3.20 mainly because of performance and platform fit.",
       "<b>Case B -> Python</b> (4.45). Delivery speed, the available skills and the ML ecosystem dominate. Scala scores 3.45 because its slower start and smaller talent pool hurt in six weeks.",
       "The scores are the analyst's judgement; the value of the matrix is that it makes the reasoning explicit and lets stakeholders change a weight and see the effect. "
       "If Case B later grows to terabytes, revisit the weights: the decision can change."]),
]

longs = [
    LONG("Python versus Scala versus Java versus R", 10, c1_prompt, c1_answer,
         "criteria covered (at least 8) 5, comparison across languages 3, when to use each 2."),
    LONG("Language selection case studies with a decision matrix", 10, c2_prompt, c2_answer,
         "method and weights 3, scoring and arithmetic 3, justification of each choice 3, caveats 1."),
]

MODULE_5 = MODULE(
    5, "Programming language selection criteria", "6 hours",
    "size of the deployment (data, resource and load); security; skill set; targeted platform; elasticity of a language; time to production; performance; "
    "support and community; purpose; programmer experience; ease of development and maintenance; efficiency; availability of an IDE; error checking and diagnosis.",
    [P("Your FAT notes group the same ideas into <b>13 criteria</b> (for example IDE and diagnostics together); the syllabus names about fourteen. "
       "Use the syllabus wording in answers and mention the grouping if the question says \"13\"."),
     P("Textbooks for this module are not specific; the reference listed in the syllabus is an article on factors to consider when choosing a programming language "
       "(see the resources section).")],
    mcqs, shorts, longs,
    exam_notes=[TIP("Never answer \"which language is best\". Answer \"best for this project, because criteria X and Y outweigh Z\". "
                    "Quote facts from the scenario in each justification.")],
)
