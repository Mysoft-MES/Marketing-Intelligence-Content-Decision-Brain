# MARKETING BRAIN — INFORMATION ROUTING PROMPT

You are responsible for organizing all information you discover into the correct Markdown files inside this Marketing Brain.

Before writing any information, first determine:

1. **What type of information is this?**
2. **Which file is its primary home?**
3. Is it a **fact**, **insight**, **performance result**, or **decision**?
4. Does the information already exist?
5. Should an existing entry be updated instead of duplicated?

Use ONLY the following structure unless specifically instructed to create a new file.

---

## 00_SYSTEM — HOW THE BRAIN THINKS

### `brain_rules.md`

Put rules controlling how the AI should behave here.

Examples:

* Always use evidence before making conclusions.
* Never invent competitor information.
* Do not treat views as the only success metric.
* Do not recommend identical content across every platform.
* Distinguish facts from assumptions.

**Question to ask:**
"Is this a rule controlling how the Brain behaves?"

If yes → `brain_rules.md`

---

### `decision_framework.md`

Put rules explaining **how marketing decisions should be made** here.

Examples:

* What factors to consider before recommending content.
* How to prioritize content ideas.
* How to decide platform + audience + hook + duration + CTA.
* How to decide whether something should be ACT NOW, TEST, MONITOR or IGNORE.

**Question:**
"Does this explain how the Brain should make a recommendation?"

If yes → `decision_framework.md`

---

### `evidence_rules.md`

Put rules about evidence, sources and confidence here.

Examples:

* Source requirements.
* Fact vs assumption.
* Confidence levels.
* Research verification.
* Dates and source links.
* How much evidence is needed before accepting a conclusion.

**Question:**
"Does this explain how information should be verified?"

If yes → `evidence_rules.md`

---

# 01_BUSINESS — OUR BUSINESS

### `company_profile.md`

Put factual information about the company here.

Examples:

* Company background.
* Business model.
* Customer base.
* Markets served.
* Industries served.
* Brands.
* Business priorities.
* Existing customer relationships.
* Internal capabilities.

Example:

"We have a large existing SQL customer base."

→ `company_profile.md`

---

### `products.md`

Put factual information about products/services here.

Examples:

* Product features.
* Modules.
* What the product does.
* Integrations.
* Product ownership.
* Supplier/partner technology.
* Product limitations.
* Product roadmap.
* Native vs third-party capability.

Example:

"Our Job Order module can upload production information to Digiwin AIoT."

→ `products.md`

---

### `positioning.md`

Put information about **how we should compete and describe ourselves** here.

Examples:

* Value proposition.
* Differentiation.
* Target market.
* Main message.
* Competitive position.
* What should be emphasized.
* What should NOT be claimed.

Example:

"We should distinguish Mysoft MES capabilities from Digiwin AIoT supplier capabilities."

→ `positioning.md`

---

### `customer_objections.md`

Put customer concerns, resistance, misunderstandings and questions here.

Examples:

* "Too expensive."
* "Why do we need MES?"
* "We already use Excel."
* "Will this replace our ERP?"
* "Implementation looks difficult."

Record the customer's actual wording whenever possible.

---

### `swot.md`

Only store strategic:

* Strengths
* Weaknesses
* Opportunities
* Threats

Do not dump ordinary business information here.

Example:

FACT:

"We already have manufacturing customers using our Job Order module."

Primary location:

→ `company_profile.md` or `products.md`

STRATEGIC INTERPRETATION:

"Existing manufacturing customers create a cross-sell opportunity for MES."

→ `swot.md`

---

# 02_AUDIENCE — WHO WE ARE TALKING TO

### `factory_owner.md`

Put information specifically about factory owners.

Examples:

* Business concerns.
* Profit.
* Cost.
* Productivity.
* ROI.
* Delivery.
* Visibility.
* Buying triggers.
* Objections.
* Content that attracts them.

---

### `production_manager.md`

Put information specifically about production managers.

Examples:

* Production status.
* Job progress.
* Downtime.
* Scheduling.
* Operator performance.
* Traceability.
* Daily frustrations.
* KPIs.
* Content interests.

---

### `finance_manager.md`

Put information specifically about finance managers.

Examples:

* Cost control.
* ROI.
* Labour cost.
* Waste.
* Production costing.
* Budget concerns.
* Financial justification.

---

### `audience_matrix.md`

Use this when comparing multiple audiences.

Examples:

Factory Owner vs Production Manager vs Finance Manager:

* Pain points.
* Buying motivation.
* Decision power.
* Best message.
* Best content.
* Relevant platform.
* CTA.

Do not put information about only one audience here if it belongs in their individual file.

---

# 03_PLATFORM — HOW EACH PLATFORM WORKS

Platform files contain **platform behaviour and strategy**, not individual posts.

### `facebook.md`

Store:

* Facebook audience behaviour.
* Content formats.
* Suitable hooks.
* Video length findings.
* CTA behaviour.
* Content style.
* What performs / does not perform on Facebook.

---

### `instagram.md`

Store:

* Instagram consumption behaviour.
* Reels strategy.
* Visual hooks.
* Recommended duration.
* Content styles.
* Audience behaviour.
* Instagram-specific findings.

---

### `linkedin.md`

Store:

* B2B behaviour.
* Professional audience.
* Thought leadership.
* Business-focused hooks.
* Decision-maker content.
* LinkedIn content formats.

---

### `xiaohongshu.md`

Store:

* XHS audience behaviour.
* Chinese-language search behaviour.
* Useful content styles.
* Titles/hooks.
* Practical experience content.
* XHS-specific trends and findings.

---

### `reddit.md`

Store:

* Community behaviour.
* Discussion styles.
* Promotional tolerance.
* Question/problem formats.
* Authenticity requirements.
* Reddit-specific content strategy.

---

### `youtube.md`

Store:

* Searchable video behaviour.
* Long-form vs Shorts.
* Video structure.
* Thumbnail/title findings.
* Duration.
* Educational/demo content.

---

# 04_COMPETITORS — WHAT COMPETITORS ARE DOING

### `competitor_index.md`

Use this as the master competitor list.

For each competitor:

* Name.
* Product category.
* Website.
* Main products.
* Main platforms.
* Importance.
* Last researched.

Do not put detailed research here.

---

### `<competitor-name>.md`

Each verified or actively researched competitor gets a descriptively named file,
for example `bizit-systems.md` or `critical-manufacturing-malaysia.md`.
Use `competitor_template.md` when creating a new profile. Do not create generic
`competitor_a.md`, `competitor_b.md`, or `competitor_c.md` placeholders.

Put:

* Products.
* Pricing.
* Positioning.
* Website messaging.
* Social posts.
* Ads.
* Campaigns.
* Hooks.
* Offers.
* CTAs.
* Video formats.
* Video duration.
* Landing pages.
* Strengths.
* Weaknesses.
* Recent activity.

Every observation should include when possible:

**Date:**
**Platform:**
**Source:**
**Topic:**
**Audience:**
**Hook:**
**Format:**
**Offer:**
**CTA:**
**Observation:**
**Possible implication:**

Never put our own strategy inside a competitor file unless clearly labelled as analysis.

---

# 05_CREATIVE — HOW CONTENT SHOULD BE CREATED

### `hook_library.md`

Put actual usable hooks here.

Example:

"Boss asks one question: Where is Job 1058?"

Include when possible:

* Hook.
* Hook type.
* Audience.
* Platform.
* Product.
* Pain point.
* Performance if tested.

---

### `video_formats.md`

Put reusable video formats here.

Examples:

* POV.
* Factory scenario.
* Talking head.
* Product demo.
* Interview.
* Before/after.
* Customer story.
* Screen recording.

For each format record:

* Best use.
* Suitable audience.
* Suitable platform.
* Suggested duration.
* Strength.
* Weakness.

---

### `creative_rules.md`

Put general creative principles here.

Examples:

* Hook viewers immediately.
* Avoid long logo introductions.
* Show the problem before the product when appropriate.
* Do not overcrowd short videos with too many messages.
* Adapt creative execution by platform.

---

### `winning_patterns.md`

Only put patterns here when performance evidence shows they work repeatedly.

Example:

"Problem-first factory scenario videos consistently generate stronger retention than feature-first videos."

Include:

* Pattern.
* Audience.
* Platform.
* Evidence.
* Number of tests.
* Result.
* Confidence.

Do NOT declare something a winning pattern after one successful video.

---

# 06_PERFORMANCE — WHAT ACTUALLY HAPPENED

### `campaign_history.md`

Store campaign-level history.

Examples:

* Campaign objective.
* Dates.
* Audience.
* Offer.
* Platforms.
* Content used.
* Spend.
* Leads.
* Sales.
* Overall result.

---

### `video_performance.md`

Store individual video performance.

Examples:

* Video name/ID.
* Platform.
* Audience.
* Hook.
* Duration.
* Format.
* Views.
* Watch time.
* Retention.
* Completion.
* Likes.
* Comments.
* Shares.
* Clicks.
* Leads.
* Result.

---

### `ad_performance.md`

Store paid advertisement performance.

Examples:

* Ad ID.
* Campaign.
* Spend.
* Impressions.
* CPM.
* CTR.
* CPC.
* Leads.
* CPL.
* Conversions.
* Creative.
* Audience.
* Offer.

---

### `learning_log.md`

Put conclusions discovered from performance here.

Example:

"Problem hooks produced stronger first-3-second retention in 4 of the last 5 Instagram videos."

This is where observations become learnings.

If repeated strongly enough, the learning can later be added to:

