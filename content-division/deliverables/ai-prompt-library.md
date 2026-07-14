# BioKev — AI Animation Prompt Library

**Maintained by:** Avatar Creative Director. Always paste the palette block and feed the canonical BioKev reference sheet. Keep the face authored in Character Animator / Cartoon Animator; use diffusion/video tools for motion, backgrounds, B-roll, and transitions — not for redrawing the face.

**Palette block (paste into every prompt):**
`hot pink #FF4DB2, biotech yellow #FFD12A, alert red #FF1E2D, deep black #111111, off-white #F4F4F4, accent gray #2B2B2B. Bright saturated flat fills, wobbly black marker outlines, hand-drawn street-art 2D animation, no corporate blue, no 3D, no photoreal.`

---

## 1. Adobe Character Animator (source-of-truth talking puppet)
Not a text-prompt tool — a rig. Setup checklist:
- Import BioKev PSD/AI (layered per Ch. Animator naming: `+Head`, `+Mouth` visemes, `+Left Eye`, etc.).
- Behaviors: Lip Sync (6-viseme), Eye Gaze, Blink, Breathing, Triggers for the 8 expressions and prop swaps (runway plane, juice, coin, stamp, bullseye).
- Drive audio from ElevenLabs BioKev VO or Kevin live.
- Export: transparent PNG sequence or ProRes 4444 for compositing in CapCut.

## 2. Cartoon Animator (CTA) (full-body + prop gags)
- Use the G3/free-bone BioKev rig; keyframe the recurring gags (juice pour, coin flip, dart-to-bullseye, stamp slam).
- Prompt-free; assemble from the prop library PNGs. Export transparent for CapCut.

## 3. Hedra (audio-driven expressive avatar beats)
> Feed the BioKev reference still + ElevenLabs VO. Constrain to head/shoulders explainer shots.
```
Prompt: Animated 2D cartoon pharmacist "BioKev" (reference image) talking to camera, warm confident expression, subtle head movement and blinking, lip-synced to the provided audio. White lab coat with hot-pink collar, yellow "BIOKEV PharmD" badge, thin black glasses. Flat marker-outline 2D style. [palette block]. Static hand-drawn biotech-lab-desk background. No photoreal, no morphing of facial features.
```
Settings: portrait 9:16, keep motion low/medium to avoid identity drift.

## 4. Runway (transitions, motion graphics, B-roll)
```
Gen prompt (B-roll): Hand-drawn 2D marker-style animated biotech lab desk — beakers, a whiteboard with a trial timeline, sticky notes reading catalyst dates, a candlestick chart drawn in marker. Slow parallax camera push-in. [palette block]. Looping, no text artifacts, no people.
```
```
Transition prompt: Quick marker-swipe wipe in hot pink and yellow, hand-drawn ink splatter reveal, 0.4s. [palette block].
```
Use for: metaphor motion (runway plane taxiing, pie shrinking), scene wipes. Do NOT use to generate BioKev's face.

## 5. Krea (real-time style-consistent stills & backgrounds)
```
Prompt: Hand-drawn street-art 2D illustration, biotech-meets-Wall-Street research desk, bold black marker outlines, flat saturated fills. [palette block]. Elements: molecule lock-and-key, FDA calendar with red stamp, dartboard endpoint, airplane on a short runway, glass of watered-down juice. Transparent-friendly, high contrast, no text, no photoreal.
```
Use for: prop stills, background plates, thumbnail elements. Style-reference lock to the BioKev sheet.

## 6. Luma (cinematic short motion clips / camera moves)
```
Prompt: Short 3–5s cinematic move over a hand-drawn 2D biotech command-center desk, gentle dolly, shallow parallax, marker-outline flat-color art. [palette block]. Mood: smart, bright, playful-clinical. No people, no text, no morphing.
```
Use for: opener stinger, section transitions, dreamy B-roll. Keep BioKev out of Luma shots (identity drift).

## 7. Thumbnail / cover-frame prompt (Krea or manual)
```
Prompt: Bold 9:16 thumbnail, BioKev cartoon head (reference) pointing with a marker, huge yellow marker headline "[HOOK]", ticker chip, hot-pink accents, deep-black background. Hand-drawn 2D. [palette block]. Leave bottom 15% clear for platform UI.
```

## Guardrails
- Every generated asset passes the Avatar Creative Director QC (on-model, palette, logged in style bible).
- Reject any output with photoreal faces, corporate-blue gradients, warped text, rocket ships, or lambos.
- Log the exact prompt + tool + settings next to each asset for repeatability.
