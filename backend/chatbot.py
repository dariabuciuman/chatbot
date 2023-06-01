import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from keras.models import load_model
from ontology.query import get_punishments
from output.process_output import build_response
from ro_diacritics import restore_diacritics

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('helpers/good_intents.json').read())

words = pickle.load(open('neural/words.pkl', 'rb'))
classes = pickle.load(open('neural/classes.pkl', 'rb'))
model = load_model('neural/keywords_model.h5')


def clean_up_diacritics(sentence):
    special_chars = {
        'Äƒ': 'ă',
        'Ã¢': 'â',
        'Ã®': 'î',
        'È™': 'ș',
        'È›': 'ț'
    }
    for special_char, regular_char in special_chars.items():
        sentence = sentence.replace(special_char, regular_char)
    return sentence


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words


def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
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
    for i in list_of_intents:
        if i['tag'] == tag:
            result = i['responses']
            break
    return result


print("Chatbot is running!")

while True:
    message = input("")
    ints = predict_class(clean_up_diacritics(message))
    print(ints)
    crime = get_response(ints, intents)
    # print("Infractiunea: " + crime)
    punishments = get_punishments(crime)
    # print(punishments)
    print(build_response(crime, punishments))
    # for result in results:
    #     print(restore_diacritics(result))
