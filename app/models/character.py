"""
Character Models
================
The main feature! Characters with AI-assisted generation.

YOUR TASKS:
1. Create enums for: Gender, Mood (and any others you want)
2. Create a CharacterBase model with fields like:
   - name, gender, race, age, mood
   - appearance, personality, backstory
   - interests (list), abilities (list)
3. Create CharacterCreateInput - what the user provides to the AI
4. Create CharacterSuggestion - what the AI returns
5. Create Character - the final saved character. This is the same as the CharacterBase model, but with an id.

THINK ABOUT:
- What makes a character interesting?
- What info does the AI need to generate good suggestions?
- What relationships might characters have?

HINT: See EXAMPLES.md for Pydantic patterns
"""

from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional
import uuid

"""
Starting values will eventually go to the database, but for now we'll use this.
"""

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    NON_BINARY = "non-binary"
    OTHER = "other"

class Race(str, Enum):
    HUMAN = "human"
    ELF = "elf"
    DWARF = "dwarf"
    GNOME = "gnome"
    ORC = "orc"
    TROLL = "troll"
    HALFLING = "halfling"
    DRAGONBORN = "dragonborn"
    AASIMAR = "aasimar"
    GNOLL = "gnoll"
    KOBOLD = "kobold"
    LIZARD_PERSON = "lizard person"
    VAMPIRE = "vampire"
    WEREWOLF = "werewolf"
    CHANGELING = "changeling"
    BASTET = "bastet"

class Vibe(str, Enum):
    PLAYFUL = "playful"
    SERIOUS = "serious"
    COMEDIAN = "comedian"
    ROMANTIC = "romantic"
    SAD = "sad"
    ANGRY = "angry"
    FRIGHTENED = "frightened"
    CONFUSED = "confused"
    CURIOUS = "curious"
    ANXIOUS = "anxious"
    DEPRESSED = "depressed"
    MELODRAMATIC = "melodramatic"
    CHAOTIC = "chaotic"
    ORDERLY = "orderly"
    LAZY = "lazy"
    NERVOUS = "nervous"
    HARD_WORKING = "hard working"
    RIGHTEOUS = "righteous"
    SELFISH = "selfish"
    ALCOHOLIC = "alcoholic"
    DRUG_ADDICT = "drug addict"
    PSYCHOTIC = "psychotic"
    NARCISSISTIC = "narcissistic"
    ANTISOCIAL = "antisocial"
    SOCIAL = "social"
    SWEETHEART = "sweetheart"

class CharacterBase(BaseModel):
    name: str
    gender: Gender
    race: Race
    age: int
    vibe: list[Vibe]
    appearance: str
    personality: str
    backstory: str
    interests: list[str]
    abilities: list[str]

class CharacterCreateInput(CharacterBase):
    name: Optional[str] = None
    gender: Optional[Gender] = None
    race: Optional[Race] = None
    age: Optional[int] = None
    vibe: Optional[list[Vibe]] = None
    appearance: Optional[str] = None
    personality: Optional[str] = None
    backstory: Optional[str] = None
    interests: Optional[list[str]] = None
    abilities: Optional[list[str]] = None

class CharacterSuggestion(CharacterBase):
    pass

class Character(CharacterBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)