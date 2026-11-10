"""Authored HOT question (Module 2): A/B comparison of two teaching methods with NumPy and SciPy."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

a = np.array([85, 90, 78, 92, 88, 76])
b = np.array([70, 65, 80, 72, 68, 74])
print("--- step 1: describe each group with NumPy ---")
for name, g in (("Method A", a), ("Method B", b)):
    print(f"{name}: n={g.size}, mean={g.mean():.2f}, median={np.median(g):.1f}, sample std={g.std(ddof=1):.2f}, min={g.min()}, max={g.max()}")
print("note: np.std defaults to the POPULATION std (ddof=0):", round(a.std(), 2), "versus the sample std (ddof=1):", round(a.std(ddof=1), 2))
print("difference of means:", round(a.mean() - b.mean(), 2))

print("\n--- step 2: choose and run the test ---")
t, p = stats.ttest_ind(a, b)
tw, pw = stats.ttest_ind(a, b, equal_var=False)
print(f"Student t-test (equal variances): t={t:.3f}, p={p:.4f} | Welch t-test (unequal variances): t={tw:.3f}, p={pw:.4f}")
u, pu = stats.mannwhitneyu(a, b, alternative="two-sided")
print(f"Mann-Whitney U (no normality assumption): U={u:.1f}, p={pu:.4f}")
print("variance check, Levene test p =", round(stats.levene(a, b).pvalue, 3), "| normality (Shapiro) p for A, B:", round(stats.shapiro(a).pvalue, 3), round(stats.shapiro(b).pvalue, 3))

print("\n--- step 3: effect size and confidence interval ---")
sp = np.sqrt(((a.size - 1) * a.var(ddof=1) + (b.size - 1) * b.var(ddof=1)) / (a.size + b.size - 2))
d = (a.mean() - b.mean()) / sp
se = sp * np.sqrt(1 / a.size + 1 / b.size)
tcrit = stats.t.ppf(0.975, a.size + b.size - 2)
lo, hi = (a.mean() - b.mean()) - tcrit * se, (a.mean() - b.mean()) + tcrit * se
print(f"Cohen's d = {d:.2f} (about 0.8 or more is a large effect) | 95% CI for the difference of means: [{lo:.1f}, {hi:.1f}]")
print("the interval excludes 0, which agrees with p < 0.05")

print("\n--- step 4: paired design would be different ---")
before = np.array([70, 65, 80, 72, 68, 74]); after = before + np.array([5, 7, 2, 6, 4, 3])
print("paired t-test (same students measured twice):", tuple(round(float(x), 4) for x in stats.ttest_rel(after, before)), "| using ttest_ind here would ignore the pairing")

fig, ax = plt.subplots(1, 2, figsize=(7.5, 3.1))
ax[0].boxplot([a, b], tick_labels=["Method A", "Method B"]); ax[0].set_title("Scores by method"); ax[0].set_ylabel("marks")
ax[1].hist(a, alpha=0.6, label="A", bins=5); ax[1].hist(b, alpha=0.6, label="B", bins=5); ax[1].legend(); ax[1].set_title("Histogram")
fig.tight_layout(); fig.savefig("hot_m2_q8.png", dpi=140)
print("saved hot_m2_q8.png")
