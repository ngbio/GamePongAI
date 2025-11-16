import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
from joblib import dump

from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

warnings.filterwarnings("ignore", category=UserWarning)

# ======================================================
# Load dataset
# ======================================================
df = pd.read_csv("dataset1.csv", header=0)
X = df[['ball_y', 'ball_angle']]
y = df['paddle_y']

# ======================================================
# Thực nghiệm với các giá trị K
# ======================================================
K_values = [50, 100, 400] # thử với nhìu k để tìm hiệu năng và tốc độ
results = []

for K in K_values:
    print(f"\n🔹 Training model with K={K} trees ...")
    model = Pipeline([
        ('rf', RandomForestRegressor(n_estimators=K, random_state=42))
    ])

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Metrics
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    results.append([
        f"Random Forest (K={K})",
        round(mse, 2),
        round(rmse, 2),
        round(mae, 2),
        round(r2, 2)
    ])

# ======================================================
# Vẽ bảng 4.2
# ======================================================
columns = ["Mô hình", "MSE", "RMSE", "MAE", "R²"]

fig, ax = plt.subplots(figsize=(9, 2))
ax.axis('tight')
ax.axis('off')
table = ax.table(cellText=results, colLabels=columns,
                 cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1.2, 1.2)
plt.savefig("results_table_dataset.png", bbox_inches="tight")
plt.close()

# ======================================================
# Ball & Bat position theo thời gian
# ======================================================
plt.figure(figsize=(10, 5))
plt.plot(df.index, df["ball_y"], label="ball position y")
plt.plot(df.index, df["paddle_y"], label="bat position y")
plt.xlabel("t")
plt.ylabel("position")
plt.legend()
plt.title("Ball and bat position against time")
plt.savefig("plot-time.png")
plt.close()

# ======================================================
# Train final model (chọn K=400) các thông số dự đoạn số liệu lấy từ final model k=400
# ======================================================
final_model = Pipeline([
    ('rf', RandomForestRegressor(n_estimators=400, random_state=42))
])
final_model.fit(X, y)
y_pred_all = final_model.predict(X)
#dump(final_model, 'rf_model.joblib')

# So sánh dự đoán với dữ liệu thật
plt.figure(figsize=(10, 5))
plt.plot(df.index, df["paddle_y"], label="actual bat position y", c="red")
plt.plot(df.index, y_pred_all, label="estimated bat position y", c="blue")
plt.xlabel("t")
plt.ylabel("bat position y")
plt.legend()
plt.title("Estimated vs Actual bat position")
plt.savefig("plot-estimated-vs-actual.png")
plt.close()


# ======================================================
# Train final model trên toàn bộ dataset (K=800)
# ======================================================
final_model = Pipeline([('rf', RandomForestRegressor(n_estimators=800, random_state=42))])
final_model.fit(X, y)
y_pred_all = final_model.predict(X)
dump(final_model, 'spline_model.joblib')