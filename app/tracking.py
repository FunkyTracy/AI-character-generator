"""Rules for which character details still need the writer's attention."""

from typing import Any

_THIN_TEXT = {"", "unknown", "n/a", "na", "none", "tbd", "-", "?"}


def _is_thin(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip().lower() in _THIN_TEXT
    if isinstance(value, (list, tuple)):
        return len(value) == 0
    return False


def tracking_gaps(character: dict[str, Any], roles: list[str], bond_count: int) -> list[str]:
    """Return human-readable holes in a character's tracked record.

    bond_count is the number of directed bonds that touch this character.
    """

    gaps: list[str] = []
    if _is_thin(character.get("backstory")):
        gaps.append("Backstory is still unknown")
    if _is_thin(character.get("personality")):
        gaps.append("Personality is blank")
    if _is_thin(character.get("appearance")):
        gaps.append("Appearance is blank")
    if _is_thin(character.get("vibe")):
        gaps.append("No vibe recorded")
    if _is_thin(character.get("interests")):
        gaps.append("No interests recorded")
    if _is_thin(character.get("abilities")):
        gaps.append("No abilities recorded")
    if not roles:
        gaps.append("No role in this story")
    if bond_count == 0:
        gaps.append("No bonds to other characters")
    return gaps
