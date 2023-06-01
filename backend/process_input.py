import spacy
import ro_diacritics
nlp = spacy.load('ro_core_news_lg')

# text = "Care e pedeapsa pentru omor?"
text = "Cum se pedepseste omorul"
doc1 = nlp("omor")
doc2 = nlp("sinucidere")
print(doc1.similarity(doc2))

docs = nlp(ro_diacritics.restore_diacritics(text))
for doc in docs:
    print(doc.text + " " + str(doc.is_stop) + " "+ str(doc.is_punct))
    # if not doc.is_stop and not doc.is_punct:
    #     print(doc.text + " -> " + doc.lemma_)


