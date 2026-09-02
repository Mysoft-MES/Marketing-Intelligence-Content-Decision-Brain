# MARKETING BRAIN — INFORMATION ROUTING PROMPT

Last updated: 2026-09-02

You are responsible for organizing all information you discover into the correct Markdown files inside this Marketing Brain.

Before writing any information, first determine:

1. **What type of information is this?**
2. **Which file is its primary home?**
3. Is it a **fact**, **insight**, **performance result**, or **decision**?
4. Does the information already exist?
5. Should an existing entry be updated instead of duplicated?

Use ONLY the following structure unless specifically instructed to create a new file.
This file is kept in sync with `00_SYSTEM/taxonomy.md` and `00_SYSTEM/update_rules.md`.
If the three disagree, that is a routing bug — raise it in
`08_DECISIONS/brain_update_proposals.md`.

---

## 00_SYSTEM — HOW THE BRAIN THINKS

`00_SYSTEM/` is **protected**. Never write to it directly. Propose changes in
`08_DECISIONS/brain_update_proposals.md`; a human applies them.

### `brain_rules.md`

Rules controlling how the AI should behave.
Examples: always use evidence before conclusions; never invent competitor
information; do not treat views as the only success metric; do not recommend
identical content across every platform; distinguish facts from assumptions.
**Question:** "Is this a rule controlling how the Brain behaves?"

### `decision_framework.md`

Rules explaining **how marketing decisions should be made**: what to consider
before recommending content; how to prioritize; how to decide platform +
audience + hook + duration + CTA; how to classify ACT NOW / TEST / MONITOR / IGNORE.
**Question:** "Does this explain how the Brain makes a recommendation?"

### `evidence_rules.md`

Rules about evidence, sources and confidence: source tiers, fact vs assumption,
confidence levels, verification, dates and source links, how much evidence is
needed before a conclusion is accepted.
**Question:** "Does this explain how information should be verified?"

### `routing_rules.md`

This file. Where every type of information belongs. Update whenever a new file
or folder type is added anywhere in `02_`–`08_`.

### `taxonomy.md`

The controlled vocabulary: allowed audiences, platforms, funnel stages, evidence
types, confidence levels, hook types, creative formats, decision statuses.
Extend a list here only after checking existing values.

### `update_rules.md`

The rules for *how* to change knowledge safely: read before write, update don't
duplicate, keep fact/insight/action separate, never promote one result to a
rule, filename conventions, archive conventions, index-maintenance duty.

### `content_benchmark.md`

The scoring models used to grade content quality (website scorecard, and — when
approved — a separate social scorecard). Reference only.

### `daily_operating_spec.md`

The daily run: schedule, autonomy boundaries, rotation, stopping rule, tool
sequence, routing decisions for a normal operating cycle.

---

## 01_BUSINESS — OUR BUSINESS

`01_BUSINESS/` is **protected** foundational knowledge. Never write directly.
Propose changes in `08_DECISIONS/brain_update_proposals.md`.

### `company_profile.md`

Factual company context: background, business model, customer base, markets and
industries served, geography, business model, buying committee, customer
situation, strategic direction, business-intelligence gaps.
Example: "We have a large existing SQL customer base." → here.

### `products.md`

Factual product/service knowledge: features, modules, what the product does,
integrations, technology ownership (Mysoft-owned vs Digiwin/supplier), product
limitations, roadmap status, claim-safety rules (§30–31), product knowledge gaps.
Example: "Our Job Order module can upload production data to Digiwin AIoT." → here.

### `positioning.md`

How we compete and describe ourselves: value proposition, differentiation,
target market, main message, competitive position, what to emphasize, **what must
not be claimed**.

### `customer_objections.md`

Customer concerns, resistance, misunderstandings and questions, in the
customer's actual wording. Each entry carries an evidence class (HYPOTHESIS
until customer-proven). A raw customer quote lands first in
`07_RESEARCH/customer_insights.md`; a recurring deal-blocker is summarised here.

### `sales_insights.md`

Learnings from the sales team and the sales process: what prospects ask, why
deals are won or lost, which competitors appear in deals, sales-cycle and
deal-value patterns, which messages generate qualified enquiries.
Route: sales-team learning → here (per `update_rules.md`).

### `swot.md`

Only strategic Strengths, Weaknesses, Opportunities, Threats. Each important
entry: Statement / Evidence / Source / Date / Confidence / Business Impact /
Recommended Response. Do not dump ordinary business facts here.
Example — FACT "we have manufacturing customers on the Job Order module" →
`company_profile.md`; STRATEGIC INTERPRETATION "existing manufacturing customers
are a cross-sell opportunity for MES" → here.

