import os
from dotenv import load_dotenv
load_dotenv()

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

class RAGAdvisorAgent:
    def __init__(self):
        
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

        with open("rag/finance_knowledge.txt") as f:
            text = f.read()

        splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
        docs = splitter.create_documents([text])

        self.db = FAISS.from_documents(docs, OpenAIEmbeddings())

        self.qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.db.as_retriever()
        )

    def explain(self, question, summary):
        context = f"""
        Financial Dashboard Context:
        Year: {summary['year']}
        Total Income: ₹{summary['income_total']}
        Total Expense: ₹{summary['expense_total']}
        Savings: ₹{summary['savings']}
        Savings Rate: {summary['savings_rate']:.2%}
        Health Score: {summary['health_score']} ({summary['health_label']})

        Answer the question strictly based on this financial situation.
        """

        prompt = context + "\n\nUser Question: " + question
        return self.qa.run(prompt)
