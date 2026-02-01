📊 FinSight AI — Personal Finance Intelligence

FinSight AI is a personal finance analytics application that converts raw transaction data into clear financial insights, visualizations, and actionable recommendations. The project focuses on data-driven analysis with explainable AI support, keeping all financial calculations transparent and reliable.

🚀 What This Project Does

- Cleans and validates raw financial CSV data
- Automatically categorizes income and expenses
- Provides year-wise financial summaries
- Visualizes income and spending patterns
- Calculates a financial health score
- Generates rule-based financial advice
- Uses AI (RAG) to explain insights in simple terms

🧠 System Design (High Level)

- Data Cleaning Module – Handles missing and invalid records
- Categorization Module – Classifies transactions into categories
- Insight Engine – Computes income, expenses, savings, and metrics
- Rule-Based Advisor – Produces deterministic financial guidance
- RAG Advisor – Explains financial concepts using LLM + vector search
- Streamlit App – Orchestrates the flow and displays the dashboard
- Financial logic is deterministic; AI is used only for explanations.

🛠️ Tech Stack

- Python, Pandas
- Streamlit (UI & dashboard)
- LangChain + OpenAI API
- FAISS / Chroma (Vector store for RAG)

📊 Key Insights Provided

- Income vs expense comparison (year-wise)
- Category-wise spending distribution
- Monthly income and expense trends
- Financial health scoring
- Personalized savings and investment guidance

▶️ How to Run
- pip install -r requirements.txt
- streamlit run app.py
- Upload a CSV file in the supported format to start analysis.

🎯 Use Cases

- Personal finance tracking
- Financial literacy tools
- Advisory dashboards
- Expense and savings analysis

👤 Author

Tejas Gurav  
Data Engineering & AI Enthusiast
