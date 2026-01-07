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

import json
from typing import Any
from app.ai.llm_client import LLMClient
from ..models.character import CharacterSuggestionList
from .prompt_library import CHARACTER_CREATION_PROMPT
from .helpers import extract_json_object

class CharacterGenerator:
    def __init__(self, llm: LLMClient) -> None:
        self.llm = llm
    
    def generate_character(self, user_prompt: str, context: dict[str, Any]) -> CharacterSuggestion:
        messages = [
            {
                "role": "system",
                "content": CHARACTER_CREATION_PROMPT,
            },
            {
                "role": "user",
                "content": f"Prompt:\n{user_prompt}\n\nContext JSON:\n{json.dumps(context, ensure_ascii=False)}",
            },
        ]

        raw = self.llm.chat(messages, temperature=0.7)

        print("------- Raw LLM Response --------")
        print(raw)
        print("--------- End Raw Output ---------")

        data = extract_json_object(raw)

        return CharacterSuggestionList.model_validate(data)
