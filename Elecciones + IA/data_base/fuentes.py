#Actualiza la tabla fuentes de la base de datos

from time import sleep
import pyodbc
import instaloader
from publicaciones import conectar_base_datos
import pandas as pd


canales = ['infobae', 'todonoticias', 'clarincom', 'lanacioncom', 'minutouno', 'filonewsok', 'diario.ole', 'tv_publica', 'pagina12', 'c5n', 'a24noticias', 'canal26', 'canal9oficial', 'cronicaweb', 'eldestapeweb']

bot = instaloader.Instaloader()
bot.load_session_from_file('oscar_ds.py')

def Consultar_fuente_recopilada(fuente):
        conn = conectar_base_datos()
        cursor = conn.cursor()
        result = 0
        SQL_STATEMENT = f"""
                SELECT COUNT(*) AS Cantidad
                FROM Publicaciones 
                WHERE fuente = '{fuente}'
                """
        records = cursor.execute(SQL_STATEMENT)

        for r in records:
                result = r.Cantidad
        conn.close()
        
        return result

info_canales = {'nombre':[],
                'cant_seguidores':[],
                'cant_publicaciones':[],
                'cant_recopilado':[]}

for canal in canales:
    try:
        perfil = instaloader.Profile.from_username(bot.context, canal)

        info_canales['cant_recopilado'].append(Consultar_fuente_recopilada(canal))
        info_canales['nombre'].append(canal)

        info_canales['cant_seguidores'].append(perfil.followers)
        info_canales['cant_publicaciones'].append(perfil.mediacount)
        
        print('Actualizando datos...')
        sleep(2)
    except instaloader.exceptions.AbortDownloadException:
        print('Ocurrio un error!')
        break

df = pd.DataFrame(info_canales)

conn = conectar_base_datos()
cursor = conn.cursor()

for index, row in df.iterrows():
    SQL_STATEMENT = f""" 
    UPDATE Fuentes 
    SET cant_recopilado = '{row.cant_recopilado}', cant_seguidores = '{row.cant_seguidores}', cant_publicaciones = '{row.cant_publicaciones}'
    WHERE [nombre] = '{row.nombre}' 
    """
        #    cant_seguidores = '{row.cant_seguidores}', cant_publicaciones = '{row.cant_publicaciones}', 

    print('Subiendo datos al server')
    cursor.execute(SQL_STATEMENT)
    conn.commit()

conn.close()
