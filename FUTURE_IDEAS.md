# Future ideas

A running list of where this project could go. Nothing here is built unless the README or code says so. Order inside each section is rough priority, not a commitment.

## Where we are

The **character ledger** is the first slice:

- One story (book) with its cast, stored in Neo4j.
- Each character has a dossier: role, vibe, appearance, personality, backstory, interests, abilities.
- Characters are linked by directed bonds (`FRIEND`, `FAMILY`, `RIVAL`, `ENEMY`, `LOVER`, `MENTOR`, `ALLY`, `SERVES`, `KNOWS`) with an optional note.
- Open threads list the thin fields and the characters with no bonds.
- The ontology lives in `app/models/world_elements.py`.

Places, creatures, factions, and items are reserved labels. They are not stored yet.

---

## 1. Series and chronology

- **Series record.** A series has a name and a list of books. Each book has a `series_position` (the order the books are published or read).
- **Chronology is the writer's call.** Story time and series position are separate fields. A prequel gets its own in-story position, placed by the writer, so the app never guesses.
- **Drag-and-drop timeline.** The writer drags books into publication order and then into in-story order. Dragging a prequel to the front should not reorder anything else silently. Show what changed and ask.
- **Per-book character state over time.** A character can be alive in one book and gone in another. Chronology decides which state applies where.

## 2. Manuscript ingest

- Upload a book file (plain text or Markdown first, then `.docx` and `.epub`).
- Extract entities into the agreed ontology: characters, places, creatures, factions, items.
- Extract bonds and roles from the text, not just the entities.
- **Review before saving.** Extracted entities and bonds land in a review queue. The writer accepts, edits, or rejects each one before it touches the graph. This keeps the model from quietly rewriting the cast.
- **Evidence links.** Each extracted fact points to the chapter and passage it came from. The existing `evidence_node_ids` field on suggestions is the start of this.
- Chunk long books and merge the results, so a 100k-word manuscript does not depend on one prompt.

## 3. Writer direction

- Store plot ideas, themes, and tone or overtones per book and per series.
- Keep them as separate fields, not one text blob, so they can be edited and reused.
- When generating anything, combine three inputs in order:
  1. The writer's direction (themes, tone, planned plot).
  2. What ingest found in the existing book(s).
  3. The ledger: current cast, bonds, and open threads.

## 4. Character suggestion wizard

- A short guided flow that asks what the story needs before generating anything. Examples: which role is missing, which open thread should a new character close, how dark the tone is, how many bonds the new character should have.
- Generate candidates that fill those gaps. The prompt library already asks for three.
- Accepting a candidate creates the character, its role in the book, and its first bonds in one step.
- Let the writer reject a candidate with a reason ("too similar to Simon"). Feed that reason into the next round.

## 5. Plot twists and conclusions

- Suggest twists built from existing bonds. Example: a `RIVAL` who is secretly `FAMILY`, or a `MENTOR` who is the `ENEMY` of a different character.
- For each open thread, suggest a few ways it could resolve.
- Every suggestion should cite the bonds or facts it relies on, so the writer can check it against the book.

## 6. Ledger improvements

- Edit and delete characters. Currently characters are created only through the sample loader.
- Edit and remove bonds. Currently bonds can be added but not changed.
- **Change history.** Record when a detail changed and in which chapter or book.
- Chapter-level appearances: which characters appear in which chapter.
- Filter the dossiers by role or by open thread.
- Export a character sheet as Markdown or PDF.
- A wider graph view for large casts. The current web fits about a dozen characters.

## 7. Ontology growth

- Promote the reserved labels to real nodes: `Place`, `Creature`, `Faction`, `Item`.
- Add relationships between non-characters: `LOCATED_IN`, `MEMBER_OF`, `OWNS`, `RULES`.
- Decide whether a creature species is a `CreatureKind` and an individual creature is a `Character`. The current docstring says so, but nothing enforces it yet.
- Directed bond labels that read naturally both ways. `MENTOR` from A to B can display as "mentors" in one direction and "is mentored by" in the other.

## 8. Platform and hygiene

