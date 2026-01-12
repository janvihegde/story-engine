from fastapi import APIRouter, HTTPException
from graph.story_generator import generate_story_path
from enum import Enum

router = APIRouter()

# 1. Define the Choices for the Dropdown
class Genre(str, Enum):
    horror = "horror"
    thriller = "thriller"
    comedy = "comedy"

@router.get("/generate-story")
def get_story(genre: Genre = Genre.horror):
    """
    Generates a story. 
    Select a genre from the dropdown menu!
    """
    # We use genre.value to get the actual string ("horror")
    result = generate_story_path(genre.value)
    
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
        
    return {"genre": genre, "story": result}