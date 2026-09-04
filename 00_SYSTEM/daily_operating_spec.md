# DAILY OPERATING SPEC

Version: 2.3
Created: 2026-09-02
Authorised by: human owner (explicit instruction, 2026-09-02)
Status: ACTIVE

> **2026-09-04 — v2.3 change, authorised by the human owner in session.** The competitor
> set was **reset**. The owner deleted the prior 14-competitor set from GitHub and supplied
> one replacement analysis (Allied Solutions Global / ASPL), copied verbatim into
> `04_COMPETITORS/allied-solutions-global.md`. **The daily run does not discover or add
> competitors.** It researches and analyses **only** the competitor(s) listed in
> `04_COMPETITORS/competitor_index.md`. Adding a competitor is a human action. If a run
> encounters a possible new competitor, it notes it for the owner (e.g. in
> `08_DECISIONS/analysis_log.md` open questions) and does not create a profile.
> Every "14 verified MES competitors" phrasing below is superseded by this note.
> `competitor_gaps.md` and `competitor_patterns.md` are stubs until the tracked set is
> large enough to support gap/pattern analysis again.

> **2026-09-04 — v2.2 change, authorised by the human owner in session.** The loop's
> **"human checking"** node is now a real gate. Generation prompts are **no longer pushed to
> `main` by the run**. New and regenerated DRAFT prompts go onto a branch
> `approvals/<run_date>` and the run opens a **GitHub Pull Request** (§9, §3). The owner
> merges the PR to approve every prompt in it, comments `deny <POST-ID>: <reason>` then
> merges to reject specific ones, or closes the PR to reject all. At bootstrap (§2A) every
> run applies the previous run's PR decision: approved prompts are flipped to APPROVED and
> logged, denied ones are logged to `08_DECISIONS/rejected_ideas.md` and regenerated. New
> §13 describes the flow and the four `server.py` tools (`list_generation_prompt_status`,
> `open_prompt_approval_pr`, `get_prompt_approval_pr`, `apply_prompt_decision`); operator
> detail in `APPROVAL_UI.md`. A merged PR **is** the explicit human confirmation §3
> requires — nothing else may set a prompt APPROVED. An earlier attempt at this (a published
> Artifact + `db` panel) was abandoned 2026-09-03 (`decision_log.md`).

> **2026-09-03 — v2.1 change, authorised by the human owner in session.** The loop now has
> **two analysis stages**, not one. **Analysis #1 ("Researching")** runs after Research and
> before Prompting — it interprets the run's findings into an explicit content decision
> (new §4A; output → `08_DECISIONS/analysis_log.md`). **Analysis #2 ("Posting")** runs
> after the prompting stage — our-performance review **plus** a competitor comparison of
> our posts/ads/cadence/formats against the competitor(s) listed in `competitor_index.md`, producing
> suggestions for beating them (new §9A; output → `06_PERFORMANCE/competitive_benchmark.md`
> + a `REFINEMENT:` note in `06_PERFORMANCE/learning_log.md`). The loop is **closed**: each
> run reads the previous run's most recent `REFINEMENT:` note at bootstrap (§2A) and
> applies it to that run's Research and Prompting. The full-sweep Research stage now
> includes a competitor **content/social** audit as deep as public sources allow (§4).
> A third autonomous GitHub push carries the Analysis #2 output. Owner will supplement the
> competitor audit with first-hand competitor information separately.

> **2026-09-03 — v2.0 change, authorised by the human owner in session.** The daily run
> is now FULLY AUTONOMOUS: it sweeps all research areas every run (no single-theme
> rotation), and it PUSHES research and generation prompts to GitHub `main` on its own
> authority — no human confirmation, no manual sync step. The push-related restrictions in
> §3, the rotation in §4, the file cap in §5, and §9–§10 were rewritten to match. The
> limits that remain hard: no direct writes to `00_SYSTEM/` or `01_BUSINESS/`, no social
> publishing, no spend, no "APPROVED"/"VALIDATED" without the stated gate. Owner accepts
> the risk of unreviewed AI output on a public repo and will intervene if a problem
> appears. Recorded in `08_DECISIONS/decision_log.md` (2026-09-03).

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

# 2A. BOOTSTRAP — READ THE LAST RUN'S REFINEMENT (loop close)

Immediately after `know_yourself` and reading this spec, every run reads:

