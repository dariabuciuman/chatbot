import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

romanian_stopwords = stopwords.words('romanian')
romanian_stemmer = SnowballStemmer('romanian')
print(romanian_stemmer.stem("alergare si miscarea"))


def preprocess_text(text):
    tokens = word_tokenize(text.lower(), language='romanian')
    tokens = [romanian_stemmer.stem(token) for token in tokens if token.isalpha() and token not in romanian_stopwords]
    return tokens


def extract_keywords(text):
    tokens = preprocess_text(text)
    keywords = set()
    for token in tokens:
        if len(token) > 2:
            keywords.add(token)
    return keywords


# question = input("Your question here: ")
print(extract_keywords("Care e pedeapsa"))
