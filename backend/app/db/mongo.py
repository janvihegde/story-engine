from pymongo import MongoClient
import os
from dotenv import load_dotenv

# 1. Load environment variables from the .env file
load_dotenv()

# 2. Get the URI safely. If missing, default to localhost (for safety)
MONGO_URI = os.getenv("MONGO_URI")

print("🔌 Connecting to MongoDB...")

try:
    if not MONGO_URI:
        raise ValueError("No MONGO_URI found in .env file")

    client = MongoClient(MONGO_URI)
    db = client["story_map"]
    events_collection = db["start"]

    # Simple ping check
    client.admin.command('ping')
    print("✅ MongoDB Connected Successfully!")

except Exception as e:
    print(f"❌ Connection Error: {e}")
    events_collection = None

def get_all_events():
    if events_collection is not None:
        return list(events_collection.find({}, {'_id': 0}))
    return []