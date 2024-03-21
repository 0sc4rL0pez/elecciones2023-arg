import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

parties = ['Union por la Patria','Juntos por el Cambio', 'La Libertad Avanza','Hacemos juntos nuestro Pais', 'Frente de Izquierda y Trabajadores']
primera_vuelta = pd.read_csv('Elecciones + IA/getting_data/surveys/data_scraped/Survey_primera_vuelta.csv')
ballotage = pd.read_csv('Elecciones + IA/getting_data/surveys/data_scraped/Survey_ballotage.csv')

#Check the analysis in : Elecciones + IA\analisis_exploratorio\surveys_plots.ipynb

#cleaning

careless = primera_vuelta['Indecisos']+primera_vuelta['Blanco']

# Saving only the columns that matters
columnas = parties + ['Inicio', 'Final']
clean = primera_vuelta.loc[:,columnas]
clean.to_csv('C:/Users/54911/OneDrive/Escritorio/Data Science/Elecciones + IA/getting_data/encuestas/Encuestas_primera_vuelta.csv',
             index= False)

ballotage = pd.read_csv('FILL')
ballotage.dropna(inplace=True)

otros = ['Blanco', 'Indecisos']




ballotage = ballotage[ballotage['Indecisos']<20]

labels = ['La Libertad Avanza','Union por la Patria','Inicio','Final']

ballotage = ballotage[labels]

