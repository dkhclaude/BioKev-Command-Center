"""
BIOKEV BIOTECH COMMAND CENTER
A visual operating system for Kevin's biotech rebrand, research process, and
short-form video production. Streamlit + Plotly + Pandas, reading from flat files.

Run:  streamlit run app.py
Data: defaults to ./data_demo/data ; override with BIOKEV_DATA_DIR env var.

Honesty: the dashboard only reflects what is in the data files. It never fabricates
agent work. Missing/blank fields render as explicit "awaiting" labels.
"""
import os, json, datetime
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------------------------------- #
# Config & palette
# --------------------------------------------------------------------------- #
PINK, YELLOW, RED = "#FF4DB2", "#FFD12A", "#FF1E2D"
BLACK, OFFWHITE, GRAY = "#111111", "#F4F4F4", "#2B2B2B"
PLOT_SEQ = [PINK, YELLOW, RED, "#7ad1ff", "#2ecc71", "#b18cff"]

HERE = Path(__file__).parent
DATA_DIR = Path(os.environ.get("BIOKEV_DATA_DIR", HERE / "data_demo" / "data"))
TODAY = datetime.date(2026, 7, 13)  # demo "now"; swap to datetime.date.today() when live

st.set_page_config(page_title="BioKev Biotech Command Center",
                   page_icon="🧬", layout="wide", initial_sidebar_state="expanded")

def load_css():
    css = HERE / "styles.css"
    if css.exists():
        st.markdown(f"<style>{css.read_text()}</style>", unsafe_allow_html=True)
load_css()

# --------------------------------------------------------------------------- #
# Data loading (cached, resilient)
# --------------------------------------------------------------------------- #
# ttl keeps reads fast but lets edits to the data files show up on a browser
# refresh within a couple seconds — no manual cache-clear needed.
@st.cache_data(show_spinner=False, ttl=2)
def read_csv(rel):
    fp = DATA_DIR / rel
    if not fp.exists():
        return pd.DataFrame()
    return pd.read_csv(fp).fillna("")

@st.cache_data(show_spinner=False, ttl=2)
def read_json(rel):
    fp = DATA_DIR / rel
    if not fp.exists():
        return {}
    return json.loads(fp.read_text())

