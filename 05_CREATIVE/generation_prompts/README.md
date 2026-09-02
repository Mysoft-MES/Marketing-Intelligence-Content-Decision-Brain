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

No prompts written yet.

| Date | Post ID | Platform | Status |
|---|---|---|---|
| — | — | — | — |
