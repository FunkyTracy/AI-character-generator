"""
Story Models
============
A Story is the container for characters, settings, and factions.

YOUR TASKS:
1. Create a Genre enum with genres you like (fantasy, sci-fi, etc.)
2. Create a StoryCreate model with: title, description, genre
3. Create a Story model that adds: id, owner_id, created_at

THINK ABOUT:
- What fields would help the AI generate better characters?
- What other story metadata might be useful?

HINT: See EXAMPLES.md for Enum and Pydantic patterns
"""

from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum
import uuid


class Genre(str, Enum):
    FANTASY = "fantasy"
    SCI_FI = "sci-fi"
    HORROR = "horror"
    MYSTERY = "mystery"
    ROMANCE = "romance"
    WESTERN = "western"
    ACTION = "action"
    ADVENTURE = "adventure"
    COMEDY = "comedy"
    DRAMA = "drama"
    NON_FICTION = "non-fiction"

class StoryCreate(BaseModel):
    title: str = Field(...)
    description: str = Field(...)
    genre: str = Field(...)

class Story(StoryCreate):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    owner_id: str
    created_at: datetime = Field(default_factory=datetime.now)