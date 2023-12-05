# Ingresa los datos de data_base\data_candidatos_partidos.py a la base de datos

from publicaciones import conectar_base_datos
import data_candidatos_partidos
import pandas as pd

conn = conectar_base_datos()
cursor = conn.cursor()

#######################################PARTIDOS############################################

"""
eleccion1 = (data_candidatos_partidos.Elecciones_2011,2011)
eleccion2 = (data_candidatos_partidos.Elecciones_2015,2015)
eleccion3 = (data_candidatos_partidos.Elecciones_2019,2019)
eleccion4 = (data_candidatos_partidos.Elecciones_2023,2023)
lista_elecciones = [eleccion1, eleccion2, eleccion3, eleccion4]

partidos = {'id':[],'nombre':[], 'anio':[]}

def agregarPartido(eleccion,anio):

    for partido in eleccion:
        datos = partido.retornarDatosLista()
        partidos['nombre'].append(datos[0])
        partidos['anio'].append(anio)
    
for eleccion, anio in lista_elecciones:
    agregarPartido(eleccion=eleccion, anio=anio)

largo = len(partidos['anio'])

partidos['id'] = range(largo)

df = pd.DataFrame(partidos)

for index, row in df.iterrows():

    SQL_STATEMENT = f
    INSERT Partidos
    VALUES ('{row.id}', '{row.nombre}', {row.anio})
    
    cursor.execute(SQL_STATEMENT)
    conn.commit()




#conn.close()
"""
#       Agregando
id = [12,13]
nombres = ['Hacemos por Nuestro País','Frente de Izquierda y de Trabajadores']
presi =['Juan Schiaretti','Myriam Bregman',]
vice = ['Florencio Randazzo','Nicolás del Caño']
anio = [2023,2023]
df = pd.DataFrame({'id':id,'nombre':nombres, 'anio':anio})

for index, row in df.iterrows():

    SQL_STATEMENT = f"""
    INSERT Partidos
    VALUES ('{row.id}', '{row.nombre}', {row.anio})
    """
    cursor.execute(SQL_STATEMENT)
    conn.commit()

nombres_candidatos =['Myriam','Nicolás','Juan','Florencio']
apellidos = ['Bregman', 'del Caño','Schiaretti','Randazzo']
puesto = ['Presidente','Vicepresidente']*2
id=[13,13,12,12]
df_candidatos = pd.DataFrame({'id':id,'nombres':nombres_candidatos, 'apellidos':apellidos,'puesto':puesto})

for index, row in df_candidatos.iterrows():

    SQL_STATEMENT = f"""
    INSERT Candidatos
    VALUES ('{row.id}', '{row.nombres}', '{row.apellidos}', '{row.puesto}')
    """
    cursor.execute(SQL_STATEMENT)
    conn.commit()
#######################################CANDIDATOS############################################

"""
Candidatos = {
    'id':[],
    'nombres':[],
    'apellidos':[],
    'puesto':[]
}
def agregarCandidatos(eleccion, id):

    for candidatos in eleccion:

        nom_apells = candidatos.retornarDatosLista()[1]

        for nom_appel in nom_apells:

            separado = nom_appel.split(' ')
            apellido = separado[-1]
            nombres = nom_appel[:nom_appel.index(apellido)-1] #CORREGIR
            Candidatos['apellidos'].append(apellido)
            Candidatos['nombres'].append(nombres)
            Candidatos['id'].append(id)
        
        id +=1
    
    return id


id = 0
for eleccion, anio in lista_elecciones:
    id = agregarCandidatos(eleccion=eleccion,id=id)

puestos_posibles = ['Presidente', 'Vicepresidente']
Candidatos['puesto'] = puestos_posibles*largo

df = pd.DataFrame(Candidatos)

for index, row in df.iterrows():

    SQL_STATEMENT = f
    INSERT Candidatos
    VALUES ('{row.id}', '{row.nombres}', '{row.apellidos}', '{row.puesto}')
    
    cursor.execute(SQL_STATEMENT)
    conn.commit()

"""
conn.close()


       