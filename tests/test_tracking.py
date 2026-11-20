from app.models.world_elements import BondType, StoryRole
from app.tracking import tracking_gaps


def _character(**overrides):
    character = {
        "name": "Simon",
        "gender": "male",
        "race": "human",
        "age": 47,
        "vibe": ["chaotic"],
        "appearance": "brown and white fur",
        "personality": "terribly behaved",
        "backstory": "found under a car",
        "interests": ["eating"],
        "abilities": ["stealing hearts"],
    }
    character.update(overrides)
    return character


def test_unknown_backstory_is_a_gap():
    gaps = tracking_gaps(_character(backstory="unknown"), ["SIDEKICK"], 1)
    assert "Backstory is still unknown" in gaps


def test_full_character_with_a_bond_has_no_gaps():
    assert tracking_gaps(_character(), ["SIDEKICK"], 1) == []


def test_isolated_character_needs_a_bond():
    gaps = tracking_gaps(_character(), ["PROTAGONIST"], 0)
    assert gaps == ["No bonds to other characters"]


def test_missing_role_is_a_gap():
    gaps = tracking_gaps(_character(), [], 2)
    assert gaps == ["No role in this story"]


def test_relationship_tokens_are_cypher_safe():
    for kind in (*StoryRole, *BondType):
        assert " " not in kind.value
        assert kind.value.replace("_", "").isalnum()
