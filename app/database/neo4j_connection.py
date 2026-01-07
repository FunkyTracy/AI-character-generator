"""
Neo4j Database Connection
=========================
Connect to Neo4j and run Cypher queries.

YOUR TASKS:
1. Create a connection class that connects to Neo4j
2. Implement methods for:
   - create_user(user_data) -> creates a User node
   - find_user_by_email(email) -> finds a User node
   - create_story(story_data, owner_id) -> creates Story, links to User
   - create_character(char_data, story_id) -> creates Character, links to Story
   - create_relationship(source_id, target_id, rel_type, properties)
3. Add any query methods you need

SETUP FIRST:
1. Install Neo4j Desktop or use Neo4j Aura (free cloud)
2. Create a database and set a password
3. Practice Cypher queries in the Neo4j Browser before coding

HINT: See EXAMPLES.md for Neo4j patterns
"""

import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

class Neo4jDB:
   def __init__(self) -> None:
      uri = os.environ["NEO4J_URI"]
      user = os.environ["NEO4J_USER"]
      password = os.environ["NEO4J_PASSWORD"]
      self._driver = GraphDatabase.driver(uri, auth=(user, password))

   def close(self) -> None:
      self._driver.close()

   def execute_write(self, fn, *args, **kwargs):
      with self._driver.session() as session:
         return session.execute_write(fn, *args, **kwargs)
   
   def execute_read(self, fn, *args, **kwargs):
      with self._driver.session() as session:
         return session.execute_read(fn, *args, **kwargs)