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

st.set_page_config (page_title = 'Visão Entregadores', page_icon='🛵', layout='wide')

# ============================================
# Funções
# ============================================


def delivers_faster (df1):
    df_aux = ( df1.loc[:,['Delivery_person_ID', 'Time_taken(min)', 'City']]
                  .groupby(['City', 'Delivery_person_ID']).mean()).reset_index()

    top_10 = df_aux.groupby(['City']).apply(lambda x: x.nsmallest(10, 'Time_taken(min)')).reset_index(drop=True)

    top_10 = top_10.rename(columns={'Time_taken(min)': 'Tempo Levado (min)', 
                                    'City' : 'Cidade',
                                    'Delivery_person_ID' : 'ID do Entregador'})
    return top_10
            

def delivers_slowly (df1):
                
    df_aux = ( df1.loc[:,['Delivery_person_ID', 'Time_taken(min)', 'City']]
          .groupby(['City', 'Delivery_person_ID']).mean()).reset_index()

    top_10 = df_aux.groupby(['City']).apply(lambda x: x.nlargest(10, 'Time_taken(min)')).reset_index(drop=True)

    top_10 = top_10.rename(columns={'Time_taken(min)': 'Tempo Levado (min)', 
                                    'City' : 'Cidade',
                                    'Delivery_person_ID' : 'ID do Entregador'})

    return top_10

def clean_code(df1):
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
    #fazendo limpeza das linhas:

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

st.header( '🛵 Marketplace - Visão Entregadores' )

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

tab1, tab2, tab3 = st.tabs (['Visão Gerencial', ' - ', ' - '])

with tab1:
    with st.container():
        st.title ('Overall Metrics')
        
        col1, col2, col3, col4 = st.columns (4, gap='small')
        with col1:
            # A maior idade dos entregadores
            #st.write ('Maior Idade')
            maior_idade = df1.loc[:, "Delivery_person_Age"].max()
            col1.metric ('Maior Idade', maior_idade)
            
        with col2:
            # A menor idade dos entregadores
            #st.write ('Menor Idade')
            menor_idade = df1.loc[:, "Delivery_person_Age"].min()
            col2.metric ('Menor Idade', menor_idade)
            
        with col3:
            # A melhor condição do veículo:
            #st.write ('Melhor Condição')
            melhor_cond = df1.loc[:, "Vehicle_condition"].max()
            col3.metric ('Melhor Condição', melhor_cond)
            
        with col4:
            # A pior condição do veículo:
            #st.write ('Pior Condição')
            pior_cond = df1.loc[:, "Vehicle_condition"].min()
            col4.metric ('Pior Condição', pior_cond)
            
    with st.container():
        st.markdown ("""---""")
        st.title ('Avaliações')
        
        col1, col2 = st.columns(2, gap='large')
        
        with col1:
            
        
            st.write ('Avaliação Média por entregador')
            avg_deliver = df1.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']].groupby(['Delivery_person_ID']).mean().reset_index()
            
            avg_deliver = avg_deliver.rename(columns = {'Delivery_person_ID' : 'ID do Entregador',
                                                        'Delivery_person_Ratings' : 'Nota média Avaliação'})
            
            st.dataframe (avg_deliver, use_container_width=True, hide_index=True)
        
        with col2:
            st.write ('Avaliação Média por Trânsito')
            df_aux = (df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']].groupby('Road_traffic_density')
                         .agg({'Delivery_person_Ratings' : ['mean', 'std']}))

            df_aux.columns = ['delivery_mean', 'delivery_std']

            aval_transito = df_aux.reset_index()
            
            aval_transito = aval_transito.rename(columns={'delivery_mean' : 'Nota Média Avaliação',
                                                    'delivery_std' : 'Desvio Padrão',
                                                    'Road_traffic_density' : 'Condição do Trânsito'})
            st.dataframe (aval_transito, use_container_width=True, hide_index=True)
            
            
            st.write ('Avaliação Média por Clima')
            
            df_aux = (df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']].groupby(['Weatherconditions'])
                         .agg({'Delivery_person_Ratings' : ['mean', 'std']}))

            df_aux.columns = ['delivery_mean', 'delivery_std']


            aval_clima = df_aux.reset_index()
            
            aval_clima = aval_clima.rename(columns={'delivery_mean' : 'Nota Média Avaliação',
                                                    'delivery_std' : 'Desvio Padrão',
                                                    'Weatherconditions' : 'Condição do Tempo'})
            st.dataframe (aval_clima, use_container_width=True, hide_index=True)
            
    with st.container():
        st.markdown ("""---""")
        st.title ('Velocidade de Entrega')
        
        col1, col2 = st.columns (2)
        
        with col1:
            st.write ('Top Entregadores mais rápidos')
            top_10 = delivers_faster (df1)
            st.dataframe (top_10, use_container_width=True, hide_index=True, column_config={
            "Cidade": st.column_config.Column( "Cidade", help="**Nome da Cidade**🎈", width=None, required=True), 
                                             
            "ID do Entregador": st.column_config.Column( "ID do Entregador", help="**Id do Entregador**🎈", width=None, required=True),
            "Tempo Levado (min)": st.column_config.Column( "Tempo Levado (min)", help=" **Tempo médio de entrega**🎈", width='small', required=True)})
            
                      
            
        with col2:
            st.write ('Top Entregadores mais lentos')
            top_10 = delivers_slowly (df1)
            st.dataframe (top_10, use_container_width=True, hide_index=True, column_config={
                "Cidade": st.column_config.Column( "Cidade", help=" **Nome da Cidade**🎈", width=None, required=True), 

                "ID do Entregador": st.column_config.Column( "ID do Entregador", help="**ID do Entregador**🎈", width=None, required=True),
                "Tempo Levado (min)": st.column_config.Column( "Tempo Levado (min)", help=" **Tempo médio de entrega**🎈", width='small', required=True)})
            
            
            
                
         
            
            
            
            