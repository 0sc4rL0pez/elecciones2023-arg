
import instaloader
import os
from publicacionesV2 import agregar_base_datos,agregar_base_datos_comentarios
import json

#path = 'getting_data/instagram/main/'
path = ''
#### FUNCIONES AUXILIARES ####
def formatear_Caption(texto):
    res = ''
    try:
        res = texto.replace('\\n',' ').replace('"','').replace("'",'').replace('[', '')
    except AttributeError:
        print('Descripcion vacia')
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
        agregar_base_datos(id,usuario,likes,dia,descripcion)
        return dia
        
    except TypeError:
        print('Error de tipo!')

def guardar_iterador(estructura, target_user,mode):
    congelado = estructura.freeze()
    if mode == 'OLD':
        nombre = path + 'iteradoresV2/'+target_user+'_Iterador_congelado.json'
    else : nombre = path + 'iteradoresV2_new/'+target_user+'_Iterador_congelado.json'
    instaloader.save_structure_to_file(congelado,nombre)

def obtener_directorio_actualizado(lista_dir):
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

def cambiaUsuario(user,direct):
    jsonFile = open(direct, "r") 
    data = json.load(jsonFile) 
    jsonFile.close()

    data['node']['context_username'] = user

    jsonFile = open(direct, "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()


#               USUARIOS DE CANALES DE NOTICIAS
usuarios_unique = ['oscar_pkong', 'oscar_ds.py','oscarrcitolopez.py']
canales = ['infobae', 'todonoticias', 'clarincom', 'lanacioncom','minutouno', 'diario.ole', 'pagina12', 'c5n', 'a24noticias', 'canal26', 'canal9oficial','cronicaweb','eldestapeweb','tv_publica','filonewsok']

# print(len(canales),len(user_ordenado))
#print(canales.index('cronicaweb'))
