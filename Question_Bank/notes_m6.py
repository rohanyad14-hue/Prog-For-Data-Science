from dsl import *

sub_6_1 = SUB("6.1", "Privacy, security and ethics in data work", [
    WARN("The syllabus gives Module 6 no topic list. These sections cover themes that usually come under 'contemporary issues'. Confirm with your faculty which topics were taught."),
    B(["<b>Personal data</b> identifies a person directly or with other data. Laws to know by name: the EU General Data Protection Regulation (GDPR) and India's Digital Personal Data Protection Act, 2023.",
       "Principles: lawful basis and consent, purpose limitation, <b>data minimisation</b> (collect only what is needed), storage limitation (delete when no longer needed), accuracy, security, accountability.",
       "<b>Anonymised</b> data cannot be linked back to a person; <b>pseudonymised</b> data can, using separately kept extra information, so it is usually still personal data.",
       "Security basics: least-privilege access, encryption at rest and in transit, audit logs, secrets in a vault or environment variables (never in code), patched dependencies."]),
    QA("List practices for handling personal data in a pipeline.", [P("Get a lawful basis and consent; minimise the fields; pseudonymise or anonymise before analysis; control access; encrypt; log access; set retention limits; document lineage so you can show where data came from and who used it.")], "5 marks"),
    QA("Anonymisation versus pseudonymisation.", [P("Anonymisation is irreversible; pseudonymisation replaces identifiers with tokens but keeps a mapping, so the data can be re-identified by whoever holds it and is still regulated as personal data.")], "tricky"),
    QA("Why should API keys not be in source code?", [P("Source code is shared and committed to version control; a leaked key can be abused. Keep it in an environment variable or secrets manager and rotate it if exposed.")], "2 marks"),
])

sub_6_2 = SUB("6.2", "Bias, fairness and responsible AI", [
    B(["Bias enters through unrepresentative data, historical prejudice in labels, proxy features (a postcode standing in for a protected attribute) and evaluation only on the overall average.",
       "Mitigation: audit and rebalance data, review features, evaluate metrics <b>per group</b>, set fairness checks before release, keep a human in the loop, document the model (purpose, limits) and allow appeals."]),
    QA("Where does bias in a machine-learning system come from and how can it be reduced?", [T(["Source", "Mitigation"], [["unrepresentative or historically biased training data", "audit, rebalance, collect missing groups"], ["proxy features", "review and constrain features"],
                                                                                                                         ["biased labels", "clear guidelines, several annotators"], ["only the overall metric", "report metrics per group"]], [0.5, 0.5])], "5 marks"),
    QA("A model is 95% accurate overall but wrong for 40% of one minority group. Is it acceptable?", [P("Not without investigation. The overall average hides a large per-group error. Report per-group error rates (compare with the metrics in 2.10), find the cause (data coverage, features) and fix or restrict use.")], "3 marks"),
])

sub_6_3 = SUB("6.3", "Generative AI and AI coding assistants", [
    B(["Large language models generate plausible text and code; they can <b>hallucinate</b> (fluent but wrong or invented answers), reproduce outdated or insecure patterns, and raise privacy and licensing questions when private data or code is pasted in.",
       "Good practice: treat output as a draft, run and test it, check statistics and API usage against documentation, never paste secrets or personal data, cite assistance where required, and be able to explain every line."]),
    QA("Benefits and risks of AI coding assistants for data-science programming?", [P("Benefits: faster boilerplate, explanations, test ideas. Risks: wrong or hallucinated code, subtle statistical errors (for example data leakage as in 2.10), insecure code, over-reliance that weakens understanding, and data privacy. Mitigate by testing, reading documentation and keeping private data out.")], "5 marks"),
    QA("Why can an assistant's pipeline code that 'works' still be wrong?", [P("It may run without errors while leaking test data into training, scaling before the split, or mis-specifying a join. Run the checks in these notes (pipelines, `validate=` in merges) and compare results by hand on small data.")], "tricky"),
])

sub_6_4 = SUB("6.4", "Model and data drift, monitoring, reproducibility", [
    B(["<b>Data drift</b>: the distribution of incoming data changes. <b>Concept drift</b>: the relationship between inputs and target changes. Either lowers accuracy after deployment.",
       "Monitor input statistics and model metrics, alert on thresholds, retrain on a schedule or trigger, version data, code and models, and fix random seeds so results can be reproduced."]),
    QA("What is drift and how do you handle it?", [P("A change after deployment in the data or in the input-target relationship. Handle it with monitoring, alerts and retraining on recent data, plus versioned data and models so you can roll back.")], "3 marks"),
    QA("Why do these notes set `random_state`/`default_rng(seed)` in every demo?", [P("Reproducibility: with a fixed seed the same numbers appear on each run, so results can be checked, compared and debugged.")], "2 marks"),
])

NOTES_6 = NMODULE(
    6, "Contemporary issues", "2 hours", "no topics are listed in the syllabus.",
    [("Privacy, security, ethics", "6.1"), ("Bias and responsible AI", "6.2"), ("Generative AI and coding assistants", "6.3"), ("Drift, monitoring, reproducibility", "6.4")],
    [sub_6_1, sub_6_2, sub_6_3, sub_6_4],
)
