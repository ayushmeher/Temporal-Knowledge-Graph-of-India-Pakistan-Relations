
# Temporal Knowledge Graph of India-Pakistan Relations

This project constructs a **Temporal Knowledge Graph** to analyze the evolution of relations between India and Pakistan. By parsing historical text data, it extracts entities (people, places, events) and models time-varying relationships to represent how interactions have changed over time.

## Project Overview

This Python-based model uses `NetworkX` and `spaCy` to build a knowledge graph where:
- **Nodes** represent entities such as people, events, and places.
- **Edges** depict temporal relationships like conflicts or alliances.
- **Querying capabilities** allow users to explore historical conflicts and alliances over time.

## Key Features

1. **Entity Extraction**: Automatically extracts people, places, and events from `historical_data.csv`.
2. **Temporal Relationship Modeling**: Uses `NetworkX` to model relationships that evolve over time.
3. **Timeline Summary Generation**: Summarizes major events, conflicts, and alliances for each year in the dataset.
4. **Interactive Querying**: Enables questions like:
   - "Which countries were in conflict during 1965?"
   - "How did India-Pakistan relations evolve from 1947 to 1999?"

## Requirements

- Python 3.x
- `NetworkX` for graph processing
- `pandas` for data handling
- `spaCy` for entity extraction

To install dependencies, run:
```bash
pip install networkx pandas spacy
python -m spacy download en_core_web_sm
```

## Code Overview

The project contains two main scripts:

1. **file1.py**: Creates the knowledge graph and allows querying of relationships.
2. **file2.py**: Adds functionality for generating a timeline summary of events, classifying relationships as conflicts or alliances.

### file1.py - Knowledge Graph Creation and Querying

- **load_data()**: Loads historical data from `historical_data.csv`.
- **extract_entities()**: Extracts entities (people, places, events) using `spaCy`.
- **extract_temporal_relationships()**: Identifies relationships between entities by year.
- **create_knowledge_graph()**: Builds a graph with nodes for each entity and edges for relationships over time.
- **query_graph()**: Queries the knowledge graph for specific relationships, such as conflicts or alliances in a given year.

### file2.py - Timeline Summary Generation

- **timeline_summary()**: Produces a timeline of events for each year, categorizing relationships as conflicts or alliances based on context.
- **print_timeline_summary()**: Displays the timeline in a readable format.

## Usage

1. **Run file1.py** to create the knowledge graph:
   ```bash
   python file1.py
   ```
   - Includes examples of querying for conflicts in specific years and the evolution of relations between entities.

2. **Run file2.py** to view a timeline summary:
   ```bash
   python file2.py
   ```
   - This script outputs major events by year, noting conflicts and alliances.

## Example Queries

- **Conflict in 1965**: Returns relationships categorized as conflicts for the year 1965.
- **Evolution of Relations**: Shows how the relationship between entities (e.g., India and Pakistan) evolved over time.

## Example Timeline Summary Output

```plaintext
**1947**
- India and Pakistan: Conflict

**1965**
- India and Pakistan: Conflict

**1971**
- India and Bangladesh: Alliance

**1999**
- India and Pakistan: Conflict
```

## Contributing

Contributions are welcome! You can enhance entity extraction, refine relationship modeling, or expand query capabilities.

## License

This project is licensed under the MIT License.
