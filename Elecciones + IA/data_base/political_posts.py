import pandas as pd

def max_likes(id:str,dataFrame:pd.DataFrame):
    res = dataFrame[dataFrame['id'] == id]['cantidad_likes'].idxmax()
    return dataFrame.loc[[res]]

def deleteDuplicates(dataframe):
    dataframe_with_out_duplicates_list = []
    for id in dataframe['id'].unique():
        row = max_likes(id,dataframe)
        dataframe_with_out_duplicates_list.append(row)

    dataframe_with_out_duplicates = pd.concat(dataframe_with_out_duplicates_list)
    return dataframe_with_out_duplicates

def isSubstring(string,subsequence):
    return subsequence in string

def searchPostsKeyWord(data,key_word,party):
    index_is_in = data['descripcion'].map(lambda x: isSubstring(str(x),key_word))
    res =  data[index_is_in][['id','fuente','cantidad_likes','fecha']]
    res['partido'] = party
    return res

def buildPartyDataFrame(party,key_words_party):
    res_list = []
    for key_word in key_words_party:
        df_key_word = searchPostsKeyWord(raw_posts,key_word,party)
        res_list.append(df_key_word)
    res = pd.concat(res_list)
    deleteDuplicates(res)
    return res

key_words = [
            'MILEI', 'VILLARRUEL', 'LA LIBERTAD AVANZA',
            'BULLRICH', 'PETRI', 'JUNTOS POR EL CAMBIO',
            'MASSA', 'ROSSI', 'UNIÓN POR LA PATRIA',
            'Bregman', 'del Caño', 'Frente de Izquierda y de Trabajadores',
            'Schiaretti', 'Randazzo', 'Hacemos juntos nuestro Pais'
            ]

key_words = [x.lower() for x in key_words]

dicc_parties_key_word = {
    'La Libertad Avanza':key_words[0:3],
    'Juntos por el Cambio':key_words[3:6],
    'Union por la Patria':key_words[6:9],
    'Frente de Izquierda y de Trabajadores':key_words[9:12],
    'Hacemos Nuestro Pais':key_words[12:15]
}

#WARNING: This dir doesn't exists by default!
#Before running this code unzip de file: Elecciones + IA\data_base\data_base_csv\Publicaciones.zip
raw_posts = pd.read_csv('Elecciones + IA\data_base\data_base_csv\Publicaciones\Publicaciones\Publicaciones.csv')
raw_posts['descripcion'] = raw_posts['descripcion'].map(lambda x:str(x).lower())

df_parties = []
for party,key_words_party in dicc_parties_key_word.items():
    df_party = buildPartyDataFrame(party,key_words_party)
    df_parties.append(df_party)

political_posts = pd.concat(df_parties)
political_posts.to_csv('Elecciones + IA/modeling/Preparing_data/political_posts.csv',index=False)
