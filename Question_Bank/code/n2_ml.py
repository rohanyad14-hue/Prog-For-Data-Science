"""Notes M2: K-means by hand, evaluation metrics, data leakage, overfitting, pipelines (scikit-learn)."""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import load_breast_cancer, load_iris, make_blobs
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score, silhouette_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

np.set_printoptions(precision=3, suppress=True)

print("=== K-MEANS by hand: 6 points, k = 2, one full iteration ===")
P = np.array([[1, 1], [1.5, 2], [3, 4], [5, 7], [3.5, 5], [4.5, 5]])
cent = np.array([[1.0, 1.0], [5.0, 7.0]])
print("start centroids:", cent.tolist())
d = np.linalg.norm(P[:, None, :] - cent[None, :, :], axis=2)
print("distances to c1, c2:\n", d)
lab = d.argmin(axis=1)
print("assignment:", lab.tolist())
new = np.array([P[lab == k].mean(axis=0) for k in range(2)])
print("new centroids (means of members):", new.tolist())
print("point 3 = (3, 4) is equally far from both centroids (3.606 each); argmin keeps the first, so it joins cluster 0")
inertia = sum(((P[lab == k] - new[k]) ** 2).sum() for k in range(2))
print("inertia (sum of squared distances to the NEW centroids):", round(float(inertia), 3))
d2 = np.linalg.norm(P[:, None, :] - new[None, :, :], axis=2)
lab2 = d2.argmin(axis=1)
print("second assignment:", lab2.tolist(), "-> unchanged, so converged:", bool((lab2 == lab).all()))
km = KMeans(2, init=cent, n_init=1).fit(P)
print("sklearn with the same start: labels", km.labels_.tolist(), "centroids", km.cluster_centers_.tolist(), "inertia", round(km.inertia_, 3))

print("\n=== K-means choices: k-means++, n_init, elbow, silhouette, scaling ===")
X, _ = make_blobs(300, centers=4, cluster_std=0.8, random_state=7)
for k in range(2, 7):
    m = KMeans(k, n_init=10, random_state=0).fit(X)
    print(f"k={k}: inertia={m.inertia_:8.1f}  silhouette={silhouette_score(X, m.labels_):.3f}")
single = [round(KMeans(4, init="random", n_init=1, random_state=s).fit(X).inertia_, 1) for s in range(6)]
print("one random start per seed gives different inertias (local minima):", single)
print("n_init=10 keeps the best one:", round(KMeans(4, init="random", n_init=10, random_state=0).fit(X).inertia_, 1))
Xs = np.column_stack([X[:, 0] * 1000, X[:, 1]])
lab_raw = KMeans(4, n_init=10, random_state=0).fit_predict(Xs)
lab_std = KMeans(4, n_init=10, random_state=0).fit_predict(StandardScaler().fit_transform(Xs))
lab_ref = KMeans(4, n_init=10, random_state=0).fit_predict(X)
from sklearn.metrics import adjusted_rand_score as ari
print("agreement (ARI) with the unit-scaled clustering - raw x1000 feature:", round(ari(lab_ref, lab_raw), 3), "| after standardising:", round(ari(lab_ref, lab_std), 3))

