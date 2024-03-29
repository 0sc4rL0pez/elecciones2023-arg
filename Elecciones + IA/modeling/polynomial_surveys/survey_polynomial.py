import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import pandas as pd
from datetime import datetime

def stringToDatetime(fecha):
    #format_string = '%Y-%m-%d'
    anio,mes,dia= fecha.split('-')
    aux_dia = dia.split(' ')
    if len(aux_dia)>1:dia = aux_dia[0]
    res = datetime(int(anio),int(mes),int(dia))
    return res

def trainPolyModel(data,party,degree):
    axis_x = np.arange(len(data))    
    poly_reg_model = LinearRegression()
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    poly_features = poly.fit_transform(axis_x.reshape(-1, 1))
    y = data[party].to_numpy()
    poly_reg_model.fit(poly_features, y)
    Y_=poly_reg_model.predict(poly_features)

    return np.round(Y_,3)

def buildDataPoly(data,columns,degrees):
    adjusted_values = np.zeros((len(data),len(columns)))
    for i,party in enumerate(columns):
        adjusted = trainPolyModel(data,party,degrees[i])
        adjusted_values[:,i] = adjusted
    poly_data_frame = pd.DataFrame(data=adjusted_values,columns=columns)
    poly_data_frame['Inicio'] = data['Inicio']
    poly_data_frame['Final'] = data['Final']
    return poly_data_frame


# Check the optimization plots in plotting.ipynb
primera_vuelta = pd.read_csv('Elecciones + IA/getting_data/surveys/data_scraped/primera_vuelta_cleaned.csv')
ballotage = pd.read_csv('Elecciones + IA/getting_data/surveys/data_scraped/ballotage_cleaned.csv')

parties_primera_vuelta = primera_vuelta.columns[0:5]
parties_ballotage = ballotage.columns[0:2]

primera_vuelta['Inicio'] = primera_vuelta['Inicio'].map(lambda x:stringToDatetime(x))
primera_vuelta['Final'] = primera_vuelta['Final'].map(lambda x:stringToDatetime(x))
ballotage['Inicio'] = ballotage['Inicio'].map(lambda x:stringToDatetime(x))
ballotage['Final'] = ballotage['Final'].map(lambda x:stringToDatetime(x))

primera_vuelta_clean_grouped = primera_vuelta.groupby(by=['Inicio','Final'])[parties_primera_vuelta].mean().reset_index()
ballojate_clean_grouped = ballotage.groupby(by=['Inicio','Final'])[parties_ballotage].mean().reset_index()

degrees_primera_vuelta = [6,8,8,2,2]
degrees_ballotage = [4,3]

polynomial_primera_vuelta = buildDataPoly(primera_vuelta_clean_grouped,parties_primera_vuelta,degrees_primera_vuelta)
polynomial_ballotage = buildDataPoly(ballojate_clean_grouped,parties_ballotage,degrees_ballotage)

polynomial_primera_vuelta.to_csv('Elecciones + IA/modeling/polynomial_surveys/data_built/polynomial_primera_vuelta.csv',index= False)
polynomial_ballotage.to_csv('Elecciones + IA/modeling/polynomial_surveys/data_built/polynomial_ballotage.csv',index= False)



