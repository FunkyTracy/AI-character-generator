"""
Main Application
================
FastAPI application entry point.

YOUR TASKS:
1. Create the FastAPI app
2. Add CORS middleware (so a frontend can call your API)
3. Include your routers (auth, stories, characters)
4. Add startup/shutdown events for database connection
5. Create a health check endpoint

TO RUN:
    uvicorn app.main:app --reload

Then visit http://localhost:8000/docs for interactive API docs!

HINT: See EXAMPLES.md for FastAPI patterns
"""

from .database.neo4j_connection import Neo4jDB
from .database.db import init_schema, upsert_character, upsert_story, link_character_to_story
from .models.character import Character
from .models.story import Story

def main() -> None:
    db = Neo4jDB()

    simon = Character(
        name="Simon",
        gender="male",
        race="human",
        age=47,
        vibe=["chaotic", "selfish", "curious"],
        appearance="brown and white fur",
        personality="terribly behaved - viking reincarnated as a rabbit",
        backstory="found under a car when he was a baby, taken care of by foster parents, bonded to lady bun",
        interests=["destroying things", "eating"],
        abilities=["able to steal your heart"],
    )

    frechetta = Character(
        name="Freschetta",
        gender="female",
        race="human",
        age=68,
        vibe=["playful", "sweetheart", "nervous"],
        appearance="white and black fur - californian rabbit",
        personality="Sweetest lady out there. Wants to hangout and cuddle all day",
        backstory="unknown",
        interests=["pets", "cuddles", "eating"],
        abilities=["always gets the attention she demands"]
    )

    ashlynStory = Story(
        title="Ashlyn's Life",
        description="all about ashlyns life",
        genre="non-fiction",
        owner_id="ashlyn123",
    )

    try:
        db.execute_write(init_schema)

        print("Freschetta:", db.execute_write(upsert_character, frechetta))
        print("Simon:", db.execute_write(upsert_character, simon))
        print("Story:", db.execute_write(upsert_story, ashlynStory))

        db.execute_write(link_character_to_story, str(simon.id), str(ashlynStory.id), "SIDEKICK")
        db.execute_write(link_character_to_story, str(frechetta.id), str(ashlynStory.id), "SIDEKICK")
    
    finally:
        db.close()

if __name__ == "__main__":
    main()