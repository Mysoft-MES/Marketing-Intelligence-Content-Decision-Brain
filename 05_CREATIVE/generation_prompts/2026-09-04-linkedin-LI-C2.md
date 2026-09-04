# LI-C2 — LinkedIn — 2026-09-04

**Status:** APPROVED (human via approval PR, 2026-09-04)
**Calendar row:** none yet — sequence asset. Run only *after* LI-C1 has produced a first
dwell/saves read, so the two carousels test the *frame* (shift-handover vs plan-vs-actual)
with format held constant. Needs a human to add a carousel row or approve as a standalone
follow-up test.
**Platform:** LinkedIn
**Audience:** General Manager (primary); Operations Manager / Production Manager (secondary) — under-45 researchers
**Objective / funnel stage:** Awareness / top-of-funnel — problem-first, no hard sell
**Asset type:** image (carousel — 8–10 panels, single shared visual system)
**Aspect ratio:** 4:5 (1080×1350) per panel
**Target duration:** n/a (static carousel)
**Language:** English

## Evidence basis
- **Research file:** `06_PERFORMANCE/competitive_benchmark.md` (2026-09-04 entries);
  `03_PLATFORM/linkedin.md` (2026-09-03 + 2026-09-04 addenda); `01_BUSINESS/positioning.md` §32;
  `01_BUSINESS/swot.md` §12.
- **Findings used:**
  1. The one tracked competitor, Allied Solutions Global, leads its MES content with OEE,
     downtime, compliance and ERP-connectivity — it does **not** lead with "can management
     verify what actually happened on the floor?" That verification / plan-vs-actual frame
     is white space against the competitor's positioning
     (`06_PERFORMANCE/competitive_benchmark.md` 2026-09-04; `04_COMPETITORS/allied-solutions-global.md` §3, §5).
  2. LinkedIn 2026 ranks on active dwell time ("Depth Score"); document / carousel posts are
     the highest-engagement format, 8–12 slides optimal (external benchmark → TESTING,
     `03_PLATFORM/linkedin.md`).
  3. Mysoft's strategic positioning territory is "from what people say is happening to what
     the production data shows is happening" (`positioning.md` §32) — this asset is that
     territory in carousel form.
- **Evidence tier and confidence:** external benchmark (Tier 4) + single-competitor
  comparison (LOW-MEDIUM). `build_recommendation_context` returns **maximum_confidence: LOW**
  (`current_priorities.md` empty; pre-revenue, zero customers, zero demo notes). This is a
  TEST, not a recommendation.

## Concept
Carousel of **9 panels: "The report says 500. The floor made 480."** Walks through how a
reported production number and the actual production number drift apart on a manually-recorded
floor, why the gap is invisible until it causes a problem, and what a digital job record
changes about it. One idea per panel, plain language, no product screenshots (a representative
labelled mock only if any UI is shown).

## Panel-by-panel

**Panel 1 — Hook**
On-screen text: "The end-of-day report says 500. The floor actually made 480. Which number is running your schedule tomorrow?"
Visual: two paper slips side by side on a desk — one printed "500", one hand-corrected to "480".

**Panel 2 — Frame**
Text: "On a manually-recorded floor, the number you manage from is not the number that happened. It's the number that got written down."
Visual: a production report on a clipboard, a pen hovering.

**Panel 3 — Where the gap comes from**
Text: "A miscount here. A late entry there. A job logged against the wrong number. None of it is dishonest — it's just manual."
Visual: three small vignettes — an operator counting cartons, someone filling a log an hour later, a similar-looking job card.

**Panel 4 — The gap is invisible**
Text: "Nobody sees the 20-unit gap. It's spread across a shift, a few jobs, a few people."
Visual: a bar that reads 500, with a faint slice at the top shaded differently.

**Panel 5 — Until it isn't**
Text: "It shows up later — as a short delivery, a stock count that won't reconcile, a customer asking where their order is."
Visual: a dispatch bay, a picker looking at a gap on a shelf.

**Panel 6 — The planning cost**
Text: "Next week's plan was built on 500. It was really 480. The plan starts wrong."
Visual: a planning board / schedule with one row circled.

