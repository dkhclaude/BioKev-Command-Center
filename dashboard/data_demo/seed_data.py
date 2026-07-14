"""
BioKev Biotech Command Center — demo data seed generator.

Regenerates every file the dashboard reads. All companies here are FICTIONAL
demo placeholders (ticker suffix reminders in notes) so no unverified catalyst
date is ever mistaken for a real, sourced event. Replace with verified data via
the protocols in dashboard/protocols/ before using for real research.

Run:  python seed_data.py
Writes into ./data/** relative to this file.
"""
import csv, json, os, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "data")
TODAY = datetime.date(2026, 7, 13)

def p(*parts):
    path = os.path.join(D, *parts)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path

def w_csv(path, rows, header):
    with open(path, "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=header)
        wr.writeheader()
        for r in rows:
            wr.writerow(r)

def w_json(path, obj):
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)

def dd(days):
    return (TODAY + datetime.timedelta(days=days)).isoformat()

# ----------------------------------------------------------------------------
# 19 agents (12 research desk + 7 content division)
# ----------------------------------------------------------------------------
AGENTS = [
    ("cio", "Chief Investment Officer & Research Editor", "Research", "Reviewing",
     "Editing SNGX-demo dossier for publish", "Reconcile clinical vs financial risk ratings", 0.72),
    ("clin_sci", "Clinical Science & Mechanism Analyst", "Research", "Active",
     "Mechanism write-up for RENX-demo lead asset", "Confirm MoA class vs competitor", 0.80),
    ("trial_biostat", "Clinical Trial & Biostatistics Analyst", "Research", "Active",
     "Powering analysis of ZYMR-demo Ph2 readout", "Is primary endpoint adequately powered?", 0.65),
    ("fda_reg", "FDA & Regulatory Catalyst Analyst", "Research", "Blocked",
     "Verifying NOVX-demo PDUFA date", "Awaiting primary-source confirmation of date", 0.40),
    ("fin_runway", "Financial, Cash-Runway & Dilution Analyst", "Research", "Active",
     "Runway model for HELX-demo from latest 10-Q", "Confirm ATM capacity remaining", 0.78),
    ("commercial", "Commercial & Competitive Landscape Analyst", "Research", "Waiting",
     "Competitive map for RENX-demo indication", "Need clin_sci mechanism note first", 0.60),
    ("valuation", "Valuation & Scenario Analyst", "Research", "Waiting",
     "Scenario tree for ZYMR-demo readout", "Blocked on biostat power read", 0.55),
    ("market_struct", "Market Structure, Technical & Options Flow Analyst", "Research", "Active",
     "Pre-catalyst technical + flow scan on watchlist", "Any unusual flow into NOVX-demo?", 0.68),
    ("portfolio_risk", "Portfolio & Risk Manager", "Research", "Reviewing",
     "Sizing rules for binary-event names (paper)", "Confirm max binary exposure cap", 0.75),
    ("tutor", "PharmD-to-Biotech-Investor Tutor", "Research", "Active",
     "Week 3 curriculum + quiz on trial endpoints", "Which weak area to drill next?", 0.82),
    ("brand", "Public Research & Brand Strategist", "Research", "Active",
     "Positioning + weekly content thesis", "Which 2 stories lead this week?", 0.77),
    ("librarian", "Knowledge Librarian & Quality Auditor", "Research", "Reviewing",
     "Citation audit across open dossiers", "3 claims missing primary sources", 0.70),
    ("strategist", "Short-Form Content Strategist", "Content", "Active",
     "Ranking week-2 short-form ideas", "Confirm Catalyst-in-60 slot company", 0.74),
    ("scriptwriter", "Biotech Scriptwriter", "Content", "Active",
     "Drafting S07 Catalyst-in-60 for NOVX-demo", "Need verified PDUFA date from fda_reg", 0.66),
    ("avatar_cd", "Avatar Creative Director", "Content", "Complete",
     "Style bible v1 + prompt library shipped", "None — awaiting new pose requests", 0.90),
    ("storyboard", "Animation Storyboard Agent", "Content", "Waiting",
     "Storyboarding approved evergreen scripts", "Waiting on compliance PASS for S07", 0.63),
    ("compliance", "Compliance & Credibility Editor", "Content", "Reviewing",
     "Reviewing S03 & S05 evergreen scripts", "Confirm position disclosure policy w/ Kevin", 0.71),
    ("caption", "Caption & Editing Agent", "Content", "Waiting",
     "CapCut template + platform versions", "Awaiting animated cuts", 0.58),
    ("analytics", "Analytics & Iteration Agent", "Content", "Waiting",
     "Baseline metrics setup", "No posts live yet — awaiting first posts", 0.50),
]

