    
#Libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from haversine import haversine
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static


st.set_page_config (page_title = 'Visão Empresa', page_icon='📊', layout='wide')

# ============================================
# Funções
# ============================================

def country_maps (df1):
    #Order Metric
    # A localização central de cada cidade por tráfego e gerar um mapa
    df_aux = (df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']]
                  .groupby (['City', 'Road_traffic_density'])
                  .median()
                  .reset_index())

    map = folium.Map()
    for index, location_info in df_aux.iterrows():
        folium.Marker ([location_info['Delivery_location_latitude'], location_info['Delivery_location_longitude']], 
            popup=location_info[['City', 'Road_traffic_density']],  zoom_start=100, tiles= 'Stamen Toner', icon=folium.Icon(color='darkblue', icon='pushpin') ).add_to (map)
    folium_static (map, width=1024 , height=600)

        
def order_deliver_by_week (df1):
    # Quantidade de pedidos por entregador por Semana e retorna um gráfico de linha
    # Quantas entregas na semana / Quantos entregadores únicos por semana
    df_aux1 = df1.loc[:, ['ID','week_of_year']].groupby('week_of_year').count().reset_index()
    df_aux2 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby('week_of_year').nunique().reset_index()

    #Utilização do merge - utilizando a biblioteca pandas
    df_aux = pd.merge (df_aux1, df_aux2, how='inner')

    #Fazer o cálculo
    df_aux['order_by_deliver'] = df_aux['ID'] / df_aux ['Delivery_person_ID']


    #Saída Gráfico de Linha

    fig = px.line (df_aux, x='week_of_year', y='order_by_deliver', title='PEDIDOS POR ENTREGADOR POR SEMANA  📉', markers=True )
    fig.update_traces(textposition="top center")

    return fig


def order_by_week (df1):
    #Quantidade de pedidos por semana, retornando um gráfico de linha
    
    df1['week_of_year'] = df1['Order_Date'].dt.strftime ('%U')  # %U primeiro dia da semana começa no Domingo, %W primeiro dia da semana começa na Segunda

    df_aux = df1.loc[:, ['ID', 'week_of_year']].groupby ('week_of_year').count().reset_index()
    fig = px.line(df_aux, x='week_of_year', y='ID', title='PEDIDOS POR SEMANA  📉', markers=True, text='ID')
    fig.update_traces (textposition = 'bottom center')
    
    return fig


