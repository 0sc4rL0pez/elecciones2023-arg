import instaloader
from datetime import datetime
from time import sleep
from funcionesV2 import guardar_info, guardar_iterador, obtener_directorio_actualizado,fecha_limite,path,canales,usuarios_unique,cambiaUsuario
import glob

def get_data(login_user, target_user,mode,dia_hasta):
    
    contador = 0
    MAX_ITER = 110
    dia = None
    #dia_actual = datetime.now()
    #dia_actual = datetime(2022,8,1)
    
    bot = instaloader.Instaloader()
    bot.load_session_from_file(login_user)
    dir_json = []

    if mode == 'OLD':
        dir_json =  glob.glob(f'{path}iteradoresV2/{target_user}*.json')
    elif mode == 'NEW':
        dir_json =  glob.glob(f'{path}iteradoresV2_new/{target_user}*.json')
    else:
        print('Modo incorrecto!')

    try:
        perfil = instaloader.Profile.from_username(bot.context, target_user)
        publicaciones = perfil.get_posts()
        
        if(len(dir_json)!=0): # abre el iterador actualizado
            nombre_json = obtener_directorio_actualizado(dir_json)
            #OJO CON ESTA FUNCION
            cambiaUsuario(login_user,nombre_json)
            publicaciones_aux = instaloader.load_structure_from_file(bot.context,nombre_json)
            publicaciones.thaw(publicaciones_aux)

        print('Sacando data de '+target_user+' a través de '+login_user+'\n Fecha: '+str(datetime.now()))
        for post in publicaciones:

            if(contador>=MAX_ITER or fecha_limite(dia,dia_hasta)):
                if (fecha_limite(dia,dia_hasta)):
                    print('Actualizado!')
                    bot.close()
                    #borrarIterador()
                print('Cerrando sesion')
                guardar_iterador(publicaciones, target_user,mode)
                bot.close()
                break
            else:
                if mode == 'OLD':
                    guardar_info(post)
                elif mode == 'NEW':
                    dia = guardar_info(post)
                contador +=1
                sleep(2)
                
        bot.close()
        if dia !=None:
            print("Ultima dia recopilado: " + str(dia))
            return dia
            
    except (instaloader.exceptions.AbortDownloadException):
        print('Ocurrio un error a las:  '+str(datetime.now()))
        try:
            guardar_iterador(publicaciones, target_user,mode)
        except UnboundLocalError:
            print('Nada que guardar')
        bot.close()
        sleep(3*60*60)
        
    




def sacar_Datos_pendientes(lista_pendientes,tiempo_espera_min,fecha_hasta, modo):
    
    sleep(tiempo_espera_min*60)

    dia_actual = datetime.now()
    dia_hasta = fecha_hasta
    

    wait = 20*60
    i = 0

    #lista_pendientes =['canal26','lanacioncom']


    recorrida = lista_pendientes*len(usuarios_unique)
    user_recorrida = usuarios_unique*len(lista_pendientes)

    while(True):
        if i<len(recorrida):
            usuario = user_recorrida[i]
            fuente = recorrida[i]
            get_data(usuario,fuente,mode=modo,dia_hasta=dia_hasta) 
            sleep(wait)
            i+=1
        else:
            i=0

hasta = datetime(2023,11,14)
sacar_Datos_pendientes(canales,0,hasta,'NEW')