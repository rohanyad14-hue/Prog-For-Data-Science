"""M5  Weighted decision matrix for language selection (two case studies).
Scores are 1-5 judgement values chosen by the analyst - the point is the method.
"""
CRITERIA = ["Deployment size / load", "Performance", "Time to production", "Skill set available",
            "Ecosystem / community", "Maintainability", "Platform fit (Spark/JVM)"]
SCORES = {                      # criterion order as above
    "Python": [3, 2, 5, 5, 5, 3, 3],
    "Scala":  [5, 5, 3, 2, 4, 5, 5],
    "Java":   [5, 5, 3, 4, 5, 4, 4],
    "R":      [2, 2, 4, 2, 3, 2, 1],
}
CASES = {
    "Case A: real-time fraud detection, 5 TB/day, Spark cluster, 8 experienced JVM engineers":
        [0.25, 0.20, 0.05, 0.10, 0.05, 0.15, 0.20],
    "Case B: 6-week ML prototype for a startup, 3 data scientists, small CSV/Parquet data":
        [0.05, 0.05, 0.30, 0.25, 0.20, 0.05, 0.10],
}
for case, weights in CASES.items():
    assert abs(sum(weights) - 1.0) < 1e-9
    print(case)
    print("  weights:", dict(zip(CRITERIA, weights)))
    ranking = sorted(((sum(w * s for w, s in zip(weights, sc)), lang) for lang, sc in SCORES.items()),
                     reverse=True)
    for total, lang in ranking:
        print(f"    {lang:<7} weighted score = {total:.2f}")
    print("  -> choose", ranking[0][1], "\n")
