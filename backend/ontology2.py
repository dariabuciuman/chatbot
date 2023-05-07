from rdflib import Graph, Namespace, RDF, OWL, RDFS, namespace
import spacy

nlp = spacy.load('ro_core_news_lg')

g = Graph()
g.parse("C://Users//buciu//Desktop//penal-code//penal-code-v1.rdf")

ns = Namespace("http://www.semanticweb.org/buciu/ontologies/2023/3/penal-code#")


# query = """
# SELECT ?individual ?penalty ?period
# WHERE {
#   ?individual rdf:type ns:Infractiuni_contra_vietii .
#   ?individual rdfs:label ?label .
#   ?individual ns:se_pedepseste_cu ?penalty .
#   ?individual ns:pe_perioada ?period .
#   FILTER regex(?label, "omorul", "i")
# }
# """
# results = g.query(query, initNs={"ns": ns})
#
# # print the results
# for result in results:
#     print("Individual:", result.individual)
#     print("Penalty:", result.penalty)
#     print("Period:", result.period)

object_properties = []
data_properties = []
classes = []
object_keywords = []


# extract object properties, data properties and classes
def extract_properties():
    for prop in g.subjects(RDF.type, OWL.ObjectProperty):
        if prop.startswith(ns):
            object_properties.append(get_individual_label(prop))
    for prop in g.subjects(RDF.type, OWL.DatatypeProperty):
        if prop.startswith(ns):
            data_properties.append(get_individual_label(prop))
    for prop in g.subjects(RDF.type, OWL.Class):
        if prop.startswith(ns):
            classes.append(get_individual_label(prop))


# extract labels of data properties
def get_individual_label(uri):
    # create a SPARQL query with a parameter for the individual URI
    query_template = """
        SELECT ?label
        WHERE {
            <%s> rdfs:label ?label
        }
    """
    query = query_template % uri

    # execute the query and get the result
    results = g.query(query)
    label = None
    for row in results:
        label = row[0]

    return label


# method to print the ontology properties
def print_properties():
    print("Object properties:")
    for obj_prop in object_properties:
        print(obj_prop)
    print("Data properties:")
    for data_prop in data_properties:
        print(data_prop)
    print("Classes:")
    for cls in classes:
        print(cls)


# method to process the labels for the ontology properties
# TODO:
#  - add verbs to concepts
#  - maybe search for similarity
#
def process_labels(label):
    # Extract relevant concepts and relationships
    label_doc = nlp(label)
    concepts = []
    for token in label_doc:
        print(str(token) + " " + str(token.pos_))
        if token.pos_ in ["NOUN", "ADJ"]:
            if token.ent_type_ == "":
                concepts.append(token.lemma_)
            else:
                concepts.append(token.text)
        elif token.pos_ == "VERB":
            for child in token.children:
                print(str(child) + " " + str(child.pos_))
                if child.pos_ == "NOUN" and child.ent_type_ == "":
                    concepts.append("ch" + child.lemma_)
                    concepts.append("tk" + token.lemma_)
                    break
                elif child.pos_ == "ADP" and child.text == "pentru":
                    for grandchild in child.children:
                        if grandchild.pos_ == "NOUN" and grandchild.ent_type_ == "":
                            concepts.append(grandchild.lemma_)
                            concepts.append(token.lemma_)
                            break
    # Remove duplicates
    return list(set(concepts))


def print_token_fields(tokens):
    for token in tokens:
        print('{:<12}{:<10}{:<10}{:<10}'.format(token.text, token.pos_, token.dep_, token.head.text))


if __name__ == '__main__':
    print_properties()
    print(object_keywords)
    # text = "Care e pedeapsa pentru omorul calificat?"
    # text = "Daca am omorat un om, cata inchisoare trebuie sa fac?"
    text = "savarsita"

    doc = nlp(text)

    print(doc.similarity(nlp("savarsi")))
