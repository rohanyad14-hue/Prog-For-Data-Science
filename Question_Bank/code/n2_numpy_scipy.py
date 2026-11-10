"""Notes M2: NumPy views, broadcasting, linear algebra, dtype traps, and SciPy."""
import numpy as np
from scipy import integrate, linalg, optimize, stats

a = np.arange(12).reshape(3, 4)
print("--- shape, axis ---")
print(a, "\nsum axis=0 (down rows):", a.sum(axis=0), "| axis=1 (across columns):", a.sum(axis=1), "| keepdims:", a.sum(axis=1, keepdims=True).shape)
print("argmax:", a.argmax(), "| argmax(axis=0):", a.argmax(axis=0), "| reshape(-1):", a.reshape(-1)[:5], "...", "| T shape:", a.T.shape)

print("\n--- view vs copy ---")
v = a[0, :2]                 # basic slice -> view
v[0] = 99
print("slice is a view, original changed:", a[0, 0], "| shares memory with a:", np.shares_memory(v, a))
c = a[[0, 1]]                # fancy indexing -> copy
c[0, 0] = -1
print("fancy index is a copy, original unchanged:", a[0, 0], "| shares memory:", np.shares_memory(c, a))
m = a[a > 5]
print("boolean mask returns a copy:", m.base is None, "| values:", m[:4])
b = a.copy()
b[:] = 0
print("explicit copy is independent:", a[1, 1])

print("\n--- operators: * vs @ vs dot, broadcasting ---")
x = np.array([[1, 2], [3, 4]]); y = np.array([[10, 20], [30, 40]])
print("x * y (element-wise):", (x * y).tolist(), "| x @ y (matrix product):", (x @ y).tolist(), "| np.dot same:", np.dot(x, y).tolist())
print("(2,2) + (2,) :", (x + np.array([100, 200])).tolist(), "| (2,2) + (2,1):", (x + np.array([[100], [200]])).tolist())
print("== is element-wise:", (x == y).tolist(), "| np.array_equal:", np.array_equal(x, x.copy()), "| allclose(0.1+0.2, 0.3):", np.allclose(0.1 + 0.2, 0.3), "| exact:", 0.1 + 0.2 == 0.3)

print("\n--- dtype traps ---")
u = np.array([250], dtype=np.uint8)
print("uint8 250 + 10 wraps around ->", (u + 10)[0], "| int array / int true-divides ->", (np.array([7]) / 2)[0], "| // floors ->", (np.array([-7]) // 2)[0])
print("np.array([1, 2.5, 'a']) dtype:", np.array([1, 2.5, "a"]).dtype, "| np.array([1, 2.5]) dtype:", np.array([1, 2.5]).dtype)
print("NaN: np.nan == np.nan", np.nan == np.nan, "| np.isnan:", np.isnan(np.nan), "| mean with nan:", np.mean([1, np.nan]), "| nanmean:", np.nanmean([1, np.nan]))

print("\n--- where, sort, unique, random ---")
z = np.array([5, 3, 8, 3])
print("where:", np.where(z > 4, "big", "small").tolist(), "| argsort:", z.argsort().tolist(), "| unique+counts:", [r.tolist() for r in np.unique(z, return_counts=True)])
r1 = np.random.default_rng(0).integers(0, 10, 3); r2 = np.random.default_rng(0).integers(0, 10, 3)
print("same seed -> same numbers:", r1.tolist(), r2.tolist(), "| linspace:", np.linspace(0, 1, 5).tolist(), "| arange step:", np.arange(0, 1, 0.25).tolist())

print("\n--- linear algebra (basis for PCA) ---")
A = np.array([[2.0, 1.0], [1.0, 3.0]])
w, V = np.linalg.eigh(A)
print("eigenvalues:", w.round(4), "| eigenvectors (columns):\n", V.round(4), sep="")
print("A v = lambda v holds:", np.allclose(A @ V[:, 1], w[1] * V[:, 1]), "| det:", round(np.linalg.det(A), 3), "| inv @ A = I:", np.allclose(np.linalg.inv(A) @ A, np.eye(2)))
print("solve Ax=b:", np.linalg.solve(A, np.array([3.0, 5.0])).round(3), "| rank:", np.linalg.matrix_rank(A))
U, S, Vt = np.linalg.svd(A)
print("SVD singular values:", S.round(4), "(for a symmetric positive matrix these equal the eigenvalues)")

print("\n--- SciPy ---")
g1 = np.array([85, 90, 78, 92, 88, 76]); g2 = np.array([70, 65, 80, 72, 68, 74])
t, p = stats.ttest_ind(g1, g2)
print(f"ttest_ind: t={t:.2f}, p={p:.4f} -> {'significant' if p < 0.05 else 'not significant'} at 5%")
print("pearson r:", round(stats.pearsonr([1, 2, 3, 4, 5], [2, 4, 5, 4, 5])[0], 3), "| norm.cdf(1.96):", round(stats.norm.cdf(1.96), 4))
res = optimize.minimize(lambda p: (p[0] - 3) ** 2 + (p[1] + 1) ** 2, x0=[0, 0])
print("optimize.minimize minimum at:", res.x.round(3), "| integrate.quad(x^2, 0, 3):", round(integrate.quad(lambda x: x ** 2, 0, 3)[0], 4), "| linalg.solve:", linalg.solve(A, [3, 5]).round(3))
