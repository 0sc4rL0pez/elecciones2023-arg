# Palabras claves sacadas de Chat-GPT
# IDEA DESCARTADA

import instaloader
import pandas as pd
import json
import lzma 
import glob
import ast
palabras_politicas = [  "Peronismo",  "Radicalismo",  "Kirchnerismo",  "Macrismo",  "Justicialismo",  "Cambiemos",  "Partido Justicialista",  "Frente de Todos",  "Oposición",  "Oficialismo",  "Elecciones",  "Congreso",  "Senado",  "Diputados",  "Gobierno",  "Presidente",  "Vicepresidente",  "Ministro",  "Gabinete",  "Coalición",  "Partido político",  "Provincia",  "Municipio",  "Ley",  "Constitución",  "Política exterior",  "Diplomacia",  "Relaciones bilaterales",  "Deuda externa",  "Inflación",  "Desarrollo económico",  "Desigualdad",  "Derechos humanos",  "Corrupción",  "Justicia",  "Corte Suprema",  "Juez",  "Fuerzas Armadas",  "Protesta",  "Manifestación",  "Movimiento estudiantil",  "Trabajo sindical",  "Huelga",  "Libertad de expresión",  "Medios de comunicación",  "Polarización",  "Populismo",  "Reforma política",  "Participación ciudadana",  "Revolución",  "Gobernador",  "Intendente",  "Legislatura",  "Cámara de Diputados",  "Cámara de Senadores",  "Senador",  "Diputado",  "Voto",  "Ciudadanía",  "Campaña electoral",  "Propaganda política",  "Acto político",  "Sindicato",  "FMI","Fondo Monetario Internacional",  "Ajuste económico",  "Política social",  "Educación pública",  "Salud pública",  "Pensiones",  "Subsidios",  "Presupuesto",  "Impuestos",  "Política educativa",  "Movimiento obrero",  "Movimientos sociales",  "Militancia",  "Nacionalización",  "Privatización",  "Inversión extranjera",  "Plan económico",  "Desempleo",  "Planes sociales",  "Asignaciones familiares",  "Corrupción",  "Libertad de prensa",  "Democracia",  "Autonomía",  "Federalismo",  "Unidad nacional",  "Asamblea",  "Conflicto social",  "Juicio político",  "Acuerdo internacional",  "Relaciones diplomáticas",  "Balotaje",  "Voto electrónico",  "Ideología",  "Nacionalismo",  "Internacionalismo",  "Tratados", "Dolar"]
politicos_influyentes_argentina = [
    "Cristina Fernández de Kirchner",    "Mauricio Macri",
    "Alberto Fernández",    "Horacio Rodríguez Larreta",
    "Axel Kicillof",    "Sergio Massa",
    "María Eugenia Vidal",
    "Elisa Carrió",    "Juan Manuel Urtubey",
    "Gabriela Michetti",
    "Amado Boudou",    "Patricia Bullrich",
    "Hermes Binner",    "Gabriela Cerruti",
    "Daniel Scioli",    "Martín Lousteau",
    "Néstor Kirchner",    "Gabriela Cámara",
    "María Eugenia Bielsa",
    "Julio Cobos",    "Aníbal Fernández",
    "Margarita Stolbizer",
    "Ricardo Alfonsín",
    "Agustín Rossi",    "Graciela Camaño",
    "Emilio Monzó",
    "Victoria Donda",
    "Nicolás del Caño",
    "Juan Schiaretti",
    "Juan Cabandié",
    "Oscar Aguad",
    "Martín Insaurralde",
    "Florencio Randazzo",
    "Diego Santilli",
    "Felipe Solá",
    "Esteban Bullrich",
    "Jorge Capitanich",
    "Andrés Larroque",
    "Patricia Giménez",
    "Pino Solanas",
    "Miguel Ángel Pichetto",
    "Luis Juez",
    "Mario Negri",
    "Juan Grabois",
    "Juan Manuel Abal Medina",
    "Guillermo Moreno",
    "José Luis Espert",
    "Fernando Espinoza",
    "Margarita Barrientos",
    "Graciela Ocaña",
    "Victoria Tolosa Paz",
    "Juan Cabandié",
    "Andrés Ibarra",
    "Martín Redrado",
    "María Eugenia Estenssoro",
    "Adolfo Rodríguez Saá",
    "Claudio Moroni",
    "Juan José Aranguren",
    "Hugo Moyano",
    "Emilio Pérsico",
    "Alejandro Vanoli",
    "Malena Galmarini",
    "Eduardo 'Wado' de Pedro",
    "Juan Grabois",
    "Felipe Miguel",
    "Nicolás Trotta",
    "Facundo Manes",
    "Daniel Angelici",
    "María Eugenia Zamarreño",
    "Luis Caputo",
    "Fernando Espinoza",
    "María Eugenia Rodríguez Palop",
    "Julio De Vido",
    "Cristina Álvarez Rodríguez",
    "Juan José Gómez Centurión",
    "Estela de Carlotto",
    "Cecilia Todesca Bocco",
    "Jorge Macri",
    "Aníbal Fernández",
    "Martín Sabbatella",
    "Juan José Aranguren",
    "Leonardo Nardini",
    "Diego Bossio",
    "Nicolás Ducoté",
    "Emilio Pérsico",
    "Guillermo Nielsen",
    "Carolina Stanley",
    "Agustín Rossi",
    "José Luis Gioja",
    "José Corral",
    "Héctor Daer",
    "Julio Pereyra",
    "Verónica Magario",
    "Hugo Yasky",
    "Carlos Menem",
    "Patricia Cubría",
    "Andrés Rodríguez",
    "Juan Carlos Schmid",
    "Esteban Bullrich",
    "Patricia Maza"
]
apellidos_influyentes = []
for politicos in politicos_influyentes_argentina:
    apellidos_influyentes.append(politicos.split(' ')[-1])

def descomprimir_jsonXZ(directorio):
    
    with lzma.open(directorio,'r') as f:
                    json_bytes = f.read()
                    stri = json_bytes.decode('utf-8')
                    good = stri.replace("\'", "\"")
                    #good = ast.literal_eval(stri)
                    data = json.loads(good)
    return data

def devolver_shortCode(dirs):
    directorio_json = dirs.split('.')[0] + ".json.xz"
    datos = descomprimir_jsonXZ(directorio_json)
    return datos['node']['shortcode']

def buscar_Palabra (palabra,directorios):
    ids_posts = []
    cantidad = 0
    for dir_caption in directorios:
        with open(dir_caption,encoding="utf8") as f:
            for line in f:
                if palabra in line:
                    cantidad+=1
                    ids_posts.append(devolver_shortCode(dir_caption))
                    break
    
    return set(ids_posts)


dir_captions = []
for dirs in glob.glob('getting_data/infobae/*.txt'):
    dir_captions.append(dirs)
    ''

publicaciones_politicas = set()
publicaciones_politica_apellido = set()
publicaciones_politicas_palabra = set()

for palabra in apellidos_influyentes:
    publicaciones_politica_apellido = publicaciones_politica_apellido.union(buscar_Palabra(palabra, dir_captions))
for palabra in palabras_politicas:
    publicaciones_politicas_palabra = publicaciones_politicas_palabra.union(buscar_Palabra(palabra, dir_captions))

publicaciones_politicas = publicaciones_politica_apellido.union(publicaciones_politicas_palabra)

s = buscar_Palabra(apellidos_influyentes[1], dir_captions)
print(s)