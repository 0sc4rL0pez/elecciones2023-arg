import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# # Cobertura de las encuestas

partidos = ['Union por la Patria','Juntos por el Cambio', 'La Libertad Avanza','Hacemos juntos nuestro Pais', 'Frente de Izquierda y Trabajadores']
df = pd.read_csv('FILL')

fig, ax = plt.subplots(3,2,figsize=(10,10))
ploteos = ax.flatten()
for i,p in enumerate(partidos):
    sns.histplot(df[p],bins=50, kde=True,ax= ploteos[i])


otros = ['Otros', 'Blanco', 'Indecisos', 'Ventaja']
fig, ax = plt.subplots(2,2,figsize=(7,7))
ploteos = ax.flatten()
for i,p in enumerate(otros):
    sns.histplot(df[p],bins=50, kde=True,ax= ploteos[i])


sin_outliers = df[(df['Muestra']<30000) & (df['Muestra']>0)]['Muestra']
sns.histplot(sin_outliers,bins=50, kde=True)


tibios = df['Indecisos']+df['Blanco']
sns.histplot(tibios,bins=50, kde=True)


tibios.quantile(0.90)


# Filtremos los tibios con la cobertura del 90% de los datos


df  = df.loc[tibios<22]


# IDEA  :Dejar los valores de las encuestas en una sola columna, hay que eliminar aquellos que son '-' (DESCARTADO)


# Guardo solo las columas que me interesan
columnas = partidos + ['Inicio', 'Final']
clean = df.loc[:,columnas]
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

labelss = ['La Libertad Avanza','Union por la Patria','Inicio','Final']

ballotage = ballotage[labelss]

