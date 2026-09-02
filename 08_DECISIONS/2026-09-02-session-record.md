# Session Record — 2026-09-02

Working session covering a four-week posting schedule, a pipeline design, and a full repository audit and restructure.

**Filing note:** this sits in `08_DECISIONS/` rather than `07_RESEARCH/` deliberately. `routing_rules.md` scopes `07_RESEARCH/` to external evidence — "what is happening outside." This is an internal work record and the rationale behind decisions already logged in `decision_log.md`.

---

## 1. Four-week posting schedule

Built from tool evidence in the required order: `know_yourself` → `build_posting_schedule_context` → `analyze_posting_time_performance` per platform → `build_recommendation_context` per audience-platform pair.

**Every timing tool returned `can_claim_best_time: false` with `record_count: 0`.** No Mysoft-specific posting time exists on any platform. All six recommendation packets returned `maximum_confidence: LOW` and `recommended_action_class: TEST`.

External benchmarks used, all labelled TESTING, all cited with publication dates: Sprout Social (31 Mar 2026, ~2bn engagements / ~307k profiles), PostFast (6 Jun 2026, synthesising Buffer 4.8M posts), ZenWeb Malaysia (20 Aug 2026, undisclosed sample). None is B2B-manufacturing-specific, and **they disagree** — Sprout puts LinkedIn at midday, the other two in the morning.

That disagreement became the experiment rather than a guess. LinkedIn runs two slots (09:30 and 13:00), four posts each, with day-of-week alternating weekly *and* founder/company-page voice split 2–2 within each slot. Voice is counterbalanced because named-person posts reportedly reach 6–10× company-page posts — an uneven split would have biased the timing result. Four per slot is exactly the tool's `minimum_sample_size`, so LinkedIn is designed to validate within one cycle.

Facebook holds one slot to establish a baseline (4 posts across 2 slots would give n=2, which validates nothing). Instagram will reach only n=3 because Malaysia Day displaces the Week 2 slot — stated up front rather than discovered at review.

Calendars: `05_CREATIVE/content_calendars/`. All **AWAITING HUMAN APPROVAL**.

## 2. Pipeline design

Four stages agreed: daily research filed by subject → per-platform media generation prompts → media generation (deferred) → Windsor.ai + Zoho refinement loop (deferred, connectors not installed).

Operating rules in `00_SYSTEM/daily_operating_spec.md`: 09:30 MYT daily, themed rotation Monday to Friday, one new dated research file per run maximum, and an explicit instruction that a quiet day is a valid outcome.

Dependency worth remembering: social-engine runs on the local machine via the Claude desktop app. A run requires that machine online. Gmail and Google Calendar connected mid-session; Windsor.ai and Zoho CRM remain uninstalled.

## 3. Repository audit — the significant finding

**The placeholder detector matches on a heading containing "Template", not on whether a file has content.**

Proven on `02_AUDIENCE/factory_owner.md` in three steps: original (5,790 chars, flagged) → `_(placeholder)_` marker removed, heading kept (still flagged) → heading renamed to `## Profile` (clean, content byte-identical at 5,790 chars).

Consequences:

- **False positives:** eight populated files carrying ~36,000 characters of cited research were reported empty — all seven audience profiles and `03_PLATFORM/website.md`.
- **False negatives:** `current_priorities.md` (38 chars), `experiments.md` (31), `campaign_history.md` (36) were not flagged at all.
- **Downstream:** `build_recommendation_context` reads this status and lists affected files as critical evidence gaps, capping `maximum_confidence` at LOW. Part of the September schedule's LOW confidence was caused by stale heading text rather than missing evidence.

An earlier diagnosis in this session blamed the `_(placeholder)_` marker string. **That was wrong** and was corrected after testing. Files such as `hook_library.md` and `content_backlog.md` carry that marker alongside real content and were never flagged — because neither has a "Template" heading.

Headings were renamed on the eight affected files, which is defensible on its own terms (a filled profile should not be headed "Profile Template") but is a workaround. The durable fix is in `server.py` and is filed as Proposal 5 in `brain_update_proposals.md`.

**Incident:** `update_markdown_section` was pointed at an H1 during testing and destroyed `factory_owner.md`, reducing it from 5,790 characters to 173. It treats an H1 section as everything beneath it. The file was recovered verbatim from the public repository and verified. The hazard is documented in `CLAUDE.md` and `README.md`.

## 4. Restructuring applied

- Retired as duplicates: `winning_patterns.md` (→ `06_PERFORMANCE/validated_patterns.md`), `creative_experiments.md` (→ `08_DECISIONS/experiments.md`), `competitor_updates.md` (→ `04_COMPETITORS/`), `creative_rules.md` (merged into `creative_strategy.md`)
- **Kept against an earlier recommendation:** `recommended_content.md` — its template matches `build_recommendation_context`'s required output fields, so retiring it would have broken the recommendation path. `routing_rules.md` was also proposed for removal in error and kept; it is the filing map for the entire daily job.
- Cross-competitor conclusions routed out of `competitor_index.md` into `competitor_patterns.md` (4 patterns) and `competitor_gaps.md` (5 gaps)
- `platform_index.md` built from 163 characters into a real navigation layer — which surfaced that **WhatsApp is unresearched despite being the destination for every Facebook CTA in the current cycle**
- New conventions: `05_CREATIVE/generation_prompts/`, `05_CREATIVE/content_calendars/`

## 5. Two files that were nearly discarded

Both were described as test files. Both contained substantial work and were preserved.

`linkedin_content_calendar_2026-09.md` — 12 drafted LinkedIn posts with strong claim discipline: refusing to promise zero errors, telling Excel users they may not need to change, declining to claim ERP compatibility before seeing the environment, and marking unverified figures `[VERIFY]` rather than inventing them. Now the **copy bank** for the September LinkedIn calendar. It had also independently recommended the `content_calendars/` convention later adopted.

`prompt.md` — §0 is a real operating instruction naming the correct tool sequence, including the atomic sync path. It was consulted *after* the Git-subprocess sync had already timed out; it had documented the correct path all along. Left in place by instruction; its overlap with `daily_operating_spec.md` is unresolved and filed as Proposal 3.

## 6. State at close

Commits: `9d37e9e` (conventions and calendars), `decdef6` (housekeeping). Placeholder count fell from 25 files to 17, every remainder genuinely empty.

**Unresolved and requiring human input:**

- `01_BUSINESS/swot.md`, `01_BUSINESS/sales_insights.md`, `08_DECISIONS/current_priorities.md` — empty; these are what hold recommendation confidence at LOW
- September calendars unapproved; named person for the four founder-voice LinkedIn posts unconfirmed
- Proposals 1–6 in `brain_update_proposals.md` unapplied, including the `server.py` detector fix
- Competitor social audit never done across all 14
- No customer proof exists, blocking LinkedIn's strongest documented format
- The 09:30 scheduled task has **not** been created — one supervised research-and-prompting cycle was to run first