---

## 02_AUDIENCE — WHO WE ARE TALKING TO

One file per audience role. Role names must match `taxonomy.md`.
Each file: responsibilities, goals, pains, fears, objections, buying authority,
awareness level, content preferences, platform behaviour, buying triggers.

Current audience files:

- `factory_owner.md`
- `general_manager.md`
- `production_manager.md`
- `operations_manager.md`
- `supply_chain_planner.md`
- `finance_manager.md`
- `it_manager.md`

Add a new persona file only when the role is in `taxonomy.md` and there is
enough evidence to say something specific.

### `audience_matrix.md`

Cross-audience comparison only: pain points, buying motivation, decision power,
best message, best content, relevant platform, CTA — side by side. Do not put
single-audience detail here; it belongs in that audience's file.

### `audience_index.md`

Navigation catalogue: each audience file, its population status, evidence
confidence, last update. Keep in sync whenever an audience file changes.

---

## 03_PLATFORM — HOW EACH PLATFORM WORKS

Platform files hold **platform behaviour and strategy**, not individual posts.
Store: audience behaviour, consumption/discovery behaviour, suitable formats,
duration findings, hook style, tone, CTA behaviour, community expectations,
distribution characteristics where evidence exists, what performs / does not.

Current platform files (names match `taxonomy.md`):

- `facebook.md`
- `instagram.md`
- `linkedin.md`
- `xiaohongshu.md`
- `reddit.md`
- `youtube.md`
- `website.md` — owned source of truth; SEO / AEO / GEO / conversion behaviour
- `whatsapp.md` — conversational-commerce / enquiry-closing behaviour
- `google_business.md` — local discovery behaviour

### `platform_index.md`

Navigation catalogue: each platform file, priority in the current strategy,
population status, last update. Keep in sync when a platform file changes.

---

## 04_COMPETITORS — WHAT COMPETITORS ARE DOING

### `competitor_index.md`

Master competitor list only. Per competitor: name, category, website, main
products, main platforms, importance, last researched. No detailed research here.

### `<competitor-name>.md`

One descriptively named file per verified or actively researched competitor
(e.g. `bizit-systems.md`). Use `competitor_template.md` for new profiles. Never
create generic `competitor_a/b/c.md` placeholders.
Store: products, pricing, positioning, website messaging, social posts, ads,
campaigns, hooks, offers, CTAs, video formats/duration, landing pages,
strengths, weaknesses, recent activity. Each observation carries Date / Platform
/ Source / Topic / Audience / Hook / Format / Offer / CTA / Observation /
Possible implication. Never put our own strategy in a competitor file unless
clearly labelled as analysis.

### `competitor_patterns.md`

Behaviour repeated across **multiple** competitors (a shared hook, a saturated
topic, a common cadence). Route: repeated competitor behaviour → here.

### `competitor_gaps.md`

Competitive white space: audiences, messages, formats, proof or questions that
competitors collectively neglect. Route: competitor white space → here.

### `competitor_template.md`

The blank profile structure. Copy it; do not fill it in.

---

## 05_CREATIVE — HOW CONTENT SHOULD BE CREATED

### `creative_rules.md`

General creative principles: hook immediately, avoid long logo intros, show the
problem before the product when appropriate, one idea per short video, adapt by
platform.

### `creative_strategy.md`

The current creative direction: brand territory being built, recurring problems
we want to own, distinctive messages, series concepts, terminology. Higher-level
than `creative_rules.md`.

### `hook_library.md`

Actual usable hooks. Per hook: text, hook type, audience, platform, product,
pain point, performance if tested.

### `storytelling_patterns.md`

Reusable narrative structures (problem→mechanism→payoff, POV, before/after,
case-study shape). Per pattern: best use, audience, platform, strength, weakness.

### `video_formats.md`

Reusable video formats (POV, factory scenario, talking head, demo, interview,
before/after, customer story, screen recording). Per format: best use, audience,
platform, suggested duration, strength, weakness.

### `losing_patterns.md`

Creative approaches that have **underperformed** with evidence: what failed,
audience, platform, evidence, number of tests, likely reason. The mirror of
validated patterns. Do not label something a losing pattern after one weak post.

> **Repeated winning patterns are NOT stored here.** They live in
> `06_PERFORMANCE/validated_patterns.md`. (`05_CREATIVE/winning_patterns.md` is
> retired — a stub pointer only.) The guidance still holds: do not declare
> something a winning pattern after one successful video.

### `content_calendars/`

