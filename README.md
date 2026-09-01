# 🧠 Marketing Intelligence & Content Decision Brain

> Master central hub connecting strategy, market research, creative execution, and decision logs.

---

## 🧭 Core Navigation

### ⚙️ 00. System Governance
- [[00_SYSTEM/brain_rules|Brain Rules]] — Core reasoning & prompt directives
- [[00_SYSTEM/evidence_rules|Evidence Rules]] — Research standards & fact validation

### 🏢 01. Business Foundations
- [[01_BUSINESS/company_profile|Company Profile]] — Value proposition, positioning & offerings

### 🎯 02. Audience Personas
- [[02_AUDIENCE/audience_matrix|Audience Matrix]]
- [[02_AUDIENCE/factory_owner|Factory Owner]]
- [[02_AUDIENCE/production_manager|Production Manager]]
- [[02_AUDIENCE/finance_manager|Finance Manager]]

### 📱 03. Distribution Platforms
- [[03_PLATFORM/linkedin|LinkedIn]]
- [[03_PLATFORM/facebook|Facebook]]
- [[03_PLATFORM/instagram|Instagram]]
- [[03_PLATFORM/youtube|YouTube]]
- [[03_PLATFORM/reddit|Reddit]]
- [[03_PLATFORM/xiaohongshu|Xiaohongshu]]

### ⚔️ 04. Competitive Landscape
- [[04_COMPETITORS/competitor_index|Competitor Index]]
- [[04_COMPETITORS/competitor_analysis|Competitor Analysis]]
- [[04_COMPETITORS/competitor_a|Competitor A]] | [[04_COMPETITORS/competitor_b|Competitor B]] | [[04_COMPETITORS/competitor_c|Competitor C]]
- [[04_COMPETITORS/bizit-systems|Bizit Systems]] | [[04_COMPETITORS/blue-ocean-data-solutions|Blue Ocean]] | [[04_COMPETITORS/critical-manufacturing|Critical Manufacturing]]
- [[04_COMPETITORS/digiwinsoft-malaysia|Digiwinsoft]] | [[04_COMPETITORS/fsbm-mes-elite|FSBM MES]] | [[04_COMPETITORS/iot-sata|IoT SATA]] | [[04_COMPETITORS/ioti|IoTI]]
- [[04_COMPETITORS/sciengate-automation|Sciengate]] | [[04_COMPETITORS/yny-technology|YNY Tech]]

### 🎨 05. Creative Engine
- [[05_CREATIVE/creative_rules|Creative Rules]]
- [[05_CREATIVE/hook_library|Hook Library]]
- [[05_CREATIVE/video_formats|Video Formats]]
- [[05_CREATIVE/winning_patterns|Winning Patterns]]

### 📊 06. Performance & Insights
- [[06_PERFORMANCE/campaign_history|Campaign History]]
- [[06_PERFORMANCE/video_performance|Video Performance]]
- [[06_PERFORMANCE/learning_log|Learning Log]]

### 🔍 07. Market & Field Research
- [[07_RESEARCH/customer_insights|Customer Insights]]
- [[07_RESEARCH/industry_news|Industry News]]
- [[07_RESEARCH/government_updates|Government Updates]]
- [[07_RESEARCH/trends|Market Trends]]
- [[07_RESEARCH/308|Research 308]] | [[07_RESEARCH/318|Research 318]]

### 🚀 08. Execution & Decisions
- [[08_DECISIONS/current_priorities|Current Priorities]]
- [[08_DECISIONS/content_backlog|Content Backlog]]
- [[08_DECISIONS/decision_log|Decision Log]]
- [[08_DECISIONS/experiments|Active Experiments]]
- [[prompt|Latest Active Prompt]]

---

## MCP Tool Workflow

Recommended operating order:

1. `know_yourself` — load governance and business context.
2. `health_check` — inspect required files, placeholders, Git state, and sync readiness.
3. `search_knowledge` / `inspect_doc` — retrieve focused evidence before editing.
4. `build_recommendation_context` — assemble and score mandatory recommendation inputs.
5. `route_intelligence` / `save_intelligence` — append structured findings to controlled destinations.
6. `record_video_performance` / `query_video_performance` — store and compare quantitative results.
7. `create_experiment` → `record_experiment_result` → `close_experiment` — preserve experiment history.
8. `check_github_connection` — validate repository access without writing.
9. `preview_github_api_sync` — compare local files with GitHub blob hashes.
10. `sync_to_github_atomic` — create one non-forced commit after explicit SHA-bound approval.

Safety controls:

- `write_doc` preserves existing files unless `overwrite=true` is explicit.
- Protected system and foundational business files require human approval.
- `update_markdown_section` supports SHA-256 concurrency checks.
- Runtime records and mutation audit logs live in `.mcp_data/`, which is excluded from Git.
- Obsidian UI-state files are excluded from MCP Git previews unless `include_obsidian=true` is explicit.
- The atomic GitHub workflow does not spawn local Git, never deletes remote files, and refuses to update a branch that changed after preview.
- Legacy Git subprocess and per-file Contents API tools remain for compatibility but are deprecated.
