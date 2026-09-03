# Decision Log

_(placeholder)_

## 2026-09-02
## Decision — Shift-Change "Process Breakdown" Reel Opportunity: MONITOR (2026-09-02)

**Date:** 2026-09-02
**Decision:** Classify the proposed "Shift-Change Process Breakdown Reel" opportunity (Production Manager audience, Instagram, Mysoft MES — see `08_DECISIONS/content_backlog.md` and `07_RESEARCH/2026-09-02-instagram-content-opportunities-production-manager.md`) as **MONITOR**, not TEST or CREATE.
**Context:** AI-proposed content opportunity generated via research task on 2026-09-02, reviewed by human decision-maker.
**Evidence:** LOW-MEDIUM confidence — supporting sources are Tier 4 (marketing-agency blogs), non-Malaysia, non-MES-specific, and largely single-case-study sourced. `01_BUSINESS/sales_insights.md` and `01_BUSINESS/swot.md` are TEMPLATE_ONLY, so no internal sales or SWOT evidence exists to strengthen this. No Mysoft first-party Instagram performance data exists yet.
**Options considered:** CREATE (rejected — evidence too weak), TEST (considered — low incremental production cost if bundled with existing planned shoot), MONITOR (selected).
**Why this option was chosen:** Human decision-maker selected MONITOR.
**Expected result:** No immediate production action. Revisit if Mysoft's own Instagram performance data becomes available, if `sales_insights.md`/`swot.md` are populated with real evidence, or if a Malaysia/MES-specific signal for the process-breakdown format emerges.
**Actual result:** Pending — not yet applicable.
**Learning:** Pending — not yet applicable.
**Approved by:** Human review (this conversation, 2026-09-02).

## 2026-09-02
## Operating and structure decisions — 2026-09-02

Human-approved in session. These are actual decisions, not AI proposals.

**1. Daily automated cycle approved.**
Research then prompting, 09:30 MYT daily. Operating rules in `00_SYSTEM/daily_operating_spec.md`. Reason: build a continuous evidence loop rather than ad-hoc content. Dependency acknowledged — social-engine runs on the local machine, so a run requires that machine online with the desktop app open.

**2. Autonomy boundaries set.**
Agent may write directly to `02_AUDIENCE/` through `08_DECISIONS/`. `00_SYSTEM/` and `01_BUSINESS/` changes go to `08_DECISIONS/brain_update_proposals.md` for human approval. No GitHub push and no publication without explicit human confirmation.

**3. New conventions created.**
`05_CREATIVE/generation_prompts/` for media generation prompts. `05_CREATIVE/content_calendars/` for dated per-platform calendars with a combined index. Reason: `routing_rules.md` defined no home for either; the prior LinkedIn calendar had independently flagged the second gap.

**4. Duplicate files retired.**
`05_CREATIVE/winning_patterns.md` → use `06_PERFORMANCE/validated_patterns.md`.
`05_CREATIVE/creative_experiments.md` → use `08_DECISIONS/experiments.md`.
`07_RESEARCH/competitor_updates.md` → use individual competitor profiles, patterns and gaps files.
`08_DECISIONS/recommended_content.md` was proposed for retirement and **kept** — its template matches `build_recommendation_context` required output fields, so retiring it would have broken the recommendation output path.
`00_SYSTEM/routing_rules.md` was proposed for removal in error and **kept** — it is the filing map for the entire daily job.

**5. September LinkedIn calendar — combined approach approved.**
The 12 drafted posts in `05_CREATIVE/linkedin_content_calendar_2026-09.md` are retained as the copy bank. The Mon/Wed/Fri cadence is replaced by a Tue/Thu counterbalanced two-slot design in `05_CREATIVE/content_calendars/2026-09-linkedin.md`. Reason: preserves written work while making posting time measurable within one cycle. 8 posts scheduled, 1 outside the experiment, 3 parked.

**6. Content benchmarking extended to social.**
A social scorecard is to be added alongside the existing website scorecard in `00_SYSTEM/content_benchmark.md`, reweighted to hook strength, platform fit, audience fit, message clarity, CTA appropriateness and claim safety. Weighting approved 2026-09-02; application pending as a protected-file change.

