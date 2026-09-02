import os
import streamlit as st
import pandas as pd
from groq import Groq

from utils.finance import (
    calculate_total_expense,
    calculate_balance
)

# Page configuration
st.set_page_config(
    page_title="FinanceIQ",
    page_icon="💰",
    layout="wide"
)

# Groq API
api_key = os.getenv("GROQ_API_KEY")

if not api_key and "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=api_key) if api_key else None


def generate_ai_advice(income, total_expense, data):
    if client is None:
        return "Groq API key is not configured."

    prompt = f"""
You are FinanceIQ, a personal finance educational assistant.

Income: ₹{income:.2f}
Total expenses: ₹{total_expense:.2f}

Expense data:
{data.to_string(index=False)}

Give a simple and easy-to-understand financial summary.
Identify major spending areas and provide 3 practical budgeting suggestions.

Do not provide investment, loan, tax, or trading recommendations.
Keep the answer educational and concise.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful personal finance education assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4,
        max_tokens=500
    )

    return response.choices[0].message.content


# Header
st.title("💰 FinanceIQ")
st.subheader("FinanceIQ — Personal Finance Assistant")

st.write(
    "Gen AI powered personal finance assistant for "
    "expense analysis and budgeting guidance."
)

st.success("100% Free & Open Source")

# Feature cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📊 Expense Analytics")
    st.write("Understand your income and expenses clearly.")

with col2:
    st.markdown("### 🤖 AI Financial Insights")
    st.write("Get intelligent insights using an LLM.")

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
    1,
    12,
    6
)

# Sample Data
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

        st.session_state["finance_data"] = pd.DataFrame(data)

# Upload CSV
else:

    uploaded_file = st.sidebar.file_uploader(
        "Upload your finance CSV",
        type=["csv"]
    )

    if uploaded_file:
        st.session_state["finance_data"] = pd.read_csv(
            uploaded_file
        )


# Dashboard
st.header("🏠 Dashboard")

if "finance_data" in st.session_state:

    df = st.session_state["finance_data"]

    st.subheader("📋 Expense Data")

    st.dataframe(
        df,
        use_container_width=True
    )

    if "Amount" in df.columns:

        total_expense = calculate_total_expense(
            df["Amount"].tolist()
        )

        st.metric(
            "💸 Total Expense",
            f"₹{total_expense:,.2f}"
        )

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

        st.subheader("🤖 AI Financial Insights")

        if st.button("Generate AI Financial Insights"):

            with st.spinner("FinanceIQ AI is analysing your data..."):

                advice = generate_ai_advice(
                    income,
                    total_expense,
                    df
                )

            st.info(advice)

        st.caption(
            "FinanceIQ provides general educational budgeting guidance."
        )

else:

    st.info(
        "👈 Select a data source and generate sample data "
        "or upload your CSV to start."
    )