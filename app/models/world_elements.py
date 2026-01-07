"""
World Elements
==============
Settings (locations), Factions (groups), and Relationships.

YOUR TASKS:
1. Create a Setting model (places in your story)
2. Create a Faction model (groups, families, organizations)
3. Create a Relationship model (connections between characters)
4. Think about what properties relationships should have

GRAPH DATABASE THINKING:
- Settings, Factions, and Characters are NODES
- Relationships are EDGES connecting nodes
- Edges can have properties too!

Example: (Hero)-[:ENEMY {since: "childhood"}]->(Villain)
"""

from pydantic import BaseModel

# TODO: Create your world element models here
 