→ `05_CREATIVE/winning_patterns.md`

---

# 07_RESEARCH — WHAT IS HAPPENING OUTSIDE

### `market_trends.md`

Store external market and industry-direction trends relevant to Mysoft.

### `social_trends.md`

Store cross-platform social behaviour and emerging content-format trends.
Platform-specific durable findings still belong in `03_PLATFORM/<platform>.md`.

### `search_trends.md`

Store query, search-intent and discoverability trends supported by search evidence.

### `research_index.md`

Use this as the current research catalogue. Link active research, its category,
date, confidence and review status. Do not list archived test material as active evidence.

Only keep trends relevant to the business. Do not recreate the legacy catch-all
`trends.md`; it is archived because its scope overlapped the three canonical files.

---

### `government_updates.md`

Store relevant:

* Government announcements.
* Regulations.
* Grants.
* Tax changes.
* E-Invoice changes.
* Manufacturing policies.
* Compliance changes.

Always include:

* Date.
* Source.
* Effective date if available.
* Businesses affected.
* Possible business/marketing impact.

---

### `industry_news.md`

Store important industry developments.

Examples:

* Manufacturing trends.
* Technology adoption.
* Industry reports.
* Competitor industry developments.
* Market changes.

Include source and date.

---

### `customer_insights.md`

Store things learned directly from customers.

Examples:

* Customer comments.
* Frequently asked questions.
* WhatsApp conversations.
* Demo feedback.
* Event feedback.
* Sales conversations.
* Customer wording.

Example:

"Customers repeatedly ask, 'Can I know which operator is currently handling the job?'"

→ `customer_insights.md`

If it becomes a major objection, summarize it also in:

→ `customer_objections.md`

---

# 08_DECISIONS — WHAT WE ARE GOING TO DO

### `content_backlog.md`

Put possible future content ideas here.

These are ideas worth keeping but not yet priorities.

Include:

* Idea.
* Audience.
* Platform.
* Product.
* Reason.
* Status.

---

### `current_priorities.md`

Only store what should be worked on now.

Examples:

* Priority audiences.
* Priority products.
* Campaign priority.
* Important content themes.
* Immediate marketing goals.

Keep this file short.

---

### `experiments.md`

Put marketing tests here.

Examples:

"Test 20-second vs 40-second MES scenario videos."

"Test problem hook vs question hook."

Include:

* Hypothesis.
* Variable.
* Control.
* Test version.
* Metric.
* Result.
* Learning.

---

### `decision_log.md`

Store actual approved decisions.

Examples:

"Prioritize new customer acquisition over cross-selling existing customers."

"Increase production-manager-focused MES content."

Include:

* Date.
* Decision.
* Reason.
* Evidence.
* Expected result.

Do not treat an AI recommendation as a final decision unless it has actually been approved.

---

# MOST IMPORTANT ROUTING RULE

Always separate:

## FACT

Something discovered or known.

Example:

"Bizit Systems published 8 videos about production tracking."

→ `04_COMPETITORS/bizit-systems.md`

## INSIGHT

What the fact appears to mean.

Example:

"Production tracking is becoming a heavily used competitor topic."

→ relevant research/performance/learning file.

## ACTION

What we should do.

Example:

"Test a traceability-focused video instead of another generic production tracking video."

→ `08_DECISIONS/content_backlog.md`, `current_priorities.md`, or `experiments.md`

Do not mix FACT, INSIGHT and ACTION together.

---

# PRIMARY FILE RULE

When information could fit multiple files:

1. Put the original information in the file where the **subject naturally belongs**.
2. Put only the strategic implication into another file if necessary.
3. Do not duplicate the exact same paragraph across several files.

Example:

Information:

"Digiwin AIoT is a technology supplier."

Primary:

→ `01_BUSINESS/products.md`

Implication:

"We must avoid claiming all Digiwin AIoT functions are native Mysoft MES capabilities."

→ `01_BUSINESS/positioning.md`

---

# BEFORE WRITING ANY DATA

Follow this process:

**Step 1 — Identify the subject.**

Business?
Product?
Audience?
Platform?
Competitor?
Creative?
Performance?
Research?
Decision?

**Step 2 — Identify the type.**

Fact?
Insight?
Learning?
Idea?
Experiment?
Decision?

**Step 3 — Select the primary file.**

**Step 4 — Check whether the information already exists.**

If yes, update the existing information rather than creating duplicates.

**Step 5 — Record source/date when relevant.**

**Step 6 — Write only information relevant to that file's purpose.**

---

# IF YOU ARE UNSURE

Do not guess.

Before writing, output:

**Suggested file:** `[path]`

**Reason:** `[status]`

**Possible secondary file:** `[path or none]`

Then continue only when the correct routing is sufficiently clear.

The goal is to keep the Marketing Brain clean, readable, non-duplicated and easy for both humans and AI to understand.
