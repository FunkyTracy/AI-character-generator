const THIN = new Set(["", "unknown", "n/a", "na", "none", "tbd", "-", "?"]);

const state = {
  stories: [],
  atlas: null,
  ontology: null,
  selectedId: null,
};

const title = document.getElementById("story-title");
const meta = document.getElementById("story-meta");
const description = document.getElementById("story-description");
const banner = document.getElementById("banner");
const workspace = document.getElementById("workspace");
const empty = document.getElementById("empty");
const storySelect = document.getElementById("story-select");
const sampleButton = document.getElementById("sample-button");
const filterInput = document.getElementById("filter");
const bondForm = document.getElementById("bond-form");
const bondError = document.getElementById("bond-error");

function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  }[char]));
}

function labelize(value) {
  return String(value || "")
    .toLowerCase()
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function isThin(value) {
  if (value == null) return true;
  if (Array.isArray(value)) return value.length === 0;
  return THIN.has(String(value).trim().toLowerCase());
}

function showBanner(message) {
  banner.hidden = !message;
  banner.textContent = message || "";
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });
  const text = await response.text();
  let data = null;
  if (text) {
    try {
      data = JSON.parse(text);
    } catch {
      data = { detail: text };
    }
  }
  if (!response.ok) {
    const detail = data?.detail || response.statusText;
    throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
  }
  return data;
}

function field(label, value) {
  let body;
  if (Array.isArray(value)) {
    body = value.length
      ? `<div class="chips">${value.map((item) => `<span class="chip">${esc(item)}</span>`).join("")}</div>`
      : `<p class="missing">—</p>`;
  } else {
    const thin = isThin(value);
    body = `<p class="${thin ? "missing" : ""}">${esc(thin ? "—" : value)}</p>`;
  }
  return `<p class="field-label">${label}</p>${body}`;
}

function bondLines(character) {
  const names = Object.fromEntries(state.atlas.characters.map((item) => [item.id, item.name]));
  const lines = state.atlas.bonds.filter(
    (bond) => bond.source_id === character.id || bond.target_id === character.id,
  );
  if (!lines.length) return `<p class="missing">No bonds yet.</p>`;
  return `<ul class="bond-list">${lines.map((bond) => {
    const outbound = bond.source_id === character.id;
    const otherId = outbound ? bond.target_id : bond.source_id;
    const other = names[otherId] || "Unknown";
    const note = bond.note ? `<span class="bond-note">${esc(bond.note)}</span>` : "";
    const direction = outbound ? `to ${esc(other)}` : `from ${esc(other)}`;
    return `<li><span class="chip">${esc(labelize(bond.bond_type))}</span><span>${direction}</span>${note}</li>`;
  }).join("")}</ul>`;
}

function renderDossiers() {
  const host = document.getElementById("dossiers");
  const characters = state.atlas?.characters || [];
  if (!characters.length) {
    host.innerHTML = `<p class="quiet">This story has no characters yet.</p>`;
    return;
  }

  host.innerHTML = characters.map((character) => {
    const selected = character.id === state.selectedId;
    const roles = (character.roles || []).map((role) => `<span class="role">${esc(labelize(role))}</span>`).join("");
    const gapBadge = character.gaps.length
      ? `<span class="gap-badge">${character.gaps.length} open</span>`
      : "";
    return `
      <article class="dossier${selected ? " is-selected" : ""}" id="dossier-${esc(character.id)}" data-id="${esc(character.id)}" data-name="${esc(character.name)}" aria-current="${selected}">
        <div class="dossier-head">
          <h3>${esc(character.name)}</h3>
          ${gapBadge}
        </div>
        <p class="identity">${esc(character.race)} · ${esc(character.gender)} · age ${esc(character.age)}</p>
        <div class="roles">${roles}</div>
        ${field("Vibe", character.vibe || [])}
        ${field("Appearance", character.appearance)}
        ${field("Personality", character.personality)}
        ${field("Backstory", character.backstory)}
        ${field("Interests", character.interests || [])}
        ${field("Abilities", character.abilities || [])}
        <p class="field-label">Bonds</p>
        ${bondLines(character)}
      </article>
    `;
  }).join("");

  host.querySelectorAll(".dossier").forEach((card) => {
    card.addEventListener("click", () => selectCharacter(card.dataset.id));
  });
  applyFilter();
}