**Panel 7 — What a digital job record changes**
Text: "When the count is entered against the job at the step — by the person doing it, at the time — the reported number and the real number are the same number."
Visual: a clean, simple representative record card (LABELLED "illustrative") — job, step, operator, timestamp, quantity entered.

**Panel 8 — Manage from the floor, not the write-up**
Text: "You manage from what the floor recorded, not from what got summarised on the way up."
Visual: a shared screen at the line showing the same record, a supervisor looking at it.

**Panel 9 — The point + soft CTA**
Text: "Plan from the real number."
Sub-line: "That's the problem Mysoft MES works on — a production record that matches what actually happened."
CTA: "Follow for more on shop-floor visibility." (No link in the post body; if used, first comment.)

## Tone and art direction
Documentary, plain, Malaysian SME factory — not glossy corporate 3D. One restrained palette
across all panels, one accent colour reserved for the two numbers (500 / 480), large legible
type readable at feed-thumbnail size. Real-looking paper, real-looking floor. No stock-photo
boardroom imagery.

## On-screen text
As per panels above. Numbers 500 and 480 are the recurring visual motif — same typeface,
accent colour, carried across panels.

## What must NOT appear
- No percentage figures, no "reduce variance by X%", no "eliminates miscounts", no "100%
  accurate", no ROI, no cost-saving figure, no implementation duration
  (`01_BUSINESS/products.md` §20, §31). The 500/480 numbers are an illustrative scenario,
  not a claimed result — the caption must make that explicit.
- Do not depict or describe the Digiwin AIoT upload mechanism — TO VERIFY (`products.md` §7).
- Do not claim regulatory / audit outcomes (`products.md` §19, §31).
- Traceability / accuracy language capped at "what was entered against the job" — not "full
  traceability", not "proof", not "guaranteed accurate".
- Panel 7's record card is explicitly labelled illustrative; not an actual Mysoft screenshot
  until a real capture is supplied.
- No competitor names. Do not frame this as "unlike other MES" — it is a problem story, not
  a comparison.

## CTA
Primary: "Follow for more on shop-floor visibility." Secondary (first comment, optional):
link to the relevant mysoftmes.com page once REC-6 (the verification-frame explainer) exists.

## Caption (publish copy) — DRAFT

The end-of-day report says 500. The floor actually made 480.

Which number is running your schedule tomorrow?

On a manually-recorded floor, the number you manage from isn't the number that happened — it's the number that got written down. A miscount here, a late entry there, a job logged against the wrong number. None of it dishonest. Just manual.

Nobody sees the 20-unit gap on the day. It shows up later — a short delivery, a stock count that won't reconcile, a customer asking where their order is. And next week's plan was already built on 500.

When the count is entered against the job, at the step, by the person doing it — the reported number and the real number are the same number. You plan from the floor, not from the write-up.

(The 500 and 480 here are an illustration, not a Mysoft result.)

Swipe through → and follow for more on shop-floor visibility.

#ShopFloorVisibility #ManufacturingMalaysia #MES #ProductionPlanning #Industry4WRD

(Link, if used, goes in the first comment per the LinkedIn 2026 algo note.)

## Hypothesis
WE BELIEVE a 9-panel carousel built on the plan-vs-actual / verification frame FOR general
managers and operations managers ON LinkedIn WILL produce dwell time and saves per impression
at least equal to LI-C1's shift-handover frame BECAUSE the verification frame is the
positioning territory Mysoft intends to own (`positioning.md` §32) and is white space against
the one tracked competitor's OEE-led content — so it should resonate with the budget-holding
audience at least as strongly as the operational shift-handover story does with production
managers.

## Success metric
- **Primary:** average dwell time per impression (or saves per impression if dwell is
  unavailable) — compared to **LI-C1** and to the September LinkedIn text-post median.
- **Secondary:** follows; qualified comments (people describing their own reported-vs-real
  gap); profile visits from GM / director titles specifically.
- **Comparison baseline:** LI-C1's first read + the September text cycle. No numeric target
  until those exist (`decision_framework.md` §26).

## Review date
After LI-C1 and the September LinkedIn cycle have produced first-party data, or 2026-11-15,
whichever is first.
