# BIOKEV — Biotech Intelligence Desk (Content Division + Command Center)

Two things live here, sharing one brand (`BioKev`, PharmD-led biotech research; positioning: *building a public body of pharmacist-led biotech research — teaching the science, catalysts, and risks behind biotech investing*).

## 1. `content-division/` — the short-form video production system
A 7-agent division that turns weekly research into short-form video for LinkedIn / TikTok / Reels / Shorts, in a bright hand-drawn style with a recurring 2D avatar and zero hype.

- `agents/` — the 7 agent briefs (Strategist, Scriptwriter, Avatar Creative Director, Storyboard, Compliance & Credibility Editor, Caption & Editing, Analytics).
- `deliverables/` — the 30-day calendar, **10 scripts**, **10 storyboards**, visual identity guide, avatar design brief, AI prompt library, production workflow, disclosure policy, and the "every report → ≥3 videos" system.
- Start at `content-division/README.md`.

## 2. `dashboard/` — the BIOKEV BIOTECH COMMAND CENTER
A working Streamlit dashboard — the visual operating system for the whole desk: 19 agents, catalyst calendar, social content calendar, research Kanban, content studio, learning tracker, watchlist/paper-portfolio. Reads from flat files; never fabricates agent work.

- Run: `cd dashboard && pip install -r requirements.txt && streamlit run app.py`
- Start at `dashboard/README.md`, schema in `dashboard/DATA_DICTIONARY.md`, update rules in `dashboard/protocols/`.

## How they connect
The content division is the "how we make videos"; the dashboard is the "command center that shows the whole operation." The dashboard's Content pages (Social Content Calendar, Content Production Studio) track exactly the pipeline the content division runs, and the catalyst→content links implement the report-to-3-videos system.

## Guardrails (everywhere)
Educational only — not investment or medical advice. No price targets, no buy/sell, no invented dates/data. Estimated catalyst dates are labeled estimated. Statistical ≠ clinical significance. All demo companies in the dashboard are fictional placeholders; replace with verified, sourced data before real use.
