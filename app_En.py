import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

etapas = ('Data','First phase', 'Second phase')
visualizacion = st.sidebar.selectbox('Visualize: ',etapas)

st.header('**Elections + IA**')

if visualizacion==etapas[1]:
    st.subheader('First phase')
    st.text("Surveys through  time (Wikipedia)")

    df = pd.read_csv('Elecciones + IA/getting_data/surveys/data_scraped/primera_vuelta_cleaned.csv')

    df['Inicio'] = pd.to_datetime(df['Inicio'])
    df.rename(columns={'Inicio':'Fecha'},inplace=True)
    partidos = df.columns[2:7].to_list()

    colores = ['#137DCC','#CCCA27','#A71FCC','#180D73','#D12437']
    options = st.multiselect(
        'Political party: ',partidos,
        default=partidos[:3])
    
    para_concatenar = []
    lista_partidos = []
    df_aux = pd.DataFrame()
    for p in options:
        para_concatenar += df[p].values.tolist()
        lista_partidos += len(df)*[p]

    if len(para_concatenar)>0:
        df_aux['Percentage'] = para_concatenar
        df_aux['Party'] = lista_partidos
        df_aux['Date'] = np.array(len(options)*df['Fecha'].values.tolist()).flatten()
        
        df_aux['Date'] = pd.to_datetime(df_aux['Date'],utc=True).dt.tz_convert(tz='America/Argentina/Buenos_Aires')
        
        linea = alt.Chart(df_aux).mark_circle(size=40).encode(
            x='Date',
            y='Percentage',
            color = alt.Color('Party').scale(domain=partidos, range=colores).legend(
                orient='bottom',columns = 3,labelFontSize=12,symbolSize=120
            )
        ).properties(
                width=700,
                height=320
            )
        
        st.altair_chart(linea)
        st.subheader('Machine learning model')
        st.text('Doing some changes...')
    '''df_predicc = pd.read_csv('Elecciones + IA/dashboard/predicciones_score_df_prim.csv')
    agrupado = df_predicc.groupby(['Inicio']).mean(numeric_only=True)[partidos + ['Scores']].reset_index()
    if len(options)>0:
        fecha_selec = st.select_slider(
        'Input date',
        options=agrupado['Inicio'].values.tolist())

        df_fecha_selec = agrupado[agrupado['Inicio']==fecha_selec]
        st.text("Score (-MSE): "+str(round(df_fecha_selec['Scores'].values[0],2))+" *")
        df_fecha_selec = df_fecha_selec.rename(index={0:'Porcentaje'})
    
    porcentajes = []
    for p in options:
        porcentajes.append(df_fecha_selec[p].values.tolist())
    aux_df = pd.DataFrame()
    aux_df['Percentage'] = np.round(np.array(porcentajes).flatten())
    aux_df['Party'] = options
    if len(options)>0:
        pie = alt.Chart(aux_df).mark_arc(innerRadius=60,outerRadius=120).encode(
                theta=alt.Theta(field="Percentage", type="quantitative",stack=True),
                color=alt.Color('Party').scale(domain=partidos, range=colores).legend(orient='top-right',columns = 1)
        )
        text = pie.mark_text(radius=150, size=15).encode(text="Percentage")
    
        st.altair_chart(pie+text, theme=None, use_container_width=True)
    st.caption("*MSE: Mean squared error")'''
