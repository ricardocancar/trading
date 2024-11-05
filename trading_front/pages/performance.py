import requests
import pandas as pd
import plotly.express as px
import streamlit as st

from config import API_URL

# Configurar la URL base de FastAPI


def performance():
# Realizar una solicitud a la API de FastAPI para obtener datos de indicadores
    try:
        indicators = ["sma", "mre"]
        indicator = st.selectbox("Ingresa el indicador a analizar", options=indicators)
        stocks = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]  # Example stock symbols
        selected_stock = st.selectbox("Select one stock", options=stocks)
        strategies = ["crossover", "bolling"]
        if indicator == "mre":
            strategies = ["bolling"]
        strategy = st.selectbox("select one strategie", options=strategies)

        if not selected_stock:
            return {}
        if not indicator: 
            return {}
        time_spans = ["1y", "2y", "5y"]  # Define time spans for analysis
        selected_time_span = st.selectbox("Select a time span for analysis", options=time_spans)
        if strategy == "bolling":
            indicator = "mre"
        response = requests.get(f"{API_URL}/performance/strategy/{strategy}/{indicator}/{selected_stock}?span_time={selected_time_span}")
        response.raise_for_status()
        indicators = response.json()
        df = pd.DataFrame(indicators)
        df.dropna(inplace=True)

        fig = px.line(df[["Date", "returns", "strategy_returns", "drawdown"]], x="Date", y=["returns", "strategy_returns", "drawdown"],
                    title="Performance",
                    labels={"value": "Valor", "Performance": "Performance"})
        
        st.plotly_chart(fig)

        ingress = list(df[["returns","strategy_returns"]].sum().to_dict().items())
        df = pd.DataFrame(ingress, columns=['Ingress', 'Value'])
        fig2 = px.bar(
            df, x='Ingress', y='Value',
            title='Ingresos en porcentaje',
            text='Value',
            labels={'Ingress': 'ingresos en porcentage', 'Value': 'Valor'}
            )
        st.plotly_chart(fig2)
        response = requests.get(f"{API_URL}/performance/strategy/{strategy}/risk/{indicator}/{selected_stock}")
        response.raise_for_status()
        risk = response.json()
        data = list(risk.items())

        df = pd.DataFrame(data, columns=['Risk', 'Value'])
        fig1 = px.bar(
            df, x='Risk', y='Value',
            title='Rendimiento de la Estrategia Crossover',
            text='Value',
            labels={'Risk': 'riesgo', 'Value': 'Valor'}
            )
        st.plotly_chart(fig1)
    except requests.exceptions.RequestException as e:
        st.error(f"Error al obtener indicadores: {e}")

performance()
