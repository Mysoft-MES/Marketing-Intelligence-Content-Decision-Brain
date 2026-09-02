# DAILY OPERATING SPEC

Version: 1.0
Created: 2026-09-02
Authorised by: human owner (explicit instruction, 2026-09-02)
Status: ACTIVE

---

# 1. PURPOSE

This file is the operating agreement for the automated daily research and prompting cycle.

It exists in `00_SYSTEM/` for one specific reason: `know_yourself` loads `00_SYSTEM/`, `01_BUSINESS/company_profile.md` and `05_CREATIVE/prompting_rules.md` — it does **not** load `08_DECISIONS/`. Any operating agreement stored only in the decision log would be invisible to a fresh scheduled run. This file guarantees every run inherits the same operating rules.

Each scheduled run starts as a completely fresh session with no memory of prior conversations. This file plus `know_yourself` is the full bootstrap.

This file governs **process**. It does not override `brain_rules.md`, `decision_framework.md`, `evidence_rules.md` or `routing_rules.md`. Where it appears to conflict with those, those win and this file is wrong and must be corrected.

---

# 2. SCHEDULE

Run time: **09:30 MYT (UTC+8), daily.**

Hard dependency: the social-engine MCP server runs on the local machine `mysoftware-nb-34` and is reached through the Claude desktop app. **If that machine is offline or the desktop app is closed at 09:30 MYT, the run cannot happen.** A missed run is a skipped day, not a queued job. Do not attempt to compensate by doubling output the next day — that violates the stopping rule in Section 5.

If a run finds evidence that one or more days were missed, note it in `06_PERFORMANCE/learning_log.md` and continue with the current day's theme only.

---

# 3. AUTONOMY BOUNDARIES

Confirmed by the human owner on 2026-09-02.

## MAY WRITE DIRECTLY

- `02_AUDIENCE/`
- `03_PLATFORM/`
- `04_COMPETITORS/`
- `05_CREATIVE/`
- `06_PERFORMANCE/`
- `07_RESEARCH/`
- `08_DECISIONS/`

## MUST NOT WRITE DIRECTLY

- `00_SYSTEM/`
- `01_BUSINESS/`

Changes to these two folders are proposed in `08_DECISIONS/brain_update_proposals.md` with the exact intended text, and applied only after human approval. This matches `update_rules.md` — Protected Knowledge.

## MUST NOT DO WITHOUT EXPLICIT HUMAN CONFIRMATION

- Push to GitHub. `sync_changed_files_to_github` requires `dry_run=False` and the confirmation string. A run may write locally and preview, but never pushes on its own authority.
- Publish or schedule any post for actual publication.
- Mark any content calendar as approved.
- Record a pattern as VALIDATED without the sample-size threshold being met by the analysis tool itself.

---

# 4. DAILY ROTATION

One theme per day. Rotation exists to prevent the brain filling with seven loosely-related files a week, per `brain_rules.md` §31 (Never Become A Content Factory).

| Day | Theme | Primary destination |
|---|---|---|
| Monday | Competitor activity | `04_COMPETITORS/<competitor>.md`, patterns and gaps files |
| Tuesday | Platform behaviour and algorithm change | `03_PLATFORM/<platform>.md` |
| Wednesday | Audience and customer signals | `02_AUDIENCE/<role>.md`, `07_RESEARCH/customer_insights.md` |
| Thursday | Industry, government, grants, regulation | `07_RESEARCH/industry_news.md`, `government_updates.md` |
| Friday | Search and social trends, then weekly synthesis and hygiene | `07_RESEARCH/search_trends.md`, `social_trends.md` |

Friday additionally runs: `audit_knowledge_freshness`, `find_knowledge_conflicts`, and an update of `07_RESEARCH/research_index.md`, `02_AUDIENCE/audience_index.md`, `03_PLATFORM/platform_index.md`, `04_COMPETITORS/competitor_index.md`.

Weekends: no scheduled run.

---

# 5. RESEARCH STOPPING RULE

Applies every run, per `evidence_rules.md` §38.

1. Before writing, search existing knowledge. If the finding already exists, **update the existing entry rather than creating a new one.**
2. Maximum **one** new dated research file per run. Everything else updates existing files.
3. Never duplicate the same paragraph across multiple files. Put the fact in its primary home and only the strategic implication elsewhere, per `routing_rules.md` — Primary File Rule.
4. If a run finds nothing that materially changes the brain's understanding, **write nothing and say so.** A quiet day is a valid outcome. Volume is not the objective.
5. Every entry records: source, publication date, evidence tier, confidence, and date checked.

