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
5. **Status starts at DRAFT.** Only a human moves it to APPROVED — and only through the
   approval Pull Request (see below). The daily run never sets APPROVED itself.

---

## Approval — the "human checking" gate

New and regenerated DRAFT prompts are **not** pushed to `main` by the daily run. They go onto
a branch `approvals/<YYYY-MM-DD>` and the run opens a Pull Request to `main`. The owner:

- **merges** the PR to approve every prompt in it,
- comments `deny <POST-ID>: <reason>` (then merges) to reject specific prompts,
- **closes** the PR to reject all.

The next run (or the same-day apply run) reads the PR and does the bookkeeping via
`apply_prompt_decision` — flipping approved prompts to `APPROVED`, logging them to
`08_DECISIONS/decision_log.md`, logging denied ones to `08_DECISIONS/rejected_ideas.md`, and
regenerating the denied ones into the next PR. Full flow and the `server.py` tools:
[`APPROVAL_UI.md`](../../APPROVAL_UI.md).

Status strings set by the flow:

| Status | Meaning |
|---|---|
| `DRAFT` | In (or awaiting) an approval PR; not yet decided |
| `APPROVED (human via approval PR, <date>)` | Merged approval PR — asset may be produced, not published |
| `REJECTED (human via approval PR, <date>) — see 08_DECISIONS/rejected_ideas.md` | Denied; regenerated into a later PR |

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

Drafted 2026-09-02 from the September 2026 Facebook and Instagram calendars. **All DRAFT — none approved.** The parent calendars are themselves `AWAITING HUMAN APPROVAL`; these prompts do not change that. LinkedIn's September posts are text (copy in `05_CREATIVE/linkedin_content_calendar_2026-09.md`); **LI-C1 (added 2026-09-03) is a new carousel-format TEST proposal with no calendar row yet** — derived from `07_RESEARCH/2026-09-03-competitor-content-activity-first-pass.md` and the 2026-09-03 LinkedIn algorithm findings. A human must add a row or approve it standalone before production.

| Date | Post ID | Platform | Asset | Status |
|---|---|---|---|---|
| 2026-09-08 | FB-01 | Facebook | 30–45s Reel — "where is this job" silence | DRAFT |
| 2026-09-15 | FB-02 | Facebook | 30–45s Reel — paper vs digital job record, split screen | DRAFT |
| 2026-09-22 | FB-03 | Facebook | 30–45s Reel — brand-line message test (看不见的损失…) | APPROVED |
| 2026-09-29 | FB-04 | Facebook | 30–45s Reel — "the record just can't be checked" | APPROVED |
| 2026-09-09 | IG-01 | Instagram | 60–90s process-breakdown — six stations, one number | APPROVED |
| 2026-09-17 | IG-02 | Instagram | 45–60s screen recording — Digital Job Order record tour | APPROVED |
| 2026-09-23 | IG-03 | Instagram | 60–90s — traceability check, step by step | DRAFT |
| 2026-09-30 | IG-04 | Instagram | 60–90s process-breakdown — what replaces the clipboard | APPROVED |
| 2026-09-03 | LI-C1 | LinkedIn | 6-panel carousel — "a shift handover, panel by panel" (NEW format test; no calendar row yet) | APPROVED |

### Open dependencies before any of these can be produced

- **Named founder** for FB voice consistency is a LinkedIn-calendar prerequisite; not required for FB/IG here, but the same person should front any talking-head.
- **Real Mysoft Digital Job Order screen capture** for IG-02 (and the tablet insert in FB-01/FB-02). Until supplied, those use an accurately-labelled representative mock.
- Human approval of the parent calendars in `08_DECISIONS/decision_log.md`.
