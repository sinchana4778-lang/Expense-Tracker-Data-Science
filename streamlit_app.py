import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Expense Tracker", layout="wide")

# -----------------------------
# TITLE (Styled)
# -----------------------------
st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>💰 Expense Tracker Dashboard</h1>",
    unsafe_allow_html=True
)

st.markdown("Analyze your spending patterns with interactive insights")

# -----------------------------
# LOAD DATA WITH SPINNER
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/expenses.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    return df

with st.spinner("Loading data..."):
    df = load_data()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔍 Filters")

category_filter = st.sidebar.multiselect(
    "Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

payment_filter = st.sidebar.multiselect(
    "Payment Method",
    options=df["Payment Method"].unique(),
    default=df["Payment Method"].unique()
)

filtered_df = df[
    (df["Category"].isin(category_filter)) &
    (df["Payment Method"].isin(payment_filter))
]

# -----------------------------
# SIDEBAR SUMMARY
# -----------------------------
st.sidebar.markdown("### 📊 Quick Summary")
st.sidebar.write(f"Total Records: {len(filtered_df)}")
st.sidebar.write(f"Total Spend: ₹ {filtered_df['Amount'].sum()}")

# -----------------------------
# METRICS
# -----------------------------
total_spent = filtered_df["Amount"].sum()
avg_spent = filtered_df["Amount"].mean()
transactions = len(filtered_df)

col1, col2, col3 = st.columns(3)

col1.metric("💸 Total Spending", f"₹ {total_spent}")
col2.metric("📊 Avg Transaction", f"₹ {round(avg_spent, 2)}")
col3.metric("🧾 Transactions", transactions)

# -----------------------------
# BUDGET ALERT
# -----------------------------
st.subheader("💡 Budget Monitoring")

budget = st.number_input("Set Monthly Budget (₹)", value=50000)

if total_spent > budget:
    st.error(f"⚠️ Budget Exceeded! ₹ {total_spent}")
elif total_spent > 0.8 * budget:
    st.warning(f"⚠️ Near Budget Limit! ₹ {total_spent}")
else:
    st.success(f"✅ Within Budget. ₹ {total_spent}")

# -----------------------------
# CHARTS
# -----------------------------
st.subheader("📊 Spending Analysis")

col1, col2 = st.columns(2)

category_data = filtered_df.groupby("Category")["Amount"].sum().reset_index()

# Bar Chart
fig_bar = px.bar(
    category_data,
    x="Category",
    y="Amount",
    title="Category-wise Spending",
    text_auto=True
)

col1.plotly_chart(fig_bar, use_container_width=True)

# Pie Chart
fig_pie = px.pie(
    category_data,
    names="Category",
    values="Amount",
    title="Expense Distribution"
)

col2.plotly_chart(fig_pie, use_container_width=True)

# -----------------------------
# MONTHLY TREND (FIXED SORTING)
# -----------------------------
st.subheader("📈 Monthly Trend")

monthly_data = filtered_df.groupby("Month")["Amount"].sum().reset_index()
monthly_data = monthly_data.sort_values("Month")

fig_line = px.line(
    monthly_data,
    x="Month",
    y="Amount",
    markers=True,
    title="Monthly Spending Trend"
)

st.plotly_chart(fig_line, use_container_width=True)

# -----------------------------
# SMART INSIGHTS
# -----------------------------
st.subheader("🧠 Smart Insights")

if not category_data.empty:
    highest = category_data.loc[category_data["Amount"].idxmax()]["Category"]
    lowest = category_data.loc[category_data["Amount"].idxmin()]["Category"]

    st.write(f"🔴 Highest Spending: **{highest}**")
    st.write(f"🟢 Lowest Spending: **{lowest}**")

# -----------------------------
# TOP 3 EXPENSES
# -----------------------------
st.subheader("🏆 Top 3 Expenses")

top3 = filtered_df.sort_values(by="Amount", ascending=False).head(3)
st.table(top3)

# -----------------------------
# DOWNLOAD DATA
# -----------------------------
st.subheader("⬇️ Download Data")

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name='filtered_expenses.csv',
    mime='text/csv',
)

# -----------------------------
# RAW DATA
# -----------------------------
st.subheader("📄 Raw Data")
st.dataframe(filtered_df)