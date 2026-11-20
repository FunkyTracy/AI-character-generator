"""Idempotent sample cast so the ledger has something to show."""

import uuid

from neo4j import ManagedTransaction

from ..models.character import Character
from ..models.story import Story
from .db import link_character_to_story, upsert_character, upsert_story

SAMPLE_STORY_ID = uuid.UUID("33333333-3333-4333-8333-333333333333")
SIMON_ID = uuid.UUID("11111111-1111-4111-8111-111111111111")
FRESCHETTA_ID = uuid.UUID("22222222-2222-4222-8222-222222222222")


def seed_sample_story(tx: ManagedTransaction) -> str:
    simon = Character(
        id=SIMON_ID,
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
    freschetta = Character(
        id=FRESCHETTA_ID,
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
    story = Story(
        id=SAMPLE_STORY_ID,
        title="Ashlyn's Life",
        description="all about ashlyns life",
        genre="non-fiction",
        owner_id="ashlyn123",
    )

    upsert_character(tx, freschetta)
    upsert_character(tx, simon)
    upsert_story(tx, story)
    link_character_to_story(tx, str(simon.id), str(story.id), "SIDEKICK")
    link_character_to_story(tx, str(freschetta.id), str(story.id), "SIDEKICK")
    return str(story.id)
