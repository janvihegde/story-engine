import sys
import os
import random

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from db.mongo import get_events
from graph.graphbuilder import build_graph
from graph.dag_validator import validate_dag

def generate_story_path(genre="horror"):
    """
    Generates a story for the requested genre.
    Defaults to 'horror' if nothing is specified.
    """
    # 1. Build the Graph for THIS genre only
    graph, start_nodes = build_graph(genre)
    
    # 2. Safety Checks
    if not graph:
        return {"error": f"No events found for genre: '{genre}'. Did you add the data?"}
    if not start_nodes:
        return {"error": f"No start nodes found for genre: '{genre}'."}
    if not validate_dag(graph):
        return {"error": "Infinite Loop Detected in story logic!"}

    # 3. Fetch full text for lookup
    all_events = get_events(genre)
    event_lookup = {e['event_id']: e for e in all_events}

    # 4. Generate the path
    story_path = []
    current_node = random.choice(start_nodes)
    
    while current_node:
        event_data = event_lookup.get(current_node)
        
        if event_data:
            story_path.append({
                "event_id": event_data["event_id"],
                "text": event_data["text"],
                "genre": event_data.get("genre", "unknown")
            })
            
        neighbors = graph.get(current_node, [])
        if not neighbors:
            break
            
        current_node = random.choice(neighbors)
        
    return story_path