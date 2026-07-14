# Deploying the BioKev Command Center on Streamlit Community Cloud

Free hosting. Model: your code lives in a GitHub repo → Streamlit Cloud runs it → you get a public URL that redeploys automatically whenever you push changes.

## What's already set up for you
- `requirements.txt` at the repo root (streamlit, pandas, plotly) — Streamlit Cloud installs these automatically.
- `.gitignore` (keeps `.venv/`, caches, and secrets out of the repo).
- The app reads bundled data from `dashboard/data_demo/data/`, so the deployed site works with no external database.

## Entrypoint (you'll need this in the deploy dialog)
- **Main file path:** `dashboard/app.py`
- **Branch:** `main`
- **Python version (Advanced settings):** 3.11

---

## Step 1 — Put the project in a GitHub repo (GitHub Desktop)
1. Open **GitHub Desktop** → sign in to GitHub (create a free account at github.com if needed).
2. **File → New Repository.**
   - Name: `biokev-command-center`
   - Local path: pick a normal spot like your **Documents** (see note below about moving the folder).
   - Leave "Initialize with README" unchecked (the project already has one).
3. Copy the entire `BioKev-Command-Center` contents into that new repo folder in Finder.
4. Back in GitHub Desktop you'll see all the files listed as changes. Add a summary like "Initial commit" → **Commit to main**.
5. Click **Publish repository** (private is fine — Community Cloud supports private repos).

## Step 2 — Deploy on Streamlit Community Cloud
1. Go to **https://share.streamlit.io** (or streamlit.io/cloud) → **Sign in with GitHub** → authorize.
2. Click **Create app** / **Deploy an app**.
3. Fill in:
   - **Repository:** `your-username/biokev-command-center`
   - **Branch:** `main`
   - **Main file path:** `dashboard/app.py`
   - **(Advanced settings) Python version:** 3.11
4. Click **Deploy**. First build takes a few minutes while it installs the packages. You'll get a URL like `https://biokev-command-center.streamlit.app`.

## Step 3 — Updating the live site later
Edit files locally → in GitHub Desktop, **Commit** then **Push** → Streamlit Cloud redeploys automatically in ~1 minute. That includes your data files: change a CSV, commit, push, and the live dashboard updates.

---

## Important caveat about the "live agent updates" workflow
Streamlit Cloud runs on an **ephemeral filesystem** — anything the app writes at runtime is wiped on restart. So the "agents edit the data files and the dashboard reflects it" loop works locally, but on Cloud the data updates by **committing new files to GitHub**, not by writing to disk on the server. That's fine for a published, always-on dashboard.

When you're ready for true live updates from a hosted app, the next step is to move the data into a hosted store (e.g., a small Postgres/Supabase DB, Google Sheets, or a cloud bucket) and point the `read_*` helpers at it. Until then: **local = live file editing; Cloud = commit-to-update.**

## Notes
- Don't commit `.venv/` — the `.gitignore` already excludes it (Streamlit builds its own environment from `requirements.txt`).
- To keep the repo private but the app shareable, that's the default on Community Cloud — the app URL is public even if the repo is private.
- If the build fails on a package, check the log in the Streamlit Cloud "Manage app" panel; usually it's a version pin in `requirements.txt`.
