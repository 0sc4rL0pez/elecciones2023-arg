import instaloader
from datetime import datetime
from time import sleep
from functions_main import guardar_info, guardar_iterador, getUpdatedDIR,hasPassed,path,sources,usuarios_unique,changeName
import glob

def get_data(login_user, target_user,mode,till_date):
    
    counter = 0
    MAX_ITER = 110
    date = None
    #date_actual = datetime.now()
    #date = datetime(2022,8,1)
    
    bot = instaloader.Instaloader()
    bot.load_session_from_file(login_user)
    dir_json = []

    if mode == 'OLD':
        dir_json =  glob.glob(f'{path}iterators/{target_user}*.json')
    elif mode == 'NEW':
        dir_json =  glob.glob(f'{path}iterators_new/{target_user}*.json')
    else:
        print('Wrong mode!')

    try:
        perfil = instaloader.Profile.from_username(bot.context, target_user)
        posts = perfil.get_posts()
        
        if(len(dir_json)!=0): # Opens updated iterator
            nombre_json = getUpdatedDIR(dir_json)

            #Be carefull with with this function!
            changeName(login_user,nombre_json)

            post_aux = instaloader.load_structure_from_file(bot.context,nombre_json)
            posts.thaw(post_aux)

        print('Getting data from '+target_user+' with '+login_user+'\n Date: '+str(datetime.now()))
        for post in posts:

            if(counter>=MAX_ITER or hasPassed(date,till_date)):
                if (hasPassed(date,till_date)):
                    print('Actualizado!')
                    bot.close()
                    #borrarIterador()
                print('Cerrando sesion')
                guardar_iterador(posts, target_user,mode)
                bot.close()
                break
            else:
                if mode == 'OLD':
                    guardar_info(post)
                elif mode == 'NEW':
                    date = guardar_info(post)
                counter +=1
                sleep(2)
                
        bot.close()
        if date !=None:
            print("Last date downloaded: " + str(date))
            return date
            
    except (instaloader.exceptions.AbortDownloadException):
        print('An error has occurred at :  '+str(datetime.now()))
        try:
            guardar_iterador(posts, target_user,mode)
        except UnboundLocalError:
            print('There is nothing to save')
        bot.close()
        sleep(3*60*60)
        

def getDueData(due_sources_list,wait_time_minutes,till_date, mode):
    
    sleep(wait_time_minutes*60)

    #dia_actual = datetime.now()
    
    wait = 20*60
    i = 0
    #This loop need to be optimized!
    recorrida = due_sources_list*len(usuarios_unique)
    user_recorrida = usuarios_unique*len(due_sources_list)

    while(True):
        if i<len(recorrida):
            usuario = user_recorrida[i]
            fuente = recorrida[i]
            get_data(usuario,fuente,mode=mode,dia_hasta=till_date) 
            sleep(wait)
            i+=1
        else:
            i=0

hasta = datetime(2023,11,14)

#getDueData(sources,0,hasta,'NEW')