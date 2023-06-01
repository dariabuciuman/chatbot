import random
import json
import pickle
import numpy as np
import spacy

import nltk
from nltk.stem import WordNetLemmatizer

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD

lemmatizer = WordNetLemmatizer()
nlp = spacy.load('ro_core_news_lg')

intents = json.loads(open('../helpers/good_intents.json').read())

words = []
classes = []
documents = []
ignore_letters = ['?', '!', '.', ',']


# Define a function to preprocess a single sentence
def preprocess_sentence(sentence):
    doc = nlp(sentence)
    tokens = [token.lemma_ for token in doc]  # Lemmatize each token
    pos_tags = [token.pos_ for token in doc]  # Get the POS tag for each token
    entities = [(entity.text, entity.label_) for entity in doc.ents]  # Get the named entities in the sentence
    return tokens, pos_tags, entities


for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)     # splits the words in a sentence by spaces
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# there might be a problem with identifying the words, maybe tokenizing the words would be a better idea
# and use the spacy tokenizer
words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))

print(classes)
classes = sorted(set(classes))

print("words: ")
print(words)
print("classes: ")
print(classes)

print("nn: ")
with open("words.pkl", 'wb') as f:
    pickle.dump(words, f)

# pickle.dump(words, open('words.pkl', 'w'))
pickle.dump(classes, open("classes.pkl", 'wb'))

training = []
output_empty = [0] * len(classes)

print(documents)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training, dtype=object)

train_x = list(training[:, 0])
train_y = list(training[:, 1])

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('keywords_model.h5', hist)
print("Done")