status_json = {"_meta": {"generated": TODAY.isoformat(),
                         "note": "Demo data. Companies are fictional placeholders. Agents update their own block after work.",
                         "source": "seed_data.py"},
               "agents": []}
tasks = []
tid = 100
for aid, name, div, status, task, question, conf in AGENTS:
    folder = f"outputs/agents/{aid}/"
    files_created = [f"{folder}notes.md"]
    if div == "Research":
        files_created.append(f"{folder}latest_analysis.md")
    else:
        files_created.append(f"{folder}handoff.md")
    status_json["agents"].append({
        "id": aid, "name": name, "division": div,
        "role": name, "status": status,
        "mission": f"{name} for the BioKev Biotech Intelligence Desk.",
        "current_task": task,
        "last_updated": (datetime.datetime(2026,7,13,8,0) + datetime.timedelta(minutes=tid)).isoformat(timespec="minutes"),
        "files_created": files_created,
        "files_editing": [f"{folder}draft.md"] if status in ("Active","Reviewing") else [],
        "open_questions": [question],
        "blockers": ([task.split(" ")[-1]] if status == "Blocked" else []),
        "next_action": question,
        "confidence": conf,
        "output_folder": folder,
    })
    for k, st in enumerate(["completed", "in_progress", "pending"]):
        tasks.append({"agent": aid, "task_id": tid, "title": f"{name.split('&')[0].strip()} task {k+1}",
                       "status": st, "priority": ["High","Medium","Low"][k],
                       "due_date": dd(k*3), "notes": task if st=="in_progress" else ""})
        tid += 1
w_json(p("agents","agent_status.json"), status_json)
w_csv(p("agents","agent_tasks.csv"), tasks,
      ["agent","task_id","title","status","priority","due_date","notes"])

# ----------------------------------------------------------------------------
# Biotech catalysts (fictional demo companies)
# ----------------------------------------------------------------------------
CO = [("NOVX","Novexis Therapeutics (demo)"),("RENX","Renexa Bio (demo)"),
      ("ZYMR","Zymara Sciences (demo)"),("HELX","Helixon Pharma (demo)"),
      ("SNGX","Sangenix (demo)"),("CELA","Celastra Bio (demo)"),
      ("ATLB","Atlasbio (demo)")]
catalysts = [
    ("NOVX", dd(9), "PDUFA Decision", "FDA decision on lead asset in rare disease", "Needs Verification","Binary","fda_reg", dd(11)),
    ("RENX", dd(21), "Phase 3 Topline Readout", "Pivotal Ph3 primary endpoint readout", "Estimated","High","trial_biostat", dd(23)),
    ("ZYMR", dd(5), "Phase 2 Data (conference)", "Ph2 data at scientific conference", "Likely","High","clin_sci", dd(7)),
    ("HELX", dd(14), "Q2 Earnings", "Quarterly earnings + cash update", "Confirmed","Medium","fin_runway", dd(15)),
    ("SNGX", dd(2), "Advisory Committee (AdComm)", "AdComm vote on BLA", "Estimated","Binary","fda_reg", dd(4)),
    ("CELA", dd(30), "Investor Conference Presentation", "Corporate presentation at conf", "Likely","Low","brand", dd(31)),
    ("ATLB", dd(45), "Phase 1 Data", "First-in-human dose-escalation data", "Estimated","Medium","trial_biostat", dd(47)),
    ("RENX", dd(-6), "Abstract Release", "Conference abstract titles released", "Confirmed","Medium","clin_sci", dd(-4)),
    ("NOVX", dd(60), "AdComm Briefing Docs", "FDA briefing documents expected", "Estimated","High","fda_reg", dd(61)),
    ("ZYMR", dd(3), "Watchlist Review", "Scheduled thesis review", "Confirmed","Low","cio", dd(17)),
    ("HELX", dd(-2), "SEC 10-Q Filing", "Quarterly filing reminder", "Confirmed","Low","fin_runway", dd(12)),
    ("SNGX", dd(20), "Post-Catalyst Review", "Post-mortem after AdComm", "Confirmed","Medium","cio", dd(20)),
]
crows = []
for i,(tk,date,etype,desc,conf,impact,agent,review) in enumerate(catalysts):
    name = dict(CO)[tk]
    crows.append({"date":date,"company":name,"ticker":tk,"event_type":etype,
                  "description":desc,"source_link":"https://EXAMPLE-verify-before-use.invalid/"+tk.lower(),
                  "source_date":dd(-10),"confidence":conf,"impact":impact,
                  "assigned_agent":agent,"prep_work":f"Prep {etype.lower()} explainer + risk breakdown",
                  "post_event_review_date":review})
