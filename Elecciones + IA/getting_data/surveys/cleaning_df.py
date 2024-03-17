import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

parties = ['Union por la Patria','Juntos por el Cambio', 'La Libertad Avanza','Hacemos juntos nuestro Pais', 'Frente de Izquierda y Trabajadores']
primera_vuelta = pd.read_csv('Elecciones + IA/getting_data/surveys/data_scraped/Survey_primera_vuelta.csv')
ballotage = pd.read_csv('Elecciones + IA/getting_data/surveys/data_scraped/Survey_ballotage.csv')

#plotting need to be moved out!
# fig, ax = plt.subplots(3,2,figsize=(10,10))
# ploteos = ax.flatten()
# for i,p in enumerate(parties):
#     sns.histplot(df[p],bins=50, kde=True,ax= ploteos[i])


# otros = ['Otros', 'Blanco', 'Indecisos', 'Ventaja']
# fig, ax = plt.subplots(2,2,figsize=(7,7))
# ploteos = ax.flatten()
# for i,p in enumerate(otros):
#     sns.histplot(df[p],bins=50, kde=True,ax= ploteos[i])


#with_out_outliers = primera_vuelta[(primera_vuelta['Muestra']<30000) & (primera_vuelta['Muestra']>0)]['Muestra']

careless = primera_vuelta['Indecisos']+primera_vuelta['Blanco']


limit = careless.quantile(0.90)
primera_vuelta  = primera_vuelta.loc[careless<limit]


# Guardo solo las columas que me interesan
columnas = parties + ['Inicio', 'Final']
clean = primera_vuelta.loc[:,columnas]
clean.to_csv('C:/Users/54911/OneDrive/Escritorio/Data Science/Elecciones + IA/getting_data/encuestas/Encuestas_primera_vuelta.csv',
             index= False)

#ballotaje
ballotage = pd.read_csv('FILL')
ballotage.dropna(inplace=True)

otros = ['Blanco', 'Indecisos']

fig, ax = plt.subplots(1,2,figsize=(12,5))
ploteos = ax.flatten()
for i,p in enumerate(otros):
    sns.histplot(ballotage[p],bins=50, kde=True,ax= ploteos[i])


ballotage = ballotage[ballotage['Indecisos']<20]

labels = ['La Libertad Avanza','Union por la Patria','Inicio','Final']

ballotage = ballotage[labels]