print("\n=== CLASSIFICATION METRICS by hand ===")
y_true = np.array([1, 1, 1, 1, 0, 0, 0, 0, 0, 0])
y_pred = np.array([1, 1, 0, 0, 1, 0, 0, 0, 0, 0])
TP = int(((y_true == 1) & (y_pred == 1)).sum()); FN = int(((y_true == 1) & (y_pred == 0)).sum())
FP = int(((y_true == 0) & (y_pred == 1)).sum()); TN = int(((y_true == 0) & (y_pred == 0)).sum())
prec, rec = TP / (TP + FP), TP / (TP + FN)
print(f"TP={TP} FN={FN} FP={FP} TN={TN}")
print(f"accuracy = (TP+TN)/all = {(TP + TN) / 10:.2f} | precision = TP/(TP+FP) = {prec:.3f} | recall = TP/(TP+FN) = {rec:.3f} | F1 = 2PR/(P+R) = {2 * prec * rec / (prec + rec):.3f}")
print("sklearn agrees:", round(accuracy_score(y_true, y_pred), 2), round(precision_score(y_true, y_pred), 3), round(recall_score(y_true, y_pred), 3), round(f1_score(y_true, y_pred), 3))
print("confusion_matrix rows=true, cols=predicted:\n", confusion_matrix(y_true, y_pred))
print("accuracy paradox: predicting 'negative' for everyone on a 95/5 dataset gives accuracy", accuracy_score([0] * 95 + [1] * 5, [0] * 100), "and recall", recall_score([0] * 95 + [1] * 5, [0] * 100))

print("\n=== DATA LEAKAGE: choosing features on ALL the data, then cross-validating ===")
from sklearn.feature_selection import SelectKBest, f_classif
rng = np.random.default_rng(0)
Xr, yr = rng.normal(size=(100, 2000)), rng.integers(0, 2, 100)      # pure noise: no real signal at all
Xsel = SelectKBest(f_classif, k=20).fit_transform(Xr, yr)            # WRONG: the selector saw every label
leaky_acc = cross_val_score(LogisticRegression(max_iter=1000), Xsel, yr, cv=5).mean()
safe = Pipeline([("select", SelectKBest(f_classif, k=20)), ("clf", LogisticRegression(max_iter=1000))])
safe_acc = cross_val_score(safe, Xr, yr, cv=5).mean()
print(f"noise data, selector fitted outside CV : accuracy {leaky_acc:.2f}   (looks like skill, but there is none)")
print(f"same data, selector inside a Pipeline  : accuracy {safe_acc:.2f}   (honest: about a coin flip)")
Xc, yc = load_breast_cancer(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(Xc, yc, test_size=0.3, random_state=0, stratify=yc)
pipe = Pipeline([("scale", StandardScaler()), ("clf", LogisticRegression(max_iter=1000))]).fit(Xtr, ytr)
print("Pipeline test accuracy:", round(pipe.score(Xte, yte), 3), "| 5-fold CV (scaler refitted inside each fold):", cross_val_score(pipe, Xc, yc, cv=5).round(3), "mean", round(cross_val_score(pipe, Xc, yc, cv=5).mean(), 3))
print("stratify keeps class ratio: train positives", round(ytr.mean(), 3), "| test positives", round(yte.mean(), 3), "| overall", round(yc.mean(), 3))

print("\n=== OVERFITTING: training vs test accuracy ===")
Xn, yn = make_blobs(400, centers=2, cluster_std=4.5, random_state=3)
Xa, Xb, ya, yb = train_test_split(Xn, yn, test_size=0.4, random_state=1)
for depth in (1, 3, None):
    t = DecisionTreeClassifier(max_depth=depth, random_state=0).fit(Xa, ya)
    print(f"max_depth={str(depth):<5} train acc={t.score(Xa, ya):.2f}  test acc={t.score(Xb, yb):.2f}  leaves={t.get_n_leaves()}")
print("a gap between train and test accuracy is the symptom; limit depth, add data, or regularise")

print("\n=== PCA inside a pipeline (fit on training data only) ===")
Xi, yi = load_iris(return_X_y=True)
from sklearn.decomposition import PCA
p = Pipeline([("scale", StandardScaler()), ("pca", PCA(2)), ("clf", LogisticRegression(max_iter=500))])
print("5-fold CV accuracy with 2 PCs:", cross_val_score(p, Xi, yi, cv=5).round(3), "| with all 4 features:",
      cross_val_score(Pipeline([("scale", StandardScaler()), ("clf", LogisticRegression(max_iter=500))]), Xi, yi, cv=5).round(3))
