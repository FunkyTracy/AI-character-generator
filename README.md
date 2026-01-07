# 🎭 AI Character Generator

A learning project for AI integration, graph databases, and Python APIs.

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
# Edit .env with your credentials

# 4. Run (once you've built it!)
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
