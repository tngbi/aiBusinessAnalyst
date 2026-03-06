
import streamlit as st
import plotly.express as px

def render_dashboard(df,kpis,forecast):

    st.subheader("Key Metrics")

    cols = st.columns(len(kpis))

    for i,(key,value) in enumerate(kpis.items()):
        cols[i].metric(key,value)

    if "Revenue" in df.columns and "Date" in df.columns:

        fig = px.line(df,x="Date",y="Revenue",title="Revenue Trend")

        st.plotly_chart(fig)

    if forecast is not None:

        fig2 = px.line(forecast,x="ds",y="yhat",title="Revenue Forecast")

        st.plotly_chart(fig2)
