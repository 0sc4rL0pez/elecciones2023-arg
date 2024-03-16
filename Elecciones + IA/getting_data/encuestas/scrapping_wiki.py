
# Wikipedia's surveys
# Doing some web scrapping from https://es.wikipedia.org/wiki/Anexo:Encuestas_de_intenci%C3%B3n_de_voto_para_las_elecciones_presidenciales_de_Argentina_de_2023

from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
import seaborn as sns


dicc_month_ES = {
    'enero': "01",
    'febrero': "02",
    'marzo': "03",
    'abril': "04",
    'mayo': "05",
    'junio': "06",
    'julio': "07",
    'agosto': "08",
    'septiembre': "09",
    'octubre': "10",
    'noviembre': "11",
    'diciembre': "12"
    }

def startDate(string_date):
    year = 2023
    splited_ = string_date.split('-')
    raw_date =  splited_[0].split(' ')

    if len(raw_date)<=2:
        day = int(raw_date[0])
        aux_splited = splited_[1].split(' ')
        if len(aux_splited)==6:
            aux_splited = aux_splited[1:]
        if len(aux_splited)==5:
            month = int(dicc_month_ES[aux_splited[2].lower()])
            year  = int(aux_splited[4])
    elif len(raw_date)==3:
        day = 1
        month = int(dicc_month_ES[raw_date[0].lower()])
        year = int(raw_date[2])
    elif len(raw_date)==4:
        day = int(raw_date[0])
        month = int(dicc_month_ES[raw_date[2].lower()])
    elif len(raw_date)==5:
        day = int(raw_date[0])
        month = int(dicc_month_ES[raw_date[2].lower()])
        try:
            year = int(raw_date[4])
        except:
            pass 
    elif len(raw_date)==6:
        day = int(raw_date[0])
        month = int(dicc_month_ES[raw_date[2].lower()])
        year = int(raw_date[4])

    return datetime.datetime(year,month,day)  

def endDate(strr):
    splited_ = strr.split('-')
    
    if len(splited_)==1:
        res =  startDate(splited_[0])
    elif len(splited_)==2:
        aux =  splited_[1].split(' ')
        if len(aux)==6 or aux[0]=='':
            aux = aux[1:]
        if len(aux)==5:
            day = int(aux[0])
            month = int(dicc_month_ES[aux[2].lower()])
            year  = int(aux[4])
        if len(aux)==4:
            day = int(aux[0])
            month = int(dicc_month_ES[aux[1].lower()])
            year  = int(aux[3])
        
        res = datetime.datetime(year,month,day)  
    
    return res


def getDataFrame(table,header):
    pages_rows = table.find_all('tr')
    rows = []

    for i,row in enumerate(pages_rows):
        row_list = []
        columns = row.find_all('td')

        for column in columns:
            row_list.append(column.text.strip())
        
        if len(row_list)==(len(header)-3):
            #If the list has 3 element less than the header, the same missing information as the last row is added
            aux = rows[-1]
            rows.append(aux[:3]+row_list)
        elif len(row_list)==len(header):
            # If the lenght matches, the data is saved
            rows.append(row_list)
        else:
            # Different cases are not added to avoid errors in DataFrame construction
            pass

    aux_dicc = dict()
    for atributo in header:
        aux_dicc[atributo] = []

    for row in rows:
        for k,celda in enumerate(row):
            aux_dicc[header[k]].append(celda)

    df = pd.DataFrame(aux_dicc)

    #return df
    #Pasamos las fechas al tipo datetime.datetime
    df['Inicio'] = ''
    df['Final'] = ''
    df['Inicio'] = df['Fecha'].map(lambda x:startDate(x))
    df['Final'] = df['Fecha'].map(lambda x:endDate(x))

    # Pasemos los valores a float
    numericos = df.columns[2:len(header)]
    df[numericos] = df[numericos].replace('-',0)
    for atr in numericos:
        aux = df[atr].map(lambda x: str(x).replace('.',''))
        aux = aux.map(lambda x: str(x).replace(',','.'))
        df[atr] = pd.to_numeric(aux)
        
    return df


URL = "https://es.wikipedia.org/wiki/Anexo:Encuestas_de_intenci%C3%B3n_de_voto_para_las_elecciones_presidenciales_de_Argentina_de_2023"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

header = [
        'Fecha',
        'Encuestadora',
        'Muestra',
        'Union por la Patria',
        'Juntos por el Cambio', 
        'La Libertad Avanza',
        'Hacemos juntos nuestro Pais', 
        'Frente de Izquierda y Trabajadores',
        'Otros',
        'Blanco',
        'Indecisos',
        'Ventaja'
        ]

table = soup.find('table',class_ = "wikitable")

primera_vuelta = getDataFrame(table,header)

primera_vuelta.to_csv('Elecciones + IA/getting_data/encuestas/Encuestas_primera_vuelta_160324.csv')

URL = "https://es.wikipedia.org/wiki/Anexo:Encuestas_de_intenci%C3%B3n_de_voto_para_las_elecciones_presidenciales_de_Argentina_de_2023#Tras_la_primera_vuelta"
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

t = soup.find_all('table')[6]
header = ['Fecha', 'Encuestadora','Muestra','La Libertad Avanza', 'Union por la Patria','Blanco','Indecisos','Ventaja']

ballotage= getDataFrame(t,header)

ballotage.to_csv('Elecciones + IA/getting_data/encuestas/Encuestas_ballotage_160324.csv')


# Some plots
partidos = ['Union por la Patria','Juntos por el Cambio', 'La Libertad Avanza','Hacemos juntos nuestro Pais', 'Frente de Izquierda y Trabajadores']
colores = ['b','y','purple','black','r']
plt.figure(figsize=(15,7))
for i,p in enumerate(partidos):
    sns.scatterplot(data=primera_vuelta,y=p,x='Final', 
                    #ax=ploteos[i],
                    color=colores[i])



colores = ['b','y','purple','black','r']
plt.figure(figsize=(15,7))
for i,p in enumerate(partidos):
    sns.scatterplot(data=primera_vuelta,y=p,x='Inicio', 
                    #ax=ploteos[i],
                    color=colores[i])






