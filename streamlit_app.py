import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Expense Tracker", layout="wide")

st.title("💰 Expense Tracker Dashboard")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/expenses.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    return df

df = load_data()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

category_filter = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

payment_filter = st.sidebar.multiselect(
    "Select Payment Method",
    options=df["Payment Method"].unique(),
    default=df["Payment Method"].unique()
)

filtered_df = df[
    (df["Category"].isin(category_filter)) &
    (df["Payment Method"].isin(payment_filter))
]

# -----------------------------
# METRICS
# -----------------------------
total_spent = filtered_df["Amount"].sum()
avg_spent = filtered_df["Amount"].mean()

col1, col2 = st.columns(2)

col1.metric("💸 Total Spending", f"₹ {total_spent}")
col2.metric("📊 Average Spending", f"₹ {round(avg_spent, 2)}")

# -----------------------------
# CATEGORY ANALYSIS (BAR CHART)
# -----------------------------
st.subheader("Category-wise Spending")

category_data = filtered_df.groupby("Category")["Amount"].sum()

fig1, ax1 = plt.subplots()
category_data.plot(kind='bar', ax=ax1)
ax1.set_ylabel("Amount")
ax1.set_xlabel("Category")
st.pyplot(fig1)

# -----------------------------
# MONTHLY TREND (LINE CHART)
# -----------------------------
st.subheader("Monthly Spending Trend")

monthly_data = filtered_df.groupby("Month")["Amount"].sum()

fig2, ax2 = plt.subplots()
monthly_data.plot(ax=ax2)
ax2.set_ylabel("Amount")
ax2.set_xlabel("Month")
st.pyplot(fig2)

# -----------------------------
# PIE CHART
# -----------------------------
st.subheader("Expense Distribution")

fig3, ax3 = plt.subplots()
category_data.plot(kind='pie', autopct='%1.1f%%', ax=ax3)
st.pyplot(fig3)

# -----------------------------
# INSIGHTS
# -----------------------------
st.subheader("Key Insights")

if not category_data.empty:
    top_category = category_data.idxmax()
    st.write(f"🔹 Highest spending category: **{top_category}**")
    st.write(f"🔹 Total transactions: **{len(filtered_df)}**")
else:
    st.write("No data available for selected filters.")
    # -----------------------------
# SMART INSIGHTS
# -----------------------------
st.subheader("Smart Insights")

if not category_data.empty:
    highest = category_data.idxmax()
    lowest = category_data.idxmin()

    st.write(f"🔴 Highest spending category: **{highest}**")
    st.write(f"🟢 Lowest spending category: **{lowest}**")

    if highest == "Shopping":
        st.write("💡 Tip: Try reducing shopping expenses to save more.")
    elif highest == "Food":
        st.write("💡 Tip: Consider budgeting for food and dining.")
    elif highest == "Travel":
        st.write("💡 Tip: Plan trips to optimize travel expenses.")

# -----------------------------
# RAW DATA TABLE
# -----------------------------
st.subheader("Raw Data")
st.dataframe(filtered_df)
# -----------------------------
# BUDGET ALERT SYSTEM
# -----------------------------
st.subheader("Budget Monitoring")

budget = st.number_input("Set Monthly Budget (₹)", value=50000)

current_spending = filtered_df["Amount"].sum()

if current_spending > budget:
    st.error(f"⚠️ Budget Exceeded! You spent ₹{current_spending}")
elif current_spending > 0.8 * budget:
    st.warning(f"⚠️ You are close to your budget! Spending: ₹{current_spending}")
else:
    st.success(f"✅ You are within budget. Spending: ₹{current_spending}")
    # -----------------------------
# DOWNLOAD DATA
# -----------------------------
st.subheader("Download Data")

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name='filtered_expenses.csv',
    mime='text/csv',
)