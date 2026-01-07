"""
Characters Routes
=================
Character CRUD and AI generation.

YOUR TASKS:
1. Basic CRUD for characters (under a story)
2. POST /stories/{id}/characters/generate - AI suggestions
3. POST /stories/{id}/characters/accept - save a suggestion
4. Endpoints for managing relationships between characters

THE AI WORKFLOW:
1. User provides requirements (CharacterCreateInput)
2. Your endpoint calls the AI generator
3. AI returns suggestions (CharacterSuggestion list)
4. User picks one, you save it as a Character

HINT: See EXAMPLES.md for patterns
"""

from fastapi import APIRouter

router = APIRouter(prefix="/stories/{story_id}/characters", tags=["characters"])

# TODO: Create your character endpoints here
