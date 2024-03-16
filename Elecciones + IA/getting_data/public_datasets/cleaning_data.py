import pandas as pd

# # Reviewing oficial data 
# See more in  https://www.argentina.gob.ar/dine/resultados-electorales
# To get the raw data visit the following link and download the file raw_data.zip:
# https://drive.google.com/file/d/1oTZ6d268UTRnBbipG00g9wvkI7eNi5h5/view?usp=sharing


def buildData(df):

    bigger_0 = df['votos_cantidad']>0
    president = df['cargo_nombre']=='PRESIDENTE'
    positive_vote = df['votos_tipo']=='POSITIVO'
    elections = df[(bigger_0) & (president) & (positive_vote)].loc[:,['agrupacion_nombre','votos_cantidad']]

    name_party = elections['agrupacion_nombre'].unique()
    total_votantes = elections['votos_cantidad'].sum()
    type_v = df['eleccion_tipo'].unique()[0]
    year = df['año'].unique()[0]

    number_votes = dict()
    for party in name_party:
        number_votes[f'{party}'] = 0
        number_votes[f'{party}']+=elections[elections['agrupacion_nombre']==party]['votos_cantidad'].sum()

            

    amoun_votes_df = pd.DataFrame.from_dict({'Nombre_partido':number_votes.keys(),'Cantidad_votos':number_votes.values()})
    amoun_votes_df.sort_values(by='Cantidad_votos',ascending=False,inplace=True)
    amoun_votes_df['total_votantes'] = total_votantes
    amoun_votes_df['tipo'] = type_v
    amoun_votes_df['anio'] = year
    

    amoun_votes_df.to_csv(f'Elecciones + IA/getting_data/public_datasets/datos_provisorios_{year}_{type_v}.csv',index=False)

def cleaning_data(dir):
    raw_data = pd.read_csv(dir)
    buildData(raw_data)

generales_2011 = 'Elecciones + IA/getting_data/public_datasets/raw_data/ResultadosElectorales_2011.csv'
paso_2011 = 'Elecciones + IA/getting_data/public_datasets/raw_data/ResultadosElectorales_2011_PASO.csv'

paso_2015 = 'Elecciones + IA/getting_data/public_datasets/raw_data/ResultadosElectorales_2015_PASO.csv'
generales_2015 = 'Elecciones + IA/getting_data/public_datasets/raw_data/ResultadosElectorales_2015.csv'
ballotaje_2015 = 'Elecciones + IA/getting_data/public_datasets/raw_data/ResultadosElectorales_2015_ballotage.csv'

# Every raw file has the same structure 

cleaning_data(generales_2011)
cleaning_data(paso_2011)
cleaning_data(paso_2015)
cleaning_data(generales_2015)
cleaning_data(ballotaje_2015)

# Files not used
'''
gral_2019 = 'Elecciones + IA/getting_data/public_datasets/raw_data/ResultadosElectorales_2019.xlsx'
df_2019 = pd.read_excel(gral_2019)
df_2019.dropna(how='all')

paso_2019 = 'Elecciones + IA/getting_data/public_datasets/raw_data/ResultadosElectorales_2019_PASO.xlsx'
df_paso_2019 = pd.read_excel(paso_2019)
df_paso_2019.dropna(how='all')
'''

