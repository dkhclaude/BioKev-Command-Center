# Social Content Calendar Update Protocol

Files: `data/content/social_posts.csv` (post records), `data/calendar/content_calendar.csv` (catalyst↔content links), `data/content/video_production.csv` (production tracker). Powers the Social Content Calendar and Content Production Studio pages, and the Executive content queue + compliance gate.

## Add a new post — `social_posts.csv`
`post_id, title, format, content_type, status, assigned_agent, source_research_file, script_file, visual_assets_needed, voiceover_status, animation_status, caption_status, scheduled_date, cta, disclosure_needed, platform, views, watch_through_pct, saves, shares, follows`

- `post_id`: `BK-###` (unique).
- `status` moves through: Idea → Researching → Scripted → Compliance Review → Filmed → Animated → Edited → Scheduled → Posted → Repurposed.
- `format` = a "show": Catalyst in 60, PharmD Explains, Trial Design Teardown, Cash Runway Check, Bull vs Bear, Myth vs Mechanism, Post-Mortem, Meta.
- `platform` ∈ {TikTok, Instagram Reels, YouTube Shorts, LinkedIn, Newsletter, X}.
- `disclosure_needed`: "Educational only" and/or "Position" — anything with "Position" renders a pink chip on the card.
- Leave metric columns blank until posted; the Analytics agent fills views/watch_through_pct/saves/shares/follows.

## Link a post to a catalyst — `content_calendar.csv`
`date, post_id, title, platform, status, linked_ticker, linked_catalyst, content_role, assigned_agent`
- `content_role`: pre-event explainer / day-of summary / post-event breakdown / trial-design explainer / risk breakdown / investor takeaway.
- This is how a PDUFA date becomes 3 videos, and a dossier becomes ≥3 shorts + a LinkedIn post (see `content-division/deliverables/report-to-3-videos-system.md`).

## Production tracking — `video_production.csv`
`video_id (=post_id), title, script_file, storyboard_file, vo_status, elevenlabs_files_needed, avatar_status, tool_assets_needed, capcut_status, captions_status, platform_versions, posting_checklist`

## Compliance gate
Any post with `status = Compliance Review` counts on the Executive compliance gate. Do not advance a post past Compliance Review until the Compliance & Credibility Editor records a PASS (see `disclaimer-disclosure-policy.md`). Never publish without the required disclosure + (if a ticker is named) a position disclosure.
