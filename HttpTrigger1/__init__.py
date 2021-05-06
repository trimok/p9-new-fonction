import logging
import json
import pandas

import azure.functions as func


web_init_df = False

# Initialisations : on charge les dataframe en mémoire
def web_init(cf_recommend_filename=None, cb_recommend_filename=None):
    global web_init_df
    global dict_df
    
    if not web_init_df:
        try:
            df_cf_recommend = pd.read_csv(cf_recommend_filename)
        except:
            pass
        try:
            df_cb_recommend = pd.read_csv(cb_recommend_filename)
        except:
            pass
        dict_df = {"cf":df_cf_recommend, "cb" :df_cb_recommend}
        
        web_init_df = True

# Fonction pour le web
# Récupère les articles les plus appropriés pour un utilisateur        
def web_search_items(type_recommandation, userId, 
                     cf_recommend_filename="data/cf_recommend.csv", 
                     cb_recommend_filename = "data/cb_recommend.csv"):
    global dict_df
    
    # Initialisations si nécessaire
    web_init(cf_recommend_filename=cf_recommend_filename, cb_recommend_filename=cb_recommend_filename);
    
    # Les données correspondant au bon type de filtering
    df = dict_df [type_recommandation]
    
    # Les items conseillés
    items = df[df.user == userId].sort_values(by=['rank'])["item"].tolist()
    
    return items

# Main
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    userId = req.params.get('userId')
    error=''
    if not userId:
        try:
            req_body = req.get_json()
        except ValueError as ve:
            error = str(ve)
            pass
        else:
            userId = req_body.get('userId')

    if userId:
        list_item = web_search_items("cb", userId)
        return func.HttpResponse(json.dumps(list_item), mimetype="application/json")        
    else:
        return func.HttpResponse(json.dumps("error : " + error), mimetype="application/json")
