"""
AI Character Generator
======================
Use OpenAI to generate character suggestions.

YOUR TASKS:
1. Create a class that connects to OpenAI
2. Build a system prompt that defines the AI's role
3. Build a method to create context from story + existing characters
4. Implement generate_suggestions(story, characters, user_input)
5. Parse the AI's JSON response into your CharacterSuggestion model

PROMPT ENGINEERING TIPS:
- Be specific about the output format you want (JSON structure)
- Include context about the story world
- Tell the AI about existing characters for consistency
- Experiment with temperature (0.3 = focused, 0.9 = creative)

HINT: See EXAMPLES.md for OpenAI patterns
"""

from openai import OpenAI
from app.config import settings

# TODO: Create your character generator class here
