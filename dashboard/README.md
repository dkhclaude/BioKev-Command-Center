# BIOKEV BIOTECH COMMAND CENTER

A visual "AI operations room" for Kevin's biotech rebrand: the research desk, the short-form video production system, the catalyst calendar, and the learning tracker — all in one Streamlit dashboard that reads from flat files. Biotech lab meets Wall Street research floor, in the BioKev palette. **The dashboard never fabricates agent work; it only reflects what's in the data files.**

## Quick start

```bash
cd dashboard
python -m venv .venv && source .venv/bin/activate      # optional
pip install -r requirements.txt
streamlit run app.py
```

Then open the URL Streamlit prints (usually http://localhost:8501).

By default the app reads demo data from `data_demo/data/`. To point it at your own live data folder:

```bash
export BIOKEV_DATA_DIR=/path/to/your/data      # macOS/Linux
# setx BIOKEV_DATA_DIR "C:\path\to\your\data"  # Windows
streamlit run app.py
```

Copy `data_demo/data/` to a working location, then edit those files — the layout must match the schema in `DATA_DICTIONARY.md`. Regenerate fresh demo data any time with `python data_demo/seed_data.py`.

## Pages
1. **Executive Command Center** — the visual workspace: KPI tiles, operational gates (compliance / source-verification / publishing), agent status donut, alerts, today's content queue, upcoming catalysts, weekly research progress.
2. **Agent Operations Room** — all 19 agents as cards with status light, current task, files, questions, blockers, next action, confidence, and output folder.
3. **Individual Agent** — per-agent page: mission, work queue, outputs, drafts, open decisions, QC checklist, handoff note.
4. **Biotech Catalyst Calendar** — list / monthly / catalyst-only / by-company / by-risk / by-confidence. Estimated dates are always labeled; placeholder sources are flagged.
5. **Social Content Calendar** — posts across platforms, pipeline status, and the catalyst→content links.
6. **Research Pipeline Board** — Kanban across the 10 research stages.
7. **Content Production Studio** — the avatar/short-form workflow and per-video production tracker.
8. **Learning Progress** — 12-week curriculum, quiz scores, milestones, streak.
9. **Portfolio & Watchlist** — watchlist with risk chips + paper portfolio (education only, no broker link).

## Data & files
- `app.py` — the dashboard (single file).
- `styles.css` — BioKev theme (palette, cards, badges, gates).
- `assets/` — SVG logo + agent icon.
- `data_demo/data/**` — sample data (all companies fictional). See `DATA_DICTIONARY.md`.
- `data_demo/seed_data.py` — regenerates the sample data.
- `protocols/` — how agents, calendars, and content get updated; instructions for future AI models.
- `DATA_DICTIONARY.md` — the schema for every file.

## How "live" status works (honestly)
There is no always-on agent runtime here. The dashboard shows each agent's latest self-reported state from `agents/agent_status.json` and timestamps ("Last updated from file"). When a field is empty, the UI says so ("No current task", "awaiting agent output") rather than inventing progress. To make it feel live, keep the data files current — see `protocols/agent-status-update-protocol.md`.

## Extending
- Swap `TODAY` in `app.py` from the fixed demo date to `datetime.date.today()` when you go live.
- To query large data with SQL, load the CSVs into DuckDB/SQLite in the `read_*` helpers — the page code is agnostic to the source.
- Deploy on Streamlit Community Cloud, or any host, by pushing this `dashboard/` folder plus a live data directory.

Educational only. Not investment or medical advice.
