# Biotech Catalyst Calendar Update Protocol

File: `data/calendar/biotech_catalysts.csv`. Powers the Catalyst Calendar page and the Executive "upcoming catalysts" + source-verification gate.

## Add a new catalyst — required fields
`date, company, ticker, event_type, description, source_link, source_date, confidence, impact, assigned_agent, prep_work, post_event_review_date`

Example row:
```
2026-08-14,Novexis Therapeutics,NOVX,PDUFA Decision,FDA decision on NVX-101 in rare metabolic disease,https://www.fda.gov/...,2026-07-01,Confirmed,Binary,fda_reg,Pre-event explainer + risk breakdown,2026-08-16
```

## Hard rules (no unsupported dates)
- `confidence` must be one of: **Confirmed, Likely, Estimated, Needs Verification**.
- Use **Confirmed** ONLY with a real primary-source `source_link` (FDA, SEC, ClinicalTrials.gov, company IR) and its `source_date`.
- If the date is a company timeline guess, use **Estimated** — the dashboard renders a pink dashed "EST." chip and, for `.invalid`/placeholder links, a ⚠️ "verify" warning.
- Never infer a PDUFA date from an estimated company timeline (mark it Estimated at best).
- `impact` ∈ {Low, Medium, High, Binary}. `assigned_agent` = an `id` from agent_status.json.
- `date` and `post_event_review_date` in ISO `YYYY-MM-DD`.

## Event types (reuse these)
PDUFA Decision · Advisory Committee (AdComm) · AdComm Briefing Docs · Phase 1/2/3 Data · Topline Readout · Earnings · Investor Conference Presentation · Scientific Conference · Abstract Release · SEC 10-Q Filing · Company Presentation · Watchlist Review · Thesis Review · Post-Catalyst Review.

## Verification workflow
1. Analyst finds the date → records the primary `source_link` + `source_date`.
2. Set `confidence` honestly.
3. Knowledge Librarian audits: any `Estimated`/`Needs Verification` row surfaces on the Executive source-verification gate until sourced.
4. After the event, the assigned agent files a Post-Catalyst Review by `post_event_review_date`.
