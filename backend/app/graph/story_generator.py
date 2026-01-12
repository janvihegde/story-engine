import sys
import os
import random

# --- PATH SETUP ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from db.mongo import get_all_events
from graph.graphbuilder import build_graph
from graph.dag_validator import validate_dag

def generate_story_path():
    # 1. Build the Graph
    graph, start_nodes = build_graph()
    
    # 2. Validate Logic (Safety Check)
    if not validate_dag(graph):
        return {"error": "Infinite Loop Detected! Please fix the story logic."}
    
    if not start_nodes:
        return {"error": "No start node found in database."}

    # 3. Create a Lookup Map (Event ID -> Full Data)
    # We need this because the graph only has IDs, but we want to return the TEXT.
    all_events = get_all_events()
    event_lookup = {e['event_id']: e for e in all_events}

    # 4. Start the Traversal
    story_path = []
    
    # Pick a random starting point (supports multiple story intros)
    current_node = random.choice(start_nodes)
    
    # 5. Walk the Graph
    while current_node:
        # Get the full event details
        event_data = event_lookup.get(current_node)
        
        if event_data:
            story_path.append({
                "event_id": event_data["event_id"],
                "text": event_data["text"]
            })
        else:
            break
            
        # Check neighbors
        neighbors = graph.get(current_node, [])
        
        if not neighbors:
            break # End of story (Leaf Node)
            
        # RANDOMIZATION: Pick one neighbor at random
        current_node = random.choice(neighbors)
        
    return story_path

# --- TEST BLOCK ---
if __name__ == "__main__":
    print("📖 Generating a new story...\n")
    story = generate_story_path()
    
    if isinstance(story, dict) and "error" in story:
        print(f"❌ {story['error']}")
    else:
        for step in story:
            print(f"🔹 {step['text']}")
            
    print("\n✅ Story Generation Complete!")