
import instaloader
import os
from functions_data_base import add_data_base,add_data_base_comentarios
import json

path = 'Elecciones + IA/getting_data/instagram/main/'
#### AUXILIARS FUNCTIONS####
def formatCaption(text):
    res = ''
    try:
        res = text.replace('\\n',' ').replace('"','').replace("'",'').replace('[', '')
    except AttributeError:
        print('Empty caption')
        return res
    return res

def guardar_info(post):
    try:
        caption = formatCaption(post.caption)
        user=post.owner_username
        likes = post.likes
        date = post.date
        id=post.shortcode
        comments = post.comments
        #agregar_base_datos_comentarios(id,comments)
        add_data_base(id,user,likes,date,caption)
        return date
        
    except TypeError:
        print('Type Error!')

def guardar_iterador(structure, target_user,mode):
    freezed = structure.freeze()
    if mode == 'OLD':
        name = path + 'iterators/'+target_user+'_Iterador_congelado.json'
    else : name = path + 'iterators_new/'+target_user+'_Iterador_congelado.json'
    instaloader.save_structure_to_file(freezed,name)

def getUpdatedDIR(lista_dir):
    return max(lista_dir, key=os.path.getctime)

def hasPassed(date, till_date):
    if date == None:
        res = False
    else:
        #aux = date_actual-date
        if (date > till_date):
            res = False
        else:
            res = True
    return res

def changeName(user,direct):
    jsonFile = open(direct, "r") 
    data = json.load(jsonFile) 
    jsonFile.close()

    data['node']['context_username'] = user

    jsonFile = open(direct, "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()


#               Usernames of new's accounts
usuarios_unique = ['', '','']
sources = ['infobae', 'todonoticias', 'clarincom', 'lanacioncom','minutouno', 'diario.ole', 'pagina12', 'c5n', 'a24noticias', 'canal26', 'canal9oficial','cronicaweb','eldestapeweb','tv_publica','filonewsok']

# print(len(canales),len(user_ordenado))
#print(canales.index('cronicaweb'))
