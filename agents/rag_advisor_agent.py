import os
from dotenv import load_dotenv
load_dotenv()

from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

from groq import Groq


class RAGAdvisorAgent:
    def __init__(self):

        # ---- Groq client ----
        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        # ---- Load knowledge base ----
        with open("rag/finance_knowledge.txt", encoding="utf-8") as f:
            text = f.read()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=50
        )
        docs = splitter.create_documents([text])
        self.texts = [d.page_content for d in docs]

        # ---- Local embeddings ----
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        embeddings = self.embedder.encode(self.texts)

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(embeddings))

    def _retrieve(self, query, k=3):
        q_emb = self.embedder.encode([query])
        _, idx = self.index.search(q_emb, k)
        return "\n".join([self.texts[i] for i in idx[0]])

    def _ask_groq(self, prompt):
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # stable & recommended
            messages=[
                {
                    "role": "system",
                    "content": "You are a financial assistant. Answer only from the given context."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content

    def explain(self, question, summary):

        context = f"""
                    Financial Dashboard Context:
                    Year: {summary['year']}
                    Total Income: ₹{summary['income_total']}
                    Total Expense: ₹{summary['expense_total']}
                    Savings: ₹{summary['savings']}
                    Savings Rate: {summary['savings_rate']:.2%}
                    Health Score: {summary['health_score']} ({summary['health_label']})
                """

        retrieved_knowledge = self._retrieve(question)

        final_prompt = f"""
                            {context}

                            Relevant Financial Knowledge:
                            {retrieved_knowledge}

                            User Question:
                            {question}
                        """

        return self._ask_groq(final_prompt)