function initials(name) {
  const parts = String(name || "").trim().split(/\s+/).slice(0, 2);
  const letters = parts.map((part) => part[0]?.toUpperCase() || "").join("");
  return letters || "?";
}

function layout(characters) {
  const width = 640;
  const height = 460;
  const cx = width / 2;
  const cy = height / 2 - 8;
  const radius = characters.length <= 1 ? 0 : Math.min(168, 108 + characters.length * 6);
  const start = characters.length === 2 ? 0 : -Math.PI / 2;
  return characters.map((character, index) => {
    const angle = start + (index * 2 * Math.PI) / characters.length;
    return {
      ...character,
      x: cx + radius * Math.cos(angle),
      y: cy + radius * Math.sin(angle),
    };
  });
}

function shorten(x1, y1, x2, y2, cutStart, cutEnd) {
  const dx = x2 - x1;
  const dy = y2 - y1;
  const length = Math.hypot(dx, dy) || 1;
  return [
    x1 + (dx / length) * cutStart,
    y1 + (dy / length) * cutStart,
    x2 - (dx / length) * cutEnd,
    y2 - (dy / length) * cutEnd,
  ];
}

function bendFor(bond, bonds) {
  const twins = bonds.filter((other) => (
    (other.source_id === bond.source_id && other.target_id === bond.target_id)
    || (other.source_id === bond.target_id && other.target_id === bond.source_id)
  ));
  if (twins.length < 2) return 0;
  const index = twins.indexOf(bond);
  return (index - (twins.length - 1) / 2) * 120;
}

function edgePath(bond, byId, bend) {
  const source = byId.get(bond.source_id);
  const target = byId.get(bond.target_id);
  if (!source || !target) return null;
  const [x1, y1, x2, y2] = shorten(source.x, source.y, target.x, target.y, 32, 40);
  const dx = x2 - x1;
  const dy = y2 - y1;
  const length = Math.hypot(dx, dy) || 1;
  // Keep the bend on a stable side of the pair. Reversing the arrow
  // would otherwise flip the perpendicular and stack both curves.
  const flip = source.x > target.x || (source.x === target.x && source.y > target.y);
  const sign = flip ? -1 : 1;
  const cx = (x1 + x2) / 2 + (-dy / length) * bend * sign;
  const cy = (y1 + y2) / 2 + (dx / length) * bend * sign;
  const label = bend === 0
    ? { x: (x1 + x2) / 2, y: (y1 + y2) / 2 }
    : { x: 0.25 * x1 + 0.5 * cx + 0.25 * x2, y: 0.25 * y1 + 0.5 * cy + 0.25 * y2 };
  const path = bend === 0
    ? `M ${x1} ${y1} L ${x2} ${y2}`
    : `M ${x1} ${y1} Q ${cx} ${cy} ${x2} ${y2}`;
  return { path, label };
}

