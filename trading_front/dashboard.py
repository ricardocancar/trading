import streamlit as st

from pages.home import home
from pages.stock_data import stock_graph
from pages.indicators import indicators


# Configurar la URL base de FastAPI (puede ser una variable de entorno en producción)


st.title("Trading Dashboard")

# Crear una barra lateral para navegación
st.sidebar.title("Navegación")
page = st.sidebar.radio("Ir a", ["Home", "Datos de Stock", "Indicadores"])





page_selector = {
    "Home": home,
    "Datos de Stock": stock_graph,
    "Indicadores": indicators
}
    

page_selector[page]()
    

