# Marketing Intelligence & Content Decision Brain

A modular knowledge base and MCP server for deciding what marketing content Mysoft MES should create next, for whom, on which platform, and why.

Last updated: 2026-09-02

## Start Here

1. Read `00_SYSTEM/brain_rules.md` for the Brain's operating principles.
2. Read `00_SYSTEM/daily_operating_spec.md` for the automated daily cycle, autonomy boundaries and confirmed routing decisions.
3. Read `00_SYSTEM/routing_rules.md` before storing new information.
4. Use `00_SYSTEM/decision_framework.md` before recommending content.
5. Use `00_SYSTEM/evidence_rules.md` to label facts, observations, assumptions and confidence.
6. Use `07_RESEARCH/research_index.md` to find current external research.
7. Use `04_COMPETITORS/competitor_index.md` as the current competitor source of truth.

## Repository Map

### 00_SYSTEM — Governance

- `brain_rules.md` — mission, reasoning principles and prohibited behaviour.
- `decision_framework.md` — required inputs and output structure for recommendations.
- `evidence_rules.md` — source quality, evidence classes and confidence rules.
- `routing_rules.md` — primary destination for each information type.
- `taxonomy.md` — controlled audiences, platforms, formats, hooks and statuses.
- `update_rules.md` — when knowledge is updated, promoted, archived or revalidated.
- `content_benchmark.md` — SEO, AEO, GEO and content-quality benchmarking.
- `daily_operating_spec.md` — daily run schedule, autonomy boundaries, rotation and stopping rule.

### 01_BUSINESS — Mysoft Business Truth

- `company_profile.md` — company, customers, market, goals and constraints.
- `products.md` — product capabilities, ownership, integrations and limitations.
- `positioning.md` — value proposition, differentiation and permitted claims.
- `customer_objections.md` — objections, underlying concerns and supported responses.
- `sales_insights.md` — evidence from sales calls, demos, wins and losses. **Empty — highest-value gap in the repository.**
- `swot.md` — living, evidence-backed strategic SWOT. **Empty — caps recommendation confidence at LOW.**

Current competitor evidence does not belong here; use `04_COMPETITORS/`.

### 02_AUDIENCE — Buyers and Influencers

- `audience_index.md` — master audience list and priorities.
- `audience_matrix.md` — cross-audience comparison.
- Individual role files — factory owner, general manager, production manager, operations manager, supply-chain planner, finance manager and IT manager. All seven populated with first-pass external research; none yet validated against Mysoft's own sales or customer data.

### 03_PLATFORM — Platform-Specific Strategy

- `platform_index.md` — channel roles and priorities.
- Individual platform files — Facebook, Instagram, LinkedIn, Reddit, Xiaohongshu, YouTube, website, Google Business Profile and WhatsApp.

These files store durable platform behaviour and strategy, not individual draft posts.

### 04_COMPETITORS — Competitive Intelligence

- `competitor_index.md` — verified master competitor list and current status.
- `competitor_template.md` — required structure for new competitor profiles.
- Named competitor files — detailed evidence for each of 14 verified competitors.
- `competitor_patterns.md` — repeated behaviour across multiple competitors.
- `competitor_gaps.md` — supported market white-space opportunities.
- `_archive/` — legacy placeholders only; not current evidence.

Social and content activity has not been audited for any competitor. That is the folder's largest gap.

### 05_CREATIVE — Reusable Creative Knowledge

- `creative_strategy.md` — creative operating principles and execution rules. Canonical.
- `hook_library.md` — usable hooks with audience/platform context.
- `video_formats.md` and `storytelling_patterns.md` — reusable execution structures.
- `losing_patterns.md` — creative patterns with repeated evidence against them.
- `prompting_rules.md` — construction standard for evidence-aware MCP prompts.
- `prompt_templates.md` — reusable operational prompt structures.
- `prompt_library.md` — reviewed prompt examples and rejected anti-patterns.
- `generation_prompts/` — image and video generation prompts for media tools.
- `content_calendars/` — dated per-platform calendars with a combined index.
- `linkedin_content_calendar_2026-09.md` — copy bank for the September LinkedIn posts. Not a schedule.
- Retired: `creative_rules.md` (merged into `creative_strategy.md`), `winning_patterns.md`, `creative_experiments.md`.