elif visualizacion==etapas[2]:
    st.subheader('Second phase')
    st.text("Surveys through  time (Wikipedia)")

    df = pd.read_csv('Elecciones + IA/getting_data/surveys/data_scraped/ballotage_cleaned.csv')

    df['Inicio'] = pd.to_datetime(df['Inicio'])
    df.rename(columns={'Inicio':'Fecha'},inplace=True)
    partidos = df.columns[:2].to_list()

    colores = ['#A71FCC','#137DCC']
    options = st.multiselect(
        'Party: ',partidos,
        default=partidos[:2])

    para_concatenar = []
    lista_partidos = []
    df_aux = pd.DataFrame()
    for p in options:
        para_concatenar += df[p].values.tolist()
        lista_partidos += len(df)*[p]
    if len(para_concatenar)>0:
        df_aux['Percentage'] = para_concatenar
        df_aux['Party'] = lista_partidos
        df_aux['Fecha'] = np.array(len(options)*df['Fecha'].values.tolist()).flatten()
        df_aux['Date'] = pd.to_datetime(df_aux['Fecha'])
        
        linea = alt.Chart(df_aux).mark_circle(size=40).encode(
            x='Date',
            y='Percentage',
            color = alt.Color('Party').scale(domain=partidos, range=colores).legend(
                orient='bottom',columns = 3,labelFontSize=12,symbolSize=120
            )
        ).properties(
                width=700,
                height=320
            )
        
        st.altair_chart(linea)
    
        st.subheader('Machine learning model')
        st.text('Doing some changes...')
    
    
    '''df_predicc = pd.read_csv('Elecciones + IA/dashboard/predicciones_score_ballotaje.csv')
    agrupado = df_predicc.groupby(['Inicio']).mean(numeric_only=True)[partidos + ['Scores']].reset_index()
    if len(options)>0:
        fecha_selec = st.select_slider(
        'Input date',
        options=agrupado['Inicio'].values.tolist())

        df_fecha_selec_aux = agrupado[agrupado['Inicio']==fecha_selec]
        st.text("Puntaje (-MSE): "+str(round(df_fecha_selec_aux['Scores'].values[0],2))+" *")
        df_fecha_selec = df_fecha_selec_aux.rename(index={0:'Porcentaje'})

    porcentajes = []
    for p in options:
        porcentajes.append(df_fecha_selec[p].values.tolist())
    aux_df = pd.DataFrame()
    aux_df['Percentage'] = np.round(np.array(porcentajes).flatten(),2)
    aux_df['Party'] = options
    if len(options)>0:
        pie = alt.Chart(aux_df).mark_arc(innerRadius=60,outerRadius=120).encode(
                theta=alt.Theta(field="Percentage", type="quantitative",stack=True),
                color=alt.Color('Party').scale(domain=partidos, range=colores).legend(orient='top-right',columns = 1)
        )
        text = pie.mark_text(radius=150, size=15).encode(text="Percentage")
    
        st.altair_chart(pie+text, theme=None, use_container_width=True)
    st.caption("*MSE: Mean squared error")'''

