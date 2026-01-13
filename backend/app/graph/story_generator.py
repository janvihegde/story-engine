import sys
import os
import random
from collections import deque

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from db.mongo import get_events
from graph.graphbuilder import build_graph
from graph.dag_validator import validate_dag

def get_starters(genre, limit=5):
    """Fetches up to 'limit' start nodes for a genre."""
    graph, start_nodes = build_graph(genre)
    all_events = get_events(genre)
    event_lookup = {e['event_id']: e for e in all_events}
    
    starters = []
    # Shuffle to get different 5 options if there are many
    random.shuffle(start_nodes)
    
    for nid in start_nodes[:limit]:
        data = event_lookup.get(nid)
        if data:
            starters.append({
                "event_id": nid,
                "text": data.get("text", "No text"),
                "preview": data.get("text", "")[:50] + "..."
            })
    return starters

def generate_story_path(genre, method="random", start_id=None):
    # 1. Build Graph
    graph, start_nodes = build_graph(genre)
    
    # 2. Safety Checks
    if not graph:
        return {"error": f"No events found for genre: '{genre}'."}
    
    # 3. Determine Start Node
    current_node = start_id if start_id else (random.choice(start_nodes) if start_nodes else None)
    
    if not current_node or current_node not in graph:
        return {"error": "Invalid Start Node or No Start Nodes available."}

    # 4. Fetch Data
    all_events = get_events(genre)
    event_lookup = {e['event_id']: e for e in all_events}

    path_ids = []

    # --- ALGORITHM: Constrained DFS (Target 5-8 steps) ---
    # We try to find a path that ends between length 5 and 8
    if method == "smart_length" or method == "dfs":
        path_ids = find_path_with_length(graph, current_node, min_len=5, max_len=8)
    
    # Fallback to Random/BFS if smart search fails or method is random
    if not path_ids:
        # Standard Random Walk
        curr = current_node
        while curr:
            path_ids.append(curr)
            neighbors = graph.get(curr, [])
            if not neighbors:
                break
            curr = random.choice(neighbors)

    # 5. Build Result
    story_path = []
    for pid in path_ids:
        event_data = event_lookup.get(pid)
        if event_data:
            story_path.append({
                "event_id": event_data["event_id"],
                "text": event_data["text"],
                "genre": event_data.get("genre", "unknown")
            })

    return story_path

def find_path_with_length(graph, current, min_len, max_len, path=None):
    """Recursive DFS to find a path of ideal length."""
    if path is None:
        path = []
    
    path.append(current)
    
    # 1. Check if we reached a valid end state
    is_end_node = len(graph.get(current, [])) == 0
    if is_end_node:
        if len(path) >= min_len:
            return list(path) # Success!
        else:
            # Too short, backtrack
            path.pop()
            return None

    # 2. Stop if too long
    if len(path) >= max_len:
        path.pop()
        return None

    # 3. Recurse
    neighbors = graph.get(current, [])
    # Shuffle neighbors to vary the story
    random.shuffle(neighbors)
    
    for neighbor in neighbors:
        result = find_path_with_length(graph, neighbor, min_len, max_len, path)
        if result:
            return result
        

def get_node_details(genre, node_id):
    """
    Fetches the details of a specific node and its immediate neighbors (options).
    Acts as the 'Game Master' for interactive mode.
    """
    # 1. Build Graph & Fetch Data
    graph, _ = build_graph(genre)
    all_events = get_events(genre)
    event_lookup = {e['event_id']: e for e in all_events}
    
    # 2. Get Current Node Info
    current_data = event_lookup.get(node_id)
    if not current_data:
        return {"error": f"Node '{node_id}' not found."}
        
    # 3. Get Neighbors (Options)
    neighbor_ids = graph.get(node_id, [])
    options = []
    
    for nid in neighbor_ids:
        n_data = event_lookup.get(nid)
        if n_data:
            # We show a preview of the next option
            preview_text = n_data.get("text", "...")
            if len(preview_text) > 60:
                preview_text = preview_text[:60] + "..."
                
            options.append({
                "event_id": nid,
                "preview": preview_text,
                "genre": n_data.get("genre", "unknown")
            })
            
    return {
        "current_node": {
            "event_id": current_data["event_id"],
            "text": current_data["text"],
            "genre": current_data.get("genre", "unknown")
        },
        "options": options,
        "is_end": len(options) == 0
    }
            
    # Backtrack if no neighbors worked
    path.pop()
    return None