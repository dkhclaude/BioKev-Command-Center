# Instructions for Future AI Models — Maintaining the BioKev Command Center

Read this first. Your job is to keep the dashboard's DATA current. **You almost never need to touch `app.py`.** The dashboard is data-driven: update the files, and the visuals update.

## Golden rules
1. **Edit data, not code.** Change files under the data directory (`data_demo/data/` by default, or wherever `BIOKEV_DATA_DIR` points). The app re-reads them on load / Reload.
2. **Never fabricate.** Do not invent agent progress, catalyst dates, trial results, cash figures, prices, or metrics. If unknown, use the honest labels (`Waiting`, `Needs Verification`, blank metrics). The whole system's credibility depends on this.
3. **Keep schemas exact.** Column names and JSON keys must match `DATA_DICTIONARY.md`. The app matches on them; a renamed column silently drops from the UI.
4. **Preserve formats.** ISO dates `YYYY-MM-DD`. Valid JSON (indent 2, keep all agents). CSV headers unchanged.
5. **Verify before you label.** A catalyst is `Confirmed` only with a real primary `source_link`. Everything else is `Estimated`/`Needs Verification`.

## Common tasks → which file + which protocol
| Task | File | Protocol |
|---|---|---|
| An agent finished work | `agents/agent_status.json` (+ `agent_tasks.csv`) | agent-status-update-protocol.md |
| Add/verify a catalyst | `calendar/biotech_catalysts.csv` | calendar-update-protocol.md |
| Add/schedule a post | `content/social_posts.csv` (+ `content_calendar.csv`, `video_production.csv`) | content-calendar-update-protocol.md |
| Move a research card | `research/research_pipeline.csv` (`stage` column) | DATA_DICTIONARY.md |
| Update watchlist / thesis | `watchlists/watchlist.csv` | DATA_DICTIONARY.md |
| Record learning progress | `learning/curriculum_progress.csv` + `learning_metrics.json` | DATA_DICTIONARY.md |
| Raise/clear an alert | `alerts/alerts.json` | DATA_DICTIONARY.md |
| Log post-performance metrics | metric columns in `social_posts.csv` | content-calendar + Analytics agent brief |

## Turning research into content (the core loop)
When a company dossier is completed by the research desk:
1. Create ≥3 `Idea` rows in `social_posts.csv` (Catalyst / Science / Risk angles), same `source_research_file`.
2. Add catalyst→content links in `content_calendar.csv`.
3. As each advances, update `status` and the `video_production.csv` row.
See `content-division/deliverables/report-to-3-videos-system.md`.

## If you MUST change the app
- Add a page: write a `page_x()` function and register it in `ROUTES` + `PAGES`. Keep the palette constants and `.bk-card`/`badge` helpers.
- New data file: add a `read_csv`/`read_json` call near the top and document it in `DATA_DICTIONARY.md`.
- Going live: change `TODAY = datetime.date(2026,7,13)` to `datetime.date.today()`.
- Don't hardcode data into `app.py`. Data lives in files.

## Sanity check after edits
- JSON files parse (`python -c "import json;json.load(open(...))"`).
- CSV headers match the dictionary.
- Reload the dashboard; confirm the page you touched shows the new data and no "missing/awaiting" placeholder where you expected content.
- Confirm no `Estimated` date is presenting as `Confirmed`.
