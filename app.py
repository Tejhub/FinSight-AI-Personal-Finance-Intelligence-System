import streamlit as st
import matplotlib.pyplot as plt
from agents.data_cleaner import DataCleaningAgent
from agents.categorizer import CategorizationAgent
from agents.insight_agent import InsightAgent
from agents.finance_advisor_agent import FinanceAdvisorAgent
from agents.rag_advisor_agent import RAGAdvisorAgent

st.set_page_config(layout="wide")
st.title("💰 FinSight AI — Your Personal Financial Intelligence")

@st.cache_resource
def load_rag():
    return RAGAdvisorAgent()

file = st.file_uploader("Upload Finance CSV", type=["csv"])

if file:
    cleaner = DataCleaningAgent()
    categorizer = CategorizationAgent()
    insight = InsightAgent()
    advisor = FinanceAdvisorAgent()

    df = categorizer.run(cleaner.run(file))

    year = st.selectbox("Select Year", sorted(df["date"].dt.year.unique()))
    summary = insight.run(df, year)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Income", f"₹{summary['income_total']:,.0f}")

    with col2:
        st.metric("Total Expense", f"₹{summary['expense_total']:,.0f}")

    with col3:
        st.metric("Savings", f"₹{summary['savings']:,.0f}")


    st.subheader("🩺 Financial Health")
    st.metric("Health Score", f"{summary['health_score']} / 100", summary["health_label"])
    st.progress(summary["health_score"] / 100)

    # Income row
    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots()
        ax.pie(summary["income_by_category"], labels=summary["income_by_category"].index, autopct="%1.1f%%")
        ax.set_title("Income Distribution")
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots()
        ax.bar(summary["income_by_month"].index, summary["income_by_month"].values)
        ax.set_title("Monthly Income")
        ax.tick_params(axis="x", rotation=45)
        st.pyplot(fig)

    # Expense row
    col3, col4 = st.columns(2)
    with col3:
        fig, ax = plt.subplots()
        ax.pie(summary["expense_by_category"], labels=summary["expense_by_category"].index, autopct="%1.1f%%")
        ax.set_title("Expense Distribution")
        st.pyplot(fig)

    with col4:
        fig, ax = plt.subplots()
        ax.bar(summary["expense_by_month"].index, summary["expense_by_month"].values)
        ax.set_title("Monthly Expenses")
        ax.tick_params(axis="x", rotation=45)
        st.pyplot(fig)

    st.subheader("🧠 Financial Advice")
    for tip in advisor.run(summary):
        st.write("•", tip)

    st.subheader("🤖 Ask AI Your Queries")
    rag = load_rag()
    for q in [
        "Is my financial situation healthy?",
        "What should I improve financially?",
        "Is SIP suitable for me this year?"
    ]:
        with st.expander(q):
            st.write(rag.explain(q, summary))

    st.subheader("💬 Ask Your Own Financial Question")

    user_question = st.text_input(
        "Ask anything about your finances for this year",
        placeholder="e.g. Can I reduce my expenses further?"
    )

    if user_question:
        with st.spinner("Analyzing your financial data..."):
            answer = rag.explain(user_question, summary)
            st.success(answer)
else:
    st.info("Upload a CSV file to begin.")
