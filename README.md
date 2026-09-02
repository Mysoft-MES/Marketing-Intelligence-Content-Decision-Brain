# Marketing Intelligence & Content Decision Brain

A modular knowledge base and MCP server for deciding what marketing content Mysoft MES should create next, for whom, on which platform, and why.

## Start Here

1. Read `00_SYSTEM/brain_rules.md` for the Brain's operating principles.
2. Read `00_SYSTEM/routing_rules.md` before storing new information.
3. Use `00_SYSTEM/decision_framework.md` before recommending content.
4. Use `00_SYSTEM/evidence_rules.md` to label facts, observations, assumptions and confidence.
5. Use `07_RESEARCH/research_index.md` to find current external research.
6. Use `04_COMPETITORS/competitor_index.md` as the current competitor source of truth.

## Repository Map

### 00_SYSTEM — Governance

- `brain_rules.md` — mission, reasoning principles and prohibited behaviour.
- `decision_framework.md` — required inputs and output structure for recommendations.
- `evidence_rules.md` — source quality, evidence classes and confidence rules.
- `routing_rules.md` — primary destination for each information type.
- `taxonomy.md` — controlled audiences, platforms, formats, hooks and statuses.
- `update_rules.md` — when knowledge is updated, promoted, archived or revalidated.
- `content_benchmark.md` — SEO, AEO, GEO and content-quality benchmarking.

### 01_BUSINESS — Mysoft Business Truth

- `company_profile.md` — company, customers, market, goals and constraints.
- `products.md` — product capabilities, ownership, integrations and limitations.
- `positioning.md` — value proposition, differentiation and permitted claims.
- `customer_objections.md` — objections, underlying concerns and supported responses.
- `sales_insights.md` — evidence from sales calls, demos, wins and losses.
- `swot.md` — living, evidence-backed strategic SWOT.

Current competitor evidence does not belong here; use `04_COMPETITORS/`.

### 02_AUDIENCE — Buyers and Influencers

- `audience_index.md` — master audience list and priorities.
- `audience_matrix.md` — cross-audience comparison.
- Individual role files — factory owner, general manager, production manager, operations manager, supply-chain planner, finance manager and IT manager.

### 03_PLATFORM — Platform-Specific Strategy

- `platform_index.md` — channel roles and priorities.
- Individual platform files — Facebook, Instagram, LinkedIn, Reddit, Xiaohongshu, YouTube, website, Google Business Profile and WhatsApp.

These files store durable platform behaviour and strategy, not individual draft posts.

### 04_COMPETITORS — Competitive Intelligence

- `competitor_index.md` — verified master competitor list and current status.
- `competitor_template.md` — required structure for new competitor profiles.
- Named competitor files — detailed evidence for each competitor.
- `competitor_patterns.md` — repeated behaviour across multiple competitors.
- `competitor_gaps.md` — supported market white-space opportunities.
- `_archive/` — legacy placeholders only; not current evidence.

### 05_CREATIVE — Reusable Creative Knowledge

- `creative_strategy.md` and `creative_rules.md` — creative operating principles.
- `hook_library.md` — usable hooks with audience/platform context.
- `video_formats.md` and `storytelling_patterns.md` — reusable execution structures.
- `winning_patterns.md` and `losing_patterns.md` — evidence-supported creative patterns.
- `creative_experiments.md` — creative test designs and results.
- `prompting_rules.md` — construction standard for evidence-aware MCP prompts.
- `prompt_templates.md` — reusable operational prompt structures.
- `prompt_library.md` — reviewed prompt examples and rejected anti-patterns.
- `linkedin_content_calendar_2026-09.md` — dated execution calendar.

### 06_PERFORMANCE — Internal Results

- `performance_framework.md` — metrics by objective.
- `content_performance.md`, `video_performance.md`, `ad_performance.md` — individual results.
- `campaign_history.md` — campaign-level history.
- `learning_log.md` — cautious interpretations of results.
- `validated_patterns.md` — repeated or controlled performance conclusions.

Quantitative MCP records are stored locally in `.mcp_data/` and are excluded from Git.

### 07_RESEARCH — External Evidence

- `research_index.md` — current research catalogue and review status.
- `market_trends.md`, `social_trends.md`, `search_trends.md` — distinct trend categories.
- `industry_news.md`, `government_updates.md`, `customer_insights.md`, `competitor_updates.md` — dated external intelligence.
- Descriptively named dated reports — scoped research analyses.
- `_archive/` — tests and superseded analyses; not current evidence.

### 08_DECISIONS — Proposed and Approved Action

- `current_priorities.md` — short list of work that matters now.
- `content_backlog.md` — worthwhile ideas not yet prioritized.
- `recommended_content.md` — evidence-backed AI proposals awaiting review.
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
7. `record_video_performance` / `query_video_performance`
8. `create_experiment` → `record_experiment_result` → `close_experiment`
9. `check_github_connection`
10. `preview_github_api_sync`
11. `sync_to_github_atomic` after explicit SHA-bound approval

## Safety

- Existing files are preserved unless overwrite is explicit.
- System and foundational business files require human approval.
- `.env`, `.git/`, `.mcp_data/`, uv runtimes and Obsidian UI state are excluded from MCP GitHub sync.
- Atomic GitHub sync never deletes remote files and never force-updates `main`.
- Archived files are provenance, not current evidence.
