from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
import os

# --- PATH SETUP ---
# This ensures Python can find your 'api' folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the routes we defined in api/routes.py
from api.routes import router

# 1. Initialize the App
app = FastAPI(title="Story Generator API")

# 2. CORS Setup (Crucial for React/Frontend)
# This allows your future website to talk to this Python backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all connections (good for dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Connect the Routes
app.include_router(router)

# 4. Root Endpoint (Just to check if it's alive)
@app.get("/")
def read_root():
    return {"status": "Story Engine is Online 🚀", "docs_url": "http://localhost:8000/docs"}

# 5. Server Launcher
if __name__ == "__main__":
    # Runs the server on localhost:8000 with auto-reload enabled
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)