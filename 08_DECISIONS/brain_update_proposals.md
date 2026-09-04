
## 2026-09-04
## daily_operating_spec.md update — competitor set reset; daily run must not add new competitors

**Status: APPLIED 2026-09-04** on the owner's explicit in-session instruction ("yes").
`daily_operating_spec.md` is now v2.3 (new header note; §2A/v2.1-note "14 verified MES
competitors" → "the competitor(s) listed in `competitor_index.md`"; §4 table competitor
rows scoped to the listed set with an explicit no-discovery rule; §9A Half 2 scoped to
`competitor_index.md`). Original proposal text kept below for the record.

**Context:** The human owner deleted the entire prior 14-competitor set from GitHub and
supplied one replacement competitor analysis (Allied Solutions Global / ASPL), which has
been copied verbatim into `04_COMPETITORS/allied-solutions-global.md` (100% human-supplied,
nothing added by the Brain). `competitor_index.md`, `competitor_gaps.md` and
`competitor_patterns.md` have been reset. Owner instruction, verbatim: *"for 9:30 am
research that you will conduct it later, please don't add any new competitor, just follow
the new added by you now, and do the analysis."*

**Proposed changes to `daily_operating_spec.md`:**

1. Header note (new v2.x): competitor set was reset 2026-09-04; the daily run does **not**
   discover or add new competitors. It analyses only the competitor(s) listed in
   `04_COMPETITORS/competitor_index.md`. Adding a competitor is a human action.
2. §4 (Research full-sweep) and §9A (Analysis #2 competitor comparison): replace every
   "the 14 verified MES competitors" / "14 verified" reference with "the competitor(s)
   listed in `competitor_index.md`".
3. §4: the competitor content/social audit covers only the listed competitor(s); it does
   not scan the market for new entrants.
4. Routing table (§ lines ~160–161, ~237): unchanged targets, but note `competitor_gaps.md`
   / `competitor_patterns.md` stay stubs until the tracked set is large enough again.

**Why:** Keeps the automated run inside the owner's explicit scope and prevents the
competitor list silently regrowing via research passes.

---

## 2026-09-04
## daily_operating_spec.md update — PR-based human approval of generation prompts (the "human checking" node)

**Status: APPLIED 2026-09-04** on the owner's explicit in-session instruction ("Can you do
it all"). `daily_operating_spec.md` is now v2.2 (header note, §2A step 4, §3, §9 step 8, §10,
new §13, new §14). `00_SYSTEM/apply_approvals_runbook.md` created. Recorded in
`decision_log.md` 2026-09-04. Original proposal text kept below for the record.

**Context:** The owner asked (interactive session, 2026-09-03/04) for the loop's **"human
checking"** node — Prompting → Generating → *Human checking* ─(No)─↺ ; (Yes) → Posting — to
be a real approval step reachable from the daily notification email, with an Approve and a
Deny action per prompt. A prior attempt (published Artifact + `db` store) was abandoned the
same day because the Artifact data runtime would not load in the owner's viewer
(`decision_log.md` 2026-09-03 "Content approval panel — attempted, then abandoned"). The
replacement uses **GitHub Pull Requests** — no artifact runtime, works from any device via
github.com, uses the owner's existing GitHub login.

**Mechanism already built (not protected, already committed/working):**
- `server.py` new tools: `list_generation_prompt_status`, `apply_prompt_decision`,
  `open_prompt_approval_pr`, `get_prompt_approval_pr`.
- `apply_prompt_decision(post_id, "approve"|"deny", reason)` flips the prompt's `**Status:**`
  line, updates the `generation_prompts/README.md` index row, and appends to
  `08_DECISIONS/decision_log.md` (approve) or `08_DECISIONS/rejected_ideas.md` (deny). It
  does not touch git.
- `open_prompt_approval_pr` puts the DRAFT prompt files on branch `approvals/<run_date>` and
  opens a PR to `main` (confirmation phrase `OPEN APPROVAL PR`). `get_prompt_approval_pr`
  reports that PR's state + comments so a later run can apply the decision.
- Operator documentation: `APPROVAL_UI.md` at the repo root.

**Proposed edits to `daily_operating_spec.md`:**