Finished, dated, platform-specific schedule + measurement layer.
`content_calendars/YYYY-MM-<platform>.md`, one file per platform per month, plus
`calendar_index.md` as the navigation overview.
**Question before filing:** "Is this finished, sequenced, ready-to-schedule post
planning for a specific platform and month?" If yes → here.
Distinguish from `hook_library.md` (reusable hooks, not full plans) and
`08_DECISIONS/content_backlog.md` (unprioritized future ideas, not scheduled).
Nothing here is approved for publication until a human records approval in
`08_DECISIONS/decision_log.md`.
Long-form post copy may live in a companion copy-bank file (e.g.
`linkedin_content_calendar_2026-09.md`) referenced by the calendar — never
duplicated into it (Primary File Rule).

### `generation_prompts/`

Ready-to-run **image and video generation prompts** for media tools.
`generation_prompts/YYYY-MM-DD-<platform>-<post-id>.md`, one file per asset,
tied by post ID to a row in `content_calendars/`. Plus `README.md` (the spec
and entry template).
Each prompt: cites the research finding it came from, carries a hypothesis and a
success metric, passes `01_BUSINESS/products.md` §30–31 claim safety, starts at
status DRAFT (only a human moves it to APPROVED). Never write one prompt and
reuse it across platforms — `brain_rules.md` §7 prohibits identical cross-posts.
Not the same as the three files below.

### `prompting_rules.md`

Rules for *constructing* operational/task prompts for the Brain and its MCP
tools. Not a store of prompts, not media generation.

### `prompt_library.md`

Reviewed example **operating prompts** (Brain / MCP tasks) that demonstrate the
construction standard. Not media generation.

### `prompt_templates.md`

Reusable MCP task scaffolds. Not media generation.

---

## 06_PERFORMANCE — WHAT ACTUALLY HAPPENED

### `performance_framework.md`

Which metric matters for which objective (awareness / engagement / education /
traffic / lead-gen / conversion), and how to judge signal vs noise. Reference.

### `campaign_history.md`

Campaign-level history: objective, dates, audience, offer, platforms, content
used, spend, leads, sales, overall result.

### `content_performance.md`

Individual non-video post performance (static, carousel, text): platform,
audience, format, hook, reach, impressions, engagements, saves, clicks, leads,
result. Use `record_post_performance`.

### `video_performance.md`

Individual video performance: name/ID, platform, audience, hook, duration,
format, views, watch time, retention, completion, likes, comments, shares,
clicks, leads, result. Use `record_video_performance` / `record_post_performance`.

### `ad_performance.md`

Paid ad performance: ad ID, campaign, spend, impressions, CPM, CTR, CPC, leads,
CPL, conversions, CPA, ROAS, creative, audience, offer.

### `learning_log.md`

First-pass conclusions drawn from performance. Route: initial performance
interpretation → here. Append-only.
Example: "Problem hooks produced stronger first-3-second retention in 4 of the
last 5 Instagram videos."

### `validated_patterns.md`

Patterns supported by **repeated** evidence or a completed experiment. Per
pattern: pattern, audience, platform, evidence, number of tests, result,
confidence, where it applies / where it may not. Route: repeated supported
result → here. A timing slot may be written here only after
`analyze_posting_time_performance` returns `can_claim_best_time: true`.

---

## 07_RESEARCH — WHAT IS HAPPENING OUTSIDE

Every research entry records: source title, URL, publication date, access date,
geography, evidence type, confidence, contradicting evidence, evidence gaps,
last checked. External benchmarks are labelled TESTING, never VALIDATED.

### `market_trends.md`

External market and industry-direction trends relevant to Mysoft.

### `social_trends.md`

Cross-platform social behaviour and emerging content-format trends. Durable
platform-specific findings still belong in `03_PLATFORM/<platform>.md`.

### `search_trends.md`

Query, search-intent and discoverability trends. Mark clearly whether an entry
is keyword-tool-verified or inferred.

### `government_updates.md`

Government announcements, regulations, grants, tax changes, e-Invoice changes,
manufacturing policies, compliance changes. Always: date, source, effective
date, businesses affected, possible business/marketing impact.

### `industry_news.md`

Material industry developments: manufacturing trends, technology adoption,
industry reports, market changes, competitor industry developments. Source + date.

### `customer_insights.md`

Things learned **directly from customers and prospects**: comments, FAQs,
WhatsApp threads, demo feedback, event feedback, sales conversations, customer
wording. First-party only — not web research, not inference. A recurring
deal-blocker is also summarised (via proposal) in
`01_BUSINESS/customer_objections.md`.

### `competitor_updates.md`

