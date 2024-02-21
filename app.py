import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


etapas = ('Datos','Primera vuelta', 'Ballotage')
visualizacion = st.sidebar.selectbox('Visualizar: ',etapas)

st.header('**Elecciones + IA**')

if visualizacion==etapas[1]:
    st.subheader('Primera vuelta')
    st.text("Encuestas en función del tiempo (Wikipedia)")

    df = pd.read_csv('Elecciones + IA/dashboard/primera_vuelta_poly_encuestas.csv')

    df['Inicio'] = pd.to_datetime(df['Inicio'])
    df.rename(columns={'Inicio':'Fecha'},inplace=True)
    partidos = df.columns[2:7].to_list()

    colores = ['#137DCC','#CCCA27','#A71FCC','#180D73','#D12437']
    options = st.multiselect(
        'Partidos: ',partidos,
        default=partidos[:3],
        placeholder='Elije una opción')

    idx_colors = [partidos.index(x) for x in options]
    #st.scatter_chart(df,x='Fecha',y=options,color=list(np.array(colores,dtype=str)[idx_colors]),
    #                size=40,width=1200,height=350)
    
    para_concatenar = []
    lista_partidos = []
    df_aux = pd.DataFrame()
    for p in options:
        para_concatenar += df[p].values.tolist()
        lista_partidos += len(df)*[p]
    if len(para_concatenar)>0:
        df_aux['Porcentaje'] = para_concatenar
        df_aux['Partido'] = lista_partidos
        df_aux['Fecha'] = np.array(len(options)*df['Fecha'].values.tolist()).flatten()
        df_aux['Fecha'] = pd.to_datetime(df_aux['Fecha'])
        
    linea = alt.Chart(df_aux).mark_circle(size=40).encode(
        x='Fecha',
        y='Porcentaje',
        color = alt.Color('Partido').scale(domain=partidos, range=colores).legend(orient='bottom',columns = 3)
    ).properties(
            width=700,
            height=320
        )
    
    st.altair_chart(linea)
    st.subheader('Modelo predictivo')
    df_predicc = pd.read_csv('Elecciones + IA/dashboard/predicciones_score_df_prim.csv')
    agrupado = df_predicc.groupby(['Inicio']).mean(numeric_only=True)[partidos + ['Scores']].reset_index()
    fecha_selec = st.select_slider(
    'Predicho por el modelo',
    options=agrupado['Inicio'].values.tolist())

    df_fecha_selec = agrupado[agrupado['Inicio']==fecha_selec]
    st.text("Puntaje (-MSE): "+str(round(df_fecha_selec['Scores'].values[0],2)))
    df_fecha_selec = df_fecha_selec.rename(index={0:'Porcentaje'})
    st.bar_chart(df_fecha_selec[options].T,height=350,use_container_width=True)
    
    porcentajes = []
    for p in options:
        porcentajes.append(df_fecha_selec[p].values.tolist())
    aux_df = pd.DataFrame()
    aux_df['porcentajes'] = np.array(porcentajes).flatten()
    aux_df['partido'] = options
    #partido no esta definido como column
    pie = alt.Chart(aux_df).mark_arc(innerRadius=60,outerRadius=120).encode(
            theta=alt.Theta(field="porcentajes", type="quantitative",stack=True),
            color=alt.Color('partido').scale(domain=partidos, range=colores).legend(orient='top-right',columns = 1)
    )
    text = pie.mark_text(radius=150, size=15).encode(text="porcentaje")

    st.altair_chart(pie+text, theme=None, use_container_width=True)

elif visualizacion==etapas[2]:
    st.subheader('Ballotaje')
    st.text("Encuestas en función del tiempo (Wikipedia)")

    df = pd.read_csv('Elecciones + IA/getting_data/encuestas/Encuestas_solo_ballotaje.csv')

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
    df_predicc = pd.read_csv('Elecciones + IA/dashboard/predicciones_score_ballotaje.csv')
    agrupado = df_predicc.groupby(['Inicio']).mean(numeric_only=True)[partidos + ['Scores']].reset_index()
    fecha_selec = st.select_slider(
    'Predicho por el modelo',
    options=agrupado['Inicio'].values.tolist())

    #color=list(np.array(colores,dtype=str)[[4,3,1,2,0]]
    df_fecha_selec_aux = agrupado[agrupado['Inicio']==fecha_selec]
    st.text("Puntaje (-MSE): "+str(round(df_fecha_selec_aux['Scores'].values[0],2)))
    df_fecha_selec = df_fecha_selec_aux.rename(index={0:'Porcentaje'})
    st.bar_chart(df_fecha_selec[options].T,height=350,use_container_width=True)