1. **§2A BOOTSTRAP** — add step 4:
   > 4. **Apply the previous run's approval decisions.** Call
   > `get_prompt_approval_pr(run_date=<previous run date>)`. Then:
   > - `recommended_apply_action: approve_all` (PR merged) → `git fetch origin &&
   >   git reset --hard origin/main`; for each `post_id`, `apply_prompt_decision(id,"approve")`;
   >   push the status flips + `decision_log.md` to `main` (§3 atomic path).
   > - `deny_all` (PR closed unmerged) → for each `post_id`,
   >   `apply_prompt_decision(id,"deny", reason="PR closed without merge")`, then regenerate
   >   each denied prompt as a fresh DRAFT addressing nothing specific (no reason given) and
   >   include them in today's new PR.
   > - `pending_or_partial` (PR still open) → honour only `deny <POST-ID>: <reason>` comments:
   >   `apply_prompt_decision(id,"deny", reason=<comment reason>)`, regenerate that prompt
   >   addressing the reason, leave the PR open for the rest.
   > If no previous approval PR exists, say so and continue.

2. **§3 AUTONOMY BOUNDARIES** — under "AUTONOMOUS GITHUB SYNC", change the prompts push:
   > Generation prompts are **not** pushed to `main` by the run. New and regenerated DRAFT
   > prompt files go onto branch `approvals/<run_date>` via `open_prompt_approval_pr`
   > (confirmation `OPEN APPROVAL PR`) and wait for the owner to merge (approve) or close
   > (reject) the PR. Research, `analysis_log.md`, `competitive_benchmark.md` and
   > `learning_log.md` still push to `main` directly as today.
   And under "MUST NOT DO WITHOUT EXPLICIT HUMAN CONFIRMATION", clarify:
   > - Mark any content calendar or prompt as APPROVED. **A merged approval PR is that
   >   confirmation for the prompts it contains** — the next run then runs
   >   `apply_prompt_decision(...,"approve")` for each. Nothing else may set a prompt APPROVED.

3. **§9 PROMPTING STAGE** — replace step 7–8:
   > 7. Status starts DRAFT. The run never sets APPROVED.
   > 8. After the prompting stage: push Analysis #1 to `main`, then call
   >    `open_prompt_approval_pr(confirmation="OPEN APPROVAL PR")` with every new or
   >    regenerated DRAFT prompt file. Record the returned `pr_url` for §10.

4. **§10 NOTIFICATION** — add to the required email content:
   > A **"REVIEW & APPROVE TODAY'S PROMPTS"** block: the approval PR URL, the list of post
   > IDs in it, and the one-line instruction — *merge to approve all; comment
   > `deny <POST-ID>: <reason>` then merge to reject some; close the PR to reject all.* Omit
   > the block only on a run that drafted no prompts.

5. **New §13 — HUMAN APPROVAL LOOP ("human checking" node).** Full description of the PR
   flow, the four `server.py` tools, the branch name convention `approvals/<run_date>`, the
   three apply paths, and the rule that a merged PR is the human confirmation §3 requires.
   Cross-reference `APPROVAL_UI.md`.

6. **Optional second scheduled run** (same-day apply) — see the companion proposal for
   `00_SYSTEM/apply_approvals_runbook.md` below.

**Limits unchanged:** no direct writes to `00_SYSTEM/`/`01_BUSINESS/`; no social publishing;
no spend; nothing VALIDATED without the sample-size gate; no remote deletions. The PR flow
*adds* a gate, it does not remove one.

---

## 2026-09-04
## Proposed CLAUDE.md update — the approval PR gate

**Status: PROPOSED — NOT APPLIED.** `CLAUDE.md` is protected.

**Context:** 2026-09-04 the approval flow for generation prompts became a GitHub Pull
Request (`decision_log.md` 2026-09-04; `daily_operating_spec.md` v2.2 §13–§14). `CLAUDE.md`
still says "September calendars … none published" and lists prompts only as DRAFT with no
gate described.

**Proposed changes to `CLAUDE.md`:**
1. "Autonomy boundaries" — add: generation prompts are not pushed to `main`; the daily run
   opens an approval PR (`approvals/<date>`); a merged PR is the human confirmation that
   moves prompts to APPROVED. Cross-reference `APPROVAL_UI.md` and `daily_operating_spec.md`
   §13.
2. "Known tooling hazards" — add the four approval tools and note `open_prompt_approval_pr`
   refuses a hand-edited branch.
3. "Current state" — note PR-based approval is live; the abandoned Artifact panel
   (2026-09-03) is superseded.