def traffic_order_city (df1):
    #Order Metric
    #Distribuição dos pedidos por tipo de tráfego e Cidade e realizado um gráfico de bolha            
    df_aux = df1.loc[:, ['ID', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).count().reset_index()

    fig = px.scatter (df_aux, x='City', y='Road_traffic_density', size='ID', color='City', title='Distribuição por Cidade e Tipo de Tráfego', size_max=30)

    return fig


def traffic_order_share(df1):
                
    #Order Metric
    #Distribuição dos pedidos por tipo de tráfego e realizado um gráfico de pizza
    df_aux = df1.loc[:, ['ID', 'Road_traffic_density']].groupby ('Road_traffic_density').count().reset_index()
    fig = px.pie (df_aux, values='ID', names='Road_traffic_density', title='Distribuição por tipo de Tráfego 🚥', hole=.4)

    return fig


def order_metric (df1):
    #Order_Metric - Gráfico de Barras (Pedidos por dia)

    df_aux = df1.loc[:, ['ID', 'Order_Date']].groupby('Order_Date').count().reset_index()
    fig = px.bar (df_aux, x='Order_Date', y='ID', title='PEDIDOS POR DIA  📊', text_auto=True)
    fig.update_traces(textfont_size=60, textangle=1, textposition="outside", cliponaxis=False)

    return fig


def clean_code( df1 ):
    """ Esta função tem a responsabilidade de limpar o dataframe:
    
        Tipos de Limpeza:
        1. Remoção dos dados NaN
        2. Mudança do tipo da coluna de dados
        3. Remoção dos espaços vazios das variáveis de texto
        4. Formatação da coluna de datas
        5. Limpeza da coluna de tempo (remoção do texto da variável numérica)
    
        Input: Dataframe
        Output: Dataframe
    """
    
    #Alterando tipo da coluna Delivery_person_Age para int:
    #Obs. Retirando também os NaN

    limp_linhas = df1['Delivery_person_Age'] != "NaN "
    df1 = df1.loc[limp_linhas, :]
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype (int)

    #Alterando tipo da coluna Delivery_person_Ratings para float:
    limp_linhas = df1['Delivery_person_Ratings'] != "NaN "
    df1 = df1.loc[limp_linhas, :]
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype (float)


    #Alterando tipo da coluna Order_Date de texto para data:
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')

    #Alterando tipo da coluna multiple_deliveries de texto para inteiro:
    #Obs. Retirando também os NaN
    limp_linhas = df1['multiple_deliveries'] != "NaN "
    df1 = df1.loc[limp_linhas, :]
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype (int)


    #Retirando Nan da coluna City:
    limp_linhas = df1['City'] != "NaN"
    df1 = df1.loc[limp_linhas, :]
    df1['City'] = df1['City'].astype (str)

    limp_linhas = df1['City'] != "NaN "
    df1 = df1.loc[limp_linhas, :]
    df1['City'] = df1['City'].astype (str)

    #Retirando Nan da coluna Festival:
    limp_linhas = df1['Festival'] != "NaN"
    df1 = df1.loc[limp_linhas, :]

    #Retirando Nan da coluna Road_traffic_density:
    limp_linhas = df1['Road_traffic_density'] != "NaN "
    df1 = df1.loc[limp_linhas, :]

    #Retirando Nan da coluna Road_traffic_density:
    limp_linhas = df1['Road_traffic_density'] != "NaN"
    df1 = df1.loc[limp_linhas, :]

    #Retirando Nan da coluna Type_of_vehicle:
    limp_linhas = df1['Type_of_vehicle'] != "NaN"
    df1 = df1.loc[limp_linhas, :]


    #Removendo espaço de strings do dataframe
    #df1 = df1.reset_index(drop=True)
    #for i in range ( len(df1)):
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()  
    df1.loc[:, 'Delivery_person_ID'] = df1.loc[:, 'Delivery_person_ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()


    #Realizando a limpeza da coluna Time_taken(min)

    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split( '(min) ' )[1] )
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    return df1


# ============================================ Início da Estrutura Lógica do Código ============================================== #
# ============================================
# Importando o dataset
# ============================================

df = pd.read_csv ("train.csv")


# ============================================
# Fazendo limpeza dos dados:
# ============================================

df1 = clean_code (df)



# ============================================
# Barra Lateral
# ============================================

st.header( ' 🛒 Marketplace - Visão Cliente' )

image_path=('logo_well_blue.png')
image = Image.open( image_path )
st.sidebar.image( image, width=80 )

st.sidebar.markdown ('# Curry Company')
st.sidebar.markdown ('### *** Fastest Delivery in Town ***')
st.sidebar.markdown( """---""" )

st.sidebar.markdown( '## Selecione uma data limite' )

date_slider = st.sidebar.slider ('Informe a Data',
                   value=pd.datetime (2022, 3, 11),
                   min_value=pd.datetime (2022, 2, 11),
                   max_value=pd.datetime (2022, 4, 6),
                   format='DD-MM-YYYY')

#st.header (date_slider)
st.sidebar.markdown( """---""" )

st.sidebar.markdown( '## Selecione a condição de trânsito' )
traffic_options = st.sidebar.multiselect ('Quais as condições de trânsito',
                                          ['Low', 'Medium', 'High', 'Jam'],
                                          default='Low')



st.sidebar.markdown( """---""" )
st.sidebar.markdown( '#### Powered by Comunidade DS' )


#Filtro de Data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

#Filtro de Condição de Trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin (traffic_options)
df1 = df1.loc[linhas_selecionadas, :]


# =======================================
# Layout no Streamlit
# =======================================

tab1, tab2, tab3 = st.tabs (['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    with st.container():
        
        fig = order_metric (df1)
        st.plotly_chart (fig, use_container_width=True, theme='streamlit')
        
                  
    with st.container():
        col1, col2 = st.columns(2)
        with col1: 
            fig = traffic_order_share (df1)
            st.markdown ('### _Order by Traffic_ 🚥')
            st.plotly_chart (fig, use_container_width=True, theme='streamlit')
            
                            
        with col2:
            
            fig = traffic_order_city (df1)
            st.markdown ('### _Order by City and Traffic_')
            st.plotly_chart (fig, use_container_width=True)
                     
            
with tab2:
    with st.container ():
        
        fig = order_by_week (df1)
        st.write ("### _Orders by Week_ :chart_with_downwards_trend:")
        st.plotly_chart (fig, use_container_width=True, theme='streamlit')
        
             
    with st.container ():
        
        fig = order_deliver_by_week (df1)
        st.write ("### _Orders Deliver by Week_ :chart_with_downwards_trend:")
        st.plotly_chart(fig, use_container_width=True, theme='streamlit')  
           
    
with tab3:
    
    st.write ("### _Central Localization by City and Traffic_ :world_map:")
    country_maps (df1)
    
    
