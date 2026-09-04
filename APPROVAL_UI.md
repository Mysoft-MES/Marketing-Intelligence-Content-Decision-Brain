# Generation-prompt approval — the "human checking" gate

How a human approves or denies the media generation prompts the daily run drafts, from the
notification email, on any device.

Last updated: 2026-09-04

---

## Why it works this way

The loop in `00_SYSTEM/daily_operating_spec.md` is:

```
Prompting → Generating → Human checking ─(No)─↺ Generating
                              │ (Yes)
                              ▼
                           Posting
```

"Human checking" needs a screen with **Approve** and **Deny** per prompt, reachable from the
run's email. There is **no always-on server** on `mysoftware-nb-34` (the MCP server only runs
while the Claude desktop app is open), so an emailed link cannot run git directly.

A published-Artifact panel was tried on 2026-09-03 and abandoned — its data runtime would not
load in the owner's viewer (`08_DECISIONS/decision_log.md`). The working design is a **GitHub
Pull Request**:

- The daily run puts the new DRAFT prompt files on a branch `approvals/<YYYY-MM-DD>` and
  opens a PR to `main`. It does **not** push prompts to `main` any more.
- The email carries the PR link.
- **Approve all** → merge the PR (one tap on github.com, works on mobile, uses your login).
- **Deny some** → comment `deny <POST-ID>: <reason>` on the PR, then merge.
- **Deny all** → close the PR without merging.
- The next run (or the same-day apply run) reads the PR's state and does the bookkeeping:
  flips approved prompts to `APPROVED`, logs them to `08_DECISIONS/decision_log.md`, logs
  denied ones to `08_DECISIONS/rejected_ideas.md`, and regenerates the denied ones into the
  next PR.

Merging the PR **publishes nothing**. It only authorises the asset to be produced. Actual
social publishing still needs a separate explicit human step.

---

## What you do