Dated, running log of material competitor activity between full profile
refreshes. A durable finding graduates into the individual competitor file or
`competitor_patterns.md` / `competitor_gaps.md`.

### `YYYY-MM-DD-<topic>.md`

Dated standalone research passes (a landscape analysis, an opportunity study).
Descriptive kebab-case names, never numeric-only. Registered in
`research_index.md` with category, date, confidence, status, next review.
Superseded passes move to `07_RESEARCH/_archive/` and stop being cited as
current evidence.

### `research_index.md`

The current research catalogue. Link active research only. Do not list archived
or test material as active evidence. Do not recreate the legacy catch-all
`trends.md` (archived — its scope overlapped the three canonical trend files).

---

## 08_DECISIONS — WHAT WE ARE GOING TO DO

### `content_backlog.md`

Possible future content ideas worth keeping but not yet prioritized: idea,
audience, platform, product, reason, status.

### `recommended_content.md`

Full evidence-backed content proposals in the `decision_framework.md` §33
format, ready for human review. Route: proposed content → here (or
`content_backlog.md` for lighter ideas). Still a recommendation, not a decision.

### `current_priorities.md`

Only what should be worked on now: priority audiences, priority products,
campaign priority, key content themes, immediate goals. Keep short.

### `experiments.md`

Marketing tests: hypothesis, variable, control, test version, metric, result,
learning.

### `rejected_ideas.md`

Ideas considered and deliberately not pursued, with the reason — so they are not
re-proposed. Route: rejected idea → here.

### `decision_log.md`

Actual **approved** decisions: date, decision, reason, evidence, expected
result, and later actual result. An AI recommendation is not a decision until a
human approves it (`brain_rules.md` §30).

### `brain_update_proposals.md`

The only sanctioned channel for proposing changes to protected `00_SYSTEM/` and
`01_BUSINESS/` files. Append proposals here (target file, reasoning, proposed
change, status). A human applies or rejects them.

### `YYYY-MM-DD-session-record.md`

Dated records of significant audits or restructuring sessions — what changed and
why. Reference, not a routing target for ordinary findings.

---

## ROOT FILES — not routing targets

`README.md` (repo navigation), `CLAUDE.md` (working context loaded each session)
and `prompt.md` (legacy operating prompt) are maintained by the human. Do not
route research, findings or ideas into them.

---

# MOST IMPORTANT ROUTING RULE

Always separate:

## FACT

Something discovered or known.
Example: "Bizit Systems published 8 videos about production tracking."
→ `04_COMPETITORS/bizit-systems.md`

## INSIGHT

What the fact appears to mean.
Example: "Production tracking is becoming a heavily used competitor topic."
→ relevant research / performance / learning file.

## ACTION

What we should do.
Example: "Test a traceability-focused video instead of another generic
production tracking video."
→ `08_DECISIONS/content_backlog.md`, `recommended_content.md`,
`current_priorities.md`, or `experiments.md`.

Do not mix FACT, INSIGHT and ACTION together.

---

# PRIMARY FILE RULE

When information could fit multiple files:

1. Put the original information in the file where the **subject naturally belongs**.
2. Put only the strategic implication into another file if necessary.
3. Do not duplicate the exact same paragraph across several files.

Example — Information: "Digiwin AIoT is a technology supplier." → primary
`01_BUSINESS/products.md`. Implication: "We must avoid claiming all Digiwin AIoT
functions are native Mysoft MES capabilities." → `01_BUSINESS/positioning.md`.

---

# BEFORE WRITING ANY DATA

**Step 1 — Identify the subject.** Business? Product? Audience? Platform?
Competitor? Creative? Performance? Research? Decision?

**Step 2 — Identify the type.** Fact? Insight? Learning? Idea? Experiment?
Decision? Proposal?

**Step 3 — Select the primary file.**

**Step 4 — Check whether the information already exists.** If yes, update the
existing entry rather than creating a duplicate.

**Step 5 — Record source / date / evidence class / confidence when relevant.**

**Step 6 — Write only information relevant to that file's purpose.**

**Step 7 — Update the matching index** in the same session: `audience_index.md`,
`platform_index.md`, `competitor_index.md`, `research_index.md`,
`content_calendars/calendar_index.md`.

---

# IF YOU ARE UNSURE

Do not guess. Before writing, output:

**Suggested file:** `[path]`
**Reason:** `[why]`
**Possible secondary file:** `[path or none]`

Then continue only when the correct routing is sufficiently clear.

The goal is to keep the Marketing Brain clean, readable, non-duplicated and easy
for both humans and AI to understand.