elif visualizacion==etapas[0]:
    ################################# DATOS #######################################################

    df_megusta_pub_pol = pd.read_csv('Elecciones + IA/modeling/Preparando_datos/publicaciones_politicas.csv')
    partidos = df_megusta_pub_pol['Partido'].unique()
    fuentes = df_megusta_pub_pol['fuente'].unique()
    colores = ['#A71FCC','#137DCC','#CCCA27','#D12437','#180D73']

    options_fuente = st.multiselect(
        'Source: ',fuentes,
        default=['infobae','lanacioncom', 'pagina12', 'c5n','filonewsok']
        )

    st.header('Posts')
    st.text('(The data has been scraped between december 2021 and november 2023)')

    df_recopilado = pd.read_csv('Elecciones + IA/data_base/data_base_csv/Fuentes.csv')
    df_recopilado.sort_values(by='cant_publicaciones',inplace=True)

    para_concatenar = []
    for p in options_fuente:
        para_concatenar.append(df_recopilado[df_recopilado['nombre']==p])
    if len(para_concatenar)>0:
        df_recopilado = pd.concat(para_concatenar)

    aux = pd.concat([df_recopilado[['nombre','cant_publicaciones']],df_recopilado.rename(columns=dict(zip(df_recopilado.columns,['a','nombre','c','d','cant_publicaciones'])))[['nombre','cant_publicaciones']]],axis=0)
    aux['Type'] = len(df_recopilado)*['Total posts'] + len(df_recopilado)*['Amount downloaded']

    bar = alt.Chart(aux).mark_bar().encode(
        alt.X('Type').axis(labels=False,title=' '),
        alt.Y('cant_publicaciones',type = 'quantitative').axis(title=' '),
        alt.Column('nombre',type='nominal',title='Source'),
        alt.Color('Type',type = 'nominal').legend(orient='bottom',title=' '),
        ).properties(
            width=50,
            height=200
        )
    
    st.altair_chart(bar,use_container_width=False)

    st.header('Political posts*')

    politicasYNormales = pd.read_csv('Elecciones + IA/data_base/data_base_csv/politicasYnormales_EN.csv')
    politicasYNormales = politicasYNormales.rename(columns={'Tipo':'Type', 'Fuente':'Source'})
    para_concatenar = []
    for p in options_fuente:
        para_concatenar.append(politicasYNormales[politicasYNormales['Source']==p])
    if len(para_concatenar)>0:
        politicasYNormales = pd.concat(para_concatenar)

    bar = alt.Chart(politicasYNormales).mark_bar().encode(
        alt.X('Source').axis(labels=False,title=' '),
        alt.Y('Cantidad',type = 'quantitative').axis(title=' '),
        alt.Column('Type',type='nominal'),
        alt.Color('Source',type = 'nominal').legend(orient='right',title=' '),
        ).properties(
            width=230,
            height=300
        )

    st.altair_chart(bar,use_container_width=False)

    partidosYFuentes = pd.read_csv('Elecciones + IA/data_base/data_base_csv/partidosYfuentes.csv')
    st.caption("*A post is political if in its caption there is at least one last name or full name of any candidate or the name of the party in question")
    st.subheader('Sources and political posts')

    para_concatenar = []
    for p in options_fuente:
        para_concatenar.append(partidosYFuentes[partidosYFuentes['fuente']==p])
    if len(para_concatenar)>0:
        partidosYFuentes = pd.concat(para_concatenar)
    
    partidosYFuentes = partidosYFuentes.rename(columns={'Partido':'Party', 'fuente':'Source'})
    bar = alt.Chart(partidosYFuentes).mark_bar().encode(
        alt.X('Party').axis(labels=False,title=' '),
        alt.Y('Cantidad',type = 'quantitative').axis(title=' '),
        alt.Column('Source',type='nominal'),
        alt.Color('Party',type = 'nominal').scale(domain=partidos, range=colores).legend(orient='bottom',title=' ',columns=3),
        ).properties(
            width=70,
            height=220
        )

    st.altair_chart(bar,use_container_width=False)

    st.header("Posts and political post")

    options_partidos = st.multiselect(
        'Party: ',partidos,
        default=partidos[:3]
        )
    
    st.subheader("Total posts")
    unidades1 = st.radio(
        "Unit of measurement",
        ["Percentage", "Thousands"]
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

    if unidades1=='Percentage':
        df_cant_publi['cantidad'] = df_cant_publi[df_cant_publi.columns[1]].map(lambda x: round(100*float(x)/sum_cant_pub,1))
    elif unidades1 == 'thousands':
        df_cant_publi['cantidad'] = df_cant_publi[df_cant_publi.columns[1]].map(lambda x: round(float(x)/1000,1))
    
    pie = alt.Chart(df_cant_publi).mark_arc(innerRadius=60,outerRadius=120).encode(
        theta=alt.Theta(field="cantidad", type="quantitative",stack=True),
        color=alt.Color('Partido').scale(domain=partidos, range=colores).legend(orient='top-right',columns = 1,title='Party')
    )
    text = pie.mark_text(radius=150, size=15).encode(text="cantidad")
    
    st.altair_chart(pie+text, theme=None, use_container_width=True)

    st.subheader("Likes")
    unidades2 = st.radio(
        "Unit of measurement",
        ["Percentage", "Millions"]
    )
    if unidades2=='Percentage':
        df_megusta['cantidad'] = df_megusta['cantidad_likes'].map(lambda x: round(100*float(x)/sum_cant_likes,1))
    elif unidades2 == 'millions':
        df_megusta['cantidad'] = df_megusta['cantidad_likes'].map(lambda x: round(float(x)/1000000,1))
    
    pie = alt.Chart(df_megusta).mark_arc(innerRadius=60,outerRadius=120).encode(
        theta=alt.Theta(field="cantidad_likes", type="quantitative",stack=True),
        color=alt.Color('Partido').scale(domain=partidos, range=colores).legend(orient='top-right',columns = 1,title='Party')
    )
    text = pie.mark_text(radius=150, size=15).encode(text="cantidad")

    st.altair_chart(pie+text, theme=None, use_container_width=True)
    


