# 📖 Code Examples Reference

Use these examples to learn patterns, then write your own code in the project files!

---

## Pydantic Models

```python
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

# Enum for constrained choices
class Color(str, Enum):
    RED = "red"
    BLUE = "blue"

# Basic model
class Item(BaseModel):
    name: str                                    # Required string
    quantity: int = 1                            # Optional with default
    description: Optional[str] = None            # Optional, can be None
    tags: List[str] = Field(default_factory=list)  # Default empty list

# Model with validation
class User(BaseModel):
    email: str = Field(..., description="User email")  # ... means required
    age: int = Field(..., ge=0, le=150)               # >= 0 and <= 150
    username: str = Field(..., min_length=3, max_length=50)

# Using the models
item = Item(name="Sword")
print(item.model_dump())  # Convert to dictionary
```

---

## Neo4j Basics

```python
from neo4j import GraphDatabase

# Connect
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

# Run a query
with driver.session() as session:
    # Create a node
    result = session.run(
        "CREATE (p:Person {name: $name, age: $age}) RETURN p",
        name="Alice", 
        age=30
    )
    record = result.single()
    print(record["p"])

# Always close when done
driver.close()
```

### Common Cypher Patterns
```cypher
-- Create node
CREATE (n:Label {property: "value"})

-- Find nodes
MATCH (n:Label) WHERE n.property = "value" RETURN n

-- Create relationship
MATCH (a:Person {name: "Alice"})
MATCH (b:Person {name: "Bob"})
CREATE (a)-[:KNOWS {since: 2020}]->(b)

-- Query with relationship
MATCH (a)-[r:KNOWS]->(b) RETURN a.name, b.name, r.since
```

---

## FastAPI Basics

```python
from fastapi import FastAPI, HTTPException, Depends

app = FastAPI()

# Simple endpoint
@app.get("/")
def read_root():
    return {"message": "Hello"}

# Path parameter
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

# Request body (uses Pydantic model)
@app.post("/items/")
def create_item(item: Item):
    return item

# Raising errors
@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in database:
        raise HTTPException(status_code=404, detail="User not found")
    return database[user_id]

# Dependency injection
def get_database():
    return DatabaseConnection()

@app.get("/data")
def get_data(db = Depends(get_database)):
    return db.query("SELECT * FROM data")
```

---

## OpenAI API

```python
from openai import OpenAI

client = OpenAI(api_key="your-key")

# Basic chat completion
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Say hello!"}
    ]
)
print(response.choices[0].message.content)

# JSON mode (structured output)
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Return JSON with keys: name, age"},
        {"role": "user", "content": "Generate a character"}
    ],
    response_format={"type": "json_object"}
)
import json
data = json.loads(response.choices[0].message.content)
```

---

## JWT Authentication

```python
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"])
hashed = pwd_context.hash("mypassword")
is_valid = pwd_context.verify("mypassword", hashed)

# Create JWT token
SECRET_KEY = "your-secret"
data = {"sub": "user_id_123", "exp": datetime.utcnow() + timedelta(hours=1)}
token = jwt.encode(data, SECRET_KEY, algorithm="HS256")

# Decode JWT token
decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
user_id = decoded["sub"]
```

---

## Putting It Together

Here's how these pieces connect in your app:

```
User Request → FastAPI Endpoint → Validate with Pydantic → Query Neo4j → Return Response
                                                      ↓
                                               Call OpenAI (for AI features)
```

Good luck! Reference these examples as you build each piece.

