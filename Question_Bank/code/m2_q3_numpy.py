"""M2-Q3  NumPy arrays and broadcasting (Lab experiment 3, FAT top-10 question 8)."""
import numpy as np

rng = np.random.default_rng(seed=7)                 # seed -> repeatable output
a = rng.integers(0, 11, size=(3, 4))                # integers 0..10
print("a =\n", a, sep="")
print("shape", a.shape, "| mean", round(a.mean(), 3), "| std", round(a.std(), 3))

print("\nfirst two rows, last two columns:\n", a[:2, -2:], sep="")
r = a.reshape(4, 3)
print("\nreshape(4, 3):\n", r, sep="")
b = rng.integers(1, 5, size=(4, 3))
print("\nelement-wise product with another (4,3) array:\n", r * b, sep="")

print("\n--- broadcasting ---")
m = np.arange(12).reshape(3, 4)                     # (3, 4)
row = np.array([10, 20, 30, 40])                    # (4,)   -> treated as (1, 4)
col = np.array([[1], [2], [3]])                     # (3, 1)
print("(3,4) + (4,)  ->", (m + row).shape)
print("(3,4) + (3,1) ->", (m + col).shape)
print("(3,1) + (1,4) ->", (col + np.array([[1, 2, 3, 4]])).shape)
try:
    m + np.array([1, 2, 3])                         # (3,4) vs (3,) -> trailing dims 4 and 3 differ
except ValueError as err:
    print("(3,4) + (3,)  -> ValueError:", err)

x = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
print("\ncolumn-wise standardisation using broadcasting:\n",
      np.round((x - x.mean(axis=0)) / x.std(axis=0), 3), sep="")
