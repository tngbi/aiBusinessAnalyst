
import streamlit as st
import pandas as pd

from config import APP_NAME, SUPPORTED_FILE_TYPES
from modules.data_loader import load_excel
from modules.data_cleaning import clean_data
from modules.feature_engineering import create_features
from modules.analytics import compute_kpis
from modules.forecasting import forecast_revenue
from modules.explainability import compute_feature_importance
from modules.insights_llm import generate_insights
from modules.recommendations import generate_recommendations
from visualization.dashboard import render_dashboard
from utils.logger import logger
from utils.helpers import dataframe_summary

# ── Page config ────────────────────────────────────────────────
st.set_page_config(page_title=APP_NAME, layout="wide", page_icon="📊")
st.title(f"📊 {APP_NAME}")
st.markdown("Upload your business data and get instant KPIs, forecasts, AI insights, and recommendations.")

# ── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.header("Data Upload")
    uploaded_file = st.file_uploader(
        "Upload Excel or CSV file",
        type=SUPPORTED_FILE_TYPES,
        help="Expects columns: Date, Revenue, Cost, Customer_ID",
    )
    st.markdown("---")
    run_explainability = st.checkbox("Run feature importance (SHAP)", value=False)

# ── Main pipeline ──────────────────────────────────────────────
if uploaded_file:
    try:
        # 1. Load
        with st.spinner("Loading data…"):
            df = load_excel(uploaded_file)
        st.success(f"Loaded data — {dataframe_summary(df)}")

        # 2. Clean
        with st.spinner("Cleaning data…"):
            df = clean_data(df)

        # 3. Feature engineering
        with st.spinner("Engineering features…"):
            df = create_features(df)

        # 4. KPIs
        with st.spinner("Computing KPIs…"):
            kpis = compute_kpis(df)

        # 5. Forecast
        with st.spinner("Generating revenue forecast…"):
            forecast = forecast_revenue(df)

        # 6. Explainability (optional)
        importance_df = None
        if run_explainability:
            with st.spinner("Computing feature importance (this may take a moment)…"):
                importance_df, _ = compute_feature_importance(df)

        # 7. AI Insights
        with st.spinner("Generating AI insights…"):
            insights = generate_insights(kpis)

        # 8. Recommendations
        recommendations = generate_recommendations(kpis)

        # ── Render ─────────────────────────────────────────────
        render_dashboard(df, kpis, forecast, importance_df=importance_df)

        st.markdown("---")

        col_left, col_right = st.columns(2)

        with col_left:
            st.subheader("🔍 AI Insights")
            st.markdown(insights)

        with col_right:
            st.subheader("💡 Recommendations")
            for rec in recommendations:
                st.markdown(f"- {rec}")

        # ── Raw data preview ───────────────────────────────────
        with st.expander("📋 View Raw Data"):
            st.dataframe(df, use_container_width=True)

        logger.info("Pipeline completed successfully")

    except ValueError as ve:
        st.error(f"Data error: {ve}")
        logger.error(f"ValueError in pipeline: {ve}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        logger.error(f"Unhandled exception in pipeline: {e}")

else:
    st.info("👈 Upload a file from the sidebar to get started.")
