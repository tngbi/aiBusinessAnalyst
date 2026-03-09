
from config import (
    REVENUE_LOW_THRESHOLD,
    REVENUE_HIGH_THRESHOLD,
    PROFIT_MARGIN_HEALTHY,
    PROFIT_MARGIN_WARNING,
)
from utils.logger import logger


def generate_recommendations(kpis):
    """Generate actionable business recommendations from KPIs."""
    recommendations = []

    revenue = kpis.get("Total Revenue", 0)
    profit = kpis.get("Total Profit", 0)
    margin = kpis.get("Profit Margin %", None)
    mom_change = kpis.get("MoM Revenue Change %", None)
    customers = kpis.get("Customers", 0)
    rev_per_cust = kpis.get("Revenue per Customer", 0)

    # Revenue-based recommendations
    if revenue < REVENUE_LOW_THRESHOLD:
        recommendations.append(
            "Revenue is below the target threshold. Consider increasing marketing spend, "
            "expanding into new channels, or launching promotional campaigns."
        )
    elif revenue > REVENUE_HIGH_THRESHOLD:
        recommendations.append(
            "Strong revenue performance. Explore opportunities to reinvest in product "
            "development and customer retention programmes."
        )

    # Profitability
    if profit < 0:
        recommendations.append(
            "The business is operating at a loss. Conduct an urgent cost audit and "
            "identify low-margin products or services to restructure."
        )
    elif margin is not None:
        if margin < PROFIT_MARGIN_WARNING:
            recommendations.append(
                f"Profit margin ({margin}%) is critically low. Prioritise cost reduction "
                "and renegotiate supplier contracts."
            )
        elif margin < PROFIT_MARGIN_HEALTHY:
            recommendations.append(
                f"Profit margin ({margin}%) is below healthy levels. Consider pricing "
                "strategy adjustments and operational efficiency improvements."
            )

    # Growth trend
    if mom_change is not None:
        if mom_change < -10:
            recommendations.append(
                f"Revenue declined {abs(mom_change):.1f}% month-over-month. "
                "Investigate root causes — market shifts, churn, or seasonal factors."
            )
        elif mom_change > 20:
            recommendations.append(
                f"Revenue grew {mom_change:.1f}% MoM — strong momentum. "
                "Ensure operational capacity can sustain this growth trajectory."
            )

    # Customer metrics
    if customers > 0 and rev_per_cust < 100:
        recommendations.append(
            "Revenue per customer is low. Explore upselling, cross-selling, "
            "and loyalty programmes to increase customer lifetime value."
        )

    if not recommendations:
        recommendations.append(
            "Business performance is healthy across all tracked metrics. "
            "Continue monitoring KPIs and look for incremental optimisation opportunities."
        )

    logger.info(f"Generated {len(recommendations)} recommendations")
    return recommendations
