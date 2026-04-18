import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# 1. CREATE SYNTHETIC DATA
# -----------------------------
np.random.seed(42)

dates = pd.date_range(start="2024-01-01", periods=200)

categories = ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Rent"]
payment_methods = ["Cash", "Card", "UPI"]

data = {
    "Date": np.random.choice(dates, 200),
    "Category": np.random.choice(categories, 200),
    "Amount": np.random.randint(100, 5000, 200),
    "Payment Method": np.random.choice(payment_methods, 200)
}

df = pd.DataFrame(data)

# Save dataset
df.to_csv("data/expenses.csv", index=False)

# -----------------------------
# 2. DATA CLEANING
# -----------------------------
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.to_period("M")

# -----------------------------
# 3. ANALYSIS
# -----------------------------
category_spending = df.groupby("Category")["Amount"].sum()

monthly_spending = df.groupby("Month")["Amount"].sum()

# -----------------------------
# 4. VISUALIZATION
# -----------------------------

# Category-wise spending
plt.figure(figsize=(8,5))
category_spending.plot(kind='bar')
plt.title("Category-wise Spending")
plt.savefig("outputs/category_spending.png")
plt.close()

# Monthly trend
plt.figure(figsize=(10,5))
monthly_spending.plot()
plt.title("Monthly Spending Trend")
plt.savefig("outputs/monthly_trend.png")
plt.close()

# Pie chart
plt.figure(figsize=(6,6))
category_spending.plot(kind='pie', autopct='%1.1f%%')
plt.title("Expense Distribution")
plt.savefig("outputs/pie_chart.png")
plt.close()

# -----------------------------
# 5. INSIGHTS
# -----------------------------
print("Top Spending Category:", category_spending.idxmax())
print("Total Spending:", df["Amount"].sum())