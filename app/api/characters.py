"""
Characters Routes
=================
Read the cast of one story. Generation and accept-suggestion come next.
"""

from fastapi import APIRouter, Depends, HTTPException

from ..database.db import get_story_atlas
from ..database.neo4j_connection import Neo4jDB
from .deps import get_db

router = APIRouter(prefix="/stories/{story_id}/characters", tags=["characters"])


@router.get("")
def list_characters(story_id: str, db: Neo4jDB = Depends(get_db)):
    atlas = db.execute_read(get_story_atlas, story_id)
    if atlas is None:
        raise HTTPException(status_code=404, detail="Story not found")
    return atlas["characters"]