w_csv(p("calendar","biotech_catalysts.csv"), crows,
      ["date","company","ticker","event_type","description","source_link","source_date",
       "confidence","impact","assigned_agent","prep_work","post_event_review_date"])

# ----------------------------------------------------------------------------
# Social posts + content calendar + video production
# ----------------------------------------------------------------------------
SHOWS = [
 ("BK-001","What a PDUFA date actually is","PharmD Explains","talking-head+avatar","Scripted","scriptwriter","outputs/research/pdufa_ref.md","scripts/S01-PDUFA-explainer-60s.md","calendar+stamp+coin","Recorded","Not started","Not started",dd(1),"Follow for the next readout","Educational only"),
 ("BK-002","Statistical vs clinical significance","Myth vs Mechanism","avatar","Compliance Review","compliance","outputs/research/biostat_ref.md","scripts/S02-stat-vs-clinical-significance-45s.md","trophy+patient","Not started","Not started","Not started",dd(4),"Follow for trial literacy","Educational only"),
 ("BK-003","How to read cash runway","Cash Runway Check","talking-head+avatar","Scripted","scriptwriter","outputs/research/runway_ref.md","scripts/S03-cash-runway-60s.md","runway plane+juice","Not started","Not started","Not started",dd(3),"Price the raise before the readout","Educational only"),
 ("BK-004","What dilution does to your shares","PharmD Explains","avatar","Idea","strategist","outputs/research/dilution_ref.md","scripts/S04-dilution-30s.md","juice+pie","Not started","Not started","Not started",dd(8),"Ask what you get for it","Educational only"),
 ("BK-005","Primary vs secondary endpoints","Trial Design Teardown","talking-head+avatar","Filmed","caption","outputs/research/endpoints_ref.md","scripts/S05-primary-vs-secondary-endpoints-45s.md","bullseye","Recorded","Rendered","In progress",dd(2),"Judge by the shot it called","Educational only"),
 ("BK-006","What an AdComm vote means","PharmD Explains","avatar","Researching","strategist","outputs/research/adcomm_ref.md","scripts/S06-advisory-committee-45s.md","referee panel","Not started","Not started","Not started",dd(10),"Mark both dates","Educational only"),
 ("BK-007","NOVX-demo catalyst in 60","Catalyst in 60","talking-head+avatar","Idea","scriptwriter","outputs/research/novx_dossier.md","scripts/S07-catalyst-in-60-TEMPLATE-60s.md","calendar+bull/bear","Not started","Not started","Not started",dd(7),"Dossier in description","Position + estimate"),
 ("BK-008","RENX-demo trial teardown","Trial Design Teardown","talking-head+avatar","Idea","scriptwriter","outputs/research/renx_dossier.md","scripts/S08-trial-teardown-TEMPLATE-45s.md","bullseye+whiteboard","Not started","Not started","Not started",dd(17),"Post-mortem after readout","Position"),
 ("BK-009","RENX-demo bull vs bear","Bull vs Bear","talking-head+avatar","Idea","strategist","outputs/research/renx_dossier.md","scripts/S09-bull-vs-bear-TEMPLATE-60s.md","bull+bear","Not started","Not started","Not started",dd(12),"Dossier in description","Position"),
 ("BK-010","30 days building in public","Meta","talking-head","Idea","brand","outputs/brand/month1_recap.md","scripts/S10-post-mortem-TEMPLATE-60s.md","marker chart","Not started","Not started","Not started",dd(29),"Follow","Educational only"),
]
sp_header = ["post_id","title","format","content_type","status","assigned_agent","source_research_file",
             "script_file","visual_assets_needed","voiceover_status","animation_status","caption_status",
             "scheduled_date","cta","disclosure_needed","platform","views","watch_through_pct","saves","shares","follows"]
