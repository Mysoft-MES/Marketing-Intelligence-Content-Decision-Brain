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



## 2026-09-03 — Operating loop gains a second analysis stage (v2.1, owner-instructed)

**Decision:** APPROVED by the human owner in an interactive session, 2026-09-03. Explicit
in-session instruction is the human approval the autonomy rule requires for the
`00_SYSTEM/` (protected) change.

**What changed — the loop now has TWO analysis stages, not one:**

- **Analysis #1 ("Researching")** — runs after Research and before Prompting. An
  interpretation pass (no new sources) that turns the run's findings into an explicit
  content decision (Create / Test / Monitor / Nothing). Output → new file
  `08_DECISIONS/analysis_log.md`, one dated entry per run. The prompting stage executes
  this decision.
- **Analysis #2 ("Posting")** — runs after the prompting stage. Two halves: (1) our own
  performance review; (2) a competitor comparison — our posts / ads / cadence / formats /
  angles vs the 14 verified MES competitors' content activity — producing a numbered
  "Suggestions to beat them" list. Output → new file
  `06_PERFORMANCE/competitive_benchmark.md`, plus one dated `REFINEMENT:` note appended to
  `06_PERFORMANCE/learning_log.md`.
- **The loop is closed.** Every run reads the previous run's most recent `REFINEMENT:`
  note (and the last benchmark suggestions + last analysis_log open questions) at bootstrap
  and applies them to that run's Research and Prompting. This is how "Research refers to
  Analysis #2".
- **Research full sweep** now includes a competitor **content/social** audit as deep as
  public/non-authenticated sources allow, flagging what needs a logged-in pass. Owner will
  supplement with first-hand competitor information separately.
- **Third autonomous GitHub push** added, carrying the Analysis #2 output. Push order:
  research → analysis #1 + prompts → competitive benchmark + refinement.

**Files edited (direct, on explicit owner instruction):**
- `00_SYSTEM/daily_operating_spec.md` → v2.1 (header note, new §2A, §3, §4, new §4A, §5,
  new §9A, §10)
- `.claude/scheduled-tasks/marketing-brain-daily/SKILL.md` → new §4A, §5, §6, new §6A,
  §1 bootstrap step 5, §2 competitor-content line, §9/§10
- `08_DECISIONS/analysis_log.md` → created
- `06_PERFORMANCE/competitive_benchmark.md` → created
- `06_PERFORMANCE/learning_log.md` → refinement-note convention added to the header

**Limits kept hard:** unchanged — no direct writes to `00_SYSTEM/`/`01_BUSINESS/` by a run,
no social publishing, no spend, nothing APPROVED/VALIDATED without the stated gate, no
remote deletions.

**Effect on tomorrow's run (2026-09-04):** first run under v2.1. No prior `REFINEMENT:`
note exists, so bootstrap notes that and proceeds with a normal full sweep. Analysis #1
runs normally. Analysis #2 Half 1 = "no first-party performance data yet"; Half 2 runs on
whatever the competitor content audit produces.

**Follow-up not done this session:** `CLAUDE.md` (protected) still describes the
single-analysis state — noted in `08_DECISIONS/brain_update_proposals.md` for the owner to
apply.

---

## 2026-09-03 — Content approval panel — attempted, then abandoned (owner-instructed)

A web approval panel (published Artifact with a `db` store, Approve/Reject/Changes buttons)
was built and seeded on 2026-09-03 so the owner could tap decisions and have the daily run
apply them. The panel UI would not load its data runtime in the owner's viewer, so the
owner asked to stop and remove it the same session. All wiring was reverted:
`00_SYSTEM/daily_operating_spec.md`, the scheduled-task SKILL.md, and the local panel files
were returned to their pre-panel state. The Human-checking gate stays manual — edit the
prompt file's `Status` and log it here (see `05_CREATIVE/generation_prompts/README.md`).
The artifact itself is deleted by the owner from claude.ai.

---

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

---

## 2026-09-04 — Generation-prompt approval is now a GitHub Pull Request (the "human checking" node)

**Decision:** APPROVED by the human owner in an interactive session, 2026-09-04 ("Can you do
it all"). Explicit in-session instruction is the human approval the autonomy rule requires
for the `00_SYSTEM/` (protected) changes.

**Problem:** the loop's "human checking" node (Prompting → Generating → *Human checking* ─No─↺
; Yes → Posting) had no screen — a human had to hand-edit `**Status:**` in each prompt file.
The owner asked for an Approve/Deny action reachable from the daily notification email. A
first attempt (published Artifact + `db` store) was abandoned 2026-09-03 because the Artifact
data runtime would not load in the owner's viewer.

**What changed:**
- Generation prompts are **no longer pushed to `main` by the daily run**. New/regenerated
  DRAFT prompts go onto a branch `approvals/<run_date>` and the run opens a **Pull Request**
  to `main`. Merge = approve all; comment `deny <POST-ID>: <reason>` then merge = reject
  those; close = reject all.
- Next run (and an optional same-day apply run) reads the PR and applies the decision:
  approved → status flipped to APPROVED, logged here; denied → logged to
  `08_DECISIONS/rejected_ideas.md` and regenerated into the next PR.
