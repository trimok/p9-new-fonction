import logging
import json

from keras import backend
from keras.models import load_model
from keras.utils import Sequence
from keras.preprocessing.image import load_img, img_to_array, array_to_img, save_img
from keras.callbacks import *

from keras import layers
from keras import models
from keras import Model
from keras.layers import *
from keras.models import *
from keras.optimizers import *
from keras import regularizers

import azure.functions as func

def test_keras():
    model = Sequential()
    model.add(Dense(12, input_dim=8, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))


def main(req: func.HttpRequest) -> func.HttpResponse:
    test_keras()
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
        return func.HttpResponse(json.dumps([2137,2662,4243]), mimetype="application/json")        
    else:
        return func.HttpResponse(json.dumps("error : " + error), mimetype="application/json")
