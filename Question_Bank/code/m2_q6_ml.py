"""M2-Q6  K-means clustering and PCA on Iris (Lab experiments 4, 11 and 12)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

iris = load_iris(as_frame=True)
X = iris.data
y = iris.target

# ---- Lab 4: feature engineering / EDA on a small random frame ---------------
rng = np.random.default_rng(3)
df = pd.DataFrame({"Feature1": rng.uniform(1, 100, 200), "Feature2": rng.normal(50, 15, 200),
                   "Target": rng.integers(0, 2, 200)})
df["log_F1"] = np.log(df["Feature1"])                                   # log feature
df["F2_bin"] = pd.cut(df["Feature2"], bins=3, labels=["low", "medium", "high"])
print("bins:", df["F2_bin"].value_counts().to_dict())
print("correlation matrix (rounded):")
print(df[["Feature1", "Feature2", "Target", "log_F1"]].corr().round(2))

# ---- Lab 11: K-means, k = 3, on the four measurements -----------------------
km = KMeans(n_clusters=3, n_init=10, random_state=42).fit(X)
print("\nKMeans cluster sizes :", np.bincount(km.labels_).tolist())
print("inertia (WCSS)       :", round(km.inertia_, 2))
print("cluster vs true species (rows = cluster):")
print(pd.crosstab(km.labels_, y.map(dict(enumerate(iris.target_names)))))

fig3d = px.scatter_3d(X.assign(cluster=km.labels_.astype(str)),
                      x="sepal length (cm)", y="sepal width (cm)", z="petal length (cm)",
                      color="cluster", title="K-means clusters (Iris)")
fig3d.write_html("kmeans_3d.html", include_plotlyjs="cdn")

# ---- Lab 12: PCA to two components ------------------------------------------
Xs = StandardScaler().fit_transform(X)                                  # scale first!
pca = PCA(n_components=2).fit(Xs)
Z = pca.transform(Xs)
print("\nPCA explained variance ratio:", pca.explained_variance_ratio_.round(3).tolist(),
      "| total", round(pca.explained_variance_ratio_.sum(), 3))
print("PC1 loadings:", dict(zip(X.columns, pca.components_[0].round(2))))

fig, ax = plt.subplots(1, 2, figsize=(9, 3.6))
ax[0].scatter(Z[:, 0], Z[:, 1], c=km.labels_, cmap="viridis", s=18)
ax[0].set_title("PCA projection coloured by K-means cluster")
ax[0].set_xlabel("PC1 (%.1f%%)" % (100 * pca.explained_variance_ratio_[0]))
ax[0].set_ylabel("PC2 (%.1f%%)" % (100 * pca.explained_variance_ratio_[1]))
ks = range(1, 8)
ax[1].plot(list(ks), [KMeans(k, n_init=10, random_state=42).fit(X).inertia_ for k in ks], marker="o")
ax[1].set_title("Elbow method: inertia vs k")
ax[1].set_xlabel("k")
ax[1].set_ylabel("inertia")
fig.tight_layout()
fig.savefig("kmeans_pca.png", dpi=150)
print("\nsaved kmeans_pca.png")