- A **merged PR is** the explicit human confirmation §3 requires. Nothing else sets a prompt
  APPROVED.

**Files edited / created:**
- `server.py` — four new tools: `list_generation_prompt_status`, `open_prompt_approval_pr`,
  `get_prompt_approval_pr`, `apply_prompt_decision` (offline; PR tools reuse the existing
  GitHub Data-API helpers).
- `00_SYSTEM/daily_operating_spec.md` → v2.2 (header note, §2A step 4, §3, §9 step 8, §10,
  new §13, new §14).
- `00_SYSTEM/apply_approvals_runbook.md` → created (same-day apply run).
- `APPROVAL_UI.md` (repo root) → created (operator doc + scheduled-task SKILL.md text block).
- `05_CREATIVE/generation_prompts/README.md` → approval section + status vocabulary.
- `.claude/settings.local.json` → allow-rules for the four new tools.

**Limits unchanged:** no direct writes to `00_SYSTEM/`/`01_BUSINESS/` by a run; no social
publishing; no spend; nothing VALIDATED without the sample-size gate; no remote deletions.
The PR flow *adds* a gate.

**Follow-up owned by the human:** (1) paste the SKILL.md text block from `APPROVAL_UI.md`
into the Claude-desktop scheduled task; (2) optionally create the 14:00 MYT same-day
apply OS task; (3) `CLAUDE.md` still predates this — proposal in `brain_update_proposals.md`.


## 2026-09-04
## Decision — Generation prompt LI-C1 (LinkedIn, 2026-09-03): APPROVED (2026-09-04)

**Date:** 2026-09-04
**Decision:** Move generation prompt `05_CREATIVE/generation_prompts/2026-09-03-linkedin-LI-C1.md` from DRAFT to APPROVED for production.
**Context:** Human approval recorded via the approval Pull Request (human via approval PR #1 (merged 2026-09-04)).
**Evidence:** As stated in the prompt's Evidence basis section. Approval authorises production of the asset, not publication.
**Approved by:** human via approval PR #1 (merged 2026-09-04), 2026-09-04.

## 2026-09-04
## Decision — Generation prompt IG-01 (Instagram, 2026-09-09): APPROVED (2026-09-04)

**Date:** 2026-09-04
**Decision:** Move generation prompt `05_CREATIVE/generation_prompts/2026-09-09-instagram-IG-01.md` from DRAFT to APPROVED for production.
**Context:** Human approval recorded via the approval Pull Request (human via approval PR #1 (merged 2026-09-04)).
**Evidence:** As stated in the prompt's Evidence basis section. Approval authorises production of the asset, not publication.
**Approved by:** human via approval PR #1 (merged 2026-09-04), 2026-09-04.

## 2026-09-04
## Decision — Generation prompt IG-02 (Instagram, 2026-09-17): APPROVED (2026-09-04)

**Date:** 2026-09-04
**Decision:** Move generation prompt `05_CREATIVE/generation_prompts/2026-09-17-instagram-IG-02.md` from DRAFT to APPROVED for production.
**Context:** Human approval recorded via the approval Pull Request (human via approval PR #1 (merged 2026-09-04)).
**Evidence:** As stated in the prompt's Evidence basis section. Approval authorises production of the asset, not publication.
**Approved by:** human via approval PR #1 (merged 2026-09-04), 2026-09-04.

## 2026-09-04
## Decision — Generation prompt FB-03 (Facebook, 2026-09-22): APPROVED (2026-09-04)

**Date:** 2026-09-04
**Decision:** Move generation prompt `05_CREATIVE/generation_prompts/2026-09-22-facebook-FB-03.md` from DRAFT to APPROVED for production.
**Context:** Human approval recorded via the approval Pull Request (human via approval PR #1 (merged 2026-09-04)).
**Evidence:** As stated in the prompt's Evidence basis section. Approval authorises production of the asset, not publication.
**Approved by:** human via approval PR #1 (merged 2026-09-04), 2026-09-04.

## 2026-09-04
## Decision — Generation prompt FB-04 (Facebook, 2026-09-29): APPROVED (2026-09-04)

**Date:** 2026-09-04
**Decision:** Move generation prompt `05_CREATIVE/generation_prompts/2026-09-29-facebook-FB-04.md` from DRAFT to APPROVED for production.
**Context:** Human approval recorded via the approval Pull Request (human via approval PR #1 (merged 2026-09-04)).
**Evidence:** As stated in the prompt's Evidence basis section. Approval authorises production of the asset, not publication.
**Approved by:** human via approval PR #1 (merged 2026-09-04), 2026-09-04.

## 2026-09-04
## Decision — Generation prompt IG-04 (Instagram, 2026-09-30): APPROVED (2026-09-04)

**Date:** 2026-09-04
**Decision:** Move generation prompt `05_CREATIVE/generation_prompts/2026-09-30-instagram-IG-04.md` from DRAFT to APPROVED for production.
**Context:** Human approval recorded via the approval Pull Request (human via approval PR #1 (merged 2026-09-04)).
**Evidence:** As stated in the prompt's Evidence basis section. Approval authorises production of the asset, not publication.
**Approved by:** human via approval PR #1 (merged 2026-09-04), 2026-09-04.
