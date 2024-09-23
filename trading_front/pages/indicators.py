import requests
import pandas as pd
import plotly.express as px
import streamlit as st

from config import API_URL

# Configurar la URL base de FastAPI


def indicators():
# Realizar una solicitud a la API de FastAPI para obtener datos de indicadores
    try:
        tipo_stop = st.text_input("Ingresa el tipo de stop a analizar")
        indicator = st.text_input("Ingresa el indicador a analizar")
        if not tipo_stop:
            return {}
        if not indicator:
            return {}
        response = requests.get(f"{API_URL}/indicators/{indicator}/{tipo_stop}")
        response.raise_for_status()
        indicators = response.json()
        df = pd.DataFrame(indicators)
        df.dropna(inplace=True)

        fig = px.line(df[["Date", "Close", "sma_short", "sma_long"]], x="Date", y=["Close", "sma_short", "sma_long"],
                    title="Indicadores de Rendimiento con SMA",
                    labels={"value": "Valor", "indicator": "Indicador"})
        st.plotly_chart(fig)

    except requests.exceptions.RequestException as e:
        st.error(f"Error al obtener indicadores: {e}")