---

## 2026-09-04
## New file 00_SYSTEM/apply_approvals_runbook.md — same-day approval apply run

**Status: APPLIED 2026-09-04** (owner instruction, same as the entry above). File created
with the outline below expanded into steps §1–§5. The owner still needs to create the OS
scheduled task (14:00 MYT suggested; task prompt in `APPROVAL_UI.md`).

**Context:** The owner wants an approved prompt committed the same day, not only at the next
09:30 run. This is a second, lightweight scheduled run that does **only** the apply step.

**Proposed file content (outline):**
- Purpose: between daily runs, apply any approval decision the owner has made on the open
  `approvals/<date>` PR(s).
- Steps: `know_yourself` (light) → for each open/recently-closed `approvals/*` PR:
  `get_prompt_approval_pr(pr_number=…)` → apply per §2A step 4 logic → push to `main` →
  `git reset --hard origin/main`. If a deny needs regeneration, do it and update that PR.
- Then: if anything changed, append a one-line note to `06_PERFORMANCE/learning_log.md` and
  send the owner a short email (same address, plain text) listing what was applied.
- Boundaries: identical to the daily run. Never opens brand-new research. Never sets
  APPROVED without a merged PR.
- Schedule: suggested 14:00 MYT Mon–Fri, same machine/desktop-app dependency as the daily
  run. Owner creates the OS scheduled task; the exact task prompt is in `APPROVAL_UI.md`.

---

## 2026-09-03
## Proposed CLAUDE.md update — reflect the two-analysis loop (v2.1)

**Status: PROPOSED — NOT APPLIED.** `CLAUDE.md` is protected.

