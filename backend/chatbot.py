import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer
import spacy

from keras.models import load_model

from helpers.text_processing import remove_diacritics, clean_up_diacritics
from ontology.query import get_punishments
from output.process_output import build_response

nlp = spacy.load('ro_core_news_lg')
intents = json.loads(open('helpers/good_intents.json').read())

words = pickle.load(open('neural/words.pkl', 'rb'))
classes = pickle.load(open('neural/classes.pkl', 'rb'))
model = load_model('neural/keywords_model.h5')


def preprocess_sentence(sentence):
    doc = nlp(sentence)
    tokens = []
    for token in doc:
        if not token.is_punct:
            tokens.append(remove_diacritics(token.text))  # Lemmatize each token
    return tokens


def bag_of_words(sentence):
    sentence_words = preprocess_sentence(sentence)
    print(sentence_words)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)


def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]), verbose=0)[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list


def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    result = []
    for i in list_of_intents:
        if i['tag'] == tag:
            result = i['responses']
            break
    return result


print("Chatbot is running!")

while True:
    message = input("")
    print(preprocess_sentence(message))
    ints = predict_class(message)
    print(ints)
    crime = get_response(ints, intents)
    extra = ""
    if "," in crime:
        crime_split = crime.split(",")
        crime = crime_split[0]
        extra = crime_split[1]
    # print("Infractiunea: " + crime)
    punishments = get_punishments(crime)
    # print(punishments)
    print(build_response(crime, punishments, extra))
