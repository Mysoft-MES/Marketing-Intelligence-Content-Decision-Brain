# Content Calendar Index

Navigation layer for all dated, platform-specific content calendars.

Convention created 2026-09-02 by human approval. `00_SYSTEM/routing_rules.md` did not define a home for finished dated calendars — the prior LinkedIn calendar identified this same gap itself and recommended exactly this convention.

**How to use:** this index is the overview. Click through to a platform file for the full detail of each post — slot, audience, format, hook, CTA, timing evidence, confidence, test metric and review date.

---

## Structure

```
05_CREATIVE/content_calendars/
├── calendar_index.md          ← you are here
├── 2026-09-linkedin.md
├── 2026-09-facebook.md
└── 2026-09-instagram.md
```

Naming: `YYYY-MM-<platform>.md`, one file per platform per month.

---

## Active calendars — September 2026

| Platform | Posts | Cadence | Slot(s) MYT | Timing validates this cycle? | Status | Detail |
|---|---|---|---|---|---|---|
| LinkedIn | 8 + 1 | Tue & Thu | 09:30 / 13:00, counterbalanced | **Yes** — n=4 per slot | AWAITING HUMAN APPROVAL | [2026-09-linkedin.md](2026-09-linkedin.md) |
| Facebook | 4 | Weekly, Tue | 20:00 | Baseline only — n=4, single slot | AWAITING HUMAN APPROVAL | [2026-09-facebook.md](2026-09-facebook.md) |
| Instagram | 4 | Weekly, Wed | 20:00 | **No** — n=3, Malaysia Day displacement | AWAITING HUMAN APPROVAL | [2026-09-instagram.md](2026-09-instagram.md) |

**Nothing here is approved for publication.** Per `00_SYSTEM/brain_rules.md` §30, an AI recommendation is not a decision until a human approves it. Approvals are recorded in `08_DECISIONS/decision_log.md`.

Total: 17 posts across 4 weeks. All at LOW confidence and TEST status — `build_recommendation_context` returned `maximum_confidence: LOW` for all six audience-platform pairs evaluated, capped by placeholder audience profiles and `01_BUSINESS/swot.md`.

---

## The cycle's one measurable objective

No Mysoft-specific posting-time evidence exists on any platform. `analyze_posting_time_performance` returned `record_count: 0` and `can_claim_best_time: false` for LinkedIn, Facebook and Instagram alike.

Every time in every calendar is an **externally-sourced TESTING hypothesis**, never a validated Mysoft best time.

LinkedIn is the platform designed to fix that: two slots, four posts each, day-of-week and voice both counterbalanced, reaching the minimum sample size within one cycle. Facebook holds one slot to establish a baseline. Instagram will fall one short and needs a second cycle — stated up front.

**Cycle review: 2026-10-08.**

---

## Copy sources

| Platform | Where the post copy lives |
|---|---|
| LinkedIn | `05_CREATIVE/linkedin_content_calendar_2026-09.md` — copy bank, not a schedule |
| Facebook | In the calendar file (topic, format, hook, CTA); prompts in `05_CREATIVE/generation_prompts/` |
| Instagram | In the calendar file; prompts in `05_CREATIVE/generation_prompts/` |

---

## Cross-references

| Need | File or tool |
|---|---|
| Media generation prompts | `05_CREATIVE/generation_prompts/` |
| Reusable hooks | `05_CREATIVE/hook_library.md` |
| Reusable video formats | `05_CREATIVE/video_formats.md` |
| Which metric counts for which objective | `06_PERFORMANCE/performance_framework.md` |
| Logging results | `record_post_performance` tool |
| Timing validation status | `analyze_posting_time_performance` tool |
| Parked ideas | `08_DECISIONS/content_backlog.md` |
| Full evidence-backed proposals | `08_DECISIONS/recommended_content.md` |
| Daily run rules | `00_SYSTEM/daily_operating_spec.md` |