**Context:** On 2026-09-03 the owner approved adding a second analysis stage to the
operating loop (see `decision_log.md` 2026-09-03 "Operating loop gains a second analysis
stage"). `00_SYSTEM/daily_operating_spec.md` (v2.1) and the scheduled-task SKILL.md were
updated. `CLAUDE.md` still implies a single end-of-loop analysis.

**Proposed changes to `CLAUDE.md`:**
1. "Read these first" — after the `daily_operating_spec.md` line, note it now defines two
   analysis stages (§4A Analysis #1, §9A Analysis #2).
2. "Current state" / "What is actually blocking quality" — add that Analysis #2's
   competitor-comparison half depends on the competitor content/social audit, which is
   still only a first pass (`07_RESEARCH/2026-09-03-competitor-content-activity-first-pass.md`).
3. "Working conventions" — add: `08_DECISIONS/analysis_log.md` (Analysis #1 output) and
   `06_PERFORMANCE/competitive_benchmark.md` (Analysis #2 output) get one dated entry per
   run; each run reads the last `REFINEMENT:` note in `06_PERFORMANCE/learning_log.md` at
   bootstrap.

## Proposed update to 00_SYSTEM/routing_rules.md
**Reasoning:** While saving the first LinkedIn content calendar (12 posts, September 2026), no existing file in the routing structure matched "finished, dated, ready-to-publish post copy." It was filed in 05_CREATIVE/ as the closest fit, but the routing rules don't currently define this file type, so future calendars (LinkedIn or other platforms) risk being filed inconsistently or overwriting each other without a naming/location convention.

**Proposed change:**
Add a new subsection under 05_CREATIVE for "content_calendars/" — finished, dated, platform-specific post copy ready to publish (e.g. `05_CREATIVE/content_calendars/linkedin_2026-09.md`). Distinguish this from hook_library.md (reusable hooks, not full posts) and 08_DECISIONS/content_backlog.md (unprioritized future ideas, not scheduled/ready content). Question to ask before filing: "Is this finished, sequenced, ready-to-publish post copy for a specific platform and month?" If yes → content_calendars/.

## 2026-09-02
## Proposed 00_SYSTEM changes — 2026-09-02

**Status: PROPOSED — NOT APPLIED.** `00_SYSTEM/` is protected per `update_rules.md`. These need human approval.

### Proposal 1 — Fix the winning_patterns / validated_patterns contradiction

**Problem:** `routing_rules.md` documents `05_CREATIVE/winning_patterns.md` as the home for repeated performance patterns, while `update_rules.md` routes "Repeated supported result -> 06_PERFORMANCE/validated_patterns.md". Two governance files, two answers.

**Resolved 2026-09-02 by human instruction:** keep `06_PERFORMANCE/validated_patterns.md`, retire `05_CREATIVE/winning_patterns.md` (done — stub in place).

**Change needed in `routing_rules.md`:** replace the `winning_patterns.md` section under 05_CREATIVE with a pointer to `06_PERFORMANCE/validated_patterns.md`, keeping the existing guidance text ("Do NOT declare something a winning pattern after one successful video") which is worth preserving.

### Proposal 2 — Add a social scorecard to content_benchmark.md

**Instruction received 2026-09-02:** apply content benchmarking to both website and social posts.

**Problem:** the existing 100-point model is weighted for web pages — SEO 30, AEO 20, GEO 25, Conversion 15, UX 10. Social posts have no meta titles, no schema markup, no internal linking. Scoring a Reel against it produces a meaningless number.

**Proposed:** keep the website scorecard unchanged, add a second social scorecard in the same file, reweighted to what applies:

- Hook strength (first 1–3 seconds) — 25
- Platform fit (format, duration, native behaviour) — 20
- Audience fit (named role, real pain, correct funnel stage) — 20
- Message clarity (one idea, extractable) — 15
- CTA appropriateness to funnel stage — 10
- Claim safety (passes `products.md` §30–31) — 10

Claim safety scored rather than assumed, because it is the most common failure mode for AI-drafted content.

Awaiting human confirmation of the weighting before applying.

### Proposal 3 — Resolve the overlap between prompt.md and daily_operating_spec.md

**Discovered 2026-09-02.** Root `prompt.md` was described by the owner as a test file, but §0 (MCP Operating Workflow) is a substantive operating instruction — it names the exact tool sequence, and references `route_intelligence`, `search_knowledge`, `propose_brain_update`, `preview_github_api_sync` and `sync_to_github_atomic`, several of which are not covered in the new `00_SYSTEM/daily_operating_spec.md`.

`prompt.md` was **not** retired, pending this decision. Options:

1. Merge `prompt.md` §0–§7 into `daily_operating_spec.md` and/or `05_CREATIVE/prompting_rules.md`, move the §8 draft LinkedIn post to `08_DECISIONS/recommended_content.md`, then retire `prompt.md`.
2. Keep `prompt.md` as the operating prompt and strip the overlapping process sections back out of `daily_operating_spec.md`.

Duplicating the same instructions across both files would breach the Primary File Rule in `routing_rules.md`. One of the two must own this.

### Proposal 4 — Note on prompt_templates.md

`05_CREATIVE/prompt_templates.md` is flagged as a placeholder by `audit_knowledge_freshness` despite containing four usable templates. Worth checking whether the placeholder marker is stale — it may be suppressing a file that is actually ready to use.


## 2026-09-02
## Proposed 00_SYSTEM changes — housekeeping pass, 2026-09-02

**Status: PROPOSED — NOT APPLIED.**

### Proposal 5 — Fix the placeholder detector in server.py

**This is the highest-value fix available in the repository, and it is code rather than content.**

**Problem:** the placeholder detector matches on a heading containing the word "Template", not on whether the file has content. Verified 2026-09-02 on `02_AUDIENCE/factory_owner.md`: removing the `_(placeholder)_` marker changed nothing, renaming `## Profile Template` to `## Profile` cleared the flag, and the file content was byte-identical at 5,790 characters throughout.

**Impact:** eight populated files carrying roughly 36,000 characters of cited research were reported as empty. `build_recommendation_context` reads that status, lists them as critical evidence gaps, and caps `maximum_confidence` at LOW — which is part of why every September content recommendation was capped at LOW confidence. The detector also produced false negatives: `current_priorities.md` (38 chars), `experiments.md` (31 chars) and `campaign_history.md` (36 chars) are effectively empty and were not flagged at all.

**Workaround applied 2026-09-02:** the eight affected files had their "Template" headings renamed to accurate ones. This is legitimate on its own terms — a filled-in profile should not be headed "Profile Template" — but it is not the fix.

**Proposed fix:** detect placeholders by content volume and substance, not by heading text. A file should be considered a placeholder when it has no content beyond headings and an unfilled field list, regardless of what its headings are called. Requires a human to approve a code change to `server.py`.

### Proposal 6 — Add dates to undated 00_SYSTEM files

`content_benchmark.md`, `routing_rules.md`, `taxonomy.md` and `update_rules.md` carry no parseable date, so `audit_knowledge_freshness` cannot measure staleness on any of them. This is why `stale_files` always returns empty — not because nothing is stale, but because nothing can be measured.

Proposed: add a `Last updated: YYYY-MM-DD` line beneath the title of each. Content otherwise unchanged.

### Note on the remaining undated files

Undated files in `02_AUDIENCE` through `08_DECISIONS` that hold real content have been dated in this pass. The remainder are genuinely empty templates — `losing_patterns.md`, `content_performance.md`, `validated_patterns.md`, `recommended_content.md`, `rejected_ideas.md`, the three trend files, `whatsapp.md`, `google_business.md` and others. Dating an empty template records nothing useful; they should be dated when first filled. No action taken on them deliberately.

### Deletion candidates — require human action

Neither sync tool exposes a deletion parameter, so these cannot be removed from this session. They exist on GitHub but not locally:

- `07_RESEARCH/19.md` — `create_dated_file` naming-collision artifact
- `07_RESEARCH/308.md` — same
- `07_RESEARCH/318.md` — same
- `07_RESEARCH/trends.md` — superseded catch-all; `routing_rules.md` says not to recreate it
- `01_BUSINESS/competitor_analysis.md` — superseded by `04_COMPETITORS/`, but still cited by `competitor_index.md`. **Archive rather than delete, and fix the reference.**

Root cause of the three numeric files: `create_dated_file` names files day+month with no separator and will keep colliding. Use `write_doc` with explicit `YYYY-MM-DD` filenames instead — now recorded in `00_SYSTEM/daily_operating_spec.md`.



## 2026-09-02 — APPLIED (not a proposal): routing_rules.md rewrite

**Status: APPLIED under explicit human instruction this session.** `update_rules.md`
permits protected-file changes on explicit human instruction OR a proposal; this was
the former. Recorded here for the audit trail.

**File:** `00_SYSTEM/routing_rules.md` (was sha256 `2b952d33…`, 14,632 chars).

**Why:** the v1 file predated the 2026-09-02 restructuring and had drifted out of sync
with the actual repository, with `taxonomy.md`, and with `update_rules.md`'s own
routing table. ~30 existing files/folders had no defined home.

**What changed:**
- Added `Last updated` line.
- 00_SYSTEM: added `routing_rules.md`, `taxonomy.md`, `update_rules.md`,
  `content_benchmark.md`, `daily_operating_spec.md`; stated the protected-folder rule.
- 01_BUSINESS: added `sales_insights.md`; stated the protected-folder rule.
- 02_AUDIENCE: generalised to "one file per taxonomy role"; listed all 7 personas
  (added general_manager, operations_manager, supply_chain_planner, it_manager) +
  `audience_index.md`.
- 03_PLATFORM: added `website.md`, `whatsapp.md`, `google_business.md`,
  `platform_index.md`.
- 04_COMPETITORS: added `competitor_patterns.md`, `competitor_gaps.md`,
  `competitor_template.md`.
- 05_CREATIVE: added `creative_strategy.md`, `storytelling_patterns.md`,
  `losing_patterns.md`, `content_calendars/`, `generation_prompts/`,
  `prompting_rules.md`, `prompt_library.md`, `prompt_templates.md`. Replaced the
  `winning_patterns.md` section with a pointer to `06_PERFORMANCE/validated_patterns.md`
  (resolves Proposal 1 from the 2026-09-02 pass and the earlier content_calendars
  proposal).
- 06_PERFORMANCE: added `performance_framework.md`, `content_performance.md`,
  `validated_patterns.md`.
- 07_RESEARCH: added `competitor_updates.md`, the `YYYY-MM-DD-<topic>.md` dated-pass
  convention, and the standard research metadata block.
- 08_DECISIONS: added `recommended_content.md`, `rejected_ideas.md`,
  `brain_update_proposals.md`, `YYYY-MM-DD-session-record.md`.
- Added a "ROOT FILES — not routing targets" section (README.md, CLAUDE.md, prompt.md).
- Added Step 7 (index-maintenance duty) to "BEFORE WRITING ANY DATA".
- Preserved verbatim: FACT/INSIGHT/ACTION, PRIMARY FILE RULE, IF YOU ARE UNSURE.

**Still open (not resolved by this edit):** Proposal 3 (prompt.md vs
daily_operating_spec.md overlap), Proposal 2 (social scorecard), Proposals 4–6.

