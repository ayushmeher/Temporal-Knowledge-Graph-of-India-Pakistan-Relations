# Import necessary libraries
import pandas as pd
import networkx as nx
import spacy
from spacy import displacy
from spacy.matcher import Matcher
from spacy.tokens import Span
from spacy.util import filter_spans
import re
from itertools import combinations
from datetime import datetime

# Load historical data from csv file
def load_data(file_name):
    try:
        data = pd.read_csv(file_name)
        return data
    except Exception as e:
        print("Error occurred while loading data: ", str(e))

# Extract entities from text data
def extract_entities(nlp, text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

# Extract temporal relationships between entities
# Extract temporal relationships between entities
def extract_temporal_relationships(entities, text):
    relationships = []
    years = re.findall(r'\b\d{4}\b', text)

    # Define valid entity types for a conflict
    valid_entity_types = {"GPE", "ORG"}

    for year in years:
        for ent1, ent2 in combinations(entities, 2):
            if ent1[1] in valid_entity_types and ent2[1] in valid_entity_types:
                # Only add relationships between valid entities like GPEs (countries) or ORGs (organizations)
                if ent1[0] != ent2[0]:
                    relationships.append((ent1[0], ent2[0], year))

    return relationships

# Create a temporal knowledge graph
def create_knowledge_graph(entities, relationships):
    G = nx.MultiGraph()
    for entity in entities:
        G.add_node(entity[0], type=entity[1])
    for relationship in relationships:
        G.add_edge(relationship[0], relationship[1], year=relationship[2])
    return G


# Query the knowledge graph
def query_graph(G, query_type, entity1=None, entity2=None, year=None):
    if query_type == "conflict":
        edges = list(G.edges(data=True))
        conflict_edges = [edge for edge in edges if 'year' in edge[2] and edge[2]['year'] == year]
        return conflict_edges
    elif query_type == "evolution" and entity1 and entity2:
        edges = list(G.edges(data=True))
        evolution_edges = [edge for edge in edges if 
                           (edge[0] == entity1 and edge[1] == entity2 or edge[0] == entity2 and edge[1] == entity1) 
                           and 'year' in edge[2]]
        return evolution_edges

# Main function
def main():
    nlp = spacy.load("en_core_web_sm")
    data = load_data("historical_data.csv")
    text_data = data['text']

    entities = []
    relationships = []
    for text in text_data:
        ents = extract_entities(nlp, text)
        rels = extract_temporal_relationships(ents, text)
        entities.extend(ents)
        relationships.extend(rels)

    G = create_knowledge_graph(entities, relationships)

    query_type = "conflict"
    year = "1965"
    conflict_edges = query_graph(G, query_type, year=year)
    print("Countries in conflict during the year 1965:")
    for edge in conflict_edges:
        print(edge)

    query_type = "evolution"
    entity1 = "India"
    entity2 = "Pakistan"
    evolution_edges = query_graph(G, query_type, entity1=entity1, entity2=entity2)
    print("Evolution of relations between India and Pakistan:")
    for edge in evolution_edges:
        print(edge)

if __name__ == "__main__":
    main()

import pandas as pd
import networkx as nx
from collections import Counter
from itertools import combinations

def generate_summary_report(G, entities, relationships):
    """
    Generates a summary report of the most common relationships and entities found within the historical text data.

    Parameters:
    G (NetworkX graph): Temporal knowledge graph.
    entities (list): List of extracted entities.
    relationships (list): List of extracted temporal relationships.

    Returns:
    summary_report (dict): Summary report of the frequency of conflicts and key participants over time.
    """

    # Initialize summary report
    summary_report = {
        "conflict_frequency": {},
        "key_participants": {},
        "entity_frequency": {}
    }

    # Calculate conflict frequency over time
    years = sorted(set([rel[2] for rel in relationships]))
    for year in years:
        conflict_edges = [(edge[0], edge[1]) for edge in G.edges(data=True) if edge[2]['year'] == year]
        summary_report["conflict_frequency"][year] = len(conflict_edges)

    # Identify key participants in conflicts over time
    for year in years:
        conflict_edges = [(edge[0], edge[1]) for edge in G.edges(data=True) if edge[2]['year'] == year]
        participants = []
        for edge in conflict_edges:
            participants.extend(edge)
        key_participants = Counter(participants).most_common(5)
        summary_report["key_participants"][year] = key_participants

    # Calculate entity frequency
    entity_types = [ent[1] for ent in entities]
    entity_frequency = Counter(entity_types)
    summary_report["entity_frequency"] = dict(entity_frequency)

    return summary_report

def print_summary_report(summary_report):
    """
    Prints the summary report in a readable format.

    Parameters:
    summary_report (dict): Summary report of the frequency of conflicts and key participants over time.
    """

    print("Conflict Frequency Over Time:")
    for year, frequency in summary_report["conflict_frequency"].items():
        print(f"{year}: {frequency}")

    print("\nKey Participants in Conflicts Over Time:")
    for year, participants in summary_report["key_participants"].items():
        print(f"{year}:")
        for participant, frequency in participants:
            print(f"  {participant}: {frequency}")

    print("\nEntity Frequency:")
    for entity_type, frequency in summary_report["entity_frequency"].items():
        print(f"{entity_type}: {frequency}")

# Example usage:
G, entities, relationships = create_knowledge_graph(entities, relationships)
summary_report = generate_summary_report(G, entities, relationships)
print_summary_report(summary_report)