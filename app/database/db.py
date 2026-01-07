from __future__ import annotations
from typing import Any
from neo4j import ManagedTransaction

from ..models.character import Character
from ..models.story import Story

def init_schema(tx: ManagedTransaction) -> None:
    tx.run("CREATE CONSTRAINT id IF NOT EXISTS FOR (c:Character) REQUIRE c.id IS UNIQUE")
    tx.run("CREATE CONSTRAINT id IF NOT EXISTS FOR (s:Story) REQUIRE s.id IS UNIQUE")

# UPdate + inSERT a character node into the graph db
def upsert_character(tx: ManagedTransaction, character: Character) -> dict[str, Any]:
    cypher = """
    MERGE (c: Character {id: $id})
    SET c.name = $name,
        c.gender = $gender,
        c.race = $race,
        c.age = $age,
        c.vibe = $vibe,
        c.appearance  = $appearance,
        c.personality = $personality,
        c.backstory = $backstory,
        c.interests = $interests,
        c.abilities = $abilities
    RETURN c { .id, .name, .gender, .race, .age, .vibe, .appearance, .personality, .backstory, .interests, .abilities} AS character
    """

    rec = tx.run(cypher, character.model_dump(mode="json")).single()
    if rec is None:
        raise RuntimeError("Upsert failed: no character record returned.")
    
    return rec["character"]

# UPdate + inSERT a story node into the graph db
def upsert_story(tx: ManagedTransaction, story: Story) -> dict[str, Any]:
    query = """
    MERGE (s: Story {id: $id})
    SET s.title = $title, 
        s.description = $description,
        s.genre = $genre,
        s.owner_id = $owner_id,
        s.created_at = $created_at
    RETURN s { .id, .title, .description, .genre, .owner_id, .created_at} AS story
    """

    rec = tx.run(query, story.model_dump(mode="json")).single()
    if rec is None:
        raise RuntimeError("Upsert failed: no story record returned")
    
    return rec["story"]

# ---- Relationship Links -----

CHARACTER_TO_STORY_RELATIONSHIPS = {"PROTAGONIST", "ANTAGONIST", "DEUTERAGONIST", "MENTOR", "SIDEKICK", "LOVE INTEREST", "CONFIDANT", "SUPPORT CHARACTER", "FOIL"}

# TODO: Do we want to add details about when they come into the story on the relationship props? 
def link_character_to_story(tx, from_id: str, to_id: str, rel_type: str, rel_props: dict | None = None):
    if rel_type not in CHARACTER_TO_STORY_RELATIONSHIPS:
        raise ValueError(f"Disallowed realtionship type: {rel_type}")
    
    rel_props = rel_props or {}

    query = f"""
    MATCH (a:Character {{id: $from_id}})
    MATCH (b:Story {{id: $to_id}})
    MERGE (a)-[r:{rel_type}]->(b)
    SET r += $rel_props
    """

    tx.run(query, {"from_id": from_id, "to_id": to_id, "rel_props": rel_props})

# ------ Grab Context Functions -------

def retrieve_character_context(tx, character_id: str) -> dict[str, Any]:
    matched_character = tx.run(
        """
        MATCH (c:Character)
        WHERE c.id contains $c_id
        RETURN 
            c.name AS name,
            c.gender AS gender,
            c.race AS race,
            c.age AS age,
            c.vibe AS vibe,
            c.appearance AS appearance,
            c.personality AS personality,
            c.backstory AS backstory,
            c.interests AS interests,
            c.abilities AS abilities
        """,
        c_id=character_id,
    ).data()

    neighbors: list[dict[str, Any]] = []

    if matched_character:
        neighbors = tx.run(
            """
            MATCH (c:Character {id:$c_id})-[r]-(n)
            RETURN
                type(r) AS rel_type,
                labels(n)[0] AS neighbor_label,
                properties(n) AS neighbor_props
            LIMIT 30
            """,
            c_id=character_id,
        ).data()

    return {
        "query": character_id,
        "matched_character": matched_character,
        "neighbors": neighbors
    }