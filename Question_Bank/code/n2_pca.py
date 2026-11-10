"""Notes M2: PCA step by step on a 5-point dataset, checked against SVD and scikit-learn."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_iris, make_classification
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

np.set_printoptions(precision=4, suppress=True)
X = np.array([[2, 1], [3, 5], [4, 3], [5, 6], [6, 5]], dtype=float)
n = len(X)

print("STEP 1  mean and centering")
mu = X.mean(axis=0)
Xc = X - mu
print("mean =", mu, "\ncentered data:\n", Xc, "\ncolumn sums of centered data:", Xc.sum(axis=0))

print("\nSTEP 2  covariance matrix  C = Xc^T Xc / (n-1)")
C = Xc.T @ Xc / (n - 1)
print(C, "| same as np.cov:", np.allclose(C, np.cov(X.T)))
print("variances on the diagonal:", np.diag(C), "| covariance off-diagonal:", C[0, 1], "| total variance (trace):", np.trace(C))

print("\nSTEP 3  eigenvalues and eigenvectors  (C v = lambda v)")
tr, det = np.trace(C), np.linalg.det(C)
disc = np.sqrt(tr ** 2 - 4 * det)
lam_hand = np.array([(tr + disc) / 2, (tr - disc) / 2])
print(f"characteristic equation: lambda^2 - {tr:.2f} lambda + {det:.4f} = 0  ->  lambda = {lam_hand[0]:.4f}, {lam_hand[1]:.4f}")
w, V = np.linalg.eigh(C)
order = np.argsort(w)[::-1]
w, V = w[order], V[:, order]
print("eigenvalues (sorted):", w, "| eigenvectors as columns:\n", V)
v1_hand = np.array([C[0, 1], lam_hand[0] - C[0, 0]])
v1_hand /= np.linalg.norm(v1_hand)
print("hand-built PC1 from (C - lambda I)v = 0:", v1_hand, "| orthogonal PCs: v1.v2 =", round(float(V[:, 0] @ V[:, 1]), 10))

print("\nSTEP 4  explained variance")
ratio = w / w.sum()
print("explained variance ratio:", ratio, "| cumulative:", np.cumsum(ratio))

print("\nSTEP 5  project  Z = Xc W  (keep k = 1)")
Z = Xc @ V[:, :1]
print("scores on PC1:", Z.ravel(), "| variance of scores:", round(float(Z.var(ddof=1)), 4), "= lambda1")

print("\nSTEP 6  reconstruct and measure the loss")
Xhat = Z @ V[:, :1].T + mu
print("reconstruction from 1 component:\n", Xhat)
sse = ((X - Xhat) ** 2).sum()
print("squared error =", round(float(sse), 4), "| (n-1) * discarded eigenvalue =", round(float((n - 1) * w[1]), 4))

print("\nCHECK  SVD route and scikit-learn")
U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
print("singular values^2/(n-1):", S ** 2 / (n - 1), "| components (rows of Vt):\n", Vt)
pca = PCA(n_components=2).fit(X)
print("sklearn explained_variance_:", pca.explained_variance_, "| ratio:", pca.explained_variance_ratio_)
print("sklearn components_:\n", pca.components_, "\n(signs of a component may be flipped: -v and v are the same direction)")
print("sklearn transform equals centered data @ components^T:", np.allclose(pca.transform(X), Xc @ pca.components_.T) or np.allclose(np.abs(pca.transform(X)), np.abs(Xc @ pca.components_.T)))

print("\n--- does scaling matter? Iris, raw vs standardised ---")
iris = load_iris().data
raw = PCA().fit(iris)
std = PCA().fit(StandardScaler().fit_transform(iris))
print("raw (cm)       ratio:", raw.explained_variance_ratio_, "| PC1 loadings:", raw.components_[0])
print("standardised   ratio:", std.explained_variance_ratio_, "| PC1 loadings:", std.components_[0])
print("components needed for >= 95% (standardised):", int(np.searchsorted(np.cumsum(std.explained_variance_ratio_), 0.95) + 1),
      "| PCA(0.95) picks:", PCA(0.95).fit(StandardScaler().fit_transform(iris)).n_components_)

print("\n--- a unit change alone rewrites PC1 ---")
height_cm_weight_kg = np.column_stack([np.random.default_rng(1).normal(170, 10, 200), np.random.default_rng(2).normal(65, 12, 200)])
mm = height_cm_weight_kg.copy(); mm[:, 0] *= 10          # height in millimetres
print("cm: PC1 =", PCA(1).fit(height_cm_weight_kg).components_[0], "| mm: PC1 =", PCA(1).fit(mm).components_[0], "(height dominates just because its numbers got bigger)")

print("\n--- high variance is not the same as predictive ---")
rng = np.random.default_rng(0)
noise_big = rng.normal(0, 10, 300)                      # large variance, unrelated to y
signal = rng.normal(0, 1, 300)                          # small variance, determines y
y = (signal > 0).astype(int)
F = np.column_stack([noise_big, signal])
p = PCA(2).fit(F)
print("PC1 loadings:", p.components_[0], "-> PC1 is almost entirely the noisy feature")
print("correlation of PC1 score with y:", round(abs(np.corrcoef(p.transform(F)[:, 0], y)[0, 1]), 3), "| of PC2 score:", round(abs(np.corrcoef(p.transform(F)[:, 1], y)[0, 1]), 3))

print("\n--- limits: max components, outliers, inverse_transform ---")
print("components limit = min(n_samples, n_features):", PCA().fit(np.random.default_rng(0).normal(size=(4, 10))).n_components_)
base = np.random.default_rng(3).normal(size=(50, 2)) @ np.array([[3, 0], [0, 0.5]])
out = np.vstack([base, [[30, 30]]])
print("PC1 direction without outlier:", PCA(1).fit(base).components_[0], "| with one outlier:", PCA(1).fit(out).components_[0])

# ---- figure: data with PC axes, scree plot, projection
fig, ax = plt.subplots(1, 3, figsize=(11, 3.4))
ax[0].scatter(X[:, 0], X[:, 1], color="#2f6db5")
for k, color in zip(range(2), ["#d9534f", "#2e8b57"]):
    d = V[:, k] * np.sqrt(w[k])                 # half-length = standard deviation along the component
    ax[0].annotate("", xy=mu + d, xytext=mu - d, arrowprops=dict(arrowstyle="<->", color=color, lw=2), annotation_clip=False)
    ax[0].text(*(mu + d * 1.15), f"PC{k + 1}", color=color, ha="center", va="center", fontweight="bold")
ax[0].scatter(*mu, color="black", marker="x", zorder=4)
ax[0].set_xlim(0, 8); ax[0].set_ylim(0, 8); ax[0].set_aspect("equal")
ax[0].set_title("Data and principal axes"); ax[0].set_xlabel("x1"); ax[0].set_ylabel("x2")
ev = std.explained_variance_ratio_
ax[1].bar(range(1, 5), ev, color="#2f6db5"); ax[1].plot(range(1, 5), np.cumsum(ev), "o-", color="#d9534f")
ax[1].axhline(0.95, ls="--", color="grey"); ax[1].set_title("Scree plot (Iris, standardised)"); ax[1].set_xlabel("component"); ax[1].set_ylabel("variance ratio / cumulative")
ax[2].scatter(Z, np.zeros_like(Z), color="#2f6db5", zorder=3)
ax[2].scatter(Xc @ V[:, 1:2], np.full(n, -0.15), color="#5cb85c", zorder=3)
ax[2].set_yticks([0, -0.15]); ax[2].set_yticklabels(["PC1 scores", "PC2 scores"]); ax[2].set_title("Scores: PC1 has the spread"); ax[2].set_ylim(-0.4, 0.3)
fig.tight_layout(); fig.savefig("notes_pca.png", dpi=150)
print("\nsaved notes_pca.png")
