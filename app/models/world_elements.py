"""
Story ontology
==============
Nodes and edges the ledger tracks today, plus labels reserved for later ingest.

Nodes
- Story: one book. A series is a later grouping of stories.
- Character: a person or being the story treats as a character.
- Place, Creature, Faction, Item: reserved. Manuscript ingest will create these.

Edges
- (Character)-[:PROTAGONIST|SIDEKICK|...]->(Story)
  The relationship type is the role in that book.
- (Character)-[:BOND {kind, note}]->(Character)
  Directed. A friend bond from A to B does not imply the reverse.

Chronology and series order are not stored yet. When a prequel is written,
the writer will place that Story among the others explicitly.
"""

from enum import Enum

from pydantic import BaseModel, Field


class EntityKind(str, Enum):
    CHARACTER = "character"
    PLACE = "place"
    CREATURE = "creature"
    FACTION = "faction"
    ITEM = "item"


class StoryRole(str, Enum):
    PROTAGONIST = "PROTAGONIST"
    ANTAGONIST = "ANTAGONIST"
    DEUTERAGONIST = "DEUTERAGONIST"
    MENTOR = "MENTOR"
    SIDEKICK = "SIDEKICK"
    LOVE_INTEREST = "LOVE_INTEREST"
    CONFIDANT = "CONFIDANT"
    SUPPORT = "SUPPORT"
    FOIL = "FOIL"


class BondType(str, Enum):
    FRIEND = "FRIEND"
    FAMILY = "FAMILY"
    RIVAL = "RIVAL"
    ENEMY = "ENEMY"
    LOVER = "LOVER"
    MENTOR = "MENTOR"
    ALLY = "ALLY"
    SERVES = "SERVES"
    KNOWS = "KNOWS"


class Place(BaseModel):
    """A town, region, or other location. Persisted later as a Place node."""

    name: str
    description: str = ""


class CreatureKind(BaseModel):
    """A species or monster. A named individual who acts in scenes is a Character."""

    name: str
    description: str = ""


class Faction(BaseModel):
    name: str
    description: str = ""


class Item(BaseModel):
    name: str
    description: str = ""


class Bond(BaseModel):
    source_id: str = Field(min_length=1)
    target_id: str = Field(min_length=1)
    kind: BondType
    note: str = Field(default="", max_length=280)


def ontology_catalog() -> dict:
    return {
        "entities": [
            {
                "kind": EntityKind.CHARACTER.value,
                "status": "tracked",
                "summary": "People and beings who act in the story.",
            },
            {
                "kind": EntityKind.PLACE.value,
                "status": "reserved",
                "summary": "Towns, regions, and other locations.",
            },
            {
                "kind": EntityKind.CREATURE.value,
                "status": "reserved",
                "summary": "Species and monsters. A named individual is a character.",
            },
            {
                "kind": EntityKind.FACTION.value,
                "status": "reserved",
                "summary": "Families, orders, and organizations.",
            },
            {
                "kind": EntityKind.ITEM.value,
                "status": "reserved",
                "summary": "Objects that matter to the plot.",
            },
        ],
        "story_roles": [role.value for role in StoryRole],
        "bond_types": [bond.value for bond in BondType],
    }
