from rdflib import Graph, Namespace, RDF, OWL

g = Graph()
g.parse("C://Users//buciu//Desktop//penal-code//codpenal1-1.rdf")
ns = Namespace("http://www.semanticweb.org/alinl/ontologies/2022/5/untitled-ontology-53#")


def get_label(uri):
    query_template = """
        SELECT ?label
        WHERE { <%s> rdfs:label ?label }
    """
    query = query_template % uri
    results = g.query(query)
    label = None
    for row in results:
        label = row[0]
    return label


def merge_punishments(individual_label):
    query = """
            SELECT ?individual ?punishment
            WHERE {
                ?individual rdfs:label "%s" .
                ?individual ns:are_pedeapsa_principala ?punishment .
            }
        """ % individual_label
    res = g.query(query, initNs={"ns": ns})
    punishments = []
    for row in res:
        punishments.append(str(get_label(row[1])))
    punishments_str = " sau ".join(punishments)
    return punishments_str


def merge_complementary_punishments(individual_label):
    query = """
            SELECT ?individual ?punishment
            WHERE {
                ?individual rdfs:label "%s" .
                ?individual ns:are_pedeapsa_complementara ?punishment .
            }
        """ % individual_label
    res = g.query(query, initNs={"ns": ns})
    punishments = []
    for row in res:
        punishments.append(str(get_label(row[1])))
    punishments_str = " sau ".join(punishments)
    return punishments_str


def get_punishment_type_for_crime(crime, punishment_type):
    query = f"""
        SELECT ?relationship ?object WHERE {{
        ?individual rdfs:label "{crime}" .
        ?individual ?relationship ?object .
        FILTER(CONTAINS(str(?relationship), "are_pedeapsa_{punishment_type}"))
        }}   """
    result = g.query(query, initNs={"ns": ns})
    output_text = ""

    for row in result:
        print(row)
        for element in row:
            print(element)
            output_text += get_label(element) + " "
    return output_text[:-1]


def get_punishments(crime):
    complementary_punishment = merge_complementary_punishments(crime)
    punishment = "inchisoare " + merge_punishments(crime)
    if complementary_punishment:
        punishment += ", iar pedeapsa complementara este " + complementary_punishment
    return punishment
    # print(merge_punishments(crime))
    # print(merge_complementary_punishments(crime))
    # print(crime + " se pedepseste cu " + punishment)


# def get_punishment(crime):
#     main_punishment = get_punishment_type_for_crime(crime, "principala")
#     complementary_punishment = get_punishment_type_for_crime(crime, "complementara")
#     output = crime + " " + main_punishment + " si " + complementary_punishment + "."
#     return output


# print(get_punishment("Vatamarea corporala"))
# print(merge_complementary_punishments("Omorul"))
# get_punishments("Omorul")
