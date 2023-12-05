###           ESTRUCTURAS
### info recolectada de forma manual wikipedia
class formula_electoral:
    def __init__(self, presi, vice):
        self.presidente = presi
        self.vice_presidente = vice

    def retornar(self):
        return self.presidente, self.vice_presidente
    
class Partido:
    def __init__(self, nombre, candidatos):
        self.nombre = nombre
        self.candidatos = candidatos

    def retornarDatosLista(self):
        res = [self.nombre]
        for candidato in self.candidatos:
            res.append(candidato.retornar())

        return res
###                               DATOS ELECCIONES
# 2023
formula1_2023 = formula_electoral('JAVIER GERARDO MILEI','VICTORIA VILLARRUEL')
formula2_2023 = formula_electoral('PATRICIA BULLRICH','LUIS PETRI')
formula3_2023 = formula_electoral('HORACIO ANTONIO RODRIGUEZ LARRETA','GERARDO MORALES')
formula4_2023 = formula_electoral('SERGIO TOMAS MASSA','AGUSTIN ROSSI')
formula5_2023 = formula_electoral('JUAN GRABOIS','PAULA ABAL MEDINA')

Candidatos_relevantes_2023_1 = Partido('LA LIBERTAD AVANZA',[formula1_2023])
Candidatos_relevantes_2023_2 = Partido('JUNTOS POR EL CAMBIO',[formula2_2023,formula3_2023])
Candidatos_relevantes_2023_3 = Partido('UNION POR LA PATRIA',[formula4_2023,formula5_2023])

Elecciones_2023 = [Candidatos_relevantes_2023_1, Candidatos_relevantes_2023_2, Candidatos_relevantes_2023_3]
# Se agrego en partidos_candidatos frente de izquierda, Hacemos por Nuestro País
# 2019
formula1_2019 = formula_electoral('Alberto Fernández','Cristina Fernández de Kirchner')
formula2_2019 = formula_electoral('Mauricio Macri','Miguel Ángel Pichetto')
formula3_2019 = formula_electoral('Roberto Lavagna','Juan Manuel Urtubey')

Candidatos_relevantes_2019_1 = Partido('Frente de Todos',[formula1_2019])
Candidatos_relevantes_2019_2 = Partido('Juntos por el Cambio',[formula2_2019])
Candidatos_relevantes_2019_3 = Partido('Consenso Federal',[formula3_2019])

Elecciones_2019 = [Candidatos_relevantes_2019_1, Candidatos_relevantes_2019_2, Candidatos_relevantes_2019_3]

# 2015
formula1_2015 = formula_electoral('Mauricio Macri','Gabriela Michetti')
formula2_2015 = formula_electoral('Daniel Scioli','Carlos Zannini')
formula3_2015 = formula_electoral('Sergio Massa','Gustavo Sáenz')

Candidatos_relevantes_2015_1 = Partido('CAMBIEMOS',[formula1_2015])
Candidatos_relevantes_2015_2 = Partido('Frente para la Victoria',[formula2_2015])
Candidatos_relevantes_2015_3 = Partido('Unidos por una Nueva Alternativa',[formula3_2015])

Elecciones_2015 = [Candidatos_relevantes_2015_1, Candidatos_relevantes_2015_2, Candidatos_relevantes_2015_3]

# 2011
formula1_2011 = formula_electoral('Cristina Fernández de Kirchner','Amado Boudou')
formula2_2011 = formula_electoral('Hermes Binner','Norma Morandini')
formula3_2011 = formula_electoral('Ricardo Alfonsín','Javier González Fraga')

Candidatos_relevantes_2011_1 = Partido('Frente para la Victoria',[formula1_2011])
Candidatos_relevantes_2011_2 = Partido('Frente Amplio Progresista',[formula2_2011])
Candidatos_relevantes_2011_3 = Partido('Unión para el Desarrollo Social',[formula3_2011])

Elecciones_2011 = [Candidatos_relevantes_2011_1, Candidatos_relevantes_2011_2, Candidatos_relevantes_2011_3]

Datos_elecciones = [Elecciones_2011,Elecciones_2015,Elecciones_2019,Elecciones_2023]