**7. Navigation indexes must be updated daily** whenever a file they point to changes.

**8. Root `prompt.md` left in place** by human instruction. Its §0 operating workflow overlaps `daily_operating_spec.md`; the overlap is noted in `brain_update_proposals.md` and not yet resolved.

**Still not decided:** whether the September calendars are approved for publication. All three remain AWAITING HUMAN APPROVAL.



## 2026-09-03 — Daily run made fully autonomous (v2.0)

**Decision:** APPROVED by the human owner in an interactive session, 2026-09-03.

**What changed:**
- The `marketing-brain-daily` scheduled run now does a **full sweep of all research areas
  every run** (competitor, platform, audience, industry, government, market, search,
  social) instead of one theme per day.
- The run **pushes to GitHub `main` autonomously** — research after the research stage,
  DRAFT generation prompts after the prompting stage — with **no human confirmation and
  no manual sync step**.
- The prompting stage is active every run when the evidence warrants an asset.
- Email + calendar record still happen at the end of every run.

**Files edited (direct, on explicit owner instruction):**
- `00_SYSTEM/daily_operating_spec.md` → v2.0 (header note, §3, §4, §5, §9, §10)
- `.claude/scheduled-tasks/marketing-brain-daily/SKILL.md` → rewritten
- `CLAUDE.md` → autonomy boundaries + tooling-hazard note

**Limits kept hard:** no direct writes to `00_SYSTEM/` or `01_BUSINESS/`; no social
publishing / outreach / paid spend; nothing marked APPROVED or VALIDATED without the
stated gate; no remote deletions.

**Reason:** Owner wants hands-off daily operation and accepts the risk of unreviewed AI
output landing on the public repo. Owner will intervene if a problem appears
("we will check it once there is a problem").

**Risk accepted:** LOW-confidence / secondary-source research and AI-drafted content
prompts become publicly visible on GitHub `main` the same day, with no human review before
publication to the repo. Mitigation retained: evidence classes and claim-safety §30–31
still enforced in every entry and prompt; prompts stay DRAFT; nothing reaches an actual
social platform without a human.

**Expected result / review:** Monitor the first few autonomous runs via the daily email.
Revisit if research quality drops, the repo fills with noise, or a claim-safety issue
reaches `main`.



## 2026-09-03 — swot.md restored, sales_insights.md populated (owner-instructed)

**Decision:** APPROVED by the human owner in an interactive session, 2026-09-03. Both are
`01_BUSINESS/` (protected) files; the owner gave explicit in-session instruction, which is
the human approval the autonomy rule requires.

**1. `01_BUSINESS/swot.md` — restored from GitHub commit `19bcc1f` ("Add SWOT analysis for
Mysoft MES").** The full ~15-section SWOT was replaced with a placeholder template by a
later "structure/templates" commit (`c14cd7a` / `b04e1b8`) and has been empty since. Owner
asked for the `19bcc1f` content back, verbatim. Restored as-is (still dated "Last Updated:
2026-09-01" — not changed). This clears the "swot.md empty" evidence gap that was capping
`build_recommendation_context` at LOW.

**2. `01_BUSINESS/sales_insights.md` — populated with the current sales stage** (first-party,
stated by the owner 2026-09-03): Mysoft MES is **pre-revenue**; an initial workshop is done;
**zero customers**; the sales motion is currently **demos with potential customers**, and no
demo outcomes/objections/win-loss data exist yet. The file records this, reconciles it
against the forward-looking "customer/implementation" language in swot.md / positioning.md /
products.md ("direction, not proof"), lists what to capture from each demo going forward,
and keeps an empty entry log.

**Effect:** two of the three "blocking quality" files in `CLAUDE.md` are no longer empty.
`08_DECISIONS/current_priorities.md` is still empty. Customer proof still does not exist
(pre-customer), so the quantified case-study format stays unavailable and
`customer_objections.md` stays all-HYPOTHESIS.