sp_rows = []
platforms_cycle = ["TikTok","Instagram Reels","YouTube Shorts","LinkedIn"]
for i,row in enumerate(SHOWS):
    (pid,title,show,ctype,status,agent,src,script,assets,vo,anim,cap,sched,cta,disc)=row
    plat = platforms_cycle[i % 4]
    posted = status in ("Posted","Repurposed")
    sp_rows.append({"post_id":pid,"title":title,"format":show,"content_type":ctype,"status":status,
        "assigned_agent":agent,"source_research_file":src,"script_file":script,
        "visual_assets_needed":assets,"voiceover_status":vo,"animation_status":anim,"caption_status":cap,
        "scheduled_date":sched,"cta":cta,"disclosure_needed":disc,"platform":plat,
        "views":"" ,"watch_through_pct":"","saves":"","shares":"","follows":""})
w_csv(p("content","social_posts.csv"), sp_rows, sp_header)

# content_calendar.csv = the scheduling/linking layer connecting catalysts -> posts
cc_rows = []
link = [("BK-001","NOVX","PDUFA Decision","pre-event explainer"),
        ("BK-007","NOVX","PDUFA Decision","day-of summary"),
        ("BK-008","RENX","Phase 3 Topline Readout","trial-design explainer"),
        ("BK-009","RENX","Phase 3 Topline Readout","risk breakdown"),
        ("BK-005","ZYMR","Phase 2 Data (conference)","investor takeaway")]
for pid,tk,ev,role in link:
    prow = next(r for r in sp_rows if r["post_id"]==pid)
    cc_rows.append({"date":prow["scheduled_date"],"post_id":pid,"title":prow["title"],
        "platform":prow["platform"],"status":prow["status"],"linked_ticker":tk,
        "linked_catalyst":ev,"content_role":role,"assigned_agent":prow["assigned_agent"]})
w_csv(p("calendar","content_calendar.csv"), cc_rows,
      ["date","post_id","title","platform","status","linked_ticker","linked_catalyst","content_role","assigned_agent"])

# video_production.csv
vp_rows = []
for r in sp_rows:
    sb = r["script_file"].replace("scripts/S","storyboards/SB").split("-")[0]
    vp_rows.append({"video_id":r["post_id"],"title":r["title"],"script_file":r["script_file"],
        "storyboard_file":sb+"-*.md","vo_status":r["voiceover_status"],
        "elevenlabs_files_needed":"BioKev v1 preset; per-shot WAVs" if "avatar" in r["content_type"] else "Kevin live",
        "avatar_status":r["animation_status"],
        "tool_assets_needed":"Character Animator + "+r["visual_assets_needed"],
        "capcut_status":r["caption_status"],"captions_status":r["caption_status"],
        "platform_versions":"9:16 x3 + 1:1 LinkedIn","posting_checklist":"Pending" if r["status"]!="Posted" else "Complete"})
w_csv(p("content","video_production.csv"), vp_rows,
      ["video_id","title","script_file","storyboard_file","vo_status","elevenlabs_files_needed",
       "avatar_status","tool_assets_needed","capcut_status","captions_status","platform_versions","posting_checklist"])

