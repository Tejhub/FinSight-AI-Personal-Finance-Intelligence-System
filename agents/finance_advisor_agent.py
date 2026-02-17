class FinanceAdvisorAgent:
    def run(self, summary):

        advice = []
        income = summary["income_total"]
        expense = summary["expense_total"]
        savings = summary["savings"]

        if income <= 0:
            return ["⚠️ Insufficient income data."]

        rate = savings / income

        # Financial health classification
        if rate >= 0.3:
            advice.append("🟢 You are financially strong. Focus on long-term wealth creation.")
            sip_percent = 0.20   # Invest 20% of savings
        elif rate >= 0.2:
            advice.append("🟡 Your finances are stable. Improve savings discipline.")
            sip_percent = 0.12   # Invest 12% of savings
        else:
            advice.append("🔴 Your expenses are too high. Immediate correction is required.")
            sip_percent = 0.05  # Invest only 5% of savings

        # SIP calculation based on savings, not income
        if savings > 0:
            monthly_savings = savings / 12
            sip = monthly_savings * sip_percent
        else:
            sip = 0

        advice.append(f"📈 Suggested SIP: ₹{sip:,.0f}/month")

        advice.append("🛡️ Prioritize health insurance before risky investments.")
        advice.append("💰 Build an emergency fund covering at least 6 months of expenses to safeguard against uncertainties.")

        return advice
