from collections import deque

def validate_dag(graph):
    # 1. Calculate In-Degrees (Count of incoming edges for each node)
    in_degree = {node: 0 for node in graph}
    
    for node in graph:
        for neighbor in graph[node]:
            # Ensure neighbor exists in our key map to avoid KeyError
            if neighbor not in in_degree:
                in_degree[neighbor] = 0
            in_degree[neighbor] += 1
            
    # 2. Initialize Queue with nodes having 0 in-degree
    queue = deque([node for node in in_degree if in_degree[node] == 0])
    
    processed_count = 0
    
    # 3. Process the queue
    while queue:
        current = queue.popleft()
        processed_count += 1
        
        # "Remove" this node -> reduce in-degree of its neighbors
        if current in graph:
            for neighbor in graph[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
                    
    # 4. Conclusion: If we processed all nodes, it's a DAG.
    # If processed_count < total_nodes, there was a cycle (some nodes never reached 0).
    total_nodes = len(in_degree)
    
    is_valid = processed_count == total_nodes
    return is_valid

# --- TEST BLOCK ---
if __name__ == "__main__":
    # Test 1: A Valid DAG
    # A -> B -> C
    good_graph = {
        "A": ["B"],
        "B": ["C"],
        "C": []
    }
    
    # Test 2: A Cycle (Invalid)
    # A -> B -> A (Loop!)
    bad_graph = {
        "A": ["B"],
        "B": ["A"]
    }
    
    print(f"Test 1 (Good Graph): {'✅ Passed' if validate_dag(good_graph) else '❌ Failed'}")
    print(f"Test 2 (Bad Graph):  {'✅ Passed' if not validate_dag(bad_graph) else '❌ Failed'}")