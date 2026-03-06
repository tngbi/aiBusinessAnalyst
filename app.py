
import streamlit as st
import pandas as pd

from modules.data_loader import load_excel
from modules.data_cleaning import clean_data
from modules.feature_engineering import create_features
from modules.analytics import compute_kpis
from modules.forecasting import forecast_revenue
from modules.insights_llm import generate_insights
from modules.recommendations import generate_recommendations
from visualization.dashboard import render_dashboard

st.title("AI Business Analyst Dashboard")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:

    df = load_excel(uploaded_file)

    df = clean_data(df)

    df = create_features(df)

    kpis = compute_kpis(df)

    forecast = forecast_revenue(df)

    insights = generate_insights(kpis)

    recommendations = generate_recommendations(kpis)

    render_dashboard(df, kpis, forecast)

    st.subheader("AI Insights")
    st.write(insights)

    st.subheader("Recommendations")
    st.write(recommendations)
