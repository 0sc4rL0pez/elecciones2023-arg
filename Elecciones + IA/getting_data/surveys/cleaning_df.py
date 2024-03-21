import pandas as pd

primera_vuelta = pd.read_csv('Elecciones + IA/getting_data/surveys/data_scraped/Survey_primera_vuelta.csv')
ballotage = pd.read_csv('Elecciones + IA/getting_data/surveys/data_scraped/Survey_ballotage.csv')

#Check the analysis in : Elecciones + IA\analisis_exploratorio\surveys_plots.ipynb

#cleaning and saving only the columns that matters

careless = primera_vuelta['Indecisos']+primera_vuelta['Blanco']
filtering_outliers = (primera_vuelta['Muestra']>=1000) & (primera_vuelta['Muestra']<5000) & (careless<=20)


parties = ['Union por la Patria','Juntos por el Cambio', 'La Libertad Avanza','Hacemos juntos nuestro Pais', 'Frente de Izquierda y Trabajadores']
columns = parties + ['Inicio', 'Final']
primera_vuelta_cleaned = primera_vuelta[filtering_outliers].loc[:,columns]
primera_vuelta_cleaned.to_csv('Elecciones + IA/getting_data/surveys/data_scraped/primera_vuelta_cleaned.csv',index= False)


careless = ballotage['Indecisos']+ballotage['Blanco']
filtering_outliers = (ballotage['Muestra']>=2000) & (ballotage['Muestra']<14000) & (careless<18)
labels = ['La Libertad Avanza','Union por la Patria','Inicio','Final']
ballotage_cleaned = ballotage[filtering_outliers].loc[:,labels]
ballotage_cleaned.to_csv('Elecciones + IA/getting_data/surveys/data_scraped/ballotage_cleaned.csv',index= False)


