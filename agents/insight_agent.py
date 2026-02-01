class InsightAgent:
    def run(self, df, year):
        df = df.copy()
        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month_name()
        year_df = df[df["year"] == year]

        income_df = year_df[year_df["expense/income"] == "Income"]
        expense_df = year_df[year_df["expense/income"] == "Expense"]

        income = income_df["amount"].sum()
        expense = expense_df["amount"].sum()
        savings = income - expense

        if income > 0:
            savings_rate = savings / income
        else:
            savings_rate = 0

        if savings_rate >= 0.40:
            health_score, health_label = 90, "Excellent"
        elif savings_rate >= 0.25:
            health_score, health_label = 70, "Stable"
        else:
            health_score, health_label = 40, "Critical"

        year_df["month"] = year_df["date"].dt.month_name()
        order = ["January","February","March","April","May","June",
                 "July","August","September","October","November","December"]

        income_by_month = (
            income_df.groupby("month")["amount"].sum()
            .reindex(order, fill_value=0)               
        )

        expense_by_month = (
            expense_df.groupby("month")["amount"].sum()
            .reindex(order, fill_value=0)
        )

        return {
            "year": year,
            "income_total": income,
            "expense_total": expense,
            "savings": savings,
            "savings_rate": savings_rate,
            "health_score": health_score,
            "health_label": health_label,
            "income_by_category": income_df.groupby("category")["amount"].sum(),
            "expense_by_category": expense_df.groupby("category")["amount"].sum(),
            "income_by_month": income_by_month,
            "expense_by_month": expense_by_month
        }
