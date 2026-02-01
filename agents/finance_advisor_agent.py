class FinanceAdvisorAgent:
    def run(self, summary):
        advice = []
        income = summary["income_total"]
        savings = summary["savings"]

        if income <= 0:
            return ["⚠️ Insufficient income data."]

        rate = savings / income

        if rate >= 0.3:
            advice.append("🟢 You are financially strong. Focus on long-term wealth creation.")
        elif rate >= 0.2:
            advice.append("🟡 Your finances are stable. Improve savings discipline.")
        else:
            advice.append("🔴 Your expenses are too high. Immediate correction is required.")

        sip = (income / 12) * 0.15
        advice.append(f"📈 Suggested SIP: ₹{sip:,.0f}/month")

        advice.append("🛡️ Prioritize health insurance before risky investments.")

        advice.append("💰 Build an emergency fund covering at least 6 months of expenses to safeguard against uncertainties.")

        return advice
