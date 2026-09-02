import streamlit as st
import pandas as pd
from utils.finance import calculate_total_expense, calculate_balance, generate_financial_advice

# Page configuration
st.set_page_config(
    page_title="FinanceIQ",
    page_icon="💰",
    layout="wide"
)

# Title
st.title("💰 FinanceIQ")
st.subheader("FinanceIQ — Personal Finance Assistant")

st.write(
    "AI-powered personal finance assistant for expense analysis "
    "and budgeting guidance."
)

st.success("100% Free & Open Source")

# Feature cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📊 Expense Analytics")
    st.write("Understand your income and expenses clearly.")

with col2:
    st.markdown("### 🤖 AI Financial Insights")
    st.write("Get intelligent insights from your financial data.")

with col3:
    st.markdown("### 🧠 AI Budget Advisor")
    st.write("Get AI-powered budgeting suggestions.")

st.divider()

# Sidebar
st.sidebar.header("⚙️ FinanceIQ")

data_source = st.sidebar.radio(
    "Data Source",
    ["Sample Data", "Upload CSV"]
)

months = st.sidebar.slider(
    "Months of history",
    min_value=1,
    max_value=12,
    value=6
)

# Sample data
if data_source == "Sample Data":

    if st.sidebar.button("Generate Sample Data"):

        data = {
            "Category": [
                "Food",
                "Transport",
                "Shopping",
                "Entertainment",
                "Bills",
                "Education"
            ],
            "Amount": [
                4500,
                2500,
                3000,
                1500,
                3500,
                2000
            ]
        }

        df = pd.DataFrame(data)

        st.session_state["finance_data"] = df

# Upload CSV
else:

    uploaded_file = st.sidebar.file_uploader(
        "Upload your finance CSV",
        type=["csv"]
    )

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.session_state["finance_data"] = df


# Dashboard
st.header("🏠 Dashboard")

if "finance_data" in st.session_state:

    df = st.session_state["finance_data"]

    st.subheader("📋 Expense Data")

    st.dataframe(
        df,
        use_container_width=True
    )

    # Expense calculation
    if "Amount" in df.columns:

        total_expense = calculate_total_expense(
            df["Amount"].tolist()
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "💸 Total Expense",
                f"₹{total_expense:,.2f}"
            )

        with col2:
            income = st.number_input(
                "💰 Monthly Income",
                min_value=0.0,
                value=30000.0,
                step=1000.0
            )

            balance = calculate_balance(
                income,
                total_expense
            )

            st.metric(
                "💵 Remaining Balance",
                f"₹{balance:,.2f}"
            )

        st.divider()

        # AI Budget Advisor
        st.subheader("🧠 AI Budget Advisor")

        if st.button("Generate AI Financial Advice"):

            advice = generate_financial_advice(
                income,
                total_expense
            )

            st.info(advice)

        st.caption(
            "FinanceIQ provides general educational budgeting guidance "
            "and is not a substitute for professional financial advice."
        )

else:

    st.info(
        "👈 Select a data source and generate sample data "
        "or upload your CSV to start."
    )