### 06_PERFORMANCE — Internal Results

- `performance_framework.md` — metrics by objective and comparison rules.
- `content_performance.md`, `video_performance.md`, `ad_performance.md` — individual results.
- `campaign_history.md` — campaign-level history.
- `learning_log.md` — cautious interpretations of results.
- `validated_patterns.md` — repeated or controlled performance conclusions. Canonical home for validated patterns.

Quantitative MCP records are stored locally in `.mcp_data/` and excluded from Git. **No performance records exist yet** — `analyze_posting_time_performance` returns zero for every platform.

### 07_RESEARCH — External Evidence

- `research_index.md` — current research catalogue and review status.
- `market_trends.md`, `social_trends.md`, `search_trends.md` — distinct trend categories.
- `industry_news.md`, `government_updates.md`, `customer_insights.md` — dated external intelligence.
- Descriptively named dated reports — scoped research analyses.
- `_archive/` — tests and superseded analyses; not current evidence.
- Retired: `competitor_updates.md` — competitor findings route to `04_COMPETITORS/`.

Use `write_doc` with an explicit `YYYY-MM-DD` filename for dated research. Do not use `create_dated_file` — its day+month naming collides.

### 08_DECISIONS — Proposed and Approved Action

- `current_priorities.md` — short list of work that matters now. **Empty.**
- `content_backlog.md` — worthwhile ideas not yet prioritized.
- `recommended_content.md` — evidence-backed AI proposals awaiting review. Template matches `build_recommendation_context` output fields.
- `experiments.md` — marketing hypotheses and test plans.
- `decision_log.md` — human-approved decisions only.
- `rejected_ideas.md` — rejected options and reconsideration conditions.
- `brain_update_proposals.md` — proposed changes to protected knowledge.

## Information Lifecycle

```text
Fact or observation
→ primary subject file
→ insight or learning
→ recommendation
→ experiment
→ result
→ repeated evidence
→ validated pattern
→ human-approved decision
```

Do not duplicate the same paragraph across layers. Store the original fact once and link its implication or action where needed.

## MCP Workflow

1. `know_yourself`
2. `health_check`
3. `search_knowledge` / `inspect_doc`
4. `build_prompt_context` before constructing an operational prompt
5. `build_recommendation_context` before a content recommendation
6. `route_intelligence` / `save_intelligence`
7. `record_post_performance` / `record_video_performance` / `query_video_performance`
8. `create_experiment` → `record_experiment_result` → `close_experiment`
9. `check_github_connection`
10. `preview_github_api_sync`
11. `sync_to_github_atomic` after explicit SHA-bound approval

Use the atomic API sync path. The Git-subprocess sync tool blocks in this MCP host and will time out.

## Known Tooling Issues

- **Placeholder detection is unreliable.** It flags any file containing a "Template" heading regardless of content, and misses genuinely empty files that lack one. Verified 2026-09-02: eight populated files carrying ~36,000 characters of cited research were reported as empty, while three files of under 40 characters were not flagged at all. This propagates into `build_recommendation_context`, which reports affected files as evidence gaps and caps `maximum_confidence` at LOW. The durable fix is in the detector logic in `server.py`.
- **`update_markdown_section` must not be pointed at an H1.** It treats an H1 section as everything beneath it and will overwrite the entire file.

## Safety

- Existing files are preserved unless overwrite is explicit.
- System and foundational business files require human approval.
- `.env`, `.git/`, `.mcp_data/`, uv runtimes and Obsidian UI state are excluded from MCP GitHub sync.
- Atomic GitHub sync never deletes remote files and never force-updates `main`.
- Archived files are provenance, not current evidence.
