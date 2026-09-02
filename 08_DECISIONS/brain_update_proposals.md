
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