def file_mtime(rel):
    fp = DATA_DIR / rel
    if fp.exists():
        return datetime.datetime.fromtimestamp(fp.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
    return "missing"

agents = read_json("agents/agent_status.json")
agent_list = agents.get("agents", [])
tasks = read_csv("agents/agent_tasks.csv")
catalysts = read_csv("calendar/biotech_catalysts.csv")
content_cal = read_csv("calendar/content_calendar.csv")
posts = read_csv("content/social_posts.csv")
video_prod = read_csv("content/video_production.csv")
pipeline = read_csv("research/research_pipeline.csv")
watchlist = read_csv("watchlists/watchlist.csv")
portfolio = read_csv("portfolio/paper_portfolio.csv")
curriculum = read_csv("learning/curriculum_progress.csv")
learn_metrics = read_json("learning/learning_metrics.json")
alerts = read_json("alerts/alerts.json").get("alerts", [])

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def sclass(status):
    return str(status).lower().replace(" ", "")

def badge(status):
    return f'<span class="badge {sclass(status)}">{status}</span>'

def light(status):
    return f'<span class="light {sclass(status)}"></span>'

def kpi(num, cap):
    return f'<div class="kpi"><div class="num">{num}</div><div class="cap">{cap}</div></div>'

def chip(text, kind="demo"):
    return f'<span class="chip {kind}">{text}</span>'

def days_until(date_str):
    try:
        d = datetime.date.fromisoformat(str(date_str)[:10])
        return (d - TODAY).days
    except Exception:
        return None

def confidence_bar(conf):
    try:
        pct = int(float(conf) * 100)
    except Exception:
        pct = 0
    color = RED if pct < 50 else (YELLOW if pct < 75 else "#2ecc71")
    return (f'<div style="background:#333;border-radius:8px;height:9px;width:100%;">'
            f'<div style="background:{color};height:9px;border-radius:8px;width:{pct}%;"></div></div>'
            f'<span class="small">{pct}% confidence</span>')

def header(title_html, subtitle=None):
    st.markdown(f"<h1>{title_html}</h1>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<p class="small">{subtitle}</p>', unsafe_allow_html=True)

DEMO_NOTE = ('<span class="chip fact">LIVE</span> Watchlist, catalysts &amp; research pipeline are verified from primary '
             'sources (CELC, MNKD, VERA, CORT). Content, learning &amp; paper-portfolio tabs still show sample data.')

# --------------------------------------------------------------------------- #
# Sidebar navigation
# --------------------------------------------------------------------------- #
logo = HERE / "assets" / "biokev_logo.svg"
if logo.exists():
    st.sidebar.markdown(logo.read_text(), unsafe_allow_html=True)
st.sidebar.markdown("### Command Center")
PAGES = [
    "Executive Command Center",
    "Agent Operations Room",
    "Individual Agent",
    "Biotech Catalyst Calendar",
    "Social Content Calendar",
    "Research Pipeline Board",
    "Content Production Studio",
    "Learning Progress",
    "Portfolio & Watchlist",
]
page = st.sidebar.radio("Navigate", PAGES, label_visibility="collapsed")
st.sidebar.markdown("---")
st.sidebar.caption(f"Data source:\n`{DATA_DIR}`")
st.sidebar.caption(f"Agents file updated: {file_mtime('agents/agent_status.json')}")
if not agent_list:
    st.sidebar.error("No agent data found. Run data_demo/seed_data.py or set BIOKEV_DATA_DIR.")

# =========================================================================== #
# PAGE 1 — EXECUTIVE COMMAND CENTER (also the visual agent workspace)
# =========================================================================== #
def page_exec():
    header('BIOKEV <span class="accent">COMMAND CENTER</span>',
           "The visual operating system for the biotech rebrand · research desk meets Wall Street research floor")
    st.markdown(DEMO_NOTE, unsafe_allow_html=True)

    # KPI row
    n_active = sum(1 for a in agent_list if a["status"] == "Active")
    n_blocked = sum(1 for a in agent_list if a["status"] == "Blocked")
    upcoming = [c for _, c in catalysts.iterrows() if (days_until(c["date"]) or -99) >= 0] if len(catalysts) else []
    todays_queue = [p for _, p in posts.iterrows() if str(p["scheduled_date"])[:10] and (days_until(p["scheduled_date"]) or 99) <= 2] if len(posts) else []
    cols = st.columns(6)
    tiles = [(len(agent_list), "Agents"), (n_active, "Active"), (n_blocked, "Blocked"),
             (len(upcoming), "Upcoming catalysts"), (len(posts), "Content items"), (len(alerts), "Alerts")]
    for c, (num, cap) in zip(cols, tiles):
        c.markdown(kpi(num, cap), unsafe_allow_html=True)

    st.markdown("## Operational gates")
    g = st.columns(3)
    # Compliance gate: any post in Compliance Review or missing disclosure
    comp_pending = sum(1 for _, p in posts.iterrows() if p["status"] == "Compliance Review") if len(posts) else 0
    src_flags = sum(1 for _, c in catalysts.iterrows() if c["confidence"] in ("Estimated", "Needs Verification")) if len(catalysts) else 0
    pub_ready = sum(1 for _, p in pipeline.iterrows() if p["stage"] == "Ready to Publish") if len(pipeline) else 0
    g[0].markdown(f'<div class="gate {"warn" if comp_pending else "ok"}">Compliance gate<br>{comp_pending} in review</div>', unsafe_allow_html=True)
    g[1].markdown(f'<div class="gate {"stop" if src_flags else "ok"}">Source verification gate<br>{src_flags} dates need sourcing</div>', unsafe_allow_html=True)
    g[2].markdown(f'<div class="gate {"warn" if pub_ready else "ok"}">Publishing gate<br>{pub_ready} ready to publish</div>', unsafe_allow_html=True)

    left, right = st.columns([1.5, 1])
    with left:
        st.markdown("## Agents at a glance")
        # status distribution donut
        if agent_list:
            sdf = pd.DataFrame(agent_list)
            counts = sdf["status"].value_counts().reset_index()
            counts.columns = ["status", "n"]
            cmap = {"Active": YELLOW, "Reviewing": PINK, "Waiting": "#777",
                    "Blocked": RED, "Complete": "#2ecc71"}
            fig = px.pie(counts, names="status", values="n", hole=.6,
                         color="status", color_discrete_map=cmap)
            fig.update_layout(showlegend=True, height=260, margin=dict(t=10, b=10, l=10, r=10),
                              paper_bgcolor="rgba(0,0,0,0)", font_color=OFFWHITE,
                              legend_font_color=OFFWHITE)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("## Newest outputs by agent")
        rows = []
        for a in agent_list:
            newest = (a.get("files_created") or ["—"])[-1]
            rows.append({"Agent": a["name"], "Status": a["status"],
                         "Current task": a["current_task"], "Newest output": newest,
                         "Updated": a["last_updated"]})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True, height=330)

    with right:
        st.markdown("## Alerts")
        if not alerts:
            st.markdown('<div class="alert Low">No alerts.</div>', unsafe_allow_html=True)
        for al in alerts:
            st.markdown(
                f'<div class="alert {al["severity"]}"><b>{al["type"]}</b> · {al["severity"]}'
                f'<br>{al["message"]}<br><span class="small">{al.get("related","")}</span></div>',
                unsafe_allow_html=True)

        st.markdown("## Today's content queue")
        if len(posts):
            q = posts.copy()
            q["in_days"] = q["scheduled_date"].apply(days_until)
            q = q[(q["in_days"].notna()) & (q["in_days"] >= 0) & (q["in_days"] <= 3)].sort_values("in_days")
            if len(q) == 0:
                st.caption("Nothing scheduled in the next 3 days.")
            for _, p in q.iterrows():
                st.markdown(f'<div class="bk-card"><h4>{p["title"]}</h4>'
                            f'<div class="role">{p["platform"]} · {p["format"]}</div>'
                            f'<div class="field">{badge(p["status"])} · in {int(p["in_days"])}d</div></div>',
                            unsafe_allow_html=True)

    st.markdown("## Upcoming catalysts (next 30 days)")
    if len(catalysts):
        cc = catalysts.copy()
        cc["in_days"] = cc["date"].apply(days_until)
        cc = cc[(cc["in_days"].notna()) & (cc["in_days"] >= 0) & (cc["in_days"] <= 30)].sort_values("in_days")
        for _, c in cc.iterrows():
            flag = chip(c["confidence"], "est" if c["confidence"] in ("Estimated", "Needs Verification") else "fact")
            imp = chip(c["impact"], "binary" if c["impact"] == "Binary" else "demo")
            st.markdown(f'<div class="alert Medium"><b>{c["ticker"]}</b> · {c["event_type"]} '
                        f'· <b>{c["date"]}</b> (in {int(c["in_days"])}d) {flag} {imp}'
                        f'<br><span class="small">{c["description"]} · agent: {c["assigned_agent"]}</span></div>',
                        unsafe_allow_html=True)

    st.markdown("## Weekly research progress")
    if len(pipeline):
        order = ["Idea", "Assigned", "Researching", "Drafting", "Red-Team Review",
                 "Compliance Review", "Ready to Publish", "Published", "Post-Mortem Needed", "Archived"]
        pc = pipeline["stage"].value_counts().reindex(order).fillna(0).reset_index()
        pc.columns = ["stage", "n"]
        fig = px.bar(pc, x="stage", y="n", color_discrete_sequence=[PINK])
        fig.update_layout(height=280, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=OFFWHITE, xaxis_title="", yaxis_title="projects")
        fig.update_xaxes(tickangle=-30)
        st.plotly_chart(fig, use_container_width=True)

# =========================================================================== #
# PAGE 2 — AGENT OPERATIONS ROOM
# =========================================================================== #
def agent_card(a, compact=False):
    q = a.get("open_questions") or []
    b = a.get("blockers") or []
    fc = a.get("files_created") or []
    fe = a.get("files_editing") or []
    html = f'''<div class="bk-card">
      <h4>{light(a["status"])}{a["name"]}</h4>
      <div class="role">{a["division"]} · {badge(a["status"])}</div>
      <div class="meta">{a["current_task"] or "No current task"}</div>
      <div class="field"><span class="label">Next:</span> {a.get("next_action","—")}</div>
      <div class="field"><span class="label">Files created:</span> {len(fc)} · <span class="label">editing:</span> {(fe[0] if fe else "—")}</div>
      <div class="field"><span class="label">Open Q:</span> {(q[0] if q else "none")}</div>
      <div class="field"><span class="label">Blockers:</span> {(", ".join(b) if b else "none")}</div>
      <div class="field">{confidence_bar(a.get("confidence",0))}</div>
      <div class="small">Last updated from file: {a["last_updated"]} · 📁 {a.get("output_folder","")}</div>
    </div>'''
    return html

def page_ops():
    header('AGENT <span class="accent">OPERATIONS ROOM</span>',
           "Every agent working the biotech intelligence floor. Status is read from the latest agent files — nothing is faked.")
    st.markdown(DEMO_NOTE, unsafe_allow_html=True)
    div_filter = st.multiselect("Division", ["Research", "Content"], default=["Research", "Content"])
    stat_filter = st.multiselect("Status", ["Active", "Reviewing", "Waiting", "Blocked", "Complete"],
                                 default=["Active", "Reviewing", "Waiting", "Blocked", "Complete"])
    shown = [a for a in agent_list if a["division"] in div_filter and a["status"] in stat_filter]
    st.caption(f"{len(shown)} agents shown")
    for div in ["Research", "Content"]:
        if div not in div_filter:
            continue
        group = [a for a in shown if a["division"] == div]
        if not group:
            continue
        st.markdown(f"## {div} desk ({len(group)})")
        cols = st.columns(3)
        for i, a in enumerate(group):
            with cols[i % 3]:
                st.markdown(agent_card(a), unsafe_allow_html=True)

# =========================================================================== #
# PAGE 3 — INDIVIDUAL AGENT
# =========================================================================== #
def page_agent():
    header('INDIVIDUAL <span class="accent">AGENT</span>')
    if not agent_list:
        st.warning("No agent data.")
        return
    names = [a["name"] for a in agent_list]
    pick = st.selectbox("Select agent", names)
    a = next(x for x in agent_list if x["name"] == pick)
    st.markdown(f"<h2>{light(a['status'])}{a['name']}</h2>", unsafe_allow_html=True)
    st.markdown(f'{badge(a["status"])} &nbsp; <span class="small">{a["division"]} desk · updated {a["last_updated"]}</span>',
                unsafe_allow_html=True)
    st.markdown(f"**Mission.** {a.get('mission','')}")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Current work queue")
        at = tasks[tasks["agent"] == a["id"]] if len(tasks) else pd.DataFrame()
        if len(at):
            st.dataframe(at[["task_id", "title", "status", "priority", "due_date"]],
                         use_container_width=True, hide_index=True)
        else:
            st.caption("No tasks logged.")
        st.markdown("### Open decisions / questions")
        for q in (a.get("open_questions") or ["none"]):
            st.markdown(f"- {q}")
        st.markdown("### Blockers")
        b = a.get("blockers") or []
        st.markdown("\n".join(f"- {x}" for x in b) if b else "_none_")
    with c2:
        st.markdown("### Completed outputs")
        for f in (a.get("files_created") or []):
            st.markdown(f"- 📄 `{f}`")
        st.markdown("### Draft outputs / being edited")
        fe = a.get("files_editing") or []
        st.markdown("\n".join(f"- ✏️ `{x}`" for x in fe) if fe else "_no drafts in progress_")
        st.markdown("### Confidence")
        st.markdown(confidence_bar(a.get("confidence", 0)), unsafe_allow_html=True)

    st.markdown("### Handoff note for the next agent")
    st.info(a.get("next_action", "—"))
    st.markdown("### Quality-control checklist")
    for item in ["Sources cited (primary)", "Fact / assumption / opinion separated",
                 "Estimated dates labeled", "Peer/red-team review", "Handoff written"]:
        st.checkbox(item, value=False, key=f"qc_{a['id']}_{item}")
    st.markdown(f'<div class="bk-card"><span class="label">Output folder:</span> '
                f'<code>{a.get("output_folder","")}</code><br>'
                f'<span class="small">Open this folder to read the agent\'s Markdown files.</span></div>',
                unsafe_allow_html=True)

# =========================================================================== #
# PAGE 4 — BIOTECH CATALYST CALENDAR
# =========================================================================== #
def page_catalysts():
    header('BIOTECH <span class="accent">CATALYST CALENDAR</span>',
           "Confirmed vs estimated is always labeled. Unsupported dates are flagged, never hidden.")
    st.markdown(DEMO_NOTE, unsafe_allow_html=True)
    if not len(catalysts):
        st.warning("No catalyst data.")
        return
    view = st.radio("View", ["List", "Monthly", "Catalyst-only", "By company", "By risk", "By source confidence"],
                    horizontal=True)
    df = catalysts.copy()
    df["in_days"] = df["date"].apply(days_until)

    if view == "By company":
        tk = st.selectbox("Company", sorted(df["ticker"].unique()))
        df = df[df["ticker"] == tk]
    elif view == "By risk":
        lvl = st.selectbox("Impact level", ["Binary", "High", "Medium", "Low"])
        df = df[df["impact"] == lvl]
    elif view == "By source confidence":
        conf = st.selectbox("Confidence", ["Confirmed", "Likely", "Estimated", "Needs Verification"])
        df = df[df["confidence"] == conf]
    elif view == "Catalyst-only":
        df = df[df["event_type"].str.contains("PDUFA|AdComm|Phase|Readout|Data", case=False, na=False)]

    if view == "Monthly":
        df["month"] = df["date"].str[:7]
        fig = px.scatter(df, x="date", y="ticker", color="impact", symbol="confidence",
                         color_discrete_map={"Binary": RED, "High": PINK, "Medium": YELLOW, "Low": "#888"},
                         hover_data=["event_type", "description", "confidence"])
        fig.update_traces(marker=dict(size=16))
        fig.update_layout(height=420, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=OFFWHITE)
        st.plotly_chart(fig, use_container_width=True)

    df = df.sort_values("date")
    for _, c in df.iterrows():
        est = c["confidence"] in ("Estimated", "Needs Verification")
        conf_chip = chip(c["confidence"], "est" if est else "fact")
        imp_chip = chip(c["impact"], "binary" if c["impact"] == "Binary" else "demo")
        when = f'in {int(c["in_days"])}d' if c["in_days"] is not None and c["in_days"] >= 0 else "past"
        src_warn = ' ⚠️ <span class="small">source is a placeholder — verify</span>' if ".invalid" in str(c["source_link"]) else ""
        st.markdown(
            f'<div class="alert {"High" if c["impact"] in ("Binary","High") else "Medium"}">'
            f'<b>{c["date"]}</b> ({when}) · <b>{c["ticker"]}</b> — {c["event_type"]} {conf_chip} {imp_chip}'
            f'<br>{c["description"]}'
            f'<br><span class="small">Agent: {c["assigned_agent"]} · Prep: {c["prep_work"]} · '
            f'Review: {c["post_event_review_date"]} · Source date: {c["source_date"]}{src_warn}</span></div>',
            unsafe_allow_html=True)

# =========================================================================== #
# PAGE 5 — SOCIAL CONTENT CALENDAR
# =========================================================================== #
def page_content_cal():
    header('SOCIAL <span class="accent">CONTENT CALENDAR</span>',
           "Scheduled content across platforms, linked to the research catalysts that spawned it.")
    st.markdown(DEMO_NOTE, unsafe_allow_html=True)
    if not len(posts):
        st.warning("No content data.")
        return
    plats = sorted(posts["platform"].unique())
    fp = st.multiselect("Platform", plats, default=plats)
    df = posts[posts["platform"].isin(fp)].copy()

    st.markdown("## Pipeline status")
    stages = ["Idea", "Researching", "Scripted", "Compliance Review", "Filmed",
              "Animated", "Edited", "Scheduled", "Posted", "Repurposed"]
    sc = df["status"].value_counts().reindex(stages).fillna(0).reset_index()
    sc.columns = ["status", "n"]
    fig = px.bar(sc, x="status", y="n", color_discrete_sequence=[YELLOW])
    fig.update_layout(height=250, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=OFFWHITE, xaxis_title="", yaxis_title="posts")
    fig.update_xaxes(tickangle=-30)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("## Catalyst → content links")
    if len(content_cal):
        st.dataframe(content_cal[["date", "post_id", "linked_ticker", "linked_catalyst",
                                  "content_role", "platform", "status"]],
                     use_container_width=True, hide_index=True)

    st.markdown("## Scheduled posts")
    df = df.sort_values("scheduled_date")
    for _, p in df.iterrows():
        disc = chip(p["disclosure_needed"], "est" if "Position" in str(p["disclosure_needed"]) else "fact")
        st.markdown(
            f'<div class="bk-card"><h4>{p["title"]}</h4>'
            f'<div class="role">{p["platform"]} · {p["format"]} · {p["content_type"]}</div>'
            f'<div class="field">{badge(p["status"])} · scheduled {p["scheduled_date"]} · agent: {p["assigned_agent"]}</div>'
            f'<div class="field"><span class="label">VO:</span> {p["voiceover_status"]} · '
            f'<span class="label">Anim:</span> {p["animation_status"]} · '
            f'<span class="label">Caption:</span> {p["caption_status"]}</div>'
            f'<div class="field"><span class="label">Source:</span> <code>{p["source_research_file"]}</code> · '
            f'<span class="label">Script:</span> <code>{p["script_file"]}</code></div>'
            f'<div class="field"><span class="label">CTA:</span> {p["cta"]} · {disc}</div></div>',
            unsafe_allow_html=True)

# =========================================================================== #
# PAGE 6 — RESEARCH PIPELINE BOARD (Kanban)
# =========================================================================== #
def page_pipeline():
    header('RESEARCH <span class="accent">PIPELINE BOARD</span>',
           "Kanban across the research lifecycle. Cards carry catalyst dates, risk, and source status.")
    st.markdown(DEMO_NOTE, unsafe_allow_html=True)
    if not len(pipeline):
        st.warning("No pipeline data.")
        return
    stages = ["Idea", "Assigned", "Researching", "Drafting", "Red-Team Review",
              "Compliance Review", "Ready to Publish", "Published", "Post-Mortem Needed", "Archived"]
    cols = st.columns(len(stages))
    prio_color = {"High": RED, "Medium": YELLOW, "Low": "#888"}
    for col, stage in zip(cols, stages):
        with col:
            group = pipeline[pipeline["stage"] == stage]
            st.markdown(f'<div style="color:{PINK};font-weight:800;font-size:.8rem;'
                        f'text-transform:uppercase;border-bottom:2px solid {PINK};margin-bottom:6px;">'
                        f'{stage} ({len(group)})</div>', unsafe_allow_html=True)
            for _, r in group.iterrows():
                pc = prio_color.get(r["priority"], "#888")
                st.markdown(
                    f'<div style="background:#161616;border-radius:12px;padding:8px;margin-bottom:8px;'
                    f'border-left:5px solid {pc};font-size:.76rem;">'
                    f'<b>{r["ticker"]}</b> <span class="small">{r["research_type"]}</span><br>'
                    f'<span class="small">▸ {r["assigned_agents"]}</span><br>'
                    f'<span class="small">catalyst {r["catalyst_date"]}</span><br>'
                    f'{chip(r["risk_level"], "binary" if r["risk_level"]=="Binary" else "demo")}'
                    f'{chip(r["source_status"], "fact" if r["source_status"]=="Sourced" else "est")}</div>',
                    unsafe_allow_html=True)

# =========================================================================== #
# PAGE 7 — CONTENT PRODUCTION STUDIO
# =========================================================================== #
def page_studio():
    header('CONTENT PRODUCTION <span class="accent">STUDIO</span>',
           "Avatar + short-form workflow: research → script → compliance → storyboard → VO → animation → captions → schedule → analytics.")
    st.markdown(DEMO_NOTE, unsafe_allow_html=True)
    steps = ["Research", "Script", "Compliance", "Storyboard", "Voiceover", "Animation", "Captions", "Schedule", "Analytics"]
    st.markdown("## Workflow")
    scols = st.columns(len(steps))
    for c, s in zip(scols, steps):
        c.markdown(f'<div class="gate ok" style="font-size:.66rem;padding:8px 4px;">{s}</div>', unsafe_allow_html=True)

    if len(video_prod):
        st.markdown("## Production tracker")
        st.dataframe(video_prod[["video_id", "title", "vo_status", "avatar_status",
                                 "captions_status", "platform_versions", "posting_checklist"]],
                     use_container_width=True, hide_index=True)

        st.markdown("## Per-video status")
        for _, v in video_prod.iterrows():
            st.markdown(
                f'<div class="bk-card"><h4>{v["video_id"]} — {v["title"]}</h4>'
                f'<div class="field"><span class="label">Script:</span> <code>{v["script_file"]}</code> · '
                f'<span class="label">Storyboard:</span> <code>{v["storyboard_file"]}</code></div>'
                f'<div class="field"><span class="label">ElevenLabs:</span> {v["elevenlabs_files_needed"]}</div>'
                f'<div class="field"><span class="label">Avatar/anim:</span> {v["avatar_status"]} · '
                f'<span class="label">Tools:</span> {v["tool_assets_needed"]}</div>'
                f'<div class="field"><span class="label">CapCut/captions:</span> {v["capcut_status"]} · '
                f'<span class="label">Versions:</span> {v["platform_versions"]} · '
                f'<span class="label">Checklist:</span> {badge_studio(v["posting_checklist"])}</div></div>',
                unsafe_allow_html=True)

def badge_studio(v):
    cls = "complete" if v == "Complete" else "waiting"
    return f'<span class="badge {cls}">{v}</span>'

# =========================================================================== #
# PAGE 8 — LEARNING PROGRESS
# =========================================================================== #
def page_learning():
    header('LEARNING <span class="accent">PROGRESS</span>',
           "Kevin's 12-week path to becoming a credible biotech investor.")
    if len(curriculum):
        done = pd.to_numeric(curriculum["lessons_completed"], errors="coerce").fillna(0).sum()
        total = pd.to_numeric(curriculum["lessons_total"], errors="coerce").fillna(0).sum()
        pct = int(done / total * 100) if total else 0
        m = learn_metrics
        cols = st.columns(5)
        vals = [(f"{pct}%", "Curriculum"), (m.get("dossiers_completed", 0), "Dossiers"),
                (m.get("catalyst_postmortems_completed", 0), "Post-mortems"),
                (m.get("public_posts_published", 0), "Posts published"),
                (f'{m.get("research_streak_days", 0)}d', "Research streak")]
        for c, (n, cap) in zip(cols, vals):
            c.markdown(kpi(n, cap), unsafe_allow_html=True)

        st.markdown("## 12-week curriculum")
        cur = curriculum.copy()
        cur["completed"] = pd.to_numeric(cur["lessons_completed"], errors="coerce").fillna(0)
        cur["total"] = pd.to_numeric(cur["lessons_total"], errors="coerce").fillna(0)
        cur["pct"] = (cur["completed"] / cur["total"] * 100).round()
        fig = px.bar(cur, x="pct", y="module", orientation="h", color="pct",
                     color_continuous_scale=[[0, GRAY], [.5, YELLOW], [1, PINK]],
                     hover_data=["status", "quiz_score", "weak_areas"])
        fig.update_layout(height=430, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=OFFWHITE, xaxis_title="% complete", yaxis_title="",
                          coloraxis_showscale=False, yaxis={"categoryorder": "array",
                          "categoryarray": list(cur["module"])[::-1]})
        st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### Quiz scores & weak areas")
            show = cur[cur["quiz_score"] != ""][["week", "module", "quiz_score", "weak_areas", "status"]]
            st.dataframe(show, use_container_width=True, hide_index=True)
        with c2:
            st.markdown("### Credibility milestones")
            for ms in learn_metrics.get("credibility_milestones", []):
                mark = "✅" if ms["done"] else "⬜"
                st.markdown(f"{mark} {ms['name']}")
            st.markdown(f'<div class="small">Flashcards due: {learn_metrics.get("flashcards_due",0)}</div>',
                        unsafe_allow_html=True)
    else:
        st.warning("No curriculum data.")

# =========================================================================== #
# PAGE 9 — PORTFOLIO & WATCHLIST
# =========================================================================== #
def page_portfolio():
    header('PORTFOLIO & <span class="accent">WATCHLIST</span>',
           "Watchlist + paper portfolio. Education only — the system never places real trades.")
    st.markdown(DEMO_NOTE, unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Watchlist", "Paper portfolio"])
    with tab1:
        if len(watchlist):
            thesis = st.multiselect("Thesis status", sorted(watchlist["thesis_status"].unique()),
                                    default=sorted(watchlist["thesis_status"].unique()))
            wf = watchlist[watchlist["thesis_status"].isin(thesis)]
            for _, w in wf.iterrows():
                cd = days_until(str(w["next_catalyst"]).split(" ")[-1])
                cd_txt = f"in {cd}d" if cd is not None and cd >= 0 else ""
                st.markdown(
                    f'<div class="bk-card"><h4>{w["ticker"]} — {w["company"]}</h4>'
                    f'<div class="role">{w["sector"]} · {w["market_cap"]} · {w["thesis_status"]}</div>'
                    f'<div class="field"><span class="label">Lead:</span> {w["lead_program"]} · '
                    f'<span class="label">Next catalyst:</span> {w["next_catalyst"]} {cd_txt}</div>'
                    f'<div class="field"><span class="label">Runway:</span> {w["cash_runway"]} · '
                    f'{chip("Dilution "+w["dilution_risk"],"est")} '
                    f'{chip("Clinical "+w["clinical_risk"],"est")} '
                    f'{chip("Reg "+w["regulatory_risk"],"binary" if w["regulatory_risk"]=="Binary" else "est")}</div>'
                    f'<div class="field"><span class="label">Technical:</span> {w["technical_setup"]} · '
                    f'<span class="label">Analyst:</span> {w["assigned_analyst"]}</div>'
                    f'<div class="small">Updated {w["last_updated"]}</div></div>',
                    unsafe_allow_html=True)
        else:
            st.warning("No watchlist data.")
    with tab2:
        st.info("Paper trading / education only. No brokerage connection; prices are manual/demo.")
        if len(portfolio):
            st.dataframe(portfolio, use_container_width=True, hide_index=True)
            pv = portfolio.copy()
            pv["unrealized_pct"] = pd.to_numeric(pv["unrealized_pct"], errors="coerce")
            fig = px.bar(pv, x="ticker", y="unrealized_pct", color="unrealized_pct",
                         color_continuous_scale=[[0, RED], [.5, GRAY], [1, "#2ecc71"]])
            fig.update_layout(height=280, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              font_color=OFFWHITE, xaxis_title="", yaxis_title="unrealized %",
                              coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No portfolio data.")

# --------------------------------------------------------------------------- #
# Router
# --------------------------------------------------------------------------- #
ROUTES = {
    "Executive Command Center": page_exec,
    "Agent Operations Room": page_ops,
    "Individual Agent": page_agent,
    "Biotech Catalyst Calendar": page_catalysts,
    "Social Content Calendar": page_content_cal,
    "Research Pipeline Board": page_pipeline,
    "Content Production Studio": page_studio,
    "Learning Progress": page_learning,
    "Portfolio & Watchlist": page_portfolio,
}
ROUTES[page]()

st.markdown("---")
st.caption("BioKev Biotech Command Center · reads from data files, never fabricates agent work · "
           "Educational only. Not investment or medical advice.")
