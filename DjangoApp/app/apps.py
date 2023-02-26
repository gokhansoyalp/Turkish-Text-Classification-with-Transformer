import pickle as pickle

from django.apps import AppConfig
from tensorflow import keras


class AppConfig(AppConfig):
    name = 'app'
    model = keras.models.load_model('C:/Users/user/Desktop/TextClassificationApp/models')
    if (model):
        print("Loaded model from disk")


    with open('C:/Users/user/Desktop/TextClassificationApp/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
