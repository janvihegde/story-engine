import sys
import os

# Path Setup
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from db.mongo import get_events

def build_graph(genre=None):
    """
    Builds the graph for a specific genre.
    """
    # 1. Fetch only the events for this genre
    events = get_events(genre)
    
    graph = {}
    start_nodes = []
    
    for event in events:
        e_id = event.get("event_id")
        next_ids = event.get("next_event_ids", [])
        
        # Robust check for start node
        raw_start = event.get("is_start")
        is_start = raw_start is True or str(raw_start).lower() == "true"

        if e_id:
            graph[e_id] = next_ids
            if is_start:
                start_nodes.append(e_id)
                
    return graph, start_nodes