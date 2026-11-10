"""Notes M2: Matplotlib object-oriented API, Seaborn figure, and what each library returns."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from sklearn.datasets import load_iris
iris = load_iris(as_frame=True).frame.rename(columns=lambda c: c.replace(" (cm)", "").replace(" ", "_"))
iris["species"] = iris["target"].map({0: "setosa", 1: "versicolor", 2: "virginica"})

fig, axes = plt.subplots(1, 3, figsize=(11, 3.3))
ax = axes[0]
for sp, g in iris.groupby("species"):
    ax.scatter(g["petal_length"], g["petal_width"], s=14, label=sp)
ax.set_xlabel("petal length (cm)"); ax.set_ylabel("petal width (cm)"); ax.set_title("Matplotlib: fig, ax"); ax.legend(fontsize=7)
sns.boxplot(data=iris, x="species", y="sepal_length", ax=axes[1], hue="species", legend=False)
axes[1].set_title("Seaborn boxplot (axes-level)")
sns.heatmap(iris.drop(columns=["target", "species"]).corr(), annot=True, fmt=".2f", cmap="Blues", ax=axes[2], cbar=False, annot_kws={"size": 7})
axes[2].set_title("Seaborn heatmap of correlations"); axes[2].tick_params(labelsize=7)
fig.tight_layout()
fig.savefig("notes_viz.png", dpi=140)
print("pyplot state-machine call plt.plot(...) draws on the 'current axes'; the object-oriented form ax.plot(...) names the axes explicitly.")
print("plt.subplots returns:", type(fig).__name__, "and", type(axes).__name__, "of shape", axes.shape)
print("Seaborn axes-level functions (boxplot, heatmap, scatterplot) accept ax=...; figure-level ones (pairplot, relplot, catplot) create their own figure.")
g = sns.pairplot(iris.drop(columns="target"), hue="species")
print("pairplot returns:", type(g).__name__, "(a figure-level object)")
print("saved notes_viz.png")
