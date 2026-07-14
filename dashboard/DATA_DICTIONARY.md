# BIOKEV COMMAND CENTER — Data Dictionary

Every dashboard visual reads from these files. Update the files, not the code. All demo companies are **fictional placeholders** — replace with verified data before real use. Keep column names EXACTLY as below; the app matches on them.

Root: `dashboard/data_demo/data/` (demo). Point `BIOKEV_DATA_DIR` env var at your live copy to go live.

---

## agents/agent_status.json
Top-level: `{ "_meta": {...}, "agents": [ ... ] }`. One object per agent:

| Field | Type | Values / notes |
|---|---|---|
| id | str | stable slug, matches folder + tasks.agent |
| name / role | str | display name |
| division | str | `Research` or `Content` |
| status | str | `Active`, `Waiting`, `Blocked`, `Reviewing`, `Complete` |
| mission | str | one line |
| current_task | str | what it's doing now |
| last_updated | ISO datetime | set when the agent writes its block |
| files_created | list[str] | relative paths |
| files_editing | list[str] | in-progress files |
| open_questions | list[str] | needs from Kevin/others |
| blockers | list[str] | empty if none |
| next_action | str | next step |
| confidence | float 0–1 | self-rated |
| output_folder | str | link target for the agent's outputs |

## agents/agent_tasks.csv
`agent, task_id, title, status(pending/in_progress/completed), priority(High/Medium/Low), due_date(ISO), notes`

## calendar/biotech_catalysts.csv
`date, company, ticker, event_type, description, source_link, source_date, confidence, impact, assigned_agent, prep_work, post_event_review_date`
- `confidence` ∈ {Confirmed, Likely, Estimated, Needs Verification}. **Never label a date Confirmed without a primary source.**
- `impact` ∈ {Low, Medium, High, Binary}.
- `event_type` free text but reuse: PDUFA Decision, Advisory Committee (AdComm), AdComm Briefing Docs, Phase 1/2/3 Data, Topline Readout, Earnings, Investor Conference Presentation, Scientific Conference, Abstract Release, SEC 10-Q Filing, Watchlist Review, Thesis Review, Post-Catalyst Review.

## calendar/content_calendar.csv
Linking layer between catalysts and posts: `date, post_id, title, platform, status, linked_ticker, linked_catalyst, content_role, assigned_agent`. `content_role` e.g. pre-event explainer / day-of summary / post-event breakdown.

## content/social_posts.csv
`post_id, title, format, content_type, status, assigned_agent, source_research_file, script_file, visual_assets_needed, voiceover_status, animation_status, caption_status, scheduled_date, cta, disclosure_needed, platform, views, watch_through_pct, saves, shares, follows`
- `status` ∈ {Idea, Researching, Scripted, Compliance Review, Filmed, Animated, Edited, Scheduled, Posted, Repurposed}.
- `format` = the "show" (Catalyst in 60, PharmD Explains, Trial Design Teardown, Cash Runway Check, Bull vs Bear, Myth vs Mechanism, Post-Mortem, Meta).
- `platform` ∈ {TikTok, Instagram Reels, YouTube Shorts, LinkedIn, Newsletter, X}.
- metric columns filled by Analytics agent after posting (blank until then).

## content/video_production.csv
`video_id, title, script_file, storyboard_file, vo_status, elevenlabs_files_needed, avatar_status, tool_assets_needed, capcut_status, captions_status, platform_versions, posting_checklist`

## research/research_pipeline.csv
`ticker, company, research_type, assigned_agents(;-sep), stage, due_date, catalyst_date, priority, risk_level, source_status, output_file`
- `stage` ∈ {Idea, Assigned, Researching, Drafting, Red-Team Review, Compliance Review, Ready to Publish, Published, Post-Mortem Needed, Archived} (the Kanban columns).

## watchlists/watchlist.csv
`ticker, company, sector, market_cap, lead_program, next_catalyst, cash_runway, dilution_risk, clinical_risk, regulatory_risk, technical_setup, thesis_status, assigned_analyst, last_updated`
- `thesis_status` ∈ {Avoid, Monitor, Research further, Add to watchlist, Paper-trade candidate, Potential starter position for human review, Existing-position review}.

## portfolio/paper_portfolio.csv
`ticker, company, entry_date, shares, entry_price, current_price, unrealized_pct, thesis_status, classification, last_updated, note`. **Paper/education only — the system never places real trades.** `current_price` is demo/manual; there is no live broker link.

## learning/curriculum_progress.csv
`week, module, lessons_total, lessons_completed, quiz_score, weak_areas, status`

## learning/learning_metrics.json
`{ flashcards_due, dossiers_completed, catalyst_postmortems_completed, public_posts_published, research_streak_days, credibility_milestones:[{name, done}] }`

## alerts/alerts.json
`{ "_meta":{...}, "alerts":[ {id, type, severity(High/Medium/Low), message, related, created} ] }`
- `type` e.g. FDA date, Missing citation, Content deadline, Stale data, Incomplete report, Blocker.

---

### Honesty rules for whoever updates these files
- Set `last_updated` truthfully; the dashboard shows "Last updated from file" using it.
- If no work happened, leave status as `Waiting` / `No current task` — do not fabricate progress.
- Estimated catalyst dates MUST carry confidence `Estimated` or `Needs Verification`.
- Never invent a source_link; use the real primary source or leave a clearly-fake `.invalid` placeholder that the app flags.
