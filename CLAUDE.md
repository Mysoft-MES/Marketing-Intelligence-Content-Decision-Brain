# CLAUDE.md

Working context for the Mysoft MES Marketing Intelligence & Content Decision Brain.
Loaded automatically at session start. Keep it short and current — it is read every time.

Last updated: 2026-09-02

---

## What this repository is

A knowledge base plus MCP server that decides what marketing content Mysoft MES should create next, for whom, on which platform, and why. Mysoft MES is a Manufacturing Execution System by My Software Solutions, based in Penang, selling to Malaysian discrete manufacturers.

It is not a content factory. `00_SYSTEM/brain_rules.md` §31 says so explicitly. The objective is better market decisions, not more output.

## Read these first

1. `00_SYSTEM/daily_operating_spec.md` — schedule, autonomy, rotation, stopping rule, routing decisions
2. `00_SYSTEM/brain_rules.md` — operating principles
3. `00_SYSTEM/routing_rules.md` — where every piece of information goes
4. `00_SYSTEM/evidence_rules.md` — evidence classes and confidence
5. `01_BUSINESS/products.md` §30–31 — claim safety, before writing any content

Or call `know_yourself`, which loads `00_SYSTEM/`, `01_BUSINESS/company_profile.md` and `05_CREATIVE/prompting_rules.md` in one go.

## Autonomy boundaries

- **Write freely:** `02_AUDIENCE/` through `08_DECISIONS/`
- **Never write directly:** `00_SYSTEM/`, `01_BUSINESS/` — propose in `08_DECISIONS/brain_update_proposals.md`
- **Never without explicit human confirmation:** push to GitHub, publish anything, mark a calendar approved, or promote a pattern to VALIDATED

An AI recommendation is not a decision until a human approves it (`brain_rules.md` §30).

## Evidence discipline — non-negotiable

- Cite every external source with its publication date
- Label external benchmarks **TESTING**, never VALIDATED
- Mysoft-specific timing is validated only when `analyze_posting_time_performance` returns `can_claim_best_time: true`
- Never invent performance data, customer evidence, or research
- Vendor and competitor claims are evidence of *what that party claims*, not fact
- No percentage improvements, guaranteed ROI, implementation durations, "works with any ERP", or zero-error claims (`products.md` §31)

## Known tooling hazards

**`update_markdown_section` on an H1 destroys the file.** It treats an H1 section as everything beneath it. Verified 2026-09-02 — wiped a 5,790-character file to 173. Only ever target H2 or lower.

**Placeholder detection is unreliable.** It matches any heading containing "Template" rather than actual content. It has produced both false positives (populated files reported empty) and false negatives (sub-40-character files not flagged). This propagates into `build_recommendation_context`, which reports affected files as evidence gaps and caps `maximum_confidence` at LOW. Fix proposed in `brain_update_proposals.md` — it is a code change in `server.py`.

**`sync_changed_files_to_github` times out.** Git subprocesses block in the MCP host. Use the API path instead:

```
preview_github_api_sync  →  sync_to_github_atomic
   (returns remote SHA)      (expected_remote_sha = that SHA,
                              confirmation = "CREATE ATOMIC GITHUB COMMIT")
```

Neither sync tool can delete remote files. Deletions are a human action on GitHub.

**`create_dated_file` collides.** It names files day+month with no separator, which has already produced `19.md`, `308.md`, `318.md`. Use `write_doc` with an explicit `YYYY-MM-DD` filename.

## Current state

- 14 Malaysian MES competitors verified and profiled. Their social/content activity has **never** been audited — the largest open research gap.
- Seven audience profiles populated from external research. **None validated against Mysoft's own sales or customer data.**
- September 2026 calendars exist for LinkedIn, Facebook and Instagram in `05_CREATIVE/content_calendars/`. All **AWAITING HUMAN APPROVAL**, none published.
- **Zero performance records.** `analyze_posting_time_performance` returns nothing for every platform. The September LinkedIn cycle is deliberately designed as a counterbalanced two-slot experiment to produce the first validated posting time.

## What is actually blocking quality

Three files are empty, and no amount of research fills them:

| File | Effect |
|---|---|
| `01_BUSINESS/swot.md` | Critical evidence gap in every recommendation packet; caps confidence at LOW |
| `01_BUSINESS/sales_insights.md` | Would answer ~10 of the 30 open questions in `company_profile.md` §38 |
| `08_DECISIONS/current_priorities.md` | No business priority to rank content against |

Also: all 25 customer objections in `customer_objections.md` are HYPOTHESIS (§51 says so), and there is no customer proof anywhere — which blocks LinkedIn's strongest documented format, the quantified case study.

These need human input, not another research pass.

## Working conventions

- Update the relevant index in the same session as any file it points to changes: `audience_index.md`, `platform_index.md`, `competitor_index.md`, `research_index.md`, `content_calendars/calendar_index.md`
- One fact, one home. Put the implication elsewhere, never the same paragraph (`routing_rules.md` — Primary File Rule)
- Update an existing entry rather than adding a duplicate
- If a research pass finds nothing that changes the Brain's understanding, write nothing and say so. A quiet day is a valid outcome.

## Full background

`08_DECISIONS/2026-09-02-session-record.md` — the audit and restructuring that produced the current state, with reasoning.
