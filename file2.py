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

# Extract temporal relationships between entities with relationship classification
def extract_temporal_relationships(entities, text):
    relationships = set()  # Use a set to store unique relationships
    years = re.findall(r'\b\d{4}\b', text)

    # Define keywords for classifying relationships
    conflict_keywords = ["conflict", "war", "battle", "fight", "dispute"]
    alliance_keywords = ["allied", "treaty", "agreement", "partnership"]

    for year in years:
        for ent1, ent2 in combinations(entities, 2):
            if ent1[1] in ["GPE", "ORG", "PERSON"] and ent2[1] in ["GPE", "ORG", "PERSON"]:
                if ent1[0] != ent2[0]:  # Avoid self-relationships
                    # Default relationship type
                    relationship_type = "unknown"

                    # Check for keywords in text to determine the type
                    if any(keyword in text.lower() for keyword in conflict_keywords):
                        relationship_type = "conflict"
                    elif any(keyword in text.lower() for keyword in alliance_keywords):
                        relationship_type = "alliance"

                    relationships.add((ent1[0], ent2[0], year, relationship_type))
    
    return list(relationships)

# Create a temporal knowledge graph with relationship type attribute
def create_knowledge_graph(entities, relationships):
    G = nx.MultiGraph()
    for entity in entities:
        G.add_node(entity[0], type=entity[1])
    for relationship in relationships:
        # Avoid redundant edges based on nodes and year attribute
        existing_edges = G.get_edge_data(relationship[0], relationship[1], default={})
        if not any(data.get('year') == relationship[2] for data in existing_edges.values()):
            G.add_edge(relationship[0], relationship[1], year=relationship[2], type=relationship[3])
    return G

# Timeline summary function with differentiation between conflict and alliance
def timeline_summary(G):
    timeline = {}
    edges = list(G.edges(data=True))
    for edge in edges:
        year = edge[2]['year']
        relationship_type = edge[2]['type']
        if year not in timeline:
            timeline[year] = []
        timeline[year].append((edge[0], edge[1], relationship_type))
    return timeline

# Print timeline summary in a readable format with relationship types
def print_timeline_summary(timeline):
    for year in sorted(timeline.keys()):
        print(f"**{year}**")
        for event in timeline[year]:
            relationship_type = event[2]
            print(f"- {event[0]} and {event[1]}: {relationship_type.capitalize()}")
        print()

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
    timeline = timeline_summary(G)
    print_timeline_summary(timeline)

if __name__ == "__main__":
    main()
