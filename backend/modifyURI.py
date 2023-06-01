import re
from rdflib import Graph, URIRef

def transform_label_to_uri(label):
    # Replace spaces and special characters with underscores
    transformed_label = re.sub(r'[\s\W]+', '_', label)
    return transformed_label

def update_ontology_uris(file_path):
    # Load the RDF/OWL file
    graph = Graph()
    graph.parse(file_path)

    # Create a mapping to store old URIs and new URIs
    uri_mapping = {}

    # Iterate over all entities in the graph
    for entity in graph.subjects():
        # Check if the entity is an individual, class, or property
        if isinstance(entity, URIRef):
            # Get the label of the entity
            label = graph.value(subject=entity, predicate=URIRef('http://www.w3.org/2000/01/rdf-schema#label'))

            if label:
                # Transform the label to a URI
                new_uri = transform_label_to_uri(str(label))

                # Store the mapping between old URI and new URI
                uri_mapping[str(entity)] = new_uri

    # Update the URIs in the graph
    for old_uri, new_uri in uri_mapping.items():
        old_uri_ref = URIRef(old_uri)
        new_uri_ref = URIRef(new_uri)

        # Update the subject URI while preserving triples
        triples_with_old_uri = list(graph.triples((old_uri_ref, None, None)))
        for triple in triples_with_old_uri:
            subject, predicate, object_ = triple
            graph.remove((subject, predicate, object_))
            graph.add((new_uri_ref, predicate, object_))

        # Update the object URIs in triples
        triples_with_old_uri_as_object = list(graph.triples((None, None, old_uri_ref)))
        for triple in triples_with_old_uri_as_object:
            subject, predicate, object_ = triple
            graph.remove((subject, predicate, object_))
            graph.add((subject, predicate, new_uri_ref))

    # Save the modified RDF/OWL file
    graph.serialize(destination=file_path, format='xml')


# Example usage
file_path = "C://Users//buciu//Desktop//penal-code//codpenal.rdf"

update_ontology_uris(file_path)
