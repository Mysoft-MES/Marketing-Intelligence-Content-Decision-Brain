
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

