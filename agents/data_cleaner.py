import os
import json
import re
import pandas as pd
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

class DataCleaningAgent:

    def __init__(self):
        self.llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.3-70b-versatile",  
            temperature=0
        )

    def _safe_json_parse(self, text):
        try:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if not match:
                raise ValueError("No JSON found")
            return json.loads(match.group())
        except Exception:
            return {
                "missing_values": True,
                "invalid_dates": True,
                "negative_amounts": True,
                "action": "standard_cleaning"
            }

    def _analyze_data_health(self, df_sample):

        prompt = f"""
                    You are a Data Quality Agent.
                    Analyze dataset and return ONLY valid JSON.

                    Sample: {df_sample.to_string(index=False)}

                    Keys:
                    missing_values (true/false)
                    invalid_dates (true/false)
                    negative_amounts (true/false)
                    action (string)
                """

        res = self.llm.invoke([HumanMessage(content=prompt)])
        return self._safe_json_parse(res.content)

    def _apply_cleaning(self, df, plan):

        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_", regex=False)
        )

        # Date conversion
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")

        # Amount cleaning
        if "amount" in df.columns:
            df["amount"] = (
                df["amount"]
                .astype(str)
                .str.replace("₹", "", regex=False)
                .str.replace(",", "", regex=False)
            )
            df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

        # Drop only critical missing fields
        required_cols = ["date", "amount", "expense/income"]
        existing_cols = [c for c in required_cols if c in df.columns]
        df = df.dropna(subset=existing_cols)

        # Fix negative amounts
        if plan.get("negative_amounts", False) and "amount" in df.columns:
            df["amount"] = df["amount"].abs()

        # Normalize txn type
        if "expense/income" in df.columns:
            df["expense/income"] = df["expense/income"].astype(str).str.strip()

        return df

    def run(self, uploaded_file):

        df = pd.read_csv(uploaded_file)
        plan = self._analyze_data_health(df.head(5))
        df_cleaned = self._apply_cleaning(df, plan)

        return df_cleaned
