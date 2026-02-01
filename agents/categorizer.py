class CategorizationAgent:

    EXPENSE_RULES = {
        "Food": ["swiggy", "zomato", "grocery", "restaurant", "coffee"],
        "Travel": ["uber", "ola", "flight", "hotel", "fuel"],
        "Bills": ["electricity", "water", "recharge"],
        "Shopping": ["amazon", "flipkart"],
        "Entertainment": ["netflix", "movie", "gym"],
        "Medical": ["medical", "hospital", "pharmacy"]
    }

    INCOME_RULES = {
        "Salary": ["salary", "job"],
        "Freelancing": ["freelance"],
        "Bonus": ["bonus"],
        "Investment Returns": ["interest", "dividend"],
        "Cashback": ["cashback"],
        "Refund": ["refund"]
    }

    def categorize(self, desc, txn_type):
        desc = str(desc).lower()
        rules = self.EXPENSE_RULES if txn_type == "Expense" else self.INCOME_RULES
        for cat, keys in rules.items():
            if any(k in desc for k in keys):
                return cat
        return "Other"

    def run(self, df):
        df["category"] = df.apply(
            lambda r: self.categorize(r["description"], r["expense/income"]),
            axis=1
        )
        return df
