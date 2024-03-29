import pandas as pd
import pyodbc
def conectar_base_datos():
    SERVER = 'ACHEPE'
    DATABASE = 'elecciones-IA-data'

    connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;'

    conn = pyodbc.connect(connectionString) 
    return conn

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

def separar_por_partido(lista_palabras):
    index_condition = []
    for pal in lista_palabras:
        index_condition.append(data['palabra_clave'] == pal)
    index = (index_condition[0])
    for idx in index_condition:
        index = index | (idx) 

    df = data[index]
    return df

def max_cant_likes(id:str,df:pd.DataFrame):
    # try:
    res = df[df['id'] == id]['cantidad_likes'].idxmax()
    return df.loc[[res]][['cantidad_likes','fecha','fuente']]
    # except ValueError:
    #     id_list.append(id)
    #     return None

def eliminar_repes(dataframe):
    dataframe_sin_repes_lista = []
    for i in dataframe['id'].unique():
        fila = max_cant_likes(i,dataframe)
        # if fila != None:
        dataframe_sin_repes_lista.append(fila)

    dataframe_sin_repes = pd.concat(dataframe_sin_repes_lista)
    return dataframe_sin_repes

consulta = """
            SELECT Publicaciones.id,palabra_clave,fuente,cantidad_likes,fecha
            FROM Publicaciones_politicas
            LEFT JOIN Publicaciones
            ON Publicaciones_politicas.id = Publicaciones.id
            """

data = pasar_a_DF(consultar(consulta))

palabras_politicas = ['MILEI', 'VILLARRUEL', 'LA LIBERTAD AVANZA','JAVIER GERARDO MILEI','VICTORIA VILLARRUEL',
                      'BULLRICH', 'PETRI', 'JUNTOS POR EL CAMBIO','PATRICIA BULLRICH','LUIS PETRI',
                      'MASSA', 'ROSSI', 'UNIÓN POR LA PATRIA','SERGIO TOMAS MASSA','AGUSTIN ROSSI',
                      'Bregman', 'del Caño', 'Frente de Izquierda y de Trabajadores','Myriam Bregman','Nicolás del Caño',
                      'Schiaretti', 'Randazzo', 'Hacemos juntos nuestro Pais','Juan Schiaretti', 'Florencio Randazzo']

LLA_con_repes = separar_por_partido(palabras_politicas[:5])
JXC_con_repes = separar_por_partido(palabras_politicas[5:10])
UP_con_repes = separar_por_partido(palabras_politicas[10:15])
FIT_con_repes = separar_por_partido(palabras_politicas[15:20])
HNP_con_repes = separar_por_partido(palabras_politicas[20:25])

LLA = eliminar_repes(LLA_con_repes)
UPLP = eliminar_repes(UP_con_repes)
JXPC = eliminar_repes(JXC_con_repes)
FDIZ = eliminar_repes(FIT_con_repes)
HNP = eliminar_repes(HNP_con_repes)

publicaciones_politicas = pd.concat([LLA,UPLP,JXPC,FDIZ,HNP])

publicaciones_politicas['Partido'] = '?'

publicaciones_politicas.loc[LLA.index,'Partido'] = 'La Libertad Avanza'
publicaciones_politicas.loc[UPLP.index,'Partido'] = 'Union por la Patria'
publicaciones_politicas.loc[JXPC.index,'Partido'] = 'Juntos por el Cambio'
publicaciones_politicas.loc[HNP.index,'Partido'] = 'Hacemos juntos nuestro Pais'
publicaciones_politicas.loc[FDIZ.index,'Partido'] = 'Frente de Izquierda y Trabajadores'

publicaciones_politicas.to_csv('C:/Users/54911/OneDrive/Escritorio/Data Science/Elecciones + IA/modeling/Preparando_datos/publicaciones_politicas.csv',index=False)