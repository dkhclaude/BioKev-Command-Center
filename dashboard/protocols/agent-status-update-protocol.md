# Agent Status Update Protocol

Each agent updates its own block in `data/agents/agent_status.json` after doing work. The dashboard's Operations Room and Individual Agent pages read directly from this file.

## When to update
- After completing or advancing a task.
- When blocked (set status `Blocked`, fill `blockers`).
- When handing off (fill `next_action`).

## How to update (one agent block)
Edit the object whose `id` matches the agent. Set truthfully:

```json
{
  "id": "fda_reg",
  "name": "FDA & Regulatory Catalyst Analyst",
  "division": "Research",
  "status": "Active",                       // Active|Waiting|Blocked|Reviewing|Complete
  "current_task": "Verifying NOVX PDUFA date",
  "last_updated": "2026-07-13T10:20",       // set to NOW
  "files_created": ["outputs/agents/fda_reg/novx_catalyst.md"],
  "files_editing": ["outputs/agents/fda_reg/draft.md"],
  "open_questions": ["Awaiting primary-source confirmation"],
  "blockers": ["No confirmed PDUFA source yet"],
  "next_action": "Confirm date from FDA/company IR, then hand to scriptwriter",
  "confidence": 0.4,
  "output_folder": "outputs/agents/fda_reg/"
}
```

## Rules (honesty)
- `last_updated` must be the real time of the update. The dashboard shows it as "Last updated from file".
- If no work happened, leave `status` as `Waiting` and do not touch `last_updated`. Never invent progress.
- `confidence` is a self-rating 0–1; the UI colors it (red <0.5, yellow <0.75, green ≥0.75).
- Keep `id` stable — it links to `agent_tasks.csv` (`agent` column) and the agent's output folder.
- Also add/close rows in `data/agents/agent_tasks.csv` (`status`: pending/in_progress/completed).

## For an AI model doing the update
1. Read the whole JSON, find the agent by `id`.
2. Modify only that agent's fields.
3. Preserve valid JSON (indent 2). Do not drop other agents.
4. If you created files, list their real relative paths in `files_created`.
5. Save. The dashboard picks it up on next load / Reload.
