
import instaloader
import os
from functions_data_base import add_data_base,add_data_base_comentarios
import json

path = 'Elecciones + IA/getting_data/instagram/main/'
#### AUXILIARS FUNCTIONS####
def formatear_Caption(texto):
    res = ''
    try:
        res = texto.replace('\\n',' ').replace('"','').replace("'",'').replace('[', '')
    except AttributeError:
        print('Empty caption')
        return res
    return res

def guardar_info(post):
    try:
        descripcion = formatear_Caption(post.caption)
        usuario=post.owner_username
        likes = post.likes
        dia = post.date
        id=post.shortcode
        comentarios = post.comments
        #agregar_base_datos_comentarios(id,comentarios)
        add_data_base(id,usuario,likes,dia,descripcion)
        return dia
        
    except TypeError:
        print('Type Error!')

def guardar_iterador(estructura, target_user,mode):
    congelado = estructura.freeze()
    if mode == 'OLD':
        nombre = path + 'iterators/'+target_user+'_Iterador_congelado.json'
    else : nombre = path + 'iterators_new/'+target_user+'_Iterador_congelado.json'
    instaloader.save_structure_to_file(congelado,nombre)

def getUpdatedDIR(lista_dir):
    return max(lista_dir, key=os.path.getctime)

def fecha_limite(dia, dia_hasta):
    if dia == None:
        res = False
    else:
        #aux = dia_actual-dia
        if (dia > dia_hasta):
            res = False
        else:
            res = True
    return res

def cambiarUsuarioJSON(directorio, user):
    jsonFile = open(directorio, "r") 
    data = json.load(jsonFile) 
    jsonFile.close() 
    
    data['node']['context_username'] = user

    jsonFile = open(directorio, "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()

def changeName(user,direct):
    jsonFile = open(direct, "r") 
    data = json.load(jsonFile) 
    jsonFile.close()

    data['node']['context_username'] = user

    jsonFile = open(direct, "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()


#               USUARIOS DE CANALES DE NOTICIAS
usuarios_unique = ['', '','']
sources = ['infobae', 'todonoticias', 'clarincom', 'lanacioncom','minutouno', 'diario.ole', 'pagina12', 'c5n', 'a24noticias', 'canal26', 'canal9oficial','cronicaweb','eldestapeweb','tv_publica','filonewsok']

# print(len(canales),len(user_ordenado))
#print(canales.index('cronicaweb'))
