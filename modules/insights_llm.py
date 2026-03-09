
import os
from openai import OpenAI
from utils.logger import logger


def generate_insights(kpis):
    """Use OpenAI to generate business insights from KPIs."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logger.warning("OPENAI_API_KEY not set — returning rule-based insights")
        return _fallback_insights(kpis)

    try:
        client = OpenAI(api_key=api_key)

        prompt = (
            "You are a senior business analyst. Analyze the following KPIs "
            "and provide 3-5 actionable insights with supporting reasoning.\n\n"
            f"KPIs:\n{kpis}"
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1024,
        )

        return response.choices[0].message.content

    except Exception as e:
        logger.error(f"OpenAI API call failed: {e}")
        return _fallback_insights(kpis)


def _fallback_insights(kpis):
    """Rule-based insights when LLM is unavailable."""
    insights = []
    revenue = kpis.get("Total Revenue", 0)
    profit = kpis.get("Total Profit", 0)
    customers = kpis.get("Customers", 0)

    if revenue > 0:
        margin = (profit / revenue) * 100 if revenue else 0
        insights.append(f"Profit margin is {margin:.1f}%. "
                        + ("This is healthy." if margin > 20 else "Consider cost optimisation."))
    if customers > 0:
        rev_per_cust = revenue / customers
        insights.append(f"Average revenue per customer is ${rev_per_cust:,.2f}.")
    if profit < 0:
        insights.append("The business is currently operating at a loss — urgent cost review needed.")
    if not insights:
        insights.append("Upload data with Revenue, Cost, and Customer_ID columns for richer insights.")

    return "\n".join(f"• {i}" for i in insights)
