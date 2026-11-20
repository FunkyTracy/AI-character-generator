"""
Stories Routes
==============
List stories and return the character atlas for one book.
"""

from fastapi import APIRouter, Depends, HTTPException

from ..database.db import get_story_atlas, init_schema, link_bond, list_stories
from ..database.neo4j_connection import Neo4jDB
from ..database.seed import seed_sample_story
from ..models.world_elements import Bond
from .deps import get_db

router = APIRouter(prefix="/stories", tags=["stories"])


@router.get("")
def get_stories(db: Neo4jDB = Depends(get_db)):
    return db.execute_read(list_stories)


@router.post("/sample")
def load_sample_story(db: Neo4jDB = Depends(get_db)):
    # Schema changes cannot share a transaction with writes.
    db.execute_write(init_schema)
    story_id = db.execute_write(seed_sample_story)
    return db.execute_read(get_story_atlas, story_id)


@router.get("/{story_id}/atlas")
def read_atlas(story_id: str, db: Neo4jDB = Depends(get_db)):
    atlas = db.execute_read(get_story_atlas, story_id)
    if atlas is None:
        raise HTTPException(status_code=404, detail="Story not found")
    return atlas


@router.post("/{story_id}/bonds")
def create_bond(story_id: str, bond: Bond, db: Neo4jDB = Depends(get_db)):
    if bond.source_id == bond.target_id:
        raise HTTPException(status_code=400, detail="A character cannot bond to themselves")

    if db.execute_read(get_story_atlas, story_id) is None:
        raise HTTPException(status_code=404, detail="Story not found")

    created = db.execute_write(
        link_bond,
        story_id,
        bond.source_id,
        bond.target_id,
        bond.kind.value,
        bond.note.strip(),
    )
    if created is None:
        raise HTTPException(
            status_code=400,
            detail="Both characters need to belong to this story",
        )
    return db.execute_read(get_story_atlas, story_id)
