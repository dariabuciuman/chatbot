import random
import json
import pickle
import numpy as np
import spacy
from ro_diacritics import restore_diacritics

from nltk.stem import WordNetLemmatizer

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD

from helpers.text_processing import remove_diacritics
from neural.graph import plot_learning_curve

lemmatizer = WordNetLemmatizer()
nlp = spacy.load('ro_core_news_lg')

intents = json.loads(open('../helpers/good_intents_original.json').read())

words = []
classes = []
documents = []
ignore_letters = ['?', '!', '.', ',']


# Define a function to preprocess a single sentence
def preprocess_sentence(sentence):
    doc = nlp(restore_diacritics(sentence))
    tokens = []
    for token in doc:
        if not token.is_punct:
            tokens.append(remove_diacritics(token.text))  # Lemmatize each token
    return tokens


def lemmatize_word(word):
    doc = nlp(word)
    lemmas = [token.text for token in doc]
    return remove_diacritics(lemmas[0])


print(preprocess_sentence(restore_diacritics("cum se pedepseste omorul calificat?")))
print(lemmatize_word("pedepseste"))

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = preprocess_sentence(pattern.lower())  # splits the words in a sentence by spaces
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# there might be a problem with identifying the words, maybe tokenizing the words would be a better idea
# and use the spacy tokenizer
words = [lemmatize_word(word) for word in words if word not in ignore_letters]
words = sorted(set(words))

# print(classes)
classes = sorted(set(classes))

# print("words: ")
# print(words)
# print("classes: ")
# print(classes)

print("nn: ")
with open("words.pkl", 'wb') as f:
    pickle.dump(words, f)

# pickle.dump(words, open('words.pkl', 'w'))
pickle.dump(classes, open("classes.pkl", 'wb'))

training = []
output_empty = [0] * len(classes)

# print(documents)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatize_word(word.lower()) for word in word_patterns]
    print(word_patterns)
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
plot_learning_curve(hist)
model.save('keywords_model2.h5', hist)
print("Done")
