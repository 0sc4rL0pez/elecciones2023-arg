#Info de elecciones pasadas, recoletada de https://www.argentina.gob.ar/dine/resultados-electorales

# 2011

total_2011_paso = 22705378
total_2011_gral= 22956385
paso = 'P.A.S.O'
general = 'Generales'
seguna = 'Segunda Vuelta'
#Frente popular??

# 2015
total_2015_paso = 24021816
total_2015_gral= 26048446
total_2015_snd= 25935243

# 2019
total_2019_paso =  25859967 
total_2019_gral=  27529896 
"""

id_partido = [0,2,0,2,1,4,3,5,4,3,5,3,4,6,7,8,6,7,8]
etapa = [paso,paso,general,general,general,paso,paso,paso,general,general,general,seguna, seguna,
         paso,paso,paso,general,general,general]
cantidad_votos=[10762217,2614211,11865055,2443016,3684970,8720573,6791278,4639405,9338490,8601131,5386977,12988349,12309575, 12205085, 7948256,  2081293,12946037,10811586,1649322]
total_votantes = [total_2011_paso,total_2011_paso,total_2011_gral,total_2011_gral,total_2011_gral,
                  total_2015_paso,total_2015_paso,total_2015_paso,total_2015_gral,total_2015_gral,total_2015_gral,total_2015_snd,total_2015_snd,
                  total_2019_paso,total_2019_paso,total_2019_paso,total_2019_gral,total_2019_gral,total_2019_gral]

"""
from publicaciones import conectar_base_datos
import pandas as pd

conn = conectar_base_datos()
cursor = conn.cursor()
"""
####################################### ELECCIONES ############################################


ELECCIONES = {'id':id_partido,'etapa':etapa, 'cantidad_votos':cantidad_votos, 'total_votantes':total_votantes}



df = pd.DataFrame(ELECCIONES)


"""
paso_2023 = 'C:/Users/54911/OneDrive/Escritorio/Data Science/Elecciones + IA/data_base/2023_PASO/datos_provisorios_PASO_2023.csv'
df = pd.read_csv(paso_2023).iloc[:5]
total_2023_paso = 22539543
ids_2023_paso = [9,10,11,12,13]

i = 0
for index, row in df.iterrows():

    SQL_STATEMENT = f"""
    INSERT Resultados_Eleccion
    VALUES ({ids_2023_paso[i]}, '{paso}', {row.Cantidad_votos},{total_2023_paso})
    """
    cursor.execute(SQL_STATEMENT)
    conn.commit()
    i+=1

conn.close()

