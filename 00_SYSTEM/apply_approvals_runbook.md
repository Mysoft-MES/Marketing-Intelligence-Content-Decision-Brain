# APPLY-APPROVALS RUNBOOK

Version: 1.0
Created: 2026-09-04
Authorised by: human owner (explicit in-session instruction, 2026-09-04)
Status: ACTIVE

The step list for the **same-day approval apply run** (`daily_operating_spec.md` §14). A
second, lightweight scheduled run — suggested 14:00 MYT, Mon–Sat — whose only job is to
apply an approval decision the owner has made on an open `approvals/<date>` Pull Request,
without waiting for the next 09:30 daily run.

Same machine/desktop-app dependency as the daily run (`daily_operating_spec.md` §2). A
missed run is a skipped apply, not a queued job — the next 09:30 daily run picks it up at
its §2A step 4.

---

## 1. BOOTSTRAP (light)

1. Call `know_yourself` for grounding. Do **not** run the full research sweep, Analysis #1,
   or Analysis #2.
2. Read this runbook and `daily_operating_spec.md` §3 (autonomy), §13 (approval loop).

---

## 2. FIND PENDING DECISIONS

1. List candidate PRs: any pull request whose head branch starts `approvals/` and is `open`,
   or was `closed`/`merged` today. Use `get_prompt_approval_pr(pr_number=<n>)` per PR (or
   `get_prompt_approval_pr(run_date="<YYYY-MM-DD>")` to look one up by date).
2. If nothing is open and nothing was closed/merged today → **do nothing, send no email.**
   Stop here.

---

## 3. APPLY (per PR, exactly as §13)

Read `recommended_apply_action`:

- **`approve_all`** (PR merged) —
  `git fetch origin && git reset --hard origin/main`; for each `post_id`,
  `apply_prompt_decision(id, "approve")`; push the changed files to `main`
  (`check_github_connection` → `preview_github_api_sync` → `sync_to_github_atomic` with the
  preview `remote_commit_sha` and confirmation `CREATE ATOMIC GITHUB COMMIT`);
  `git fetch origin && git reset --hard origin/main`.

- **`deny_all`** (PR closed unmerged) —
  for each `post_id`, `apply_prompt_decision(id, "deny", reason="PR closed without merge")`;
  push as above; then regenerate each denied prompt as a fresh DRAFT (follow
  `05_CREATIVE/generation_prompts/README.md` and `05_CREATIVE/prompting_rules.md`; new
  `Review date`; note it is a regeneration) and open a fresh approval PR for them with
  `open_prompt_approval_pr(files="<the regenerated files>", confirmation="OPEN APPROVAL PR")`.

- **`pending_or_partial`** (PR still open) —
  honour only comments of the form `deny <POST-ID>: <reason>`. For each:
  `apply_prompt_decision(id, "deny", reason="<the comment reason>")`; push; regenerate that
  prompt addressing the reason; update the same PR with
  `open_prompt_approval_pr(files="<regenerated file>", run_date="<that PR's date>",
  confirmation="OPEN APPROVAL PR")`. Leave the PR open for the still-undecided prompts.

Never set a prompt APPROVED without a merged PR. Never open new research. Never publish.

---

## 4. RECORD AND NOTIFY

If **anything** was applied this run:

1. Append one line to `06_PERFORMANCE/learning_log.md`:
   `APPLY <YYYY-MM-DD HH:MM MYT> — applied <n> approval decision(s): <post-ids approved>, <post-ids denied>. Commit <url>.`
2. Push that file to `main` (same atomic path).
3. Send a short plain-text email to `posinsidernow@gmail.com` (sent directly, not a draft):
   subject `Approval decisions applied — <YYYY-MM-DD>`, body listing each post ID, the
   action taken, any regenerated prompt's new PR URL, and every commit SHA/URL.

If nothing was applied: no log entry, no email.

---

## 5. UPDATE RULE

This file changes only on explicit human instruction, same as `daily_operating_spec.md`
(§12). A run may propose changes in `08_DECISIONS/brain_update_proposals.md`.
