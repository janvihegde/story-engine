import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from db.mongo import get_all_events

def build_graph():
    events = get_all_events()
    graph = {}
    start_nodes = []
    
    print(f"\n🕵️ DEBUG: Found {len(events)} total events in DB.")

    for i, event in enumerate(events):
        e_id = event.get("event_id")
        next_ids = event.get("next_event_ids", [])
        
        # Grab the raw value to see what it really is
        raw_start = event.get("is_start") 
        
        # PRINT THE FIRST 3 ITEMS so we can see the data
        if i < 3:
            print(f"   Row {i}: ID='{e_id}', is_start='{raw_start}' (Type: {type(raw_start)})")

        # ROBUST CHECK: Handle Boolean True, String "true", or String "True"
        if raw_start is True or str(raw_start).lower() == "true":
            # Safety check: Don't add if ID is None
            if e_id:
                start_nodes.append(e_id)

        if e_id:
            graph[e_id] = next_ids
            
    return graph, start_nodes


# --- TESTING BLOCK ---
if __name__ == "__main__":
    try:
        print("🔌 Connecting to MongoDB and building graph...")
        g, s = build_graph()
        
        print("\n✅ SUCCESS: Graph Built!")
        print(f"📍 Start Nodes found: {s}")
        print(f"📊 Total Nodes: {len(g)}")
        
        print("\n🔍 Preview (First 3 Nodes):")
        count = 0
        for node, neighbors in g.items():
            print(f"   {node} -> {neighbors}")
            count += 1
            if count >= 3: break
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")