elif visualizacion==etapas[0]:
    ################################# DATOS #######################################################

    df_megusta_pub_pol = pd.read_csv('Elecciones + IA/modeling/Preparando_datos/publicaciones_politicas.csv')
    partidos = df_megusta_pub_pol['Partido'].unique()
    fuentes = df_megusta_pub_pol['fuente'].unique()
    colores = ['#A71FCC','#137DCC','#CCCA27','#D12437','#180D73']

    options_fuente = st.multiselect(
        'Fuentes: ',fuentes,
        default=['infobae','lanacioncom', 'pagina12', 'c5n','filonewsok'],
        placeholder='Elije una opción'
        )

    st.header('Publicaciones')
    st.text('(Los datos fueron recopilados entre diciembre 2021 y noviembre 2023)')

    df_recopilado = pd.read_csv('Elecciones + IA/data_base/data_base_csv/Fuentes.csv')
    df_recopilado.sort_values(by='cant_publicaciones',inplace=True)

    para_concatenar = []
    for p in options_fuente:
        para_concatenar.append(df_recopilado[df_recopilado['nombre']==p])
    if len(para_concatenar)>0:
        df_recopilado = pd.concat(para_concatenar)

    aux = pd.concat([df_recopilado[['nombre','cant_publicaciones']],df_recopilado.rename(columns=dict(zip(df_recopilado.columns,['a','nombre','c','d','cant_publicaciones'])))[['nombre','cant_publicaciones']]],axis=0)
    aux['Clase'] = len(df_recopilado)*['Publicaciones totales'] + len(df_recopilado)*['Cantidad descargada']

    bar = alt.Chart(aux).mark_bar().encode(
        alt.X('Clase').axis(labels=False,title=' '),
        alt.Y('cant_publicaciones',type = 'quantitative').axis(title=' '),
        alt.Column('nombre',type='nominal',title='Fuente'),
        alt.Color('Clase',type = 'nominal').legend(orient='bottom',title=' '),
        ).properties(
            width=50,
            height=200
        )
    
    st.altair_chart(bar,use_container_width=False)

    st.header('Publicaciones políticas')

    politicasYNormales = pd.read_csv('Elecciones + IA/data_base/data_base_csv/politicasYnormales.csv')

    para_concatenar = []
    for p in options_fuente:
        para_concatenar.append(politicasYNormales[politicasYNormales['Fuente']==p])
    if len(para_concatenar)>0:
        politicasYNormales = pd.concat(para_concatenar)

    bar = alt.Chart(politicasYNormales).mark_bar().encode(
        alt.X('Fuente').axis(labels=False,title=' '),
        alt.Y('Cantidad',type = 'quantitative').axis(title=' '),
        alt.Column('Tipo',type='nominal'),
        alt.Color('Fuente',type = 'nominal').legend(orient='right',title=' '),
        ).properties(
            width=230,
            height=300
        )

    st.altair_chart(bar,use_container_width=False)

    partidosYFuentes = pd.read_csv('Elecciones + IA/data_base/data_base_csv/partidosYfuentes.csv')

    st.subheader('Fuentes y publicaciones políticas')

    para_concatenar = []
    for p in options_fuente:
        para_concatenar.append(partidosYFuentes[partidosYFuentes['fuente']==p])
    if len(para_concatenar)>0:
        partidosYFuentes = pd.concat(para_concatenar)

    bar = alt.Chart(partidosYFuentes).mark_bar().encode(
        alt.X('Partido').axis(labels=False,title=' '),
        alt.Y('Cantidad',type = 'quantitative').axis(title=' '),
        alt.Column('fuente',type='nominal'),
        alt.Color('Partido',type = 'nominal').scale(domain=partidos, range=colores).legend(orient='bottom',title=' ',columns=3),
        ).properties(
            width=70,
            height=220
        )

    st.altair_chart(bar,use_container_width=False)

    st.header   ("Publicaciones y partidos políticos")

    options_partidos = st.multiselect(
        'Partido: ',partidos,
        default=partidos[:3],
        placeholder='Elije una opción'
        )
    
    st.subheader("Cantidad de publicaciones")
    unidades1 = st.radio(
        "Unidades",
        ["Porcentaje", "miles"]
        )

    para_concatenar = []
    for p in options_partidos:
        para_concatenar.append(df_megusta_pub_pol[df_megusta_pub_pol['Partido']==p])

    if len(para_concatenar)>0:
        df_megusta_pub_pol = pd.concat(para_concatenar)
        
    df_cant_publi = df_megusta_pub_pol['Partido'].value_counts(ascending=True).reset_index()
    df_megusta = df_megusta_pub_pol.groupby('Partido').sum()['cantidad_likes'].reset_index()
    sum_cant_pub = df_cant_publi[df_cant_publi.columns[1]].sum()
    sum_cant_likes = df_megusta['cantidad_likes'].sum()

    if unidades1=='Porcentaje':
        df_cant_publi['cantidad'] = df_cant_publi[df_cant_publi.columns[1]].map(lambda x: round(100*float(x)/sum_cant_pub,1))
    elif unidades1 == 'miles':
        df_cant_publi['cantidad'] = df_cant_publi[df_cant_publi.columns[1]].map(lambda x: round(float(x)/1000,1))
    
    pie = alt.Chart(df_cant_publi).mark_arc(innerRadius=60,outerRadius=120).encode(
        theta=alt.Theta(field="cantidad", type="quantitative",stack=True),
        color=alt.Color('Partido').scale(domain=partidos, range=colores).legend(orient='top-right',columns = 1)
    )
    text = pie.mark_text(radius=150, size=15).encode(text="cantidad")
    
    st.altair_chart(pie+text, theme=None, use_container_width=True)

    st.subheader("Likes")
    unidades2 = st.radio(
        "Unidades",
        ["Porcentaje", "millones"]
    )
    if unidades2=='Porcentaje':
        df_megusta['cantidad'] = df_megusta['cantidad_likes'].map(lambda x: round(100*float(x)/sum_cant_likes,1))
    elif unidades2 == 'millones':
        df_megusta['cantidad'] = df_megusta['cantidad_likes'].map(lambda x: round(float(x)/1000000,1))
    
    pie = alt.Chart(df_megusta).mark_arc(innerRadius=60,outerRadius=120).encode(
        theta=alt.Theta(field="cantidad_likes", type="quantitative",stack=True),
        color=alt.Color('Partido').scale(domain=partidos, range=colores).legend(orient='top-right',columns = 1)
    )
    text = pie.mark_text(radius=150, size=15).encode(text="cantidad")

    st.altair_chart(pie+text, theme=None, use_container_width=True)


