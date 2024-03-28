import pandas as pd
import numpy as np

primera_vuelta_clean = pd.read_csv('Elecciones + IA/getting_data/surveys/data_scraped/primera_vuelta_cleaned.csv')
ballotage_clean = pd.read_csv('Elecciones + IA/getting_data/surveys/data_scraped/ballotage_cleaned.csv')

parties_primera_vuelta = primera_vuelta_clean.columns[0:5]
parties_ballotage = ballotage_clean.columns[0:2]

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

normalize_df_primera_vuelta = buildNormDataFrame(primera_vuelta_clean,parties_primera_vuelta)
normalize_df_ballotage = buildNormDataFrame(ballotage_clean,parties_ballotage)

normalize_df_primera_vuelta.to_csv('Elecciones + IA/getting_data/surveys/data_scraped/normalize_primera_vuelta.csv',index= False)
normalize_df_ballotage.to_csv('Elecciones + IA/getting_data/surveys/data_scraped/normalize_ballotage.csv',index= False)
