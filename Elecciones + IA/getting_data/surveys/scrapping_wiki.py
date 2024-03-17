
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
    '''
    It extracts the initial date and cast it to datetime type
    It only works with this type of date string date
    However I think this can be generalized
    '''

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
    '''
    Same of starDate() but with the end date, 
    This function calls starDate() so be carefull
    In the future i will add test cases for this function
    '''

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

    '''
    Returns a dataframe given and htlm table object and headers,
    It only works with this case,
    But again, it think this can be generalized
    Note: Need to be tested!
    '''
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
    for atributte in header:
        aux_dicc[atributte] = []

    for row in rows:
        for k,celd in enumerate(row):
            aux_dicc[header[k]].append(celd)

    df = pd.DataFrame(aux_dicc)

    #Cast the string date to datetime
    df['Inicio'] = ''
    df['Final'] = ''
    df['Inicio'] = df['Fecha'].map(lambda x:startDate(x))
    df['Final'] = df['Fecha'].map(lambda x:endDate(x))

    # Cast surveys values to float
    numerics_type = df.columns[2:len(header)]
    df[numerics_type] = df[numerics_type].replace('-',0)
    for attr in numerics_type:
        formated = df[attr].map(lambda x: str(x).replace('.',''))
        formated = formated.map(lambda x: str(x).replace(',','.'))
        df[attr] = pd.to_numeric(formated)
        
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

primera_vuelta.to_csv('Elecciones + IA/getting_data/surveys/data_scraped/Survey_primera_vuelta.csv')

URL = "https://es.wikipedia.org/wiki/Anexo:Encuestas_de_intenci%C3%B3n_de_voto_para_las_elecciones_presidenciales_de_Argentina_de_2023#Tras_la_primera_vuelta"
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

t = soup.find_all('table')[6]
header = ['Fecha', 'Encuestadora','Muestra','La Libertad Avanza', 'Union por la Patria','Blanco','Indecisos','Ventaja']

ballotage= getDataFrame(t,header)

ballotage.to_csv('Elecciones + IA/getting_data/surveys/data_scraped/Survey_ballotage.csv')


# Some plots (move it to exploratory analisis)
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






