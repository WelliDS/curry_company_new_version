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

st.set_page_config (page_title = 'Visão Restaurantes', page_icon='🍽', layout='wide')

# ============================================
# Funções
# ============================================

def avg_std_time_on_traffic (df1):
    #Distribuição do Tempo por Cidade, Tipo de Tráfego e Desvio Padrão e retorna um gráfiico sunburst
    
    df_aux = (df1.loc[:, ['Time_taken(min)', 'City', 'Road_traffic_density']]
                 .groupby (['City', 'Road_traffic_density']).agg({'Time_taken(min)' : ['mean', 'std']}))

    df_aux.columns = ['time_mean', 'time_std']

    df_aux = df_aux.reset_index()


    fig = px.sunburst (df_aux, path=['City', 'Road_traffic_density'], values='time_mean', color='time_std', color_continuous_scale='RdBu',
           color_continuous_midpoint=np.average(df_aux['time_std'], ) )
    fig.update_layout(barmode='group', width=350, height=350, margin=dict(l=20, r=20, t=40, b=40))
    
    return fig

def avg_std_time_graph (df):
                          
    df_aux = df1.loc[:, ['City', 'Time_taken(min)']].groupby('City').agg ( {'Time_taken(min)': ['mean', 'std']} )

    df_aux.columns = ['time_mean', 'time_std']

    df_aux = df_aux.reset_index()

    fig = go.Figure()
    fig.add_trace (go.Bar(name='Control',
              x=df_aux['City'],
              y=df_aux['time_mean'],
              error_y=dict(type='data', array=df_aux['time_std'] ) ) )

    fig.update_layout(barmode='group', width=350, height=350, margin=dict(l=20, r=20, t=40, b=40))

    return fig

def distance(df1, fig):
    #função com a distância média entre os restaurantes e os locais de Entrega, com o FIG retornamos um gráfico
    
    if fig == False:
    
        df1['distance'] = (df1.loc[:, ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']]
                  .apply(lambda x: haversine ( 
                        (x['Restaurant_latitude'], x['Restaurant_longitude']), 
                        (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1))
        df_aux = np.round (df1.loc[:, 'distance'].mean(), 2)

        return df_aux
    
    else:
        df1['distance'] = (df1.loc[:, ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']]
                      .apply(lambda x: haversine ( 
                            (x['Restaurant_latitude'], x['Restaurant_longitude']), 
                            (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1))

        avg_distance = df1.loc[:, ['City', 'distance']].groupby(['City']).mean().reset_index()

        fig = go.Figure (data=[go.Pie (labels=avg_distance['City'], values=avg_distance['distance'], pull=[ 0, 0.1, 0])])  
        fig.update_layout(barmode='group', width=350, height=350, margin=dict(l=20, r=20, t=40, b=40))
        
        return fig

def clean_code(df1):
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

st.header( '🍴 Marketplace - Visão Restaurantes' )

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
                                          default='Medium')



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
               
        col1, col2, col3, col4, col5, col6 = st.columns (6, gap = 'small')
        with col1:
            entregadores = df1.loc[:,"Delivery_person_ID"].nunique()
            col1.metric('Entregadores', entregadores)
        
        with col2:
            #st.write('teste2')
            df_aux = distance (df, fig=False)
            col2.metric('Distance Média', df_aux)
                           
        
        with col3:
            tempo_c_festival = np.round(df1.loc[(df1["Festival"] == "Yes", "Time_taken(min)")].mean(), 2)
            col3.metric ('Entrega Festival',  tempo_c_festival, help='Tempo Médio de Entrega quando não há Festival')
        
        with col4:
            std_c_festival = np.round(df1.loc[(df1["Festival"] == "Yes", "Time_taken(min)")].std(), 2)
            col4.metric ('Std C/ Festival',  std_c_festival,  help='Desvio Padrão quando há Festival')
        
        with col5:
            tempo_s_festival = np.round(df1.loc[(df1["Festival"] == "No", "Time_taken(min)")].mean(), 2)
            col5.metric ('Entreg S/ Festival',  tempo_s_festival, help='Tempo Médio de Entrega quando não há Festival')
        
        with col6:
            std_s_festival = np.round(df1.loc[(df1["Festival"] == "No", "Time_taken(min)")].std(), 2)
            col6.metric ('Std S/ Festival', std_s_festival, help='Desvio Padrão quando não há Festival')
    
    with st.container():
        st.markdown ("""---""")
        
        
        col1, col2 = st.columns (2)
        
        with col1:
            fig = avg_std_time_graph (df1)
            st.write('**Distribuição do Tempo por Cidade e o Desvio Padrão**')
            st.plotly_chart (fig)
            
        with col2:
            st.write ('**Tempo médio e o desvio padrão de entrega por cidade e tipo de pedido**')
        
            df_aux = (df1.loc[:, ['Time_taken(min)', 'City', 'Type_of_order']].groupby ( ['City', 'Type_of_order'] )
           .agg ( {'Time_taken(min)' : ['mean', 'std'] } ) )
        
            df_aux.columns = ['time_mean', 'time_std']
        
            df_aux = df_aux.reset_index()
        
            st.dataframe (df_aux, use_container_width=True, hide_index=True)
        
    with st.container():
        st.markdown ("""---""")
                
        col1, col2 = st.columns (2)
            
        with col1:
            st.write('**Tempo Médio de Entrega por Cidade**')
            fig = distance (df, fig=True)
            st.plotly_chart (fig)
            
        with col2:
            st.write ('**Distribuição do Tempo por Cidade, Tipo de Tráfego e Desvio Padrão**')
            fig = avg_std_time_on_traffic (df1)                                  
            st.plotly_chart(fig)
            
   