These are gaps in what exists today, not new features.

- **Owner scoping (needs fixing before any multi-user use).** `list_stories` returns every story in the database regardless of owner, and the sample story hardcodes `owner_id="ashlyn123"`. Every story route should filter on the signed-in user.
- **Real sign-in.** `app/api/auth.py` is still a stub. Ledger routes are open to anyone who can reach the server.
- **Schema setup.** `init_schema` runs `CREATE CONSTRAINT` at app startup. Moving schema changes into a dedicated migration step would make them easier to track.
- **Wire up generation.** `app/api/characters.py` only lists characters. The generate and accept endpoints from the original plan are still missing.
- **Dependency pins.** `requirements.txt` pins `fastapi==0.109.0`, `neo4j==5.16.0`, and `pydantic==2.6.0`. The local `.venv` was tested with newer versions (fastapi 0.165, neo4j 6.0.3, pydantic 2.12.5). Pick one set and make both match.
- **Tests.** Only the tracking rules have tests. The bond and atlas queries need tests against a real Neo4j, ideally in a throwaway container.
- **Compose.** `docker-compose.yml` only starts Neo4j and Ollama. If the app gets its own service, add it there with its env vars.

## 9. Model providers and local setup

The app is meant to run on one person's machine. Whoever runs it chooses which language model does the writing, and the choice lives in the app, not in code.

- **Provider choice.** Ollama (local, no key), OpenAI (ChatGPT), and Anthropic (Claude) as the first three. Add more later without touching the ledger code.
- **Current state.** `app/ai/llm_client.py` already defines a provider interface (`LLMClient`). Only `OllamaLLM` implements it, and `app/main.py` constructs it directly. Nothing reads a provider setting yet.
- **Settings screen in the web UI.** Pick the active provider and model, and see which one is active. Each provider gets its own field for an API key, plus a base URL for Ollama.
- **Key handling.**
  - Keys are saved on the local machine only. They are never written to Neo4j and never sent back to the browser after saving. The UI shows a masked value such as `sk-…a3f2`.
  - Keys are never written to logs or error messages.
  - Open question: store them in the OS keychain, or in a gitignored local settings file. The keychain is safer; a file is simpler to set up.
- **Model lists.** Show a short list of known models per provider, and let the user type a model name for anything not on the list.
- **Cost visibility.** Paid providers show a reminder that calls cost money. Ideally the app tracks rough token counts per session.
- **Config defaults.** The `.env` values (`OPENAI_MODEL`, Ollama URL, and so on) become defaults that the settings screen overrides. Any new env var needs a matching entry in `docker-compose.yml`.
- **Connection check.** A "test connection" button for each provider, so a bad key shows up on the settings screen rather than mid-generation.

## 10. Themes

Let the person using the ledger change how it looks.

- **Theme section in the UI.** A small picker, probably in the header or a settings panel, that switches the whole page. The choice is remembered on that machine.
- **Starting themes.** The current warm paper-and-sienna look becomes the default. Add a dark theme and a high-contrast theme first, then let more be added without code changes.
- **Current state.** `app/static/styles.css` already puts the main colors in CSS variables under `:root`, so a theme is mostly a new set of values. Some colors are still hard-coded and need to move into variables before a theme can change them: the banner and badge tints (`#f3e1d4`), the chip background (`#f3ece1`), the thread and warning text (`#a89886`, `#d7c4ae`, `#e07a4c`), and the bond-form background.
- **The graph follows the theme.** The relationship web uses its own map colors, so each theme needs to set those too.
- **Fonts and density.** Optional later: a font pairing and a compact or roomy spacing setting.
- **Accessibility.** Each theme should pass a contrast check for text, and the high-contrast theme should be tested with the keyboard focus ring.
- **Per-person later.** Once there is sign-in (section 8), a theme choice can follow the user rather than the browser.

---

## Parked for later

- Multiple writers or a shared series workspace.
- Image references for appearance (a reference sheet per character).
- Voice or dialogue style notes per character.
- Import from existing tools (Scrivener projects, world-building wikis).
