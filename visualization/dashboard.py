
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from config import (
    CHART_COLOR_PRIMARY,
    CHART_COLOR_SECONDARY,
    CHART_COLOR_POSITIVE,
    CHART_COLOR_NEGATIVE,
)
from utils.helpers import format_currency, format_percent


def render_dashboard(df, kpis, forecast, importance_df=None):
    """Render the main Streamlit dashboard."""

    # ── KPI Cards ──────────────────────────────────────────────
    st.subheader("Key Metrics")
    display_kpis = {k: v for k, v in kpis.items() if k != "Date Range"}

    cols = st.columns(min(len(display_kpis), 4))
    for i, (key, value) in enumerate(display_kpis.items()):
        col = cols[i % len(cols)]
        if isinstance(value, float):
            if "%" in key:
                col.metric(key, format_percent(value))
            elif "Revenue" in key or "Profit" in key or "Cost" in key:
                col.metric(key, format_currency(value))
            else:
                col.metric(key, f"{value:,.2f}")
        else:
            col.metric(key, f"{value:,}" if isinstance(value, int) else value)

    if "Date Range" in kpis:
        st.caption(f"Data period: {kpis['Date Range']}")

    # ── Revenue Trend ──────────────────────────────────────────
    if "Revenue" in df.columns and "Date" in df.columns:
        st.subheader("Revenue Trend")
        daily = df.groupby("Date")["Revenue"].sum().reset_index()
        fig = px.line(
            daily, x="Date", y="Revenue",
            title="Daily Revenue",
            color_discrete_sequence=[CHART_COLOR_PRIMARY],
        )
        fig.update_layout(xaxis_title="Date", yaxis_title="Revenue ($)")
        st.plotly_chart(fig, use_container_width=True)

    # ── Revenue by Month ───────────────────────────────────────
    if "Month" in df.columns and "Revenue" in df.columns:
        st.subheader("Monthly Revenue Breakdown")
        monthly = df.groupby("Month")["Revenue"].sum().reset_index()
        fig_bar = px.bar(
            monthly, x="Month", y="Revenue",
            title="Revenue by Month",
            color_discrete_sequence=[CHART_COLOR_SECONDARY],
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # ── Profit vs Cost ─────────────────────────────────────────
    if "Profit" in df.columns and "Cost" in df.columns and "Date" in df.columns:
        st.subheader("Profit vs Cost Over Time")
        daily_pc = df.groupby("Date")[["Profit", "Cost"]].sum().reset_index()
        fig_pc = go.Figure()
        fig_pc.add_trace(go.Scatter(
            x=daily_pc["Date"], y=daily_pc["Profit"],
            name="Profit", line=dict(color=CHART_COLOR_POSITIVE),
        ))
        fig_pc.add_trace(go.Scatter(
            x=daily_pc["Date"], y=daily_pc["Cost"],
            name="Cost", line=dict(color=CHART_COLOR_NEGATIVE),
        ))
        fig_pc.update_layout(xaxis_title="Date", yaxis_title="Amount ($)")
        st.plotly_chart(fig_pc, use_container_width=True)

    # ── Forecast ───────────────────────────────────────────────
    if forecast is not None:
        st.subheader("Revenue Forecast")
        fig_fc = go.Figure()
        fig_fc.add_trace(go.Scatter(
            x=forecast["ds"], y=forecast["yhat"],
            name="Forecast", line=dict(color=CHART_COLOR_PRIMARY),
        ))
        if "yhat_lower" in forecast.columns and "yhat_upper" in forecast.columns:
            fig_fc.add_trace(go.Scatter(
                x=forecast["ds"], y=forecast["yhat_upper"],
                mode="lines", line=dict(width=0), showlegend=False,
            ))
            fig_fc.add_trace(go.Scatter(
                x=forecast["ds"], y=forecast["yhat_lower"],
                mode="lines", line=dict(width=0), showlegend=False,
                fill="tonexty", fillcolor="rgba(31,119,180,0.15)",
            ))
        fig_fc.update_layout(xaxis_title="Date", yaxis_title="Revenue ($)", title="30-Day Revenue Forecast")
        st.plotly_chart(fig_fc, use_container_width=True)

    # ── Feature Importance ─────────────────────────────────────
    if importance_df is not None and not importance_df.empty:
        st.subheader("Feature Importance (SHAP)")
        fig_imp = px.bar(
            importance_df.head(10),
            x="Mean |SHAP|", y="Feature",
            orientation="h",
            title="Top 10 Features by SHAP Importance",
            color_discrete_sequence=[CHART_COLOR_SECONDARY],
        )
        fig_imp.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_imp, use_container_width=True)
