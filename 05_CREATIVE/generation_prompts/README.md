# Generation Prompts

Media generation prompts for image and video tools (currently Gemini).

Created 2026-09-02 by human approval. `00_SYSTEM/routing_rules.md` did not define a home for these, and the three existing prompt files serve different purposes:

| File | Purpose | Not this |
|---|---|---|
| `05_CREATIVE/prompting_rules.md` | Rules for *constructing* prompts | Not a store of prompts |
| `05_CREATIVE/prompt_library.md` | Prompts for operating the Brain / MCP tasks | Not media generation |
| `05_CREATIVE/prompt_templates.md` | Reusable MCP task scaffolds | Not media generation |
| **`generation_prompts/`** | **Ready-to-run image and video prompts** | — |

---

## Naming

`YYYY-MM-DD-<platform>-<post-id>.md`

Examples: `2026-09-08-facebook-FB-01.md`, `2026-09-09-instagram-IG-01.md`

The post ID ties the prompt to its row in `05_CREATIVE/content_calendars/`. One file per asset. Do not batch multiple platforms into one file — platform adaptation is the point.

---

## Rules

1. **Never write one prompt and reuse it across platforms.** `brain_rules.md` §7 prohibits identical cross-posts. Shared footage is fine; shared structure, length, hook and CTA are not.
2. **Every prompt cites the research it came from.** If you cannot name the file and finding that motivated it, it is not evidence-based and should not be produced.
3. **Every prompt carries a hypothesis and a success metric** before production, per `decision_framework.md` §26.
4. **Check every claim against `01_BUSINESS/products.md` §30–31** before writing the prompt. No percentage improvements, no guaranteed ROI, no implementation durations, no "works with any ERP", no zero-error claims.
5. **Status starts at DRAFT.** Only a human moves it to APPROVED.

---

## Entry Template

```
# <Post ID> — <Platform> — <YYYY-MM-DD>

**Status:** DRAFT / APPROVED / PRODUCED / PUBLISHED
**Calendar row:** 05_CREATIVE/content_calendars/<file>.md
**Platform:** 
**Audience:** 
**Objective / funnel stage:** 
**Asset type:** image / video
**Aspect ratio:** 
**Target duration:** 
**Language:** 

## Evidence basis
- Research file: 
- Finding used: 
- Evidence tier and confidence: 

## Hook (first 1–3 seconds)

## Shot list / composition

## On-screen text

## Tone and art direction

## What must NOT appear
(claims, visuals, or language prohibited by products.md §31 or positioning.md)

## CTA

## Hypothesis
WE BELIEVE <change> FOR <audience> ON <platform> WILL <effect> BECAUSE <evidence>.

## Success metric
Primary: 
Secondary: 

## Review date
```

---

## Index

Drafted 2026-09-02 from the September 2026 Facebook and Instagram calendars. **All DRAFT — none approved.** The parent calendars are themselves `AWAITING HUMAN APPROVAL`; these prompts do not change that. LinkedIn is not represented here — its September posts are text, with copy in `05_CREATIVE/linkedin_content_calendar_2026-09.md`.

| Date | Post ID | Platform | Asset | Status |
|---|---|---|---|---|
| 2026-09-08 | FB-01 | Facebook | 30–45s Reel — "where is this job" silence | DRAFT |
| 2026-09-15 | FB-02 | Facebook | 30–45s Reel — paper vs digital job record, split screen | DRAFT |
| 2026-09-22 | FB-03 | Facebook | 30–45s Reel — brand-line message test (看不见的损失…) | DRAFT |
| 2026-09-29 | FB-04 | Facebook | 30–45s Reel — "the record just can't be checked" | DRAFT |
| 2026-09-09 | IG-01 | Instagram | 60–90s process-breakdown — six stations, one number | DRAFT |
| 2026-09-17 | IG-02 | Instagram | 45–60s screen recording — Digital Job Order record tour | DRAFT |
| 2026-09-23 | IG-03 | Instagram | 60–90s — traceability check, step by step | DRAFT |
| 2026-09-30 | IG-04 | Instagram | 60–90s process-breakdown — what replaces the clipboard | DRAFT |

### Open dependencies before any of these can be produced

- **Named founder** for FB voice consistency is a LinkedIn-calendar prerequisite; not required for FB/IG here, but the same person should front any talking-head.
- **Real Mysoft Digital Job Order screen capture** for IG-02 (and the tablet insert in FB-01/FB-02). Until supplied, those use an accurately-labelled representative mock.
- Human approval of the parent calendars in `08_DECISIONS/decision_log.md`.
