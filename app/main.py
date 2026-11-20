"""
AI Character Generator
======================
FastAPI entry point for the character ledger.

Run the ledger:
    uvicorn app.main:app --reload

Run the original generation script (needs Ollama):
    python -m app.main
"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .api import characters, meta, stories
from .database.db import init_schema
from .database.neo4j_connection import Neo4jDB

STATIC_DIR = Path(__file__).resolve().parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db = None
    app.state.db_error = None
    db = None
    try:
        db = Neo4jDB()
        db.execute_write(init_schema)
        app.state.db = db
    except Exception as exc:
        app.state.db_error = str(exc)
        if db is not None:
            db.close()
    yield
    if app.state.db is not None:
        app.state.db.close()


app = FastAPI(title="AI Character Generator", lifespan=lifespan)
app.include_router(meta.router, prefix="/api")
app.include_router(stories.router, prefix="/api")
app.include_router(characters.router, prefix="/api")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def ledger_page():
    return FileResponse(STATIC_DIR / "index.html")


def main() -> None:
    """Original script: seed two characters and ask Ollama for a third."""
    from .ai.character_generator import CharacterGenerator
    from .ai.ollama import OllamaLLM
    from .database.db import (
        link_character_to_story,
        retrieve_character_context,
        upsert_character,
        upsert_story,
    )
    from .models.character import Character
    from .models.story import Story

    db = Neo4jDB()
    llm = OllamaLLM()
    character_gen = CharacterGenerator(llm)

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
        abilities=["always gets the attention she demands"],
    )

    ashlyn_story = Story(
        title="Ashlyn's Life",
        description="all about ashlyns life",
        genre="non-fiction",
        owner_id="ashlyn123",
    )

    try:
        db.execute_write(init_schema)

        print("Freschetta:", db.execute_write(upsert_character, frechetta))
        print("Simon:", db.execute_write(upsert_character, simon))
        print("Story:", db.execute_write(upsert_story, ashlyn_story))

        db.execute_write(link_character_to_story, str(simon.id), str(ashlyn_story.id), "SIDEKICK")
        db.execute_write(link_character_to_story, str(frechetta.id), str(ashlyn_story.id), "SIDEKICK")

        context = db.execute_read(retrieve_character_context, str(frechetta.id))

        prompt = "I need a new character to be friends with Freshchetta in my story. Can you please give me some ideas?"
        raw = character_gen.generate_character(prompt, context)
        print(raw)

    finally:
        db.close()


if __name__ == "__main__":
    main()
