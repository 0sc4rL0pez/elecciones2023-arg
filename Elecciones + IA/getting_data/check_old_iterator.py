import instaloader
import pandas as pd
import glob
import os
import json
from time import sleep
import datetime

# Code to check data from multiple json files using the method post.thaw() from instaloader
# Not usefull right now

def changeNameJSON(user,direct):
    # Modify in place
    json_file = open(direct, "r") # Open the JSON file for reading
    data = json.load(json_file) # Read the JSON into the buffer
    json_file.close() # Close the JSON file
    
    ## Working with buffered content
    data['node']['context_username'] = user

    ## Save our changes to JSON file
    json_file = open(direct, "w+")
    json_file.write(json.dumps(data))
    json_file.close()


def checkName(direct):
    jsonFile = open(direct, "r") 
    data = json.load(jsonFile) 
    jsonFile.close() 
    
    res  = data['node']['context_username'] 
    return res   

def unFreezeDate(directorio,usuario,canal):
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

# fill with your username
bot = instaloader.Instaloader()
username = ''
bot.load_session_from_file(username)

#fill with path with old iterators
path = ''

dirs = glob.glob(path)

days = []
Source = []

for d in dirs:
    canal = d.split('\\')[-1].split('_I')[0]
    user = checkName(d)
    date = unFreezeDate(d,user,canal)
    days.append(date)
    sleep(2)
    Source.append(canal)

df = pd.DataFrame({'Source':Source, 'Last_date':days})

df.sort_values(by='Last_date')
pendientes = df[df['Last_date']>datetime.datetime(2023,10,6)]['Source'].values.tolist()

print(pendientes)