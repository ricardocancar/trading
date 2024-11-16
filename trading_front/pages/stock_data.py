import requests
import pandas as pd
import plotly.express as px
import streamlit as st

from config import API_URL

def stock_graph():
    st.header("Datos de Stock")
    
    # Entrada de texto para tipo de stop
    stocks = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]  # Example stock symbols
    selected_stock = st.selectbox("Select one stock", options=stocks)
    time_spans = ["1y", "2y", "5y"]  # Define time spans for analysis
    selected_time_span = st.selectbox("Select a time span for analysis", options=time_spans)
    # Función para obtener datos de stock con tipo_stop
    @st.cache_data(ttl=60)
    def fetch_stock_data(tipo_stop):
        params = {}
        if not tipo_stop:
            return {}
        response = requests.get(f"{API_URL}/stocks/{tipo_stop}?span_time={selected_time_span}", params=params)
        response.raise_for_status()
        return response.json()
    
    try:
        stock_data = fetch_stock_data(selected_stock)
        if not stock_data:
            return
        df = pd.DataFrame(stock_data)
        st.dataframe(df)

        # Crear gráfico con Plotly
        titulo = f"Precios de Stock - {selected_stock}" if selected_stock else "Precios de Stock a lo Largo del Tiempo"
        fig = px.line(df, x="Date", y="Close", title=titulo)
        st.plotly_chart(fig)
    except requests.exceptions.ConnectionError:
        st.error("No se pudo conectar con el servidor FastAPI. Asegúrate de que FastAPI esté corriendo.")
    except requests.exceptions.Timeout:
        st.error("La solicitud a FastAPI excedió el tiempo de espera.")
    except requests.exceptions.HTTPError as err:
        st.error(f"Error HTTP: {err}")
    except Exception as e:
        st.error(f"Ocurrió un error inesperado: {e}")

stock_graph()