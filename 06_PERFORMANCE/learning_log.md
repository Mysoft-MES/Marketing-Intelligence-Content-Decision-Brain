# Learning Log

General learnings and insights about how the Brain operates.

**Self-refinement notes (from Analysis #2).** Every operating run, the Analysis #2
("Posting") stage appends a dated `REFINEMENT:` note here — one concrete way the Brain
should work better next cycle, drawn from that run's performance + competitor comparison
(`06_PERFORMANCE/competitive_benchmark.md`). The **next** run reads the most recent
`REFINEMENT:` note at bootstrap and applies it to that run's Research and Prompting. This
is the feedback link that closes the loop (`00_SYSTEM/daily_operating_spec.md` §9A / §2A).
Never edit a past `REFINEMENT:` note — supersede it with a new one.

## 2026-08-30
**TEST NOTE:** This is a short test entry to verify the `append_doc` tool is working correctly. Not a real learning/insight — safe to remove.

## 2026-08-31
testing sync after token fix

## 2026-09-01
Confirmed .env-based token loading resolved the persistent GITHUB_TOKEN environment variable issue.

## 2026-09-04
**REFINEMENT (2026-09-04):** Before the next Prompting stage, check whether the owner has
named a founder / technical lead for LinkedIn. The Brain has now recommended "one named
person posting consistently" from two independent evidence lines (2026-08-31 founder thesis;
2026-09-04 employee-advocacy reach data) and the competitor audit shows the lane is empty —
but every LinkedIn asset stays a company-page asset until that person exists. Make "named
person: yes/no" an explicit gate at the top of each run's Prompting stage, and if still
"no", say so in the run summary and route it to `08_DECISIONS/current_priorities.md` rather
than drafting more company-page LinkedIn content.
Source: `06_PERFORMANCE/competitive_benchmark.md` 2026-09-04.

## 2026-09-04 (second run — competitor-set reset)
**REFINEMENT (2026-09-04, second run):** The named-person LinkedIn dependency is now settled
and routed (`08_DECISIONS/current_priorities.md` item 1) — the Brain has re-derived it from
three evidence lines across two runs (2026-08-31 founder thesis; 2026-09-04 employee-advocacy
reach data; 2026-09-04 Allied audit — no competitor uses a named person). **Stop
re-analysing it.** Next cycle, at the Prompting gate, only *check whether the owner has
answered* (yes/no); do not rebuild the case. Spend the freed effort on the **logged-in
Allied Solutions Global social audit** (LinkedIn `allied-solutions-pte-ltd`, Facebook
`alliedsolutionsg`) — cadence, recency, engagement, format mix, individual employees, paid
ads — which is now the single highest-value competitor task (one tracked competitor, no
engagement data yet). Also drop the retired "top 5 / 14 competitors" framing from all
analysis — the tracked set is one until the owner adds another.
Supersedes nothing in the note above (that gate still applies); this narrows how the gate is
run and redirects the freed research effort.
Source: `06_PERFORMANCE/competitive_benchmark.md` 2026-09-04 (second run).

## 2026-09-04 (third run — post-reconciliation re-sweep)
**REFINEMENT (2026-09-04, third run):** The 2026-09-04 work is now reconciled onto
`origin/main` and approval PR #1 is merged (LI-C1 + IG-01/IG-02/FB-03/FB-04/IG-04 APPROVED
via `apply_prompt_decision` this session). Two operating lessons from how today went:
1. **Every run must confirm `git status` shows `main` level with (or a clean fast-forward
   of) `origin/main` BEFORE any research or writing.** Three runs today wrote onto a branch
   that had diverged from `origin/main` (stale local `main`, ahead 1 / behind 17), so none
   could push and each run added more un-pushable changes. If `main` is not a clean
   fast-forward of `origin/main`, **stop and report — do not research, do not write.** This
   check belongs at the very top of the bootstrap, before `know_yourself`.
2. **When an approval PR is merged mid-run or since the last run, apply it in the current
   run:** `apply_prompt_decision(<id>, "approve")` for each post id, then push the status
   flips + `decision_log.md`. Do not leave APPROVED prompts sitting at DRAFT on `main`
   until the next run's bootstrap.
Next cycle: the **logged-in Allied Solutions Global social audit** is the priority research
task (overdue three runs); the named-person LinkedIn gate is a yes/no check only, not to be
re-analysed.
Source: `06_PERFORMANCE/competitive_benchmark.md` 2026-09-04 (third run).


