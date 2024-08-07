import pandas as pd
import numpy as np

political_posts = pd.read_csv('Elecciones + IA/data_base/political_posts.csv')

primera_vuelta_poly = pd.read_csv('Elecciones + IA/modeling/polynomial_surveys/data_built/normalize_primera_vuelta_poly.csv')
ballotaje_poly = pd.read_csv('Elecciones + IA/modeling/polynomial_surveys/data_built/normalize_ballotage_poly.csv')

parties_primera_vuelta = primera_vuelta_poly.columns[0:5]
parties_ballotage = ballotaje_poly.columns[0:2]

#Filtering posts with outliers amoun of post by range date given by surveys
def filteringPostsBySurveys(survey,posts_data):
    amount_posts = np.zeros(len(survey))
    for i in range (len(survey)):
        indx_row = i
        start = survey.iloc[indx_row]['Inicio']
        end = survey.iloc[indx_row]['Final']
        aux = posts_data[(posts_data['fecha']>start)& (posts_data['fecha']<end)]
        amount_posts[i] = len(aux)

    amount_max = np.quantile(amount_posts,0.95)
    amount_min = np.quantile(amount_posts,0.1)
    filtered_index =  np.nonzero((amount_posts>amount_min) & (amount_posts<amount_max))
    return survey.iloc[filtered_index]

def selecPostDate(survey, posts_data):
    res = []
    for indx_row in range (len(survey)):
        start = survey.iloc[indx_row]['Inicio']
        end = survey.iloc[indx_row]['Final']

        filtered_date = posts_data[(posts_data['fecha']>start)& (posts_data['fecha']<end)]
        
        res.append(filtered_date) 

    return res

primera_vuelta_poly_filtered = filteringPostsBySurveys(primera_vuelta_poly,political_posts)
separated_date_posts_primera_vuelta = selecPostDate(primera_vuelta_poly_filtered,political_posts)

ballotage_poly_filtered = filteringPostsBySurveys(ballotaje_poly,political_posts)
separated_date_posts_ballotage = selecPostDate(ballotage_poly_filtered,political_posts)

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

sources = political_posts['fuente'].unique()

def buildRow(amount_source,grouped_mean):
    row_x = np.zeros(len(sources)*2)
    for source in sources:
        if source in amount_source.index and source in grouped_mean.index:
            i_amount = list(sources).index(source)
            i_mean = list(sources).index(source)+len(amount_source)-1
            row_x[i_amount] = amount_source[[source]].values[0]
            row_x[i_mean] = grouped_mean[[source]].values[0]
        else: pass
    return row_x

def preparingX(party,separated_date_posts):

    labels_amounts = sources+'_amount'
    labels_means = sources+'_means'
    columns = np.concatenate((labels_means,labels_amounts))
    rows_x = np.zeros((len(separated_date_posts),len(columns)))

    for i in range(len(separated_date_posts)):
        df_posts_ranged= separated_date_posts[i]
        df_posts_ranged_party = df_posts_ranged[df_posts_ranged['partido']==party]
        if not df_posts_ranged_party.empty:
            df_posts_ranged_party = deleteDuplicates(df_posts_ranged_party)

            amount_source = df_posts_ranged_party['fuente'].value_counts()
            grouped_mean = df_posts_ranged_party.groupby('fuente').mean(numeric_only=True)['cantidad_likes'].round(2)

            rows_x[i] = buildRow(amount_source,grouped_mean)
    
    df_x = pd.DataFrame(data=rows_x,columns=columns)
    return df_x

def preparingY(surveys,party):
    survey_values = surveys[party].to_numpy()
    largo = len(survey_values)
    diff_relative = np.zeros(largo)

    for i in range(largo-1,0,-1):
        # Iterating backwards
        last_one = survey_values[i] 
        previuos_one = survey_values[i-1]
        diff_relative[i] = (last_one-previuos_one)/previuos_one

    res = pd.DataFrame()
    res['Target'] = diff_relative
    return res

for party in parties_primera_vuelta:
    data_x = preparingX(party,separated_date_posts_primera_vuelta)
    data_y = preparingY(primera_vuelta_poly_filtered,party)
    data_structured = pd.concat([data_x,data_y],axis=1)
    data_structured.to_csv(f'Elecciones + IA/modeling/Preparing_data/data_primera_vuelta_{party}.csv',index=False)

for party in parties_ballotage:
    data_x = preparingX(party,separated_date_posts_ballotage)
    data_y = preparingY(ballotage_poly_filtered,party)
    data_structured = pd.concat([data_x,data_y],axis=1)
    data_structured.to_csv(f'Elecciones + IA/modeling/Preparing_data/data_ballotage_{party}.csv',index=False)