1. The most recent `REFINEMENT:` note in `06_PERFORMANCE/learning_log.md` (written by the
   previous run's Analysis #2).
2. The most recent entry in `06_PERFORMANCE/competitive_benchmark.md` (its "Suggestions to
   beat them" list).
3. The most recent entry in `08_DECISIONS/analysis_log.md`, including its "Open questions
   handed to the next Research run".

These three steer this run: the Research sweep (§4) prioritises the open questions and the
competitor gaps; the Prompting stage (§9) treats the suggestions as inputs. If there is no
prior note yet (first run under v2.1), say so and proceed with a normal full sweep.

**4. Apply the previous run's approval decisions (§13).** Call
`get_prompt_approval_pr(run_date=<previous run's date>)`.

- `recommended_apply_action: approve_all` (PR merged) → `git fetch origin && git reset
  --hard origin/main`; for each `post_id`, `apply_prompt_decision(id, "approve")`; push the
  status flips + `decision_log.md` to `main` via the §3 atomic path; `git reset --hard
  origin/main`.
- `deny_all` (PR closed unmerged) → for each `post_id`,
  `apply_prompt_decision(id, "deny", reason="PR closed without merge")`; push; then
  regenerate each denied prompt as a fresh DRAFT and carry it into today's PR (§9).
- `pending_or_partial` (PR still open) → honour only `deny <POST-ID>: <reason>` comments:
  `apply_prompt_decision(id, "deny", reason=<comment reason>)`, push, regenerate that prompt
  addressing the reason; leave the PR open for the undecided prompts.

If no previous approval PR exists, say so and continue.

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

## AUTONOMOUS GITHUB SYNC (authorised by the human owner, 2026-09-03)

The daily run pushes to GitHub `main` on its own authority — research after the research
stage, Analysis #1 after the prompting stage, Analysis #2 (competitive benchmark
+ refinement note) after §9A. No human confirmation. Mechanics: the scheduled
task SKILL.md §7 (`check_github_connection` → `preview_github_api_sync` → verify every
changed file is brain content and not a CRLF false positive → `sync_to_github_atomic` with
the preview's `remote_commit_sha` and confirmation `CREATE ATOMIC GITHUB COMMIT` → local
`git reset --hard origin/main`). Never deletes remote files. Never pushes secrets or
untracked non-brain files.

**Generation prompts are the exception — they are not pushed to `main` by the run.** New and
regenerated DRAFT prompt files go onto branch `approvals/<run_date>` via
`open_prompt_approval_pr` (confirmation `OPEN APPROVAL PR`), which opens a Pull Request to
`main` for the owner to merge (approve) or close (reject). Approved prompts only reach `main`
on the next run's §2A step 4, after the merge. See §13.

## MUST NOT DO WITHOUT EXPLICIT HUMAN CONFIRMATION

- Publish to any social platform, schedule a post for actual publication, or send outreach. Opening an approval PR with a DRAFT prompt is allowed; publishing its output is not.
- Mark any content calendar or prompt as APPROVED. **A merged approval PR is that confirmation for the prompts it contains** — the next run then runs `apply_prompt_decision(..., "approve")` for each. Nothing else may set a prompt APPROVED.
- Spend money or trigger paid media.
- Record a pattern as VALIDATED without the sample-size threshold being met by `analyze_posting_time_performance` itself.
- Write directly to `00_SYSTEM/` or `01_BUSINESS/` (propose in `08_DECISIONS/brain_update_proposals.md`).

---

# 4. DAILY SCOPE — FULL SWEEP

No single-theme rotation (changed 2026-09-03). Every weekday run sweeps ALL areas below
and captures whatever materially changed since the last run. Depth is triaged by what
actually moved — discipline against becoming a content factory (`brain_rules.md` §31) is
enforced by the stopping rule in §5, not by restricting scope.

| Area | Primary destination |
|---|---|
| Competitor activity — **only the competitor(s) in `competitor_index.md`; do not discover or add new competitors** (v2.3) | `04_COMPETITORS/<competitor>.md`, `competitor_patterns.md`, `competitor_gaps.md` |
| Competitor **content/social** activity (posts, ads, cadence, formats, angles, engagement) for the listed competitor(s) — as deep as public/non-authenticated sources allow; flag what needs a logged-in pass | `04_COMPETITORS/<competitor>.md`, `competitor_patterns.md`; feeds Analysis #2 §9A |
| Platform behaviour and algorithm change | `03_PLATFORM/<platform>.md` |
| Audience and customer signals | `02_AUDIENCE/<role>.md` (`07_RESEARCH/customer_insights.md` is first-party only) |
| Industry, manufacturing, market | `07_RESEARCH/industry_news.md`, `07_RESEARCH/market_trends.md` |
| Government, grants, regulation | `07_RESEARCH/government_updates.md` |
| Search trends | `07_RESEARCH/search_trends.md` |
| Social trends | `07_RESEARCH/social_trends.md` |

Every run also runs: `audit_knowledge_freshness`, `find_knowledge_conflicts`, and an update
of `07_RESEARCH/research_index.md`, `02_AUDIENCE/audience_index.md`,
`03_PLATFORM/platform_index.md`, `04_COMPETITORS/competitor_index.md`,
`05_CREATIVE/content_calendars/calendar_index.md` for anything touched that run.

Weekends: no scheduled run.

---

# 4A. ANALYSIS #1 — "RESEARCHING"

Runs **after the research stage and its GitHub push, before the prompting stage.** It is an
interpretation pass, not new research — it adds no external sources.

1. Read this run's new/updated research entries, the last `08_DECISIONS/analysis_log.md`
   entry, and the prior `REFINEMENT:` note (§2A).
2. Decide what the findings *mean* for content — the "so what", not a restatement.
3. Produce one dated entry in `08_DECISIONS/analysis_log.md` (newest first, template in
   that file) recording: research read, prior refinement applied, what the findings mean,
   the content decision (Create / Test / Monitor / Nothing this run, with platform /
   audience / angle / derived-from entry / hypothesis / success metric if Create or Test),
   confidence, and open questions for the next Research run.
4. The prompting stage (§9) executes this decision. If the decision is "Nothing this run",
   the prompting stage is skipped and says so.

`analysis_log.md` is a running decision log, not a dated research file — it does **not**
count against the two-new-file cap in §5.

---

# 5. RESEARCH STOPPING RULE

Applies every run, per `evidence_rules.md` §38.

1. Before writing, search existing knowledge. If the finding already exists, **update the existing entry rather than creating a new one.**
2. Maximum **two** new dated research files per run (raised from one on 2026-09-03 for the full-sweep scope). Everything else updates existing files.
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

Runs after research and its GitHub push, using that run's research plus recent unactioned
findings and the current refinement statement when one exists. Runs whenever the evidence
warrants a content asset; skipped (and said so) when nothing warrants one.

1. Call `build_recommendation_context`, then `build_prompt_context`, before constructing anything.
2. Adapt every idea to its platform. Identical cross-posts are prohibited by `brain_rules.md` §7.
3. One prompt file per platform per planned asset, in `05_CREATIVE/generation_prompts/`.
4. Every prompt records the research entry it derives from, so the chain from evidence to creative is traceable.
5. Every prompt carries a hypothesis and a success metric before it is produced, per `decision_framework.md` §26.
6. No prompt may instruct generation of a claim prohibited by `products.md` §31.
7. Status starts DRAFT. The run never sets APPROVED.
8. After the prompting stage: push Analysis #1 (`analysis_log.md`) to GitHub `main` (§3),
   then call `open_prompt_approval_pr(confirmation="OPEN APPROVAL PR")` with every new or
   regenerated DRAFT prompt file from this run (pass no `files` to auto-pick every
   generation prompt that differs from `main`). Keep the returned `pr_url` and `post_ids`
   for §10. The prompt files themselves are **not** pushed to `main` — they live on the PR
   branch until the owner merges. See §13.

---

# 9A. ANALYSIS #2 — "POSTING"

Runs **after the prompting stage and its push.** Two halves, one output file, one refinement
note, one push.

**Half 1 — our performance.** Read `analyze_posting_time_performance` and
`record_post_performance` data for every platform. Until the first post is published this is
"no first-party performance data yet — zero published posts"; record that plainly and move on.

**Half 2 — competitor comparison.** Compare Mysoft's marketing output — published posts if
any, otherwise the approved/planned content calendars and positioning — against the
competitor content/social activity gathered in §4 and held in `04_COMPETITORS/` and the
dated competitor-content audits. For each competitor listed in `competitor_index.md`: what they published or ran,
format and channel, whether it worked (with evidence), recency/cadence. Then: where Mysoft
is behind, where white space still holds, what competitors tried that flopped.

**Output.**
1. One dated entry in `06_PERFORMANCE/competitive_benchmark.md` (newest first, template in
   that file), ending with a numbered "Suggestions to beat them" list.
2. One dated `REFINEMENT:` note appended to `06_PERFORMANCE/learning_log.md` — a single
   concrete way the Brain should operate better next cycle. This note is what the next run
   reads at bootstrap (§2A); it is the mechanism by which Research "refers to" Analysis #2.
3. Third GitHub push: `competitive_benchmark.md` + `learning_log.md`. Commit message
   `Automated daily run <YYYY-MM-DD> — competitive benchmark + refinement`. Skip only if
   both files are unchanged.

Evidence discipline (§6) applies in full: competitor claims are claims, not fact; nothing
here is VALIDATED; flag everything that needs a logged-in or human pass.

---

# 10. NOTIFICATION AND CALENDAR

Gmail and Google Calendar are connected (as of 2026-09-03).

Every run, after all three GitHub pushes: create one all-day Google Calendar event on
`posinsidernow@gmail.com` dated today with the full run summary, then send that same
summary as a plain-text email to `posinsidernow@gmail.com` (sent directly, not a draft),
including the calendar event's htmlLink and every commit SHA/URL from the run. The summary
must include the Analysis #1 content decision, the Analysis #2 "Suggestions to beat them"
list, and the `REFINEMENT:` note written this run. If
generation prompts were drafted, add a `[DRAFT]` all-day event per planned posting date.
Do this even on a quiet day or a partial failure. Full mechanics in the scheduled task
SKILL.md §9.

**If an approval PR was opened this run (§9 step 8), the email must include a
"REVIEW & APPROVE TODAY'S PROMPTS" block:** the PR URL, the list of post IDs in it, and the
one line — *"Merge the PR to approve all. Comment `deny <POST-ID>: <reason>` then merge to
reject some. Close the PR to reject all."* Omit the block only on a run that drafted no
prompts.

---

# 11. STAGES NOT YET ACTIVE

- **Stage 3 — media generation.** Deferred by the human owner. The Gemini API key is not required for the prompting stage; it is only needed here.
- **Stage 4 — refinement.** Requires Windsor.ai and Zoho CRM. Neither is connected as of 2026-09-02. When active, the refinement statement lands in `06_PERFORMANCE/refinement_log.md` and is read at the start of Sections 4 and 9 above.

---

# 12. UPDATE RULE

This file changes only on explicit human instruction. A scheduled run may propose changes in `08_DECISIONS/brain_update_proposals.md` but must not edit this file itself.

---

# 13. HUMAN APPROVAL LOOP — THE "HUMAN CHECKING" NODE

The loop is `Prompting → Generating → Human checking ─(No)─↺ Generating ; (Yes) → Posting`.
"Human checking" is a **GitHub Pull Request**. (A published-Artifact panel was tried first
and abandoned 2026-09-03 — its data runtime would not load in the owner's viewer;
`decision_log.md`.)

**Branch / PR convention.** One branch `approvals/<run_date>` (e.g. `approvals/2026-09-04`)
per run that drafts prompts. `open_prompt_approval_pr` puts the DRAFT prompt files (and the
`generation_prompts/README.md` index) on it and opens/refreshes a PR to `main`. It refuses
if the branch carries commits it did not make (hand-edited) — comment on the PR instead of
editing files there.

**The four `server.py` tools.**

| Tool | Role |
|---|---|
| `list_generation_prompt_status()` | Every prompt with post ID / platform / date / status |
| `open_prompt_approval_pr(files="", run_date="", confirmation="OPEN APPROVAL PR")` | Open/refresh the approval PR. Empty `files` = every generation prompt that differs from `main` |
| `get_prompt_approval_pr(pr_number=0, run_date="")` | The PR's state, files, post IDs, every comment, and a `recommended_apply_action` |
| `apply_prompt_decision(post_id, "approve"\|"deny", reason="")` | Flip one prompt's `**Status:**` line, update the index row, log to `decision_log.md` (approve) or `rejected_ideas.md` (deny). Refuses non-DRAFT. Does not touch git |

**Owner actions on the PR:** merge = approve every prompt in it; comment
`deny <POST-ID>: <reason>` then merge = reject those, approve the rest; close without merge
= reject all.

**Apply (next run §2A step 4, or the same-day apply run §14):** read the PR with
`get_prompt_approval_pr`, then follow `recommended_apply_action` —
`approve_all` / `deny_all` / `pending_or_partial` — running `apply_prompt_decision` per post
ID, pushing the status flips + logs to `main` via the §3 atomic path, and regenerating any
denied prompt (addressing the comment reason when one was given) into the next PR.

**Merging publishes nothing.** APPROVED authorises production of the asset only. Actual
social publishing remains a separate explicit human step (§3).

Operator walkthrough, email wiring, and the scheduled-task SKILL.md text block:
`APPROVAL_UI.md` (repo root).

---

# 14. SAME-DAY APPROVAL APPLY RUN

An optional second scheduled run (suggested 14:00 MYT, Mon–Fri, same machine/desktop-app
dependency as §2) so an approval made during the day is committed the same day instead of
waiting for the next 09:30 run. It does **only** the apply step of §13 (for every open or
today-closed `approvals/*` PR), pushes to `main`, regenerates denied prompts and updates
their PR, and — if anything was applied — appends a one-line note to
`06_PERFORMANCE/learning_log.md` and sends a short plain-text email to
`posinsidernow@gmail.com`. It opens no new research and sets nothing APPROVED without a
merged PR. Full steps: `00_SYSTEM/apply_approvals_runbook.md`. The owner creates the OS
scheduled task (exact task prompt in `APPROVAL_UI.md`).
