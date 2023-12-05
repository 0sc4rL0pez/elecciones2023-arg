import instaloader
#from datetime import datetime, timedelta
from time import sleep
from funcionesV1 import canales, leer_txt, guardar_info, ahora, guardar_iterador
import glob


def get_data(login_user, target_user, wait):
    sleep(wait) 

    contador = 0
    MAX_ITER = 200
    
    bot = instaloader.Instaloader()
    bot.load_session_from_file(login_user)

    dir_json =  glob.glob(f'iteradores_actualizados/{target_user}.txt')

    try:
        perfil = instaloader.Profile.from_username(bot.context, target_user)
        publicaciones = perfil.get_posts()
        
        if(len(dir_json)!=0): # abre el iterador actualizado
            nombre_json = leer_txt(dir_json[0])
            publicaciones_aux = instaloader.load_structure_from_file(bot.context,nombre_json)
            publicaciones.thaw(publicaciones_aux)

        for post in publicaciones:
            if(contador>=MAX_ITER):
                print('Esperando que se resetee el contador...'+str(ahora()))

                guardar_iterador(publicaciones, target_user)
                bot.close()
                sleep(3600)
                bot.load_session_from_file(login_user)
                contador = 0

            contador = guardar_info(post,contador)
            sleep(1)
            
    except (instaloader.exceptions.AbortDownloadException,KeyboardInterrupt,instaloader.exceptions.ConnectionException):
        contador += 1
        guardar_iterador(publicaciones, target_user)
        print('Ocurrio un error a las:  '+ahora() +'\n'+
            'total_index: '+str(publicaciones.total_index))
        
        bot.close()

from threading import Thread

def usuario1():
    get_data('oscar_ds.py', canales[-1], 0)

def usuario2():
    get_data('oscar_pkong', canales[-2], 20*60)

def usuario3():
    get_data('oscarrcitolopez', canales[-3], 40*60)

if __name__ == '__main__':
    Thread(target = usuario1).start()
    Thread(target = usuario2).start()
    Thread(target = usuario3).start()