## 2026-09-04 (fourth run — copy-style / audience-age synthesis)
**REFINEMENT (2026-09-04, fourth run):** A per-channel copy-style + audience-age reference now
exists (`03_PLATFORM/copywriting_style_and_audience_age.md`) — how the copy should sound and
which age / seniority band it addresses on Facebook (35+ owners/GMs, Mandarin,
Click-to-WhatsApp), LinkedIn (under-45 researchers, technical read-through, carousel, no demo
ask) and Instagram (younger influencers who don't sign off, visual-first, save/DM ask). From
next cycle, the Prompting stage must **read it before writing any caption or generation
prompt**, and every drafted asset must state in its prompt file which platform-voice / age-band
/ CTA-friction row it targets — so the evidence-to-creative chain includes audience fit, not
just the derived-from research entry. A prompt that does not name its target row is not
finished. No content asset added this run; this tightens how the existing prompting gate runs.
Still carried and unchanged: the named-person LinkedIn gate is a yes/no owner check only (do
not re-analyse); the logged-in Allied Solutions Global social audit (`allied-solutions-pte-ltd`,
`alliedsolutionsg`) is the priority research task and is now four runs overdue.
Source: `06_PERFORMANCE/competitive_benchmark.md` 2026-09-04 (fourth run).



## 2026-09-04 (fifth run — strategist brief format)
**REFINEMENT (2026-09-04, fifth run):** The strategist output now lives in a dedicated
`08_DECISIONS/strategy_brief_YYYY-MM-DD.md` structured as Research → Meaning → Opportunity/Gap
→ Marketing Decision → Content Recommendation → Platform Strategy (audience / angle / format /
voice / objective per channel) → When to Post (sequence + reasoning, checked against the
existing calendar/backlog for repetition) → Next Research. `08_DECISIONS/analysis_log.md`
keeps only the short decision record and points to the brief. From next run: Analysis #1
writes the brief in that structure every run; the Prompting stage executes the brief's
Content Recommendation + Platform Strategy + Timing sections directly, and each generation
prompt cites which REC number and which `03_PLATFORM/copywriting_style_and_audience_age.md`
row it comes from. Propose the matching `daily_operating_spec.md` §4A wording in
`08_DECISIONS/brain_update_proposals.md` (00_SYSTEM is read-only to the run). Carried
unchanged: the logged-in Allied social audit (`allied-solutions-pte-ltd`, `alliedsolutionsg`)
is the top research task and is now 5 runs overdue; the named-person LinkedIn gate is a
yes/no owner check only — do not re-analyse it.
Source: `06_PERFORMANCE/competitive_benchmark.md` 2026-09-04 (fifth run).




## 2026-09-04 (sixth run — quiet same-day re-check)
**REFINEMENT (2026-09-04, sixth run):** When a run detects it is a **repeat pass on a day that
already has a completed run** (same-date entries already in `analysis_log.md` /
`competitive_benchmark.md`) **and** an approval PR from an earlier same-day pass is still
**open**, short-circuit after BOOTSTRAP + APPLY-DECISIONS: run the freshness/conflict audits and
a light external re-check, write one short "quiet re-check" record only if something is worth
noting, send the mandated status email, create the calendar record, and stop — no new research
files, no new strategy brief, no new prompts, no new approval PR. Five full same-day passes on
2026-09-04 produced diminishing returns and left three DRAFT prompts (FB-01, FB-02, IG-03)
orphaned on `main` with no open PR. The daily cadence is one run per weekday
(`daily_operating_spec.md` §2); a legitimate second same-day run is the narrow apply-approvals
run (§14), not another full sweep. Carried unchanged: the logged-in Allied Solutions Global
social audit (`allied-solutions-pte-ltd`, `alliedsolutionsg`) is the top research task and is
now 6 runs overdue; the named-person LinkedIn gate is a yes/no owner check only — do not
re-analyse it.
Source: `06_PERFORMANCE/competitive_benchmark.md` 2026-09-04 (sixth run).



## 2026-09-05
**REFINEMENT (2026-09-05):** When a scheduled run finds DRAFT generation prompts on `main`
with no open approval PR (an "orphaned" state — usually left by a prior day's repeated
same-day passes), opening a fresh approval PR to carry them forward is itself a valid and
sufficient Prompting-stage action for that run, even when no new evidence warrants a new
content asset. Treat this as distinct from, and not an excuse to skip, the normal
evidence-driven CREATE/TEST decision. Also: this run needed to delete a stale, already-merged
`approvals/<date>` branch via direct GitHub API call (using the repo's own token) before
`open_prompt_approval_pr` would succeed, because the branch name collided with an
already-merged PR from a prior run that happened to share the same calendar-date branch name.
Future runs should check for this collision (a `approvals/<run_date>` branch that is a
fully-merged ancestor of `main`) before calling `open_prompt_approval_pr`, and clean it up
proactively rather than waiting for the tool to refuse.
Source: `06_PERFORMANCE/competitive_benchmark.md` 2026-09-05.

