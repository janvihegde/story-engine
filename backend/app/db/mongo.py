from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pathlib import Path
import certifi

# Path Setup
current_file_path = Path(__file__).resolve()
project_root = current_file_path.parents[3]
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)

MONGO_URI = os.getenv("MONGO_URI")

try:
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
    db = client["storydb"]
    events_collection = db["nodes"]
    print("✅ Connected to MongoDB!")
except Exception as e:
    print(f"❌ Connection Error: {e}")
    events_collection = None

def get_events(genre=None):
    """
    Fetches events. If 'genre' is provided, it filters by that genre.
    """
    if events_collection is not None:
        query = {}
        if genre:
            # Filter: Look for events where 'genre' matches the requested one
            query["genre"] = genre.lower()
            
        return list(events_collection.find(query, {'_id': 0}))
    return []