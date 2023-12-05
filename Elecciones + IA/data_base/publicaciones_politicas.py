#   Actualiza la tabla publicaciones_politicas de la base de datos


#           Librerias utilizadas
import pyodbc
import pandas as pd

#           Conectando a la base de datos
def conectar_base_datos():
    SERVER = 'ACHEPE'
    DATABASE = 'elecciones-IA-data'

    connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;'

    conn = pyodbc.connect(connectionString) 
    return conn

conn = conectar_base_datos()
cursor = conn.cursor()

#           Realizo la consulta de los datos de los Partidos del 2019 y 2023
SQL_STATEMENT = """
       SELECT partido, Nombres, Apellidos
       FROM Candidatos
       JOIN Partidos
       ON Candidatos.id = Partidos.id
       WHERE anio = 2023
"""
consulta = cursor.execute(SQL_STATEMENT) 

#           Guardo los datos en DataFrame
partidos = []
Nombres = []
Apellidos = []
for filas in consulta:
    partidos.append(filas.partido)
    Nombres.append(filas.Nombres)
    Apellidos.append(filas.Apellidos)
df = pd.DataFrame({'Partido':partidos, 'Nombres':Nombres, 'Apellidos':Apellidos})

#           Acomodo el dataframe
df['Nombre_completo'] = df['Nombres']+' '+ df['Apellidos'] 
Nombre_completo = df['Nombre_completo'].values.tolist()
df['Partido'] = df['Partido'].map(lambda x: 'UNIÓN POR LA PATRIA' if x == 'UNION POR LA PATRIA' else x)
partidos = df['Partido'].unique().tolist()
#           Funciones auxiliares
def buscarPalabra(palabra):
    conn = conectar_base_datos()
    cursor = conn.cursor()
    SQL_STATEMENT = f"""
    SELECT id, cantidad_likes
    FROM Publicaciones
    WHERE CHARINDEX('{palabra}',descripcion)>0
    -- AND YEAR(fecha)>2021 AND MONTH(fecha)>10
    """
    results = cursor.execute(SQL_STATEMENT)
    
    return results

def agregarPublicacionesPoliticas(id, likes,palabra_clave):
    conn = conectar_base_datos()
    cursor = conn.cursor()
    SQL_STATEMENT = f"""
    INSERT Publicaciones_politicas
    VALUES ('{id}','{palabra_clave}','{likes}')
    """
    cursor.execute(SQL_STATEMENT)
    conn.commit()


#               Agrego las publicaciones politicas en las que coincide algun dato en la descripcion
politica = Apellidos+partidos+Nombre_completo

#print(politica)

for frase in politica:
    data = buscarPalabra(frase)
    print(frase)
    for i,fila in enumerate(data):
        agregarPublicacionesPoliticas(fila.id, fila.cantidad_likes,frase)
    print('Cantidad_publicaciones: '+str(i))

print("Ya termino!")


    