function renderGraph() {
  const host = document.getElementById("graph");
  const characters = state.atlas?.characters || [];
  if (!characters.length) {
    host.innerHTML = `<p class="graph-caption">No characters to map yet.</p>`;
    return;
  }

  const placed = layout(characters);
  const byId = new Map(placed.map((character) => [character.id, character]));
  const bonds = state.atlas.bonds || [];
  const selected = state.selectedId;

  const edges = bonds.map((bond) => {
    const geometry = edgePath(bond, byId, bendFor(bond, bonds));
    if (!geometry) return "";
    const incident = !selected || bond.source_id === selected || bond.target_id === selected;
    const classes = ["edge"];
    if (selected && incident) classes.push("is-selected");
    if (selected && !incident) classes.push("is-dim");
    return `
      <path class="${classes.join(" ")}" d="${geometry.path}" marker-end="url(#arrow)"></path>
      <text class="edge-label" x="${geometry.label.x}" y="${geometry.label.y}" text-anchor="middle">${esc(labelize(bond.bond_type))}</text>
    `;
  }).join("");

  const nodes = placed.map((character) => {
    const classes = ["node"];
    if (character.id === selected) classes.push("is-selected");
    if (selected && character.id !== selected) classes.push("is-dim");
    const name = character.name.length > 18 ? `${character.name.slice(0, 16)}…` : character.name;
    return `
      <g class="${classes.join(" ")}" data-id="${esc(character.id)}" tabindex="0" role="button">
        <title>${esc(character.name)}</title>
        <circle cx="${character.x}" cy="${character.y}" r="28"></circle>
        <text x="${character.x}" y="${character.y}" text-anchor="middle" dominant-baseline="central">${esc(initials(character.name))}</text>
        <text class="node-name" x="${character.x}" y="${character.y + 46}" text-anchor="middle">${esc(name)}</text>
      </g>
    `;
  }).join("");

  const caption = bonds.length
    ? "The arrow points from the character who holds the bond."
    : "No bonds yet. Add one below and it will show up here.";

  host.innerHTML = `
    <svg viewBox="0 0 640 460" role="img" aria-label="Character relationship web">
      <defs>
        <marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
          <path d="M0,0 L7,3 L0,6 Z" fill="#d7c4ae"></path>
        </marker>
      </defs>
      ${edges}
      ${nodes}
    </svg>
    <p class="graph-caption">${caption}</p>
  `;

  host.querySelectorAll(".node").forEach((node) => {
    const choose = () => selectCharacter(node.dataset.id);
    node.addEventListener("click", choose);
    node.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        choose();
      }
    });
  });
}

function renderGaps() {
  const list = document.getElementById("gaps");
  const threads = [];
  for (const character of state.atlas?.characters || []) {
    for (const gap of character.gaps || []) {
      threads.push({ id: character.id, name: character.name, gap });
    }
  }
  document.getElementById("gap-count").textContent = String(threads.length);
  if (!threads.length) {
    list.innerHTML = `<li class="quiet">Tracked fields are filled in, and every character has a bond.</li>`;
    return;
  }
  list.innerHTML = threads.map((thread) => `
    <li>
      <button type="button" class="thread" data-id="${esc(thread.id)}">
        <span class="thread-name">${esc(thread.name)}</span>
        <span>${esc(thread.gap)}</span>
      </button>
    </li>
  `).join("");
  list.querySelectorAll(".thread").forEach((button) => {
    button.addEventListener("click", () => selectCharacter(button.dataset.id));
  });
}

function fillBondControls() {
  const characters = state.atlas?.characters || [];
  const source = document.getElementById("bond-source");
  const target = document.getElementById("bond-target");
  const kind = document.getElementById("bond-kind");
  const previousSource = source.value;
  const previousTarget = target.value;

  if (!kind.dataset.ready && state.ontology) {
    kind.innerHTML = state.ontology.bond_types
      .map((item) => `<option value="${esc(item)}">${esc(labelize(item))}</option>`)
      .join("");
    kind.dataset.ready = "true";
  }

  const options = characters
    .map((character) => `<option value="${esc(character.id)}">${esc(character.name)}</option>`)
    .join("");
  source.innerHTML = options;
  target.innerHTML = options;
  if ([...source.options].some((option) => option.value === previousSource)) source.value = previousSource;
  if ([...target.options].some((option) => option.value === previousTarget)) target.value = previousTarget;
  if (target.value === source.value) {
    const other = characters.find((character) => character.id !== source.value);
    if (other) target.value = other.id;
  }

  const canBond = characters.length >= 2;
  document.getElementById("bond-submit").disabled = !canBond;
  document.getElementById("bond-hint").textContent = canBond
    ? "Direction matters. This does not create the reverse bond."
    : "A bond needs two characters in the story.";
}

function renderAtlas() {
  const atlas = state.atlas;
  if (!atlas) return;
  title.textContent = atlas.story.title;
  const count = atlas.characters.length;
  meta.textContent = `${labelize(atlas.story.genre)} · ${count} character${count === 1 ? "" : "s"}`;
  description.textContent = atlas.story.description || "";
  workspace.hidden = false;
  empty.hidden = true;
  renderDossiers();
  renderGraph();
  renderGaps();
  fillBondControls();
}

