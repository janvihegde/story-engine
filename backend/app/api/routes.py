from fastapi import APIRouter, HTTPException
from graph.story_generator import generate_story_path, get_starters
from enum import Enum
from typing import Optional

router = APIRouter()

class Genre(str, Enum):
    horror = "horror"
    thriller = "thriller"
    comedy = "comedy"

class TraversalMethod(str, Enum):
    random = "random"
    smart_length = "smart_length" # New method for 5-8 steps
    bfs = "bfs"

@router.get("/start-nodes")
def get_start_options(genre: Genre = Genre.horror):
    """Returns 5 start node options for the genre."""
    return get_starters(genre.value, limit=5)

@router.get("/generate-story")
def get_story(
    genre: Genre = Genre.horror, 
    method: TraversalMethod = TraversalMethod.smart_length,
    start_id: Optional[str] = None
):
    result = generate_story_path(genre.value, method.value, start_id)
    
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
        
    return {"genre": genre, "method": method, "story": result}

# Add get_node_details to the import line:
from graph.story_generator import generate_story_path, get_starters, get_node_details

# ... (keep existing Enums)

@router.get("/story-step")
def get_step(genre: Genre, node_id: str):
    """
    Returns the text for a specific node and the choices for what comes next.
    """
    result = get_node_details(genre.value, node_id)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
        
    return result