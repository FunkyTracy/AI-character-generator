"""
User Models
===========
Define Pydantic models for user data.

YOUR TASKS:
1. Create a UserCreate model (for registration) with: email, username, password
2. Create a User model (for responses) with: id, email, username, created_at
3. Add validation (email format, username length, password requirements)

HINT: See EXAMPLES.md for Pydantic patterns
"""

from pydantic import BaseModel, Field
import uuid

class CreateUser(BaseModel):
    email: str = Field(..., pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$')
    password: str = Field(..., ge=12, le=32, pattern=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])(?=.{12,32}$)[^\s]+$')

class User(CreateUser):
    id: uuid.uuid4 = Field(default_factory=uuid.uuid4)
    password: str = Field(...)  # This will be set by the algorithm we use. Likely Argon2id and will use a specified format for storing the hashes