---

# 6. EVIDENCE DISCIPLINE

Non-negotiable, carried from `evidence_rules.md` and confirmed by the human owner:

- Every external benchmark is cited with source and publication date.
- External timing and performance benchmarks are labelled **TESTING**, never VALIDATED.
- Mysoft-specific timing may only be called validated when `analyze_posting_time_performance` returns `can_claim_best_time: true` for that segment.
- Never invent performance data, customer evidence, or research.
- Separate FACT / OBSERVATION / INFERENCE / ASSUMPTION / HYPOTHESIS / VALIDATED LEARNING.
- Competitor and vendor claims are evidence of *what that party claims*, not independently verified fact.
- Respect `01_BUSINESS/products.md` §30 (Product Claim Safety) and §31 (Prohibited Unverified Claims) in every prompt and every piece of content.

---

# 7. CONFIRMED ROUTING DECISIONS (2026-09-02)

These resolve ambiguities `routing_rules.md` did not cover.

| Subject | Destination | Note |
|---|---|---|
| Gemini image/video generation prompts | `05_CREATIVE/generation_prompts/` | New convention, approved 2026-09-02 |
| Finished dated content calendars | `05_CREATIVE/content_calendars/` | Combined index plus one file per platform |
| Repeated validated performance pattern | `06_PERFORMANCE/validated_patterns.md` | Canonical. `05_CREATIVE/winning_patterns.md` retired |
| Marketing and creative experiments | `08_DECISIONS/experiments.md` | Canonical. Use the `create_experiment` / `record_experiment_result` / `close_experiment` tools. `05_CREATIVE/creative_experiments.md` retired |
| Full evidence-backed content recommendation | `08_DECISIONS/recommended_content.md` | Its template matches `build_recommendation_context` required output fields. **Retained** |
| Lightweight parked content idea | `08_DECISIONS/content_backlog.md` | Different stage from recommended_content, not a duplicate |
| Daily competitor finding | Individual `04_COMPETITORS/<competitor>.md` first | Repeated behaviour to `competitor_patterns.md`; white space to `competitor_gaps.md`. `07_RESEARCH/competitor_updates.md` retired |
| Post results | `record_post_performance` tool, not a hand-written file | Structured records are what the timing analysis reads |
| Metric selection per objective | `06_PERFORMANCE/performance_framework.md` | Active reference, not a duplicate |

---

# 8. NAVIGATION INDEXES

`02_AUDIENCE/audience_index.md`, `03_PLATFORM/platform_index.md`, `04_COMPETITORS/competitor_index.md`, `07_RESEARCH/research_index.md` and `05_CREATIVE/content_calendars/calendar_index.md` are navigation layers.

Update the relevant index in the same run as any file it points to is created, renamed, retired, or materially changed. Confirmed requirement, 2026-09-02.

---

# 9. PROMPTING STAGE

Runs after research, using that day's research plus the current refinement statement when one exists.

1. Adapt every idea to its platform. Identical cross-posts are prohibited by `brain_rules.md` §7.
2. One prompt file per platform per planned asset, in `05_CREATIVE/generation_prompts/`.
3. Every prompt records the research entry it derives from, so the chain from evidence to creative is traceable.
4. Every prompt carries a hypothesis and a success metric before it is produced, per `decision_framework.md` §26.
5. No prompt may instruct generation of a claim prohibited by `products.md` §31.

---

# 10. NOTIFICATION AND CALENDAR

Pending connector installation. Gmail and Google Calendar are not connected as of 2026-09-02.

When connected: email the human owner on completion of the prompting stage, and create Google Calendar entries for media production dates. Until then, report in session and leave the prompts in the repository.

---

# 11. STAGES NOT YET ACTIVE

- **Stage 3 — media generation.** Deferred by the human owner. The Gemini API key is not required for the prompting stage; it is only needed here.
- **Stage 4 — refinement.** Requires Windsor.ai and Zoho CRM. Neither is connected as of 2026-09-02. When active, the refinement statement lands in `06_PERFORMANCE/refinement_log.md` and is read at the start of Sections 4 and 9 above.

---

# 12. UPDATE RULE

This file changes only on explicit human instruction. A scheduled run may propose changes in `08_DECISIONS/brain_update_proposals.md` but must not edit this file itself.