1. Open the daily email → **"REVIEW & APPROVE TODAY'S PROMPTS"** block → tap the PR link.
2. Read the PR description (each prompt's ID, platform, date, file) and open the file diffs
   for the hook / shot list / caption / "What must NOT appear" / hypothesis.
3. Then:

| You want to… | Do this on the PR |
|---|---|
| Approve every prompt | **Merge** the PR |
| Approve most, reject a few | Comment `deny FB-01: hook too close to FB-03` (one line per rejected prompt), then **Merge** |
| Reject everything | **Close** the PR (do not merge) |
| Decide later | Leave it open — the next run leaves un-mentioned prompts pending and re-includes them |

Do **not** edit files on the `approvals/*` branch — comment instead. The run force-updates
that branch and will refuse if it sees commits it didn't make.

---

## The tools (in `server.py`)

| Tool | Use |
|---|---|
| `list_generation_prompt_status()` | List every prompt with post ID / platform / date / status |
| `open_prompt_approval_pr(files="", run_date="", confirmation="OPEN APPROVAL PR")` | Put DRAFT prompts on `approvals/<run_date>` and open/refresh the PR. `files` empty = all `generation_prompts/*.md` (plus README) that differ from `main` |
| `get_prompt_approval_pr(pr_number=0, run_date="")` | Report the PR's state, prompt files, post IDs, and every comment, with a `recommended_apply_action` |
| `apply_prompt_decision(post_id, "approve"\|"deny", reason="")` | Flip one prompt's `**Status:**` line, update the index row, log to `decision_log.md` / `rejected_ideas.md`. Refuses non-DRAFT prompts. Does **not** touch git — caller pushes `changed_files` with the atomic path |

`get_prompt_approval_pr` returns one of:

- `approve_all` — PR merged. `git fetch origin && git reset --hard origin/main`, then
  `apply_prompt_decision(id,"approve")` per post ID, push status flips + `decision_log.md`.
- `deny_all` — PR closed unmerged. `apply_prompt_decision(id,"deny", reason="PR closed
  without merge")` per post ID, regenerate each, include in the next PR.
- `pending_or_partial` — PR still open. Honour only `deny <POST-ID>: <reason>` comments;
  regenerate those addressing the reason; leave the PR open for the rest.

---

## Daily run wiring (add to the scheduled-task SKILL.md)

The step list the `marketing-brain-daily` run executes lives in the Claude desktop app, not
this repo. Add these (they mirror the proposed `daily_operating_spec.md` §2A / §3 / §9 / §10
edits in `08_DECISIONS/brain_update_proposals.md`):

**Bootstrap (after `know_yourself`, before Research):**

> Apply the previous run's approval decisions. `get_prompt_approval_pr(run_date="<previous
> run's date>")`. If `approve_all`: `git fetch origin && git reset --hard origin/main`, then
> `apply_prompt_decision(<id>,"approve")` for every `post_id`, then push the changed files to
> `main` (`check_github_connection` → `preview_github_api_sync` → `sync_to_github_atomic`
> with the preview SHA and `CREATE ATOMIC GITHUB COMMIT`) → `git fetch origin && git reset
> --hard origin/main`. If `deny_all`: `apply_prompt_decision(<id>,"deny", reason="PR closed
> without merge")` for every `post_id`, regenerate each, and carry them into today's PR. If
> `pending_or_partial`: honour only `deny <POST-ID>: <reason>` comments. If no PR exists,
> note it and continue.

**Prompting stage (replace "push prompts to main"):**

> Do not push generation prompts to `main`. After pushing Analysis #1, call
> `open_prompt_approval_pr(confirmation="OPEN APPROVAL PR")` — with no `files` it picks up
> every DRAFT prompt that differs from `main`, or pass the explicit list of files you drafted
> / regenerated this run. Keep the returned `pr_url` and `post_ids`.

**Notification (§10):**

> Add a "REVIEW & APPROVE TODAY'S PROMPTS" block to the email: the `pr_url`, the `post_ids`
> in it, and: *"Merge to approve all. Comment `deny <POST-ID>: <reason>` then merge to reject
> some. Close the PR to reject all."* Skip the block only if no prompts were drafted.

---

## Optional: same-day apply run

A second scheduled task so an approval made in the afternoon is committed the same day
instead of waiting for 09:30 the next morning. Suggested 14:00 MYT, Mon–Fri, same machine.

Scheduled-task prompt:

> You are the same-day approval-apply run for the Mysoft marketing brain. Do only this:
> call `know_yourself` (for grounding), then for each open or today-closed `approvals/*`
> pull request call `get_prompt_approval_pr(pr_number=<n>)` and apply its
> `recommended_apply_action` exactly as `APPROVAL_UI.md` describes — including regenerating
> any denied prompt and updating its PR. Push only to `main` via the atomic path, then
> `git fetch origin && git reset --hard origin/main`. If anything was applied, append a
> one-line note to `06_PERFORMANCE/learning_log.md` and send a short plain-text email to
> `posinsidernow@gmail.com` listing what was applied and any commit URLs. Do not open new
> research. Do not set any prompt APPROVED without a merged PR. If nothing is pending, do
> nothing and send no email.

Create it in Windows Task Scheduler pointing at the same Claude-desktop launch the daily run
uses, with this prompt.

---

## Permissions

`.claude/settings.local.json` allows the new tools so the autonomous runs are not blocked:
`mcp__social-engine__list_generation_prompt_status`,
`mcp__social-engine__apply_prompt_decision`,
`mcp__social-engine__open_prompt_approval_pr`,
`mcp__social-engine__get_prompt_approval_pr`.

---

## Status vocabulary

Set by `apply_prompt_decision`, visible in each prompt file's `**Status:**` line and the
`05_CREATIVE/generation_prompts/README.md` index:

| Status | Meaning |
|---|---|
| `DRAFT` | Awaiting the approval PR / not yet decided |
| `APPROVED (human via approval PR, <date>)` | Merged approval PR; asset may be produced (not published) |
| `REJECTED (human via approval PR, <date>) — see 08_DECISIONS/rejected_ideas.md` | Denied; regenerated into a later PR |
| `PRODUCED` / `PUBLISHED` | Set later by hand once the asset exists / is live |