function applyFilter() {
  const query = filterInput.value.trim().toLowerCase();
  document.querySelectorAll(".dossier").forEach((card) => {
    const name = (card.dataset.name || "").toLowerCase();
    card.hidden = Boolean(query) && !name.includes(query);
  });
}

function selectCharacter(id) {
  state.selectedId = id;
  document.querySelectorAll(".dossier").forEach((card) => {
    const selected = card.dataset.id === id;
    card.classList.toggle("is-selected", selected);
    card.setAttribute("aria-current", selected ? "true" : "false");
  });
  renderGraph();
  document.getElementById(`dossier-${CSS.escape(id)}`)?.scrollIntoView({
    behavior: "smooth",
    block: "nearest",
  });
}

function showEmpty(message) {
  workspace.hidden = true;
  empty.hidden = false;
  title.textContent = "No story yet";
  meta.textContent = "";
  description.textContent = message || "";
  storySelect.innerHTML = "";
  storySelect.disabled = true;
}

async function loadAtlas(storyId) {
  const atlas = await api(`/api/stories/${encodeURIComponent(storyId)}/atlas`);
  state.atlas = atlas;
  if (!atlas.characters.some((character) => character.id === state.selectedId)) {
    state.selectedId = atlas.characters[0]?.id ?? null;
  }
  renderAtlas();
  const url = new URL(location.href);
  url.searchParams.set("story", storyId);
  history.replaceState(null, "", url);
  storySelect.value = storyId;
}

async function loadStories(preferId) {
  state.stories = await api("/api/stories");
  if (!state.stories.length) {
    showEmpty("Load the sample story to see a cast, their dossiers, and the threads still open.");
    return;
  }
  storySelect.disabled = false;
  storySelect.innerHTML = state.stories
    .map((story) => `<option value="${esc(story.id)}">${esc(story.title)}</option>`)
    .join("");
  const known = new Set(state.stories.map((story) => story.id));
  const storyId = known.has(preferId) ? preferId : state.stories[0].id;
  await loadAtlas(storyId);
}

async function loadSample() {
  sampleButton.disabled = true;
  bondError.hidden = true;
  try {
    const atlas = await api("/api/stories/sample", { method: "POST" });
    await loadStories(atlas.story.id);
    showBanner("");
  } catch (error) {
    showBanner(error.message);
  } finally {
    sampleButton.disabled = false;
  }
}

storySelect.addEventListener("change", () => {
  loadAtlas(storySelect.value).catch((error) => showBanner(error.message));
});

filterInput.addEventListener("input", applyFilter);

sampleButton.addEventListener("click", () => {
  loadSample();
});

bondForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  bondError.hidden = true;
  const submit = document.getElementById("bond-submit");
  submit.disabled = true;
  try {
    const atlas = await api(`/api/stories/${encodeURIComponent(state.atlas.story.id)}/bonds`, {
      method: "POST",
      body: JSON.stringify({
        source_id: document.getElementById("bond-source").value,
        target_id: document.getElementById("bond-target").value,
        kind: document.getElementById("bond-kind").value,
        note: document.getElementById("bond-note").value,
      }),
    });
    document.getElementById("bond-note").value = "";
    state.atlas = atlas;
    renderAtlas();
  } catch (error) {
    bondError.hidden = false;
    bondError.textContent = error.message;
    submit.disabled = false;
  }
});

async function boot() {
  try {
    const health = await api("/api/health");
    if (!health.ok) {
      sampleButton.disabled = true;
      showEmpty("Neo4j is not connected.");
      showBanner(
        `The graph database is not reachable. Start it with docker compose up -d neo4j, and match NEO4J_PASSWORD in .env to the compose password. ${health.error || ""}`,
      );
      return;
    }
    state.ontology = await api("/api/ontology");
    const preferred = new URLSearchParams(location.search).get("story");
    await loadStories(preferred);
  } catch (error) {
    showEmpty("The ledger could not be loaded.");
    showBanner(error.message);
  }
}

boot();
