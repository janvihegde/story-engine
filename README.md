# 📖 The Story Engine
### *An Interactive Narrative Generation System*

> **"Where paths diverge in yellow woods..."**

The **Story Engine** is a graph-based interactive fiction framework designed to dynamically generate, validate, and navigate branching storylines. Unlike static text adventures, this engine utilizes graph theory algorithms to ensure narrative consistency, prevent infinite loops, and offer multiple traversal modes—from random walks to structured depth-first expeditions.

---

## 🛠️ System Architecture

The system operates on a **Client-Server** architecture, separating the narrative logic (Backend) from the player experience (Frontend).

### **1. The Core (Backend)**
* **Language:** Python 3.10+
* **Framework:** FastAPI (High-performance API layer)
* **Database:** MongoDB Atlas (Stores event nodes and narrative connections)
* **Logic:** Custom Graph Traversal Algorithms (DFS, BFS, Random Walk)

### **2. The Interface (Frontend)**
* **Framework:** React (Vite)
* **Styling:** CSS3 with a custom "Dark Academia / Literary" aesthetic
* **State Management:** React Hooks for tracking narrative history and player choices

---

## ⚙️ Core Mechanics

The engine treats stories as **Directed Acyclic Graphs (DAGs)**.
* **Nodes:** Represent narrative events (e.g., "You enter a dark cave").
* **Edges:** Represent choices or consequences (e.g., "Light a torch" -> leads to next node).

### **Traversal Algorithms (The "AI Storyteller")**
The engine supports multiple modes of story generation:

1.  **🎲 Random Walk**:
    * *Behavior:* Selects a start node and randomly chooses valid neighbors until a dead end is reached.
    * *Use Case:* High replayability, chaotic fun.

2.  **⬇️ Depth-First Search (DFS)**:
    * *Behavior:* Prioritizes deep exploration of a single narrative branch.
    * *Use Case:* Finding the longest possible story path from a given start.

3.  **↔️ Breadth-First Search (BFS)**:
    * *Behavior:* Explores all immediate options level-by-level.
    * *Use Case:* Analyzing parallel timelines or "multiverse" storytelling.

4.  **📏 Smart Length (Constrained DFS)**:
    * *Behavior:* Specifically hunts for paths that are **5–8 steps long**.
    * *Use Case:* Ensuring a satisfying "Short Story" arc that isn't too short or too long.

---

## 🚀 Installation & Setup

### **Prerequisites**
* Python 3.x
* Node.js & npm
* A MongoDB Atlas Connection String

### **1. Backend Setup**
Navigate to the backend folder and set up the Python environment.

```bash
cd backend

# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure Environment
# Create a .env file in the backend/ folder and add:
