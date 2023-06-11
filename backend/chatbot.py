import json
import pickle
import logging as log

import numpy as np
import spacy
from keras.models import load_model

from helpers.text_processing import remove_diacritics
from ontology.query import get_punishments
from output.process_output import build_response

print("Load model start")
nlp = spacy.load('ro_core_news_lg')
intents = json.loads(open('helpers/good_intents.json').read())

words = pickle.load(open('neural/words.pkl', 'rb'))
classes = pickle.load(open('neural/classes.pkl', 'rb'))
model = load_model('neural/keywords_model.h5')
print("Load model finish")


def preprocess_sentence(sentence):
    print("Method preprocess sentence")

    doc = nlp(sentence)
    tokens = []
    for token in doc:
        if not token.is_punct:
            tokens.append(remove_diacritics(token.text))  # Lemmatize each token
    return tokens


def bag_of_words(sentence):
    print("Method bag of words")

    sentence_words = preprocess_sentence(sentence)
    print(sentence_words)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)


def predict_class(sentence):
    print("Method predit class")

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
    print("Method get response")
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    result = []
    for i in list_of_intents:
        if i['tag'] == tag:
            result = i['responses']
            break
    return result


print("Chatbot is running!")


# def get_response_for_message(chat_message):
#     ints = predict_class(chat_message)
#     print(ints)
#     detected_crimes = get_response(ints, intents)
#     extr = ""
#     if "," in detected_crimes:
#         tokenized_crime = detected_crimes.split(",")
#         main_crime = tokenized_crime[0]
#         extra_crime = tokenized_crime[1]
#     else:
#         main_crime = detected_crimes
#         extra_crime = extr
#     all_punishments = get_punishments(main_crime)
#     response = build_response(detected_crimes, punishments, extra_crime)
#     log.info("Response for %s is %S", chat_message, response)


while True:
    message = input("")
    print(preprocess_sentence(message))
    intents_list = predict_class(message)
    print(intents_list)
    crime = get_response(intents_list, intents)
    extra = ""
    if "," in crime:
        crime_split = crime.split(",")
        crime = crime_split[0]
        extra = crime_split[1]
    # print("Infractiunea: " + crime)
    punishments = get_punishments(crime)
    # print(punishments)
    print(build_response(crime, punishments, extra))
