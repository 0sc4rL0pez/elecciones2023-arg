import streamlit as st
# import matplotlib.plotly.figure_factory as ff
import pandas as pd
import numpy as np
from datetime import date,datetime
import plotly.express as px


etapas = ('Primera vuelta', 'Ballotage', 'Datos')
visualizacion = st.sidebar.selectbox('Visualizar: ',etapas)

st.header('**Elecciones + IA**')

if visualizacion==etapas[0]:
    st.subheader('Primera vuelta')
    st.text("Encuestas en función del tiempo (Wikipedia)")

    df = pd.read_csv('elecciones2023-arg/Elecciones + IA/dashboard/primera_vuelta_poly_encuestas.csv')

    df['Inicio'] = pd.to_datetime(df['Inicio'])
    df.rename(columns={'Inicio':'Fecha'},inplace=True)
    partidos = df.columns[2:7].to_list()

    colores = ['#137DCC','#CCCA27','#A71FCC','#180D73','#D12437']
    options = st.multiselect(
        'Partidos: ',partidos,
        default=partidos[:3],
        placeholder='Elije una opción')

    idx_colors = [partidos.index(x) for x in options]
    st.scatter_chart(df,x='Fecha',y=options,color=list(np.array(colores,dtype=str)[idx_colors]),
                    size=40,width=1200,height=350)
    
    st.subheader('Modelo predictivo')
    df_predicc = pd.read_csv('elecciones2023-arg/Elecciones + IA/dashboard/predicciones_score_df_prim.csv')
    agrupado = df_predicc.groupby(['Inicio']).mean()[partidos + ['Scores']].reset_index()
    fecha_selec = st.select_slider(
    'Predicho por el modelo',
    options=agrupado['Inicio'].values.tolist())

    #color=list(np.array(colores,dtype=str)[[4,3,1,2,0]]
    df_fecha_selec = agrupado[agrupado['Inicio']==fecha_selec]
    st.text("Puntaje (-MSE): "+str(round(df_fecha_selec['Scores'].values[0],2)))
    df_fecha_selec.rename(index={0:'Porcentaje'},inplace=True)
    st.bar_chart(df_fecha_selec[options].T,height=350,use_container_width=True)

elif visualizacion==etapas[1]:
    st.subheader('Ballotaje')
    st.text("Encuestas en función del tiempo (Wikipedia)")

    df = pd.read_csv('elecciones2023-arg/Elecciones + IA/getting_data/encuestas/Encuestas_solo_ballotaje.csv')

    df['Inicio'] = pd.to_datetime(df['Inicio'])
    df.rename(columns={'Inicio':'Fecha'},inplace=True)
    partidos = df.columns[:2].to_list()

    colores = ['#A71FCC','#137DCC']
    options = st.multiselect(
        'Partidos: ',partidos,
        default=partidos[:2],
        placeholder='Elije una opción')

    idx_colors = [partidos.index(x) for x in options]
    st.scatter_chart(df,x='Fecha',y=options,color=list(np.array(colores,dtype=str)[idx_colors]),
                    size=50,width=1200,height=350)
    
    st.subheader('Modelo predictivo')
    df_predicc = pd.read_csv('elecciones2023-arg/Elecciones + IA/dashboard/predicciones_score_ballotaje.csv')
    agrupado = df_predicc.groupby(['Inicio']).mean()[partidos + ['Scores']].reset_index()
    fecha_selec = st.select_slider(
    'Predicho por el modelo',
    options=agrupado['Inicio'].values.tolist())

    #color=list(np.array(colores,dtype=str)[[4,3,1,2,0]]
    df_fecha_selec = agrupado[agrupado['Inicio']==fecha_selec]
    st.text("Puntaje (-MSE): "+str(round(df_fecha_selec['Scores'].values[0],2)))
    df_fecha_selec.rename(index={0:'Porcentaje'},inplace=True)
    st.bar_chart(df_fecha_selec[options].T,height=350,use_container_width=True)

elif visualizacion==etapas[2]:
    st.subheader('Cantidad recolectado')
    df_recopilado = pd.read_csv('elecciones2023-arg/Elecciones + IA/data_base/data_base_csv/Fuentes.csv')
    df_recopilado.sort_values(by='cant_publicaciones',inplace=True)
    df_recopilado.rename(columns={'nombre':'Fuente','cant_publicaciones':'Publicaciones totales','cant_recopilado':'Publicaciones descargadas'},inplace=True)
    st.bar_chart(df_recopilado,x ='Fuente',y=['Publicaciones totales','Publicaciones descargadas'],height=350,use_container_width=True)

    st.subheader('Publicaciones y me gusta')
    
    st.text("Cantidad de publicaciones")
    df_megusta_pub_pol = pd.read_csv('elecciones2023-arg/Elecciones + IA/modeling/Preparando_datos/publicaciones_politicas.csv')
    partidos = df_megusta_pub_pol['Partido'].unique()
    df_cant_publi = df_megusta_pub_pol['Partido'].value_counts(ascending=True)
    st.bar_chart(df_cant_publi)

    st.text("Likes por partido")
    df_megusta = df_megusta_pub_pol.groupby('Partido').sum()['cantidad_likes']
    st.bar_chart(df_megusta)




# radio widget to take inputs from mulitple options
# partido_elegido = st.radio(
#     "Partido: ",
#     partidos)

# if partido_elegido == 'Comedy':
#     st.write('You selected comedy.')
# else:
#     st.write("You didn't select comedy.")
