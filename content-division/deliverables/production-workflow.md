# BioKev — Short-Form Production Workflow

End-to-end pipeline from a research report to posted, platform-native videos. Tools: **ElevenLabs** (voice), **Adobe Character Animator** + **Cartoon Animator** (avatar), **Hedra / Runway / Krea / Luma** (motion, B-roll, transitions), **CapCut** (edit + captions + export).

## The pipeline
```
Research report → short-form script → compliance review → avatar storyboard
→ voiceover (ElevenLabs) → animation (Character Animator/Hedra + Cartoon Animator + Runway/Krea/Luma)
→ captions & platform versions (CapCut) → scheduling → analytics review
```

## Step-by-step

**1. Research report (Intelligence Desk).** A dossier / trial summary / cash-runway note with sources. Nothing proceeds without a source file.

**2. Script (Agent 02).** Choose show + length (30/45/60s). Tag every claim Fact/Assumption/Opinion. Save to `scripts/`.

**3. Compliance review (Agent 05).** Gate. PASS / REVISE / BLOCK. Sets required disclosures + position chip.

**4. Storyboard (Agent 04).** Shot table: Kevin vs avatar, visual metaphor per concept, on-screen text, which tool renders each shot. Save to `storyboards/`.

**5. Voiceover — ElevenLabs.**
- BioKev voice: pick/clone one clear warm dry clinical voice; save preset "BioKev v1". Kevin's own voice is used for K shots (record live).
- Render avatar lines as separate WAVs per shot (filenames match shot numbers).
- Settings: stability ~50, similarity ~75, style low; export 48kHz WAV.

**6. Animation.**
- **Kevin shots:** film to camera (9:16), good light, eye-line to lens.
- **Avatar talking shots:** Character Animator lip-synced to the ElevenLabs WAVs → export transparent PNG seq / ProRes 4444.
- **Gag/full-body shots:** Cartoon Animator with prop library.
- **Backgrounds / B-roll / transitions:** Runway + Krea + Luma per the prompt library.
- Keep the face authored (Ch. Animator/CTA); use generative tools only for motion/BG/transitions.

**7. Edit + captions — CapCut.**
- Assemble to the storyboard timing; snappy overshoot cuts.
- Burn word-level captions (brand type/colors, safe areas). Add title card, lower third, callouts, end card.
- Persistent disclosure ≥3s; position chip if flagged.
- Export platform versions: 9:16 for TikTok/Reels/Shorts; 1:1 or 9:16 for LinkedIn. Set cover frame per platform.

**8. Scheduling (Agent 06 → Kevin).** Log to `data/content/social_posts.csv` with platform, scheduled date, CTA, disclosure flag. Kevin approves + schedules.

**9. Analytics (Agent 07).** After posting, pull metrics into `social_posts.csv`; weekly report + 3 experiments → back to Agent 01.

## Batch tips
- Batch-film all evergreen Kevin shots in one session.
- Pre-render reusable avatar gag clips (runway, juice, coin, stamp, bullseye) once; reuse across videos.
- Keep a "BioKev v1" ElevenLabs preset and a CapCut template project (captions style, title cards, disclosure) so every video starts 60% done.

## File handoff naming
`S##` script ↔ `SB##` storyboard ↔ VO `S##-shot#.wav` ↔ export `S##-[platform].mp4`.
