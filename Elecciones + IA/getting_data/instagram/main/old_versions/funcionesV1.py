import lzma
import json
from datetime import datetime
import instaloader


#### FUNCIONES AUXILIARES ####
def descomprimir_jsonXZ(directorio):

    '''Funcion para descomprimir los archivos del tipo .json.xz'''
    
    with lzma.open(directorio,'r') as f:
                    json_bytes = f.read()
                    stri = json_bytes.decode('utf-8')
                    data = json.loads(stri)
    return data

def devolver_shortCode(dirs):
    directorio_json = dirs.split('.')[0] + ".json.xz"
    datos = descomprimir_jsonXZ(directorio_json)
    return datos['node']['shortcode']

def buscar_Palabra (palabra,directorios):
    ids_posts = []
    aparece_en = []
    cantidad = 0
    for dir_caption in directorios:
        with open(dir_caption,encoding="utf8") as f:
            for line in f:
                if palabra in line:
                    cantidad+=1
                    #ids_posts.append(devolver_shortCode(dir_caption))
                    aparece_en.append(dir_caption)
                    break
    
    return set(aparece_en)

def guardar_info(post,contador):
    try:
        descripcion =post.caption
        usuario=post.owner_username
        likes = post.likes
        dia = post.date.strftime("%Y-%m-%d %H-%M-%S")
        id=post.shortcode
        publicaciones = {id:[descripcion,likes,usuario,dia]}
        nombre = 'data/'+str(usuario)+'_'+str(dia)[:4]+'_info_recolectada.txt'
        with open(nombre,'a',encoding='utf-8') as f:
            f.write(str(publicaciones)+','+'\n')
        return contador + 1
    except TypeError:
        print('Error de tipo!')

    #nombre = str(post.date) +post.owner_username +'.json'
    # instaloader.save_structure_to_file(post,nombre)

def guardar_iterador(estructura, target_user):
    congelado = estructura.freeze()
    nombre = 'iteradores/'+target_user+str(ahora())+'_Iterador_congelado.json'
    instaloader.save_structure_to_file(congelado,nombre)
    guardar_nombre(nombre,target_user)
     

def guardar_nombre(nombre, target_user):
    with open('iteradores_actualizados/' +f'{target_user}.txt','w',encoding='utf-8') as f:
        f.write(nombre)

def leer_txt(dir):
    with open(dir,'r',encoding='utf-8') as f:
        texto = f.read()
    return texto

def ahora():
    return datetime.now().strftime("%Y-%m-%d %H-%M-%S") 
# def esPolitico(descripcion):
#     razon = []
#     for palabra in descripcion:
#         if (palabra in palabras_politicas) or (palabra in apellidos_influyentes):
#             razon.append(palabra)
    
#     if (len(razon) == 0):
#         return (False,razon)
#     else :
#         return (True,razon)


#               USUARIOS DE CANALES DE NOTICIAS
Canales_de_noticias_instagram = {
    'infobae' : 'infobae',
    'TN' : 'todonoticias',
    'Clarin' : 'clarincom',
    'La_nacion' : 'lanacioncom',
    'Minuto_uno' : 'minutouno',
    'Filonews' : 'filonewsok',
    'Ole' : 'diario.ole',
    'TVpublica' : 'tv_publica',
    'Pagina12' : 'pagina12',
    'C5N' : 'c5n',
    'A24' : 'a24noticias',
    'Canal26' : 'canal26',
    'Canal9' : 'canal9oficial'
}
canales = list(Canales_de_noticias_instagram.values())