# ----------------------------------------------------------------------------
# Research pipeline (Kanban)
# ----------------------------------------------------------------------------
PIPE = [
 ("SNGX","Sangenix (demo)","Company Dossier","cio;fda_reg","Idea",dd(12),dd(2),"High","Binary","Needs sourcing","outputs/research/sngx_dossier.md"),
 ("NOVX","Novexis (demo)","Catalyst Deep-Dive","fda_reg;clin_sci","Researching",dd(5),dd(9),"High","High","Partial","outputs/research/novx_dossier.md"),
 ("RENX","Renexa (demo)","Trial Teardown","trial_biostat;clin_sci","Drafting",dd(8),dd(21),"High","High","Sourced","outputs/research/renx_dossier.md"),
 ("ZYMR","Zymara (demo)","Data Preview","clin_sci;valuation","Red-Team Review",dd(3),dd(5),"Medium","High","Sourced","outputs/research/zymr_preview.md"),
 ("HELX","Helixon (demo)","Cash-Runway Note","fin_runway","Compliance Review",dd(4),dd(14),"Medium","Medium","Sourced","outputs/research/helx_runway.md"),
 ("CELA","Celastra (demo)","Competitive Map","commercial","Assigned",dd(15),dd(30),"Low","Medium","Not started","outputs/research/cela_map.md"),
 ("ATLB","Atlasbio (demo)","Watchlist Add Memo","cio;market_struct","Ready to Publish",dd(1),dd(45),"Medium","Medium","Sourced","outputs/research/atlb_memo.md"),
 ("HELX","Helixon (demo)","Weekly Brief item","brand","Published",dd(-2),dd(14),"Low","Low","Sourced","outputs/research/helx_brief.md"),
 ("SNGX","Sangenix (demo)","Prior AdComm note","cio","Post-Mortem Needed",dd(-1),dd(2),"High","Binary","Sourced","outputs/research/sngx_adcomm.md"),
 ("RENX","Renexa (demo)","Old mechanism primer","clin_sci","Archived",dd(-30),dd(-20),"Low","Low","Sourced","outputs/research/renx_primer.md"),
]
w_csv(p("research","research_pipeline.csv"),
      [dict(zip(["ticker","company","research_type","assigned_agents","stage","due_date","catalyst_date",
                 "priority","risk_level","source_status","output_file"], row)) for row in PIPE],
      ["ticker","company","research_type","assigned_agents","stage","due_date","catalyst_date",
       "priority","risk_level","source_status","output_file"])

# ----------------------------------------------------------------------------
# Watchlist
# ----------------------------------------------------------------------------
WL = [
 ("NOVX","Novexis (demo)","Rare Disease","$480M","NVX-101 (rare metabolic)","PDUFA "+dd(9),"~5 quarters","High","Medium","Binary","Coiling pre-catalyst","Research further","fda_reg"),
 ("RENX","Renexa (demo)","Oncology","$1.9B","REN-2 (solid tumor)","Ph3 "+dd(21),"~8 quarters","Moderate","High","Medium","Uptrend","Add to watchlist","trial_biostat"),
 ("ZYMR","Zymara (demo)","Immunology","$720M","ZY-9 (autoimmune)","Ph2 "+dd(5),"~4 quarters","High","High","High","Range","Monitor","clin_sci"),
 ("HELX","Helixon (demo)","Neuroscience","$3.4B","HLX-CNS","Earnings "+dd(14),"~11 quarters","Low","Medium","Medium","Base building","Existing-position review","fin_runway"),
 ("SNGX","Sangenix (demo)","Gene Therapy","$260M","SGX gene tx","AdComm "+dd(2),"~3 quarters","Very High","High","Binary","Volatile","Paper-trade candidate","cio"),
 ("CELA","Celastra (demo)","Metabolic","$5.1B","CEL-GLP","Conf "+dd(30),"Profitable","Low","Low","Low","Uptrend","Monitor","commercial"),
 ("ATLB","Atlasbio (demo)","Cell Therapy","$140M","ATL-CAR","Ph1 "+dd(45),"~6 quarters","High","High","High","Illiquid","Avoid","market_struct"),
]
w_csv(p("watchlists","watchlist.csv"),
      [dict(zip(["ticker","company","sector","market_cap","lead_program","next_catalyst","cash_runway",
                 "dilution_risk","clinical_risk","regulatory_risk","technical_setup","thesis_status",
                 "assigned_analyst"], row)) | {"last_updated": TODAY.isoformat()} for row in WL],
      ["ticker","company","sector","market_cap","lead_program","next_catalyst","cash_runway",
       "dilution_risk","clinical_risk","regulatory_risk","technical_setup","thesis_status",
       "assigned_analyst","last_updated"])

