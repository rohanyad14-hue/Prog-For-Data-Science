"""Sample answer M2-Q4: a house-price model with NumPy, pandas, SciPy and scikit-learn."""
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import LeaveOneOut, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

df = pd.DataFrame({"HouseSize": [1200, 1500, 1800, 2200, 2500], "Bedrooms": [2, 3, 3, 4, 4],
                   "Age": [10, 8, 5, 3, 2], "Price": [45, 60, 75, 95, 110]})

print("--- preprocessing checks ---")
print("missing values:", int(df.isna().sum().sum()), "| duplicate rows:", int(df.duplicated().sum()), "| types:", sorted(set(df.dtypes.astype(str))))
print("values with |z| > 2:", int((np.abs(stats.zscore(df)) > 2).sum()))
X = df[["HouseSize", "Bedrooms", "Age"]]          # independent variables (features)
y = df["Price"]                                    # dependent variable (target), in lakhs
print("X:", X.shape, "y:", y.shape)

print("\n--- feature analysis with NumPy and SciPy ---")
print(df.corr().round(3))
r, p = stats.pearsonr(df["HouseSize"], df["Price"])
print("Pearson r (size, price) =", round(r, 4), "| p-value =", round(p, 5))
slope, intercept = np.polyfit(df["HouseSize"], df["Price"], 1)
print("price ~ size: slope", round(slope, 4), "lakh per sq.ft, intercept", round(intercept, 2))
vif = np.diag(np.linalg.inv(np.corrcoef(X.values, rowvar=False)))
print("variance inflation factors (above 10 means strong collinearity):", dict(zip(X.columns, vif.round(1))))

print("\n--- two algorithms and a baseline, leave-one-out cross-validation (5 rows only) ---")
models = {"baseline (mean price)": DummyRegressor(),
          "linear regression": make_pipeline(StandardScaler(), LinearRegression()),
          "random forest": RandomForestRegressor(n_estimators=200, random_state=0)}
for name, model in models.items():
    pred = cross_val_predict(model, X, y, cv=LeaveOneOut())
    print(f"{name:<22} MAE {mean_absolute_error(y, pred):6.2f}  RMSE {mean_squared_error(y, pred) ** 0.5:6.2f}  R2 {r2_score(y, pred):7.3f}")

print("\n--- predictions after fitting on all five rows ---")
new = pd.DataFrame({"HouseSize": [2000, 3000], "Bedrooms": [3, 5], "Age": [6, 1]})
for name in ("linear regression", "random forest"):
    fitted = models[name].fit(X, y)
    print(f"{name:<18} 2000 sq.ft -> {fitted.predict(new)[0]:6.1f} lakh | 3000 sq.ft (outside the training range) -> {fitted.predict(new)[1]:6.1f} lakh")
