from dsl import *

mcqs = [
    MCQ("The GDPR principle of \"data minimisation\" means:",
        ["store everything in case it is useful", "collect and keep only the data needed for the stated purpose",
         "encrypt all data twice", "delete data after one day"], 1, "Less data collected means less risk and easier compliance."),
    MCQ("A model trained on historically biased hiring data is most likely to:",
        ["remove the bias automatically", "reproduce or amplify the bias in its predictions",
         "refuse to predict", "become more accurate for every group"], 1, "Models learn patterns in the data, including unfair ones."),
    MCQ("An LLM \"hallucination\" is:",
        ["a slow response", "a fluent but incorrect or invented answer", "a syntax error", "a network timeout"], 1,
        "Generated code and facts must be verified, never trusted blindly."),
    MCQ("Pseudonymised data differs from anonymised data because:",
        ["it is public", "it can be linked back to a person using extra information that is kept separately", "it is encrypted", "it has fewer rows"], 1,
        "Truly anonymised data cannot be re-identified; pseudonymised data usually still counts as personal data under privacy laws."),
    MCQ("\"Data drift\" after deployment means:",
        ["the file moves to another disk", "the statistics of incoming data change, so the model's accuracy may fall", "the schema is deleted", "Spark loses an executor"], 1,
        "Monitor input distributions and model metrics, and retrain when needed."),
]

shorts = [
    SHORT("List practices for responsible handling of personal data in a data-science pipeline.", 5, [
        B(["Lawful basis and consent; collect the minimum data for the purpose.",
           "Access control (least privilege), encryption at rest and in transit, audit logs.",
           "Pseudonymise or anonymise before analysis; keep keys separate.",
           "Retention limits and deletion on request.",
           "Document data lineage so you can show where each field came from and who used it."]),
        P("Laws to know by name: the EU General Data Protection Regulation (GDPR) and India's Digital Personal Data Protection Act, 2023.")]),
    SHORT("Where does bias in a machine-learning system come from, and how can it be reduced?", 5, [
        T(["Source", "Mitigation"], [
            ["Unrepresentative or historically biased training data", "audit and rebalance data; collect missing groups"],
            ["Proxy features that encode sensitive attributes (such as a postcode)", "feature review; remove or constrain proxies"],
            ["Labels created by biased people", "clear labelling guidelines; multiple annotators"],
            ["Evaluation only on the overall average", "report metrics per group; set fairness checks before release"]], [0.5, 0.5])]),
    SHORT("What are the benefits and risks of using an AI coding assistant for data-science programming?", 3, [
        P("Benefits: faster boilerplate, explanations, test generation. Risks: plausible but wrong code (hallucination), insecure or outdated API usage, "
          "licence and data-leakage concerns when pasting private data. Good practice: read and run what you accept, write tests, never paste secrets or personal data, "
          "and be able to explain every line (the viva will ask).")]),
    SHORT("What is model or data drift and how do you handle it?", 3, [
        P("Drift is a change after deployment in the input data (data drift) or in the relationship between inputs and target (concept drift). "
          "Handle it by monitoring input statistics and model metrics, alerting on thresholds, and retraining with recent data on a schedule or trigger.")]),
]

c1_prompt = [
    P("A hospital wants to predict patient re-admission using ten years of records (about 4 TB) on a Spark cluster. Discuss the privacy, security and fairness issues, "
      "and justify the language(s) you would use for the pipeline and the modelling."),
]
c1_answer = [
    T(["Concern", "What to do"], [
        ["Privacy", "obtain the lawful basis and ethics approval; remove direct identifiers; pseudonymise with keys kept apart; minimise the fields used"],
        ["Security", "role-based access, encryption at rest and in transit, audit logging, isolated cluster network, no personal data in notebooks or chat tools"],
        ["Fairness", "check the data covers age, gender and region groups; evaluate error rates per group; review proxy features"],
        ["Quality and drift", "validate schemas on ingestion; monitor drift after deployment"],
        ["Language choice", "Scala (or PySpark DataFrames) for the 4 TB ETL on Spark; Python with scikit-learn or MLlib for modelling because of the ML ecosystem and the data-science team's skills"]],
      [0.2, 0.8]),
    P("A short, structured answer that names the risk, the mitigation and links the language choice to the Module 5 criteria earns the marks."),
]

c2_prompt = [
    P("Discuss how AI coding assistants change the way data-science programs are written, and give guidelines for using them responsibly in a university course."),
]
c2_answer = [
    B(["<b>Changes</b>: faster drafts of data loading, cleaning and plotting code; quick explanation of unfamiliar APIs; more time for design and interpretation.",
       "<b>Risks</b>: wrong or hallucinated code, subtle statistical mistakes, insecure patterns, over-reliance that weakens understanding, and privacy issues.",
       "<b>Guidelines</b>: treat output as a draft; run it on small data and check results by hand; add tests; do not share personal or confidential data; "
       "cite assistance where the course requires it; follow the academic-integrity policy of your institute."]),
    P("Link to the course: the lab experiments are designed so you understand the steps (for example the Scala combinators or the pandas merge). "
      "If you cannot explain a line the assistant produced, you do not yet own it."),
]

longs = [
    LONG("Responsible data science: a hospital pipeline", 10, c1_prompt, c1_answer,
         "privacy 3, security 2, fairness 2, language justification 3."),
    LONG("AI coding assistants in data-science work", 10, c2_prompt, c2_answer,
         "changes 3, risks 3, guidelines 3, link to course 1."),
]

MODULE_6 = MODULE(
    6, "Contemporary issues", "2 hours",
    "no topics are listed in the syllabus.",
    [WARN("The syllabus gives Module 6 no topic list, so the questions here cover themes that normally appear under \"contemporary issues\" "
          "(privacy and security, bias, generative AI, drift). Ask your faculty which topics were taught and drop or replace these accordingly.")],
    mcqs, shorts, longs,
)