# ----------------------------------------------------------------------------
# Paper portfolio (education only, no real trades)
# ----------------------------------------------------------------------------
PORT = [
 ("RENX","Renexa (demo)",dd(-40),100,18.20,22.15,"Intact","Paper-trade candidate"),
 ("HELX","Helixon (demo)",dd(-70),50,61.00,58.40,"Intact","Existing-position review"),
 ("ATLB","Atlasbio (demo)",dd(-10),200,4.05,3.60,"Weakening","Monitor"),
]
w_csv(p("portfolio","paper_portfolio.csv"),
      [{"ticker":t,"company":c,"entry_date":ed,"shares":sh,"entry_price":ep,"current_price":cp,
        "unrealized_pct":round((cp-ep)/ep*100,1),"thesis_status":ts,"classification":cl,
        "last_updated":TODAY.isoformat(),"note":"PAPER / education only — not a real trade"}
       for (t,c,ed,sh,ep,cp,ts,cl) in PORT],
      ["ticker","company","entry_date","shares","entry_price","current_price","unrealized_pct",
       "thesis_status","classification","last_updated","note"])

# ----------------------------------------------------------------------------
# Learning / curriculum
# ----------------------------------------------------------------------------
CURR = [
 (1,"Biotech landscape & business models",4,4,92,"—","Complete"),
 (2,"Reading a clinical trial",5,5,88,"Confidence intervals","Complete"),
 (3,"Trial endpoints & biostatistics",5,3,80,"Power & sample size","In progress"),
 (4,"FDA pathways & catalysts",4,0,None,"—","Not started"),
 (5,"Cash runway & dilution",4,0,None,"—","Not started"),
 (6,"Valuation & scenario analysis",4,0,None,"—","Not started"),
 (7,"Competitive landscapes",3,0,None,"—","Not started"),
 (8,"Market structure & technicals",4,0,None,"—","Not started"),
 (9,"Options & flow basics",3,0,None,"—","Not started"),
 (10,"Portfolio & risk management",4,0,None,"—","Not started"),
 (11,"Building public research",3,0,None,"—","Not started"),
 (12,"Capstone dossier + post-mortem",2,0,None,"—","Not started"),
]
w_csv(p("learning","curriculum_progress.csv"),
      [{"week":wk,"module":m,"lessons_total":lt,"lessons_completed":lc,
        "quiz_score":(qs if qs is not None else ""),"weak_areas":wa,"status":st}
       for (wk,m,lt,lc,qs,wa,st) in CURR],
      ["week","module","lessons_total","lessons_completed","quiz_score","weak_areas","status"])
w_json(p("learning","learning_metrics.json"), {
    "_meta":{"generated":TODAY.isoformat(),"note":"Demo learning metrics."},
    "flashcards_due": 24, "dossiers_completed": 3, "catalyst_postmortems_completed": 1,
    "public_posts_published": 0, "research_streak_days": 12,
    "credibility_milestones": [
        {"name":"First full company dossier","done":True},
        {"name":"First trial teardown video scripted","done":True},
        {"name":"First public post published","done":False},
        {"name":"10 catalysts tracked with sources","done":False},
        {"name":"First honest post-mortem published","done":False}]})

# ----------------------------------------------------------------------------
# Alerts
# ----------------------------------------------------------------------------
alerts = {"_meta":{"generated":TODAY.isoformat()}, "alerts":[
    {"id":"AL-01","type":"FDA date","severity":"High","message":"NOVX-demo PDUFA in 9 days is still 'Needs Verification' — confirm source.","related":"NOVX","created":TODAY.isoformat()},
    {"id":"AL-02","type":"Missing citation","severity":"Medium","message":"3 claims in SNGX-demo dossier lack primary sources (librarian audit).","related":"SNGX","created":TODAY.isoformat()},
    {"id":"AL-03","type":"Content deadline","severity":"Medium","message":"BK-005 endpoints video scheduled in 2 days; captions still in progress.","related":"BK-005","created":TODAY.isoformat()},
    {"id":"AL-04","type":"Stale data","severity":"Low","message":"HELX-demo runway note based on filing >90 days old — refresh after 10-Q.","related":"HELX","created":TODAY.isoformat()},
    {"id":"AL-05","type":"Incomplete report","severity":"High","message":"ZYMR-demo data preview blocked in Red-Team Review (biostat power unresolved).","related":"ZYMR","created":TODAY.isoformat()},
    {"id":"AL-06","type":"Blocker","severity":"High","message":"Scriptwriter blocked on S07: awaiting verified NOVX-demo PDUFA date.","related":"BK-007","created":TODAY.isoformat()},
]}
w_json(p("alerts","alerts.json"), alerts)

print("Seed complete. Files written under", D)
for root,_,files in os.walk(D):
    for f in sorted(files):
        print(" -", os.path.relpath(os.path.join(root,f), HERE))
