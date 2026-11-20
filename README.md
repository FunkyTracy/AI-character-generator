# 🎭 AI Character Generator

A learning project for AI integration, graph databases, and Python APIs.

## Character ledger

The current slice is character tracking. One book’s cast lives in Neo4j. The ledger shows every tracked detail, the directed bonds between characters, and the fields that are still thin.

Manuscript ingest, the suggestion wizard, and series chronology come after this ledger is a reliable home for characters. The plan for those is in [FUTURE_IDEAS.md](FUTURE_IDEAS.md). Places, creatures, factions, and items are reserved in `app/models/world_elements.py` and are not stored yet.

```bash
docker compose up -d neo4j
uvicorn app.main:app --reload
```

Open http://localhost:8000. If the graph is empty, use **Load sample story**.

The Docker Compose password is `superpass123`. `NEO4J_PASSWORD` in `.env` needs to match.

## 🎯 What You'll Build

An API that lets users:
- Create accounts and manage stories
- Store characters, settings, and factions in a graph database
- Generate character suggestions using AI
- Track relationships between characters

## 📁 Project Structure

```
app/
├── main.py           # FastAPI app - START HERE after models
├── config.py         # Settings from .env
├── models/           # Pydantic data models - START HERE
├── database/         # Neo4j connection
├── ai/               # OpenAI integration
└── api/              # REST endpoints
```

## 🚀 Setup

```bash
# 1. Virtual environment
python -m venv venv
source venv/bin/activate

# 2. Install dependencies  
pip install -r requirements.txt

# 3. Copy and edit config
cp env.example.txt .env
# Edit .env with your credentials.
# If you use the Compose file, set NEO4J_PASSWORD=superpass123

# 4. Start Neo4j
docker compose up -d neo4j

# 5. Run the character ledger
uvicorn app.main:app --reload
```

## 📚 Learning Path

### Phase 1: Data Models
Start in `app/models/`. Define what your data looks like.
- [ ] `user.py` - User accounts
- [ ] `story.py` - Story containers
- [ ] `character.py` - The main feature!
- [ ] `world_elements.py` - Settings, factions, relationships

### Phase 2: Database
Set up Neo4j and build `app/database/neo4j_connection.py`
- [ ] Install Neo4j Desktop or use Aura (free cloud)
- [ ] Practice Cypher queries in Neo4j Browser
- [ ] Build connection class with query methods

### Phase 3: API Basics
Build your endpoints in `app/api/`
- [ ] `auth.py` - Registration, login, JWT tokens
- [ ] `stories.py` - CRUD for stories
- [ ] Wire it up in `main.py`

### Phase 4: AI Integration
The fun part! Build `app/ai/character_generator.py`
- [ ] Connect to OpenAI
- [ ] Craft your system prompt
- [ ] Generate and parse suggestions
- [ ] Add the generation endpoint to `characters.py`

## 📖 Reference

See `EXAMPLES.md` for code patterns you can learn from!

## 🔑 Key Concepts

| Concept | Where You'll Use It |
|---------|---------------------|
| Pydantic | `models/` - data validation |
| Neo4j + Cypher | `database/` - graph queries |
| FastAPI | `api/` - REST endpoints |
| JWT | `api/auth.py` - authentication |
| OpenAI API | `ai/` - character generation |

## 💡 Tips

1. **Build incrementally** - Get one piece working before moving on
2. **Test in isolation** - Use Python shell to test small pieces
3. **Read the docs** - FastAPI, Neo4j, and OpenAI have great docs
4. **Check EXAMPLES.md** - Reference patterns when stuck

Good luck! 🚀
