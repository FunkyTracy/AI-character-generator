"""
Authentication Routes
=====================
User registration, login, and token management.

YOUR TASKS:
1. Create POST /auth/register - creates a new user
2. Create POST /auth/login - returns a JWT token
3. Create GET /auth/me - returns current user (requires token)
4. Create a dependency function to get the current user from a token

SECURITY REMINDERS:
- NEVER store plain text passwords (use bcrypt)
- Use JWT tokens for authentication
- Validate tokens on protected routes

HINT: See EXAMPLES.md for JWT and FastAPI patterns
"""

from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])

# TODO: Create your auth endpoints here
