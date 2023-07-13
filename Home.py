import streamlit as st
from PIL import Image

st.set_page_config ( page_title = "Home", page_icon="🏠", layout='wide', initial_sidebar_state='auto')

image_path = 'logo_well_blue.png'
image = Image.open (image_path)
st.sidebar.image (image, width = 80)

st.sidebar.markdown ('# Curry Company')
st.sidebar.markdown ('### *** Fastest Delivery in Town ***')
st.sidebar.markdown( """---""" )

st.write ('# Curry Company Growth Dashboard')

st.markdown (
    """ 
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
    ### Como utilizar esse Growth Dashboard?
    
    - Visão Empresa:
        - Visão Gerencial: Métricas Gerais de Comportamento.
        - Visão Tática: Indicadores semanais de Crescimento.
        - Visão Geográfica: Insights de Localização.
    
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento
        
    - Visão Restaurante:
        - Indicadores Semanais de Crescimento dos Restaurantes
        
    #### Ask for Help
    - Time de Data Science no Discord
        - Wellington1102#6822
    """)