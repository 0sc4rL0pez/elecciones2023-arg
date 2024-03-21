import pandas as pd
import matplotlib.pyplot as plt

import datetime
import numpy as np

def pasar_a_datetime(fecha):
    #format_string = '%Y-%m-%d'
    anio,mes,dia= fecha.split('-')
    aux_dia = dia.split(' ')
    if len(aux_dia)>1:dia = aux_dia[0]
    res = datetime.datetime(int(anio),int(mes),int(dia))
    return res

encuestas = pd.read_csv('C:/Users/54911/OneDrive/Escritorio/Data Science/Elecciones + IA/getting_data/encuestas/Encuestas_primera_vuelta.csv')
ballojate = pd.read_csv('C:/Users/54911/OneDrive/Escritorio/Data Science/Elecciones + IA/getting_data/encuestas/Encuestas_solo_ballotaje.csv')

ballojate['Inicio'] = ballojate['Inicio'].map(lambda x:pasar_a_datetime(x))
ballojate['Final'] = ballojate['Final'].map(lambda x:pasar_a_datetime(x))
encuestas['Inicio'] = encuestas['Inicio'].map(lambda x:pasar_a_datetime(x))
encuestas['Final'] = encuestas['Final'].map(lambda x:pasar_a_datetime(x))

ballojate.sort_values(by='Inicio',ascending=True,inplace=True)
ejex = np.arange(len(ballojate))
encuestas.sort_values(by='Inicio',ascending=True,inplace=True)
ejex = np.arange(len(encuestas))

partidos = ballojate.columns[:2]
partidos = encuestas.columns[:5]

# Elimino el dato de las elecciones oficiales

encuestas = encuestas.iloc[:-1,:]

ballojate = ballojate.iloc[:-1,:]

# Y si tomo las media para fechas repetidas?

encuestas.columns

ballojate.columns

ballotaje_median = ballojate.groupby(['Inicio','Final']).mean().reset_index()
encuestas_median= encuestas.groupby(['Inicio','Final']).mean().reset_index()

plt.figure(figsize=(15,6))
for p in partidos:
    plt.scatter(encuestas_median['Inicio'],encuestas_median[p],label = p,s=20)
#plt.legend(loc='upper right',bbox_to_anchor=(1.4, 0.5))
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),ncol=3)
plt.title('Encuestas (Wikipedia)')
plt.ylabel('Porcentaje')

cols_e = encuestas_median.columns.tolist()
cols_b = ballotaje_median.columns.tolist()

orden_cols_b = cols_b[2:]+cols_b[:2]
orden_cols_e = cols_e[2:]+cols_e[:2]

ballotaje_median = ballotaje_median[orden_cols_b]
encuestas_median = encuestas_median[orden_cols_e]

#encuestas_median.to_csv('C:/Users/54911/OneDrive/Escritorio/Data Science/Elecciones + IA/getting_data/encuestas/Encuestas_clean_median.csv',index=False)

# # Ajuste polinomial encuestas (median)

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# # Primera vuelta

grado =4
encuestas_polinomio_partidos = []

partidos

ejex = np.arange(len(encuestas_median))
plt.figure(figsize=(15,6))
for p in partidos:
    
    poly_reg_model = LinearRegression()
    poly = PolynomialFeatures(degree=grado, include_bias=False)
    poly_features = poly.fit_transform(ejex.reshape(-1, 1))

    y = encuestas_median[p].to_numpy()
    poly_reg_model.fit(poly_features, y)
    #X_=np.linspace(ejex.min(), ejex.max(), 200).reshape(-1, 1)
    Y_=poly_reg_model.predict(poly_features)

    encuestas_polinomio_partidos.append(Y_)

    plt.plot(ejex, Y_,label=p)
    plt.scatter(ejex,encuestas_median[p])

plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),ncol=5)
plt.title('Encuestas (Ajuste con polinomio de grado 3)')
plt.ylabel('Porcentaje')

for i,p in enumerate(partidos):
    encuestas_poly = encuestas_median
    encuestas_poly[p] = encuestas_polinomio_partidos[i]

plt.figure(figsize=(15,6))
ejex = np.arange(len(encuestas_median))
for p in partidos:
    plt.scatter(ejex,encuestas_poly[p],label = p,s=20)
#plt.legend(loc='upper right',bbox_to_anchor=(1.4, 0.5))
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),ncol=3)
plt.title('Encuestas (Wikipedia)')
plt.ylabel('Porcentaje')

encuestas_poly.to_csv('C:/Users/54911/OneDrive/Escritorio/Data Science/Elecciones + IA/getting_data/encuestas/Encuestas_primera_vuelta_poly.csv',index=False)

encuestas_poly.to_csv('C:/Users/54911/OneDrive/Escritorio/Data Science/Elecciones + IA/getting_data/encuestas/Encuestas_primera_vuelta_poly.csv',index=False)

# # Ballotaje

partidos = ballojate.columns[:2]

partidos

grado = 3
encuestas_polinomio_partidos = []

ejex = np.arange(len(ballotaje_median))
plt.figure(figsize=(15,6))
for p in partidos:
    
    poly_reg_model = LinearRegression()
    poly = PolynomialFeatures(degree=grado, include_bias=False)
    poly_features = poly.fit_transform(ejex.reshape(-1, 1))

    y = ballotaje_median[p].to_numpy()
    poly_reg_model.fit(poly_features, y)
    #X_=np.linspace(ejex.min(), ejex.max(), 200).reshape(-1, 1)
    Y_=poly_reg_model.predict(poly_features)

    encuestas_polinomio_partidos.append(Y_)

    plt.plot(ejex, Y_,label=p)
    plt.scatter(ejex,ballotaje_median[p])

plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),ncol=5)
plt.title('Encuestas (Ajuste con polinomio de grado 3)')
plt.ylabel('Porcentaje')

for i,p in enumerate(partidos):
    ballotaje_poly = ballotaje_median
    ballotaje_poly[p] = encuestas_polinomio_partidos[i]

plt.figure(figsize=(15,6))
ejex = np.arange(len(ballotaje_median))
for p in partidos:
    plt.scatter(ejex,ballotaje_poly[p],label = p,s=20)
#plt.legend(loc='upper right',bbox_to_anchor=(1.4, 0.5))
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),ncol=3)
plt.title('Encuestas (Wikipedia)')
plt.ylabel('Porcentaje')

ballotaje_poly.to_csv('C:/Users/54911/OneDrive/Escritorio/Data Science/Elecciones + IA/getting_data/encuestas/Encuestas_ballotaje_poly.csv',index=False)




