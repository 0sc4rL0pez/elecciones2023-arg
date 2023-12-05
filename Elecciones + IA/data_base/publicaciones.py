# Pasa de archivos .txt a la base de datos
# OBSOLETO

def abrir_archivo(archivo):
    data = []
    with open(archivo, 'r', encoding= 'utf-8') as f:
        data = f.readlines()
    return data

def txt_to_values(linea_publicacion):
        
    canal = linea_publicacion.split(', ')[-2].replace('\'','')
    cantidad_likes = int(linea_publicacion.split(', ')[-3])
    short_code = linea_publicacion.split(':')[0].split('{')[1].replace('\'','')
    fecha = linea_publicacion.split(', ')[-1].split(']')[0].replace('\'','')[:10]
    descripcion = ''.join(''.join(linea_publicacion.split(':')[1:]).split(', ')[0:-3]).replace('\\n',' ').replace('"','').replace("'",'').replace('[', '')
    
    return short_code, canal, cantidad_likes, fecha, descripcion


import glob 
import pyodbc

"""
Me conecto a la base de datos
"""
def conectar_base_datos():
    SERVER = 'ACHEPE'
    DATABASE = 'elecciones-IA-data'

    connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;'

    conn = pyodbc.connect(connectionString) 
    return conn

conn = conectar_base_datos()
cursor = conn.cursor()

directorios = glob.glob('data/*.txt')
contador = 0

for dir in directorios:
    data = abrir_archivo(dir)

    for linea in data:

        short_code, canal, cantidad_likes, fecha, descripcion = txt_to_values(linea)
        
        """
        Inserta cada valor a la base de datos
        """        
        SQL_STATEMENT = f"""
        INSERT Publicaciones
        VALUES ('{short_code}', '{canal}', {cantidad_likes}, '{fecha}', '{descripcion}')
        """
        cursor.execute(SQL_STATEMENT)
        conn.commit()

        #print(100*contador/(len(data)))
        contador+=1
        

        # data_df = {'ID':[],
        # 'Fuente':[],
        # 'Cantidad_Me_gusta':[],
        # 'Fecha':[],
        # 'Descripcion':[]}

        # data_df['Cantidad_Me_gusta'].append(cantidad_likes)
        # data_df['ID'].append(short_code)
        # data_df['Fecha'].append(fecha)
        # data_df['Fuente'].append(canal)
        # data_df['Descripcion'].append(descripcion)

    contador = 0
    #df = pd.DataFrame(data_df)
    #df.to_csv('datos_prueba.csv', index=False)

conn.close()
       






