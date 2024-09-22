import streamlit as st

from pages.home import home
from pages.stock_data import stock_graph


# Configurar la URL base de FastAPI (puede ser una variable de entorno en producción)


st.title("Trading Dashboard")

# Crear una barra lateral para navegación
st.sidebar.title("Navegación")
page = st.sidebar.radio("Ir a", ["Home", "Datos de Stock"])





page_selector = {
    "Home": home,
    "Datos de Stock": stock_graph
}
    

page_selector[page]()
    

