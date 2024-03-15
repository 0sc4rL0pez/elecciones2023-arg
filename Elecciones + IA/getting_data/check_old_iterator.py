import instaloader
import pandas as pd
import glob
import os
import json
from time import sleep
import datetime

path = 'C:/Users/54911/OneDrive/Escritorio/Data Science/Elecciones + IA/getting_data/instagram/main/iteradoresV2/iteradores_viejos'

bot = instaloader.Instaloader()
usuario = ''
bot.load_session_from_file(usuario)

def cambiarNombre(user,direct):
    jsonFile = open(direct, "r") # Open the JSON file for reading
    data = json.load(jsonFile) # Read the JSON into the buffer
    jsonFile.close() # Close the JSON file
    
    ## Working with buffered content
    data['node']['context_username'] = user

    ## Save our changes to JSON file
    jsonFile = open(direct, "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()

path = 'C:/Users/54911/OneDrive/Escritorio/Data Science/Elecciones + IA/getting_data/instagram/main/iteradoresV2_new/*'

dirs = glob.glob(path)

def RevisarNombre(direct):
    jsonFile = open(direct, "r") 
    data = json.load(jsonFile) 
    jsonFile.close() 
    
    res  = data['node']['context_username'] 
    return res   

def descongelar_fecha(directorio,usuario,canal):
    bot = instaloader.Instaloader()
    bot.load_session_from_file(usuario)
    perfil = instaloader.Profile.from_username(bot.context,canal)
    try:
        publicaciones = perfil.get_posts()
        publicaciones_aux = instaloader.load_structure_from_file(bot.context,directorio)
        publicaciones.thaw(publicaciones_aux)
        for post in publicaciones:
            dia = post.date
            break
        return dia
    except Exception as e:
        print(e)

dias = []
fuentes = []

for d in dirs:
    canal = d.split('\\')[-1].split('_I')[0]
    user = RevisarNombre(d)
    dia = descongelar_fecha(d,user,canal)
    dias.append(dia)
    sleep(2)
    fuentes.append(canal)

df = pd.DataFrame({'fuentes':fuentes, 'Ultima_fecha':dias})

df.sort_values(by='Ultima_fecha')
pendientes = df[df['Ultima_fecha']>datetime.datetime(2023,10,6)]['fuentes'].values.tolist()

print(pendientes)