import json
import pickle

import numpy as np
import spacy
from keras.models import load_model

from helpers.text_processing import remove_diacritics
from ontology.query import get_punishments
from output.process_output import build_response


class LegalChatbot:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, intents_dir, words_dir, classes_dir, model_dir):
        self.model_dir = model_dir
        self.intents_dir = intents_dir
        self.nlp = None
        self.intents = None
        self.words_dir = words_dir
        self.words = None
        self.classes_dir = classes_dir
        self.classes = None
        self.model = None

    def load_model(self):
        """Loads model from scratch, takes some time to compute"""
        print("Load model start")
        self.nlp = spacy.load('ro_core_news_lg')
        self.intents = json.loads(open(self.intents_dir).read())
        self.words = pickle.load(open(self.words_dir, 'rb'))
        self.classes = pickle.load(open(self.classes_dir, 'rb'))
        self.model = load_model(self.model_dir)
        print("Chatbot loaded successfully!")

    def start_chatbot(self):
        """If model is already loaded in API, do nothing, otherwise load model"""
        if not self.nlp or not self.intents or not self.words or not self.classes or not self.model:
            self.load_model()

    def preprocess_sentence(self, sentence):
        print("Preprocessing sentence %s", sentence)

        doc = self.nlp(sentence)
        tokens = []
        for token in doc:
            if not token.is_punct:
                tokens.append(remove_diacritics(token.text))  # Lemmatize each token
        return tokens

    def bag_of_words(self, sentence):
        print("Computing bag of words for sentence %s", sentence)

        sentence_words = self.preprocess_sentence(sentence)
        bag = [0] * len(self.words)
        for w in sentence_words:
            for i, word in enumerate(self.words):
                if word == w:
                    bag[i] = 1
        return np.array(bag)

    def predict_class(self, sentence):
        print("Predict penal class of sentence %s", sentence)

        bow = self.bag_of_words(sentence)
        res = self.model.predict(np.array([bow]), verbose=0)[0]
        ERROR_THRESHOLD = 0.25
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({'intent': self.classes[r[0]], 'probability': str(r[1])})
        return return_list

    def get_response(self, predicted_classes):
        print("Method get response")
        tag = predicted_classes[0]['intent']
        list_of_intents = self.intents['intents']
        result = []
        for i in list_of_intents:
            if i['tag'] == tag:
                result = i['responses']
                break
        return result

    def get_response_for_message(self, message):
        # predict the classes of infraction present in message
        print("Processing response for message %s", message)
        predicted_classes = self.predict_class(message)
        detected_crimes = self.get_response(predicted_classes)
        extr = ""
        if "," in detected_crimes:
            tokenized_crime = detected_crimes.split(",")
            main_crime = tokenized_crime[0]
            extra_crime = tokenized_crime[1]
        else:
            main_crime = detected_crimes
            extra_crime = extr
        all_punishments = get_punishments(main_crime)
        response = build_response(detected_crimes, all_punishments, extra_crime)
        print("Response for %s is %S", message, response)
        return response
