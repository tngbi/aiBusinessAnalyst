
def generate_recommendations(kpis):

    recommendations = []

    if kpis.get("Total Revenue",0) < 100000:
        recommendations.append("Increase marketing investment")

    if kpis.get("Total Profit",0) < 0:
        recommendations.append("Reduce operational costs")

    if len(recommendations) == 0:
        recommendations.append("Business performance is healthy. Continue monitoring key KPIs.")

    return recommendations
