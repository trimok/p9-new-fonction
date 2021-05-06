import logging
import json
import pandas as pd

import azure.functions as func


web_init_df = False
web_dict_df = None

# Fonction pour le web
# Initialisations : on charge les dataframe en mémoire
def web_init(cf_recommend_filename=None, cb_recommend_filename=None):
    global web_init_df
    global web_dict_df
    
    df_cf_recommend=None
    df_cb_recommend=None
    
    if not web_init_df:
        try:
            df_cf_recommend = pd.read_csv(cf_recommend_filename)
        except Exception as e:
            print(str(e))
            pass
        try:
            df_cb_recommend = pd.read_csv(cb_recommend_filename)
        except  Exception as e:
            print (str(e))
            pass
        web_dict_df = {"cf":df_cf_recommend, "cb" :df_cb_recommend}
        
        web_init_df = True

# Fonction pour le web
# Récupère les articles les plus appropriés pour un utilisateur        
def web_search_items(type_recommandation, userId, 
                     cf_recommend_filename="HttpTrigger1/data/cf_recommend.csv", 
                     cb_recommend_filename = "HttpTrigger1/data/cb_recommend.csv"):
    global dict_df
    
    # Initialisations si nécessaire
    web_init(cf_recommend_filename=cf_recommend_filename, cb_recommend_filename=cb_recommend_filename);
    
    # Les données correspondant au bon type de filtering
    df = web_dict_df [type_recommandation]
    
    # Les items conseillés
    items = df[df.user == int(userId)].sort_values(by=['rank'])["item"].tolist()
    
    return items

# Main
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    userId = req.params.get('userId')
    error=''
    if userId is None:
        try:
            req_body = req.get_json()
        except ValueError as ve:
            error = str(ve)
            pass
        else:
            userId = req_body.get('userId')

    if userId is None:
        list_item = web_search_items("cb", userId)
        return func.HttpResponse(json.dumps(list_item), mimetype="application/json")        
    else:
        return func.HttpResponse(json.dumps([-1]), mimetype="application/json")
