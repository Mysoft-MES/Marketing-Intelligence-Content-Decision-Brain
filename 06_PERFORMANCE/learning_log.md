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
