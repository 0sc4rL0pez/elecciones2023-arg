import pyodbc
import pandas as pd
from  datetime import datetime
def conectar_base_datos():
    SERVER = 'ACHEPE'
    DATABASE = 'elecciones-IA-data'

    connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;'

    conn = pyodbc.connect(connectionString) 
    return conn

def pasar_a_datetime(fecha):
    #format_string = '%Y-%m-%d'
    anio,mes,dia= fecha.split('-')
    aux_dia = dia.split(' ')
    if len(aux_dia)>1:dia = aux_dia[0]
    res = datetime(int(anio),int(mes),int(dia))
    return res

def consultar(sql_statement):
    conn = conectar_base_datos()
    cursor = conn.cursor()
    SQL_STATEMENT = f"""
        {sql_statement}
    """
    consulta = cursor.execute(SQL_STATEMENT) 
    return consulta 

def pasar_a_DF(dat_cursor):
    columnas = dat_cursor.description
    nombre = []
    datos = []

    for i in range(len(columnas)):
        nombre.append(columnas[i][0])
        datos.append([])

    for fila in dat_cursor:
        for i in range(len(columnas)):
            datos[i].append(fila[i])
    
    diccionario = dict()
    for i in range(len(columnas)):
        diccionario[nombre[i]] = datos[i]

    df = pd.DataFrame(diccionario)

    return df


'''
SQL_STATEMENT = f"""
       SELECT *
       FROM Publicaciones
"""
data = consultar(SQL_STATEMENT)
df_publicaciones = pasar_a_DF(data)
'''