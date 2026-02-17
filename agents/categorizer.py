import pandas as pd
from rapidfuzz import process, fuzz
from langchain_groq import ChatGroq
import os
from langchain_core.messages import HumanMessage


class CategorizationAgent:
    def __init__(self):
        # Tier 3: LLM Initialization
        self.llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.3-70b-versatile",
        temperature=0
    )
        
        # Tier 1: Local Cache (to prevent redundant LLM calls)
        self.cache = {}

        self.EXPENSE_RULES = {
            "Food": ["swiggy", "zomato", "grocery", "restaurant", "coffee", "tea", "chai", "blinkit"],
            "Travel": ["uber", "ola", "flight", "hotel", "fuel", "petrol", "irctc", "indigo"],
            "Bills": ["electricity", "water", "recharge", "jio", "airtel", "rent", "tata power"],
            "Shopping": ["amazon", "flipkart", "myntra", "zara", "ajio"],
            "Entertainment": ["netflix", "movie", "gym", "hotstar", "spotify", "pvr"],
            "Medical": ["medical", "hospital", "pharmacy", "apollo", "practo"]
        }

        self.INCOME_RULES = {
            "Salary": ["salary", "payout", "monthly pay"],
            "Freelancing": ["freelance", "upwork", "fiverr"],
            "Bonus": ["bonus"],
            "Investment Returns": ["interest", "dividend", "fd", "mutual fund"],
            "Cashback": ["cashback"],
            "Refund": ["refund"]
        }

    def _get_llm_category(self, desc, txn_type, possible_categories):
        """Tier 3: The LLM reasoning step for unknown vendors."""
        prompt = f"""
        Act as a financial expert. Classify this transaction: '{desc}' 
        Type: {txn_type}
        Options: {', '.join(possible_categories)} or 'Other'.
        Return ONLY the category name. If it sounds like a beverage or cafe (like 'Tea'), use 'Food'.
        """
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            category = response.content.strip()
            return category if category in possible_categories else "Other"
        except:
            return "Other"

    def categorize(self, desc, txn_type):
        desc_clean = str(desc).lower().strip()
        if not desc_clean or desc_clean == 'nan':
            return "Other"
        
        # --- Tier 1: Cache Match ---
        if desc_clean in self.cache:
            return self.cache[desc_clean]

        rules = self.EXPENSE_RULES if txn_type == "Expense" else self.INCOME_RULES
        possible_cats = list(rules.keys())

        # Check exact keywords
        for cat, keys in rules.items():
            if any(k in desc_clean for k in keys):
                self.cache[desc_clean] = cat
                return cat

        # --- Tier 2: Fuzzy Match (Typos) ---
        all_keywords = []
        for cat, keys in rules.items():
            for k in keys:
                all_keywords.append((k, cat))
        
        match = process.extractOne(desc_clean, [x[0] for x in all_keywords], scorer=fuzz.WRatio)
        if match and match[1] > 85: 
            category = next(cat for k, cat in all_keywords if k == match[0])
            self.cache[desc_clean] = category
            return category

        # --- Tier 3: LLM Semantic Intelligence ---
        category = self._get_llm_category(desc_clean, txn_type, possible_cats)
        self.cache[desc_clean] = category
        return category

    def run(self, df):
        df["category"] = df.apply(
            lambda r: self.categorize(r["description"], r["expense/income"]),
            axis=1
        )
        return df
    
