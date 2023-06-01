from rdflib import Graph, Namespace

g = Graph()
g.parse("C://Users//buciu//Desktop//penal-code//codpenal.rdf")
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


def get_all_subclasses():
    res = g.query("""
        SELECT ?subject ?object
        WHERE { ?subject rdfs:subClassOf ?object
            }
    """)
    for row in res:
        print(get_label(row[0]))


def search_for_exact_keyword(keyword):
    res = g.query(f"""
        SELECT ?individual WHERE {{
        ?individual rdfs:label ?label
        FILTER(str(?label)='{keyword}')
        }}
        ORDER BY ?label
    """)
    for row in res:
        print(get_label(row[0]))


def search_for_keyword(keyword):
    res = g.query(f"""
        SELECT ?individual WHERE {{
        ?individual rdfs:label ?label
        FILTER CONTAINS (str(?label), '{keyword}')
        }}
        ORDER BY ?label
    """)
    for row in res:
        print(get_label(row[0]))


def search_in_subclasses(keyword):
    res = g.query(f"""
         SELECT ?entity WHERE {{
                {{ ?entity rdfs:label ?label . FILTER(str(?label) = '{keyword}') }}
                UNION
                {{ ?entity rdfs:subClassOf ?superClass . ?entity rdfs:label ?label .
                    FILTER(str(?label) = '{keyword}') }}
            }}
    """)
    for row in res:
        print(get_label(row[0]))


def get_subclass_labels_of_class_with_label(class_label):
    query = """
    SELECT ?subclassLabel
    WHERE {{
        ?subclass rdfs:subClassOf ?class .
        ?class rdfs:label ?classLabel .
        ?subclass rdfs:label ?subclassLabel .
        FILTER (str(?classLabel) = "{0}" )
    }}
    """.format(class_label)

    results = g.query(query)

    subclass_labels = []
    for result in results:
        # print(result)
        subclass_label = result["subclassLabel"]
        subclass_labels.append(subclass_label)

    return subclass_labels


def get_individual_labels_of_class_with_label(class_label):
    query = """
    SELECT ?individualLabel
    WHERE {{
        ?individual rdf:type/rdfs:subClassOf* ?class .
        ?class rdfs:label ?classLabel .
        ?individual rdfs:label ?individualLabel .
        FILTER (str(?classLabel) = "{0}" && langMatches(lang(?individualLabel), "en"))
    }}
    """.format(class_label)

    results = g.query(query)

    individual_labels = []
    for result in results:
        individual_label = result["individualLabel"]
        individual_labels.append(individual_label)

    return individual_labels


def search_individuals_by_label_keywords(keyword):
    # print(keyword)
    keyword_list = keyword.split(" ")
    # print(keyword_list)

    filters = []
    for word in keyword_list:
        filters.append("CONTAINS(LCASE(str(?label)), '{0}')".format(word.lower()))

    filter_str = " || ".join(filters)
    query = f"""
        SELECT ?individual WHERE {{
            ?individual rdfs:label ?label .
            FILTER({filter_str})
        }}
    """
    results = g.query(query)
    individuals = []
    for result in results:
        individual = result["individual"]
        individuals.append(individual)

    return individuals


def extract_individual_name(url):
    """Extracts the fragment (substring after #) from a given URL and replaces underscores with spaces."""
    fragment = url.split('#')[-1]
    fragment = fragment.replace('_', ' ')
    return fragment


def merge_punishments_for_individual(individual_label):
    """Merges the punishments for each individual of the specified label in the given OWL ontology."""
    individual_punishments = {}
    query = """
        SELECT ?individual ?punishment ?period
        WHERE {
            ?individual rdfs:label "%s" .
            ?individual ns:se_pedepseste_cu ?punishment .
            ?individual ns:pe_perioada ?period .
        }
    """ % individual_label
    res = g.query(query, initNs={"ns": ns})
    # print("Punishments for: ", individual_label)
    for row in res:
        # print(row)
        individual_uri = extract_individual_name(row[0])
        punishment_label = extract_individual_name(row[1])
        if punishment_label == "inchisoare":
            punishment_label += " " + extract_individual_name(row[2])
        if individual_uri in individual_punishments:
            individual_punishments[individual_uri].append(punishment_label)
        else:
            individual_punishments[individual_uri] = [punishment_label]
    return individual_punishments


def search_ontology_for_keyword_punishment(keyword):
    """Searches the specified OWL ontology for individuals that contain the specified keyword in their label."""
    # print(keyword)
    individuals = []
    res = g.query(f"""
        SELECT ?individual WHERE {{
            ?individual rdfs:label ?label .
            FILTER(str(?label) = '{keyword}')
        }}
    """)
    print("Result for: ", keyword)
    for row in res:
        print(row)
        individual_uri = row[0]
        individual_label = extract_individual_name(individual_uri)
        punishments = merge_punishments_for_individual(individual_label)
        if punishments:
            punishments_str = ', '.join([', '.join(punishments[individual]) for individual in punishments])
            result = f'{individual_label} se pedepseste cu {punishments_str}.'
            individuals.append(result)
    return individuals


class_label = "Talharia"
individual_labels = get_individual_labels_of_class_with_label(class_label)
subclass_labels = get_subclass_labels_of_class_with_label(class_label)

print("Individuals of Class '{0}':".format(class_label))
for individual_label in individual_labels:
    print(individual_label)

print("Subclasses of Class '{0}':".format(class_label))
for subclass_label in subclass_labels:
    print(subclass_label)

keyword = "grup"

individuals = search_individuals_by_label_keywords(keyword)

# print("Individuals with Labels containing '{0}':".format(keyword))
# for individual in individuals:
#     # print(get_label(individual))
#     results = search_ontology_for_keyword_punishment(get_label(individual))
#     for r in results:
#         print(r)

# individuals = search_ontology_for_keyword_punishment("Omorul")
#  individuals = search_ontology_for_keyword_punishment("Initierea, constituirea, aderarea sau sprijinirea unui grup infractional organizat")
#
# print("Individuals with label name '{0}':".format(keyword))
# for individual in individuals:
#     print(individual)
