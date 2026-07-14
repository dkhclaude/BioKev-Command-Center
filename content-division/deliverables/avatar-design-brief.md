# BIOKEV — Recurring 2D Avatar Design Brief & Style Bible

**Maintained by:** Avatar Creative Director agent
**Purpose:** Define the recurring animated character ("BioKev") so it looks identical across every tool and every video.

---

## 1. Character concept

**BioKev** is a stylized 2D cartoon version of Kevin: a pharmacist-scientist who moonlights as a biotech research analyst. He is the on-screen "co-host" — he shows up to explain mechanisms, stamp catalyst dates, and deliver the punchline the real Kevin sets up to camera. He is confident and clear, occasionally deadpan, never a hype clown.

Think: *a friendly clinical-trial explainer character with street-art energy* — hand-drawn marker linework, flat bright fills, expressive but simple.

## 2. Core design (locked)

- **Build:** upper-body / bust framing by default (head + shoulders + hands enter frame).
- **Head:** rounded, slightly oversized for expressiveness. Confident eyebrows.
- **Signature elements (never change):**
  - **White lab coat** with a **hot-pink (#FF4DB2) collar trim** and a pen in the pocket.
  - **Yellow (#FFD12A) name badge** reading "BIOKEV, PharmD".
  - **Glasses** (thin black hand-drawn frames).
  - A **marker/highlighter** held like a pointer — his signature prop.
- **Line:** 3px wobbly black marker outline. Flat fills, minimal shading, one halftone shadow.
- **Palette on-model:** skin neutral; coat off-white `#F4F4F4`; accents hot pink + yellow; red only for "risk" moments.

## 3. Expression sheet (required poses)

Build each of these as a reusable pose/frame in Character Animator (puppet) and as reference stills for AI tools:

| # | Expression | When to use |
|---|---|---|
| 1 | Neutral explainer (pointing with marker) | Default narration |
| 2 | Big idea / lightbulb (eyebrows up, yellow bulb) | The insight beat |
| 3 | Skeptical / raised eyebrow | "But here's the catch" / bear case |
| 4 | Alarmed (sweat drop, red tint) | Risk, dilution, binary event |
| 5 | Deadpan to camera | The dry joke |
| 6 | Approving nod / thumbs (small) | Confirmed catalyst, thesis intact |
| 7 | Thinking (hand on chin) | Assumptions, "we don't know yet" |
| 8 | Wave (open/close card) | Intro and outro |

## 4. Prop & set library (recurring visual jokes)

- **The Runway Plane** — appears whenever cash runway comes up; the tarmac literally runs out.
- **The Watered-Down Juice** — dilution gag; BioKev pours water into a glass labeled "your shares".
- **The Coin Flip** — binary catalyst; BioKev flips an FDA-stamped coin, covers his eyes.
- **The Bullseye** — endpoints; a dart lands (hit) or thuds off-board (miss).
- **The Red Stamp** — FDA decisions; BioKev slams a stamp: APPROVED / CRL.
- **The Whiteboard** — trial timeline drawn in marker behind him.
- **Running gag:** BioKev's coffee mug reads a rotating clinical pun ("STAT-istically significant", "p < 0.05 caffeine").

## 5. Motion & lip-sync notes

- Mouth: 6-viseme set (AI, E, U, O, MBP, rest) for ElevenLabs/Character Animator lip-sync.
- Idle: subtle breathing + occasional blink; marker taps on "point" beats.
- Entrances: pop-in with slight overshoot; never slow-fade.
- Keep gestures readable at 9:16 mobile — one clear gesture per line.

## 6. Consistency rules across tools

- **Character Animator** is the *source of truth* puppet for talking-head avatar segments (real-time lip-sync to Kevin's or ElevenLabs audio).
- **Cartoon Animator (CTA)** for full-body walk/gesture scenes and the prop gags.
- **Hedra / Runway / Krea / Luma** are used for *stylized motion, backgrounds, transitions, and B-roll* — NOT for redrawing the face. To keep identity locked, always feed these tools the **canonical BioKev reference sheet** (front + 3/4 views) and constrain them with the color hexes.
- Any new pose must be added to this bible before it ships.

## 7. Turnaround & reference-sheet checklist (production to-do)

- [ ] Front view, 3/4 left, 3/4 right, profile
- [ ] Full expression sheet (8 above)
- [ ] Hands library (point, open palm, thumbs, chin)
- [ ] Prop library PNGs (transparent)
- [ ] Color chips embedded on the sheet with hex values
- [ ] Character Animator puppet rigged with visemes + triggers
- [ ] "Do not do" sheet (no other coat colors, no rocket ships, no changing glasses)

## 8. Voice pairing

BioKev's animated segments use the **ElevenLabs BioKev voice** (see production workflow) — a clear, warm, slightly dry clinical-explainer voice. The real Kevin's to-camera segments use Kevin's own voice. Keep the two distinct but complementary; BioKev can "finish Kevin's sentence" as a recurring device.
