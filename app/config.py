"""
Configuration
=============
Load settings from environment variables.

YOUR TASKS:
1. Create a Settings class using pydantic-settings
2. Add fields for: Neo4j connection, OpenAI key, JWT secret
3. Load from .env file

SETUP:
1. Copy env.example.txt to .env
2. Fill in your actual values
3. NEVER commit .env to git!
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # TODO: Add your settings here
    # Example:
    # neo4j_uri: str = "bolt://localhost:7687"
    # openai_api_key: str = ""
    
    class Config:
        env_file = ".env"


settings = Settings()
