# BioKev — "Every Report → ≥3 Short-Form Videos" System

A repeatable system so every company research report the Intelligence Desk produces becomes at least three short-form videos plus one LinkedIn post — with no extra research.

## The principle
A full company dossier already contains 3+ teachable stories. Don't make "a video about the company." Slice the report into single-concept videos, each mapped to a repeatable show.

## The standard slicing (minimum 3 per report)
From any company dossier, generate:

1. **The Catalyst video** — *Catalyst in 60* (S07). The next FDA/readout date, why it matters, what's binary. Source: dossier "Upcoming Catalysts".
2. **The Science video** — *Trial Design Teardown* (S08) or *PharmD Explains*. The mechanism or the pivotal trial's endpoint/design. Source: dossier "Why the Science Could Matter" / clinical section.
3. **The Risk video** — *Cash Runway Check* or *Bull vs Bear* (S09). Runway/dilution or the honest two-sided thesis. Source: dossier "Financial Survival" / "Why the Stock Could Fail".

Plus:
4. **LinkedIn insight post** — the dossier's "Thesis in one paragraph" + the single most important chart/takeaway, written insight-first.

Optional extras when the story warrants:
5. **Post-Mortem** (S10) after the catalyst resolves.
6. **Myth vs Mechanism** if there's a popular misconception to correct.

## Mapping table (dossier section → video)
| Dossier section | Show | Script template | Default length |
|---|---|---|---|
| Upcoming Catalysts | Catalyst in 60 | S07 | 60s |
| Science / mechanism | PharmD Explains | (evergreen style) | 45s |
| Clinical evidence / pivotal trial | Trial Design Teardown | S08 | 45s |
| Financial survival / runway | Cash Runway Check | S03-style | 60s |
| Bull + bear + thesis breakers | Bull vs Bear | S09 | 60s |
| After catalyst | Post-Mortem | S10 | 60s |

## Workflow hook
When a dossier lands, the Short-Form Content Strategist (Agent 01) auto-creates ≥3 `Idea` rows in `data/content/social_posts.csv`, each pointing to the same `source_research_file` but a different section + show. The Research Pipeline card for that company isn't "Published" until its 3 videos ship.

## Batching efficiency
- One filming session covers Kevin's shots for all 3 videos of a company.
- Reuse the company's ticker chip, one background plate, and the standard gag clips.
- The 3 videos release across the week (e.g., Catalyst Mon, Science Wed, Risk Fri) to sustain the arc and cross-link ("part 2 of 3 on [company]").

## Quality rule
Each of the 3 must stand alone (one concept, one payoff) AND ladder into the others. If two "videos" are really the same concept, merge them and find a genuinely different third angle from the dossier — don't pad.
