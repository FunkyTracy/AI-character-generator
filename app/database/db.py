from __future__ import annotations
from typing import Any
from neo4j import ManagedTransaction

from ..models.character import Character
from ..models.story import Story
from ..models.world_elements import BondType, StoryRole
from ..tracking import tracking_gaps

STORY_ROLES = {role.value for role in StoryRole}
BOND_TYPES = {bond.value for bond in BondType}

def init_schema(tx: ManagedTransaction) -> None:
    # Distinct names. A shared name made the second statement a no-op,
    # so Story.id was never constrained.
    tx.run(
        "CREATE CONSTRAINT character_id IF NOT EXISTS FOR (c:Character) REQUIRE c.id IS UNIQUE"
    )
    tx.run(
        "CREATE CONSTRAINT story_id IF NOT EXISTS FOR (s:Story) REQUIRE s.id IS UNIQUE"
    )

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

# TODO: Do we want to add details about when they come into the story on the relationship props?
def link_character_to_story(tx, from_id: str, to_id: str, rel_type: str, rel_props: dict | None = None):
    if rel_type not in STORY_ROLES:
        raise ValueError(f"Disallowed relationship type: {rel_type}")
    
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


def _plain(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _plain(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_plain(item) for item in value]
    iso = getattr(value, "iso_format", None)
    if callable(iso):
        return iso()
    return value


def list_stories(tx: ManagedTransaction) -> list[dict[str, Any]]:
    rows = tx.run(
        """
        MATCH (s:Story)
        OPTIONAL MATCH (c:Character)-[role]->(s)
        WHERE role IS NULL OR type(role) IN $roles
        WITH s, count(DISTINCT c) AS character_count
        ORDER BY s.title
        RETURN s { .id, .title, .description, .genre, .owner_id, .created_at } AS story,
               character_count
        """,
        roles=sorted(STORY_ROLES),
    ).data()

    stories: list[dict[str, Any]] = []
    for row in rows:
        story = _plain(row["story"])
        story["character_count"] = row["character_count"]
        stories.append(story)
    return stories


def get_story_atlas(tx: ManagedTransaction, story_id: str) -> dict[str, Any] | None:
    story_rec = tx.run(
        """
        MATCH (s:Story {id: $story_id})
        RETURN s { .id, .title, .description, .genre, .owner_id, .created_at } AS story
        """,
        story_id=story_id,
    ).single()
    if story_rec is None:
        return None

    character_rows = tx.run(
        """
        MATCH (c:Character)-[role]->(s:Story {id: $story_id})
        WHERE type(role) IN $roles
        WITH c, collect(DISTINCT type(role)) AS roles
        RETURN c {
            .id, .name, .gender, .race, .age, .vibe,
            .appearance, .personality, .backstory, .interests, .abilities
        } AS character, roles
        ORDER BY c.name
        """,
        story_id=story_id,
        roles=sorted(STORY_ROLES),
    ).data()

    bond_rows = tx.run(
        """
        MATCH (s:Story {id: $story_id})
        MATCH (a:Character)-[r:BOND]->(b:Character)
        WHERE (a)-[]->(s) AND (b)-[]->(s)
        RETURN DISTINCT a.id AS source_id,
                        b.id AS target_id,
                        r.kind AS bond_type,
                        r.note AS note
        """,
        story_id=story_id,
    ).data()

    bonds: list[dict[str, Any]] = []
    bond_counts: dict[str, int] = {}
    for row in bond_rows:
        if row["bond_type"] not in BOND_TYPES:
            continue
        bond = {
            "source_id": row["source_id"],
            "target_id": row["target_id"],
            "bond_type": row["bond_type"],
            "note": row["note"] or "",
        }
        bonds.append(bond)
        bond_counts[bond["source_id"]] = bond_counts.get(bond["source_id"], 0) + 1
        bond_counts[bond["target_id"]] = bond_counts.get(bond["target_id"], 0) + 1

    characters: list[dict[str, Any]] = []
    for row in character_rows:
        character = _plain(row["character"])
        roles = list(row["roles"])
        character["roles"] = roles
        character["gaps"] = tracking_gaps(
            character,
            roles,
            bond_counts.get(character["id"], 0),
        )
        characters.append(character)

    return {
        "story": _plain(story_rec["story"]),
        "characters": characters,
        "bonds": bonds,
    }


def link_bond(
    tx: ManagedTransaction,
    story_id: str,
    source_id: str,
    target_id: str,
    kind: str,
    note: str,
) -> dict[str, Any] | None:
    if kind not in BOND_TYPES:
        raise ValueError(f"Disallowed bond: {kind}")

    rec = tx.run(
        """
        MATCH (s:Story {id: $story_id})
        MATCH (a:Character {id: $source_id})-[]->(s)
        MATCH (b:Character {id: $target_id})-[]->(s)
        MERGE (a)-[r:BOND {kind: $kind}]->(b)
        SET r.note = $note
        RETURN a.id AS source_id, b.id AS target_id, r.kind AS bond_type, r.note AS note
        """,
        story_id=story_id,
        source_id=source_id,
        target_id=target_id,
        kind=kind,
        note=note,
    ).single()
    if rec is None:
        return None
    return rec.data()