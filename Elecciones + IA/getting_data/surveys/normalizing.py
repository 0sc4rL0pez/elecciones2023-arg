import pandas as pd
import numpy as np

def normalizePercentage(values_array):
    total = sum(values_array)
    res = 100*values_array/total
    return np.round(res,2)

def buildNormDataFrame(data,columns):
    norm_values_primera_vuelta = np.zeros((len(data),len(columns)))
    for i in range(len(data)):
        values = data[columns].iloc[i].to_numpy()
        norm_values_primera_vuelta[i] = normalizePercentage(values)

    normalize_df = pd.DataFrame(data=norm_values_primera_vuelta,columns=columns)
    normalize_df['Inicio'] = data['Inicio']
    normalize_df['Final'] = data['Final']

    return normalize_df

# Normalizing poly adjustment

primera_vuelta_poly = pd.read_csv('Elecciones + IA/modeling/polynomial_surveys/data_built/polynomial_primera_vuelta.csv')
ballotage_poly = pd.read_csv('Elecciones + IA/modeling/polynomial_surveys/data_built/polynomial_ballotage.csv')

parties_primera_vuelta = primera_vuelta_poly.columns[0:5]
parties_ballotage = ballotage_poly.columns[0:2]
normalize_df_primera_vuelta_poly = buildNormDataFrame(primera_vuelta_poly,parties_primera_vuelta)
normalize_df_ballotage_poly = buildNormDataFrame(ballotage_poly,parties_ballotage)

normalize_df_primera_vuelta_poly.to_csv('Elecciones + IA/modeling/polynomial_surveys/data_built/normalize_primera_vuelta_poly.csv',index= False)
normalize_df_ballotage_poly.to_csv('Elecciones + IA/modeling/polynomial_surveys/data_built/normalize_ballotage_poly.csv',index= False)
