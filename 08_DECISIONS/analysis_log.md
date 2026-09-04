# Analysis Log — Stage: Analysis #1 ("Researching")

Running log of the **first** analysis stage in the operating loop: the interpretation
pass that sits **after Research and before Prompting**. It turns each run's raw research
findings into an explicit content decision — what to create, for whom, on which platform,
and why — which the prompting stage then executes.

- This is interpretation, not new research. It cites the research entries it reads; it does
  not add external sources.
- One dated entry per run. Newest first. Never rewrite a past entry — add a new one.
- If a run's research changed nothing material, the entry says so and the prompting stage
  is skipped that run.
- Analysis #2 ("Posting") lives in `06_PERFORMANCE/competitive_benchmark.md` +
  `06_PERFORMANCE/learning_log.md`, not here.

See `00_SYSTEM/daily_operating_spec.md` §4A for the stage definition.

---

## Entry template

```
## <YYYY-MM-DD>

**Research read:** <files / entries this interprets, with paths>
**Prior refinement applied:** <the latest 06_PERFORMANCE/learning_log.md refinement note, or "none">

**What the findings mean:**
- <interpretation — the "so what", not a restatement of the finding>

**Content decision:**
- Create / Test / Monitor / Nothing this run — <which, and why>
- If Create/Test: platform, audience, angle, the research entry it derives from,
  hypothesis, success metric

**Confidence:** <LOW / MEDIUM / HIGH> — <why>
**Open questions handed to the next Research run:** <list, or "none">
```

---

<!-- entries below, newest first -->

## 2026-09-04 (third run — post-reconciliation re-sweep)

**Research read:** this run's in-place updates — `07_RESEARCH/government_updates.md` #2
(e-Invoice Phase 4 relaxation end-date), #8 (evening re-sweep note); `07_RESEARCH/industry_news.md`
#5 addendum; `03_PLATFORM/linkedin.md` (2026-09-04 evening re-confirmation);
`03_PLATFORM/platform_index.md`; `07_RESEARCH/research_index.md`. Context: the two earlier
2026-09-04 entries below; `06_PERFORMANCE/competitive_benchmark.md` (2026-09-04, second run).

**Prior refinement applied:** `06_PERFORMANCE/learning_log.md` REFINEMENT (2026-09-04, second
run) — "at the Prompting gate only *check* whether the owner has named a person (yes/no); do
not rebuild the case; spend freed effort on the logged-in Allied social audit." **Gate
checked this run: still NO named person** (nothing in `sales_insights.md` or
`current_priorities.md` names a founder / technical lead). Not rebuilt. Logged-in Allied
audit still not possible without authentication — attempted via public sources only this run.

**What the findings mean:**
- **This run was a reconciliation + a quiet re-sweep, not a new-evidence run.** Local `main`
  had diverged from `origin/main` (a stale branch + three unpushed same-day run outputs); it
  was rebased back onto `origin/main`. During the run the owner **merged approval PR #1**, so
  LI-C1, IG-01, IG-02, FB-03, FB-04, IG-04 are now owner-approved — `apply_prompt_decision`
  run this session to flip their status and log them (`decision_log.md`).
- **One knowledge conflict resolved:** the e-Invoice Phase 4 penalty-free relaxation
  end-date, flagged "contested" on 2026-09-03, is now consistently reported (multiple
  tax-advisory sources) as **31 December 2027** — IRBM extended it in April 2026. The
  RM10,000 per-transaction rule is not relaxed. This is a footnote sharpening, **not** a
  content trigger — Mysoft MES is not an e-Invoice product; the "your invoices are digital,
  your shop floor isn't" adjacency framing (government_updates #2) is unchanged.
- **Everything else re-confirmed with sharper external numbers, no directional change:**
  LinkedIn algo (company-page reach −60–66%; employee posts ~+561%; carousels highest
  format, 8–12 slides) and the MES-market / phased-adoption story both just firm up what the
  Brain already recorded on 2026-09-04. Per `evidence_rules.md` §38 and `brain_rules.md` §31,
  no new dated files, no new content asset.
- **Allied audit (public sources):** one addition — Allied also publishes an "MES vs ERP"
  explainer (early Jul 2026), so its buyer-education funnel is even more complete than the
  second-run audit captured. Recorded in `research_index.md` and `competitive_benchmark.md`;
  `allied-solutions-global.md` kept 100% human-supplied / verbatim (the Brain's Allied
  research lives in the analysis + benchmark logs, not that file). White space unchanged:
  named-person, short-form, shop-floor story, Penang-local.

**Content decision:**
- **Nothing new this run.** No new generation prompt. The re-sweep changed nothing that
  opens a content opportunity.
- **LI-C1 is now APPROVED** (owner merged PR #1 this day). It moves from "pending TEST" to
  "approved for production" — but production and publishing remain separate human steps, and
  it is **still gated on the owner naming a person** for any named-person framing (the
  carousel itself can run as a company-page asset; the named-person LinkedIn *direction*
  stays blocked — `current_priorities.md` item 1).
- IG-01, IG-02, FB-03, FB-04, IG-04 also APPROVED via the same merge.

**Confidence:** LOW — `current_priorities.md` still carries no owner-set business priorities;
`sales_insights.md` still records pre-revenue / zero-customer / zero-demo-notes. Nothing here
is validated against Mysoft sales, customer or performance evidence.

**Open questions handed to the next Research run:**
- Logged-in social audit of Allied (`allied-solutions-pte-ltd`, `alliedsolutionsg`) — still
  the single highest-value competitor task; cadence, recency, engagement, format mix,
  individual employees, paid ads.
- Has the owner named a founder / technical lead? (carried)
- Does Mysoft hold Malaysia Digital (MD) status? (determines whether MDEC SmartMFG+ is
  actionable — government_updates #7)
- Budget 2027 actual measures — from 9 Oct 2026.

## 2026-09-04 (second run — competitor-set reset)

**Research read:** `04_COMPETITORS/allied-solutions-global.md` — the human-supplied Allied
Solutions Global / ASPL document (copied verbatim 2026-09-04) **plus** this run's first
Brain content/social audit of Allied appended to that file. Context: `competitor_index.md`
(reset to Allied only), the earlier 2026-09-04 entry below, `06_PERFORMANCE/competitive_benchmark.md`
2026-09-04, `08_DECISIONS/content_backlog.md` (LI-C1, shift-handover idea).

**Prior refinement applied:** `06_PERFORMANCE/learning_log.md` REFINEMENT (2026-09-04) —
"before the next Prompting stage, check whether the owner has named a founder / technical
lead for LinkedIn; if still no, say so and route to `current_priorities.md` rather than
drafting more company-page LinkedIn content." **Gate checked this run: NO named person.**
Nothing in this session, `sales_insights.md`, or `current_priorities.md` names a founder or
technical lead. Routed to `current_priorities.md` this run. No new company-page LinkedIn
content drafted.

**What the findings mean:**
- **The competitor picture narrowed from 14 vendors to 1, and that 1 is a genuine content
  competitor.** Allied Solutions Global runs a sustained, plain-language, problem-first
  buyer-education programme (full funnel: what-is-MES → buyer's guide → how-to-choose →
  implementation → ROI/cost) and has a Penang office in Mysoft's own city. This is a
  stronger, more direct content competitor than the retired benchmark's "content leader"
  (DigiwinSoft), and it is strong on the exact register Mysoft intended to own.
- **But the white space Mysoft's current test aims at is unaffected.** Allied's content is
  English, regional, website/SEO-led, corporate/unbylined, long-form. No named-person
  LinkedIn presence, no authentic shop-floor storytelling, no short vertical video or
  carousel visible from public sources. LI-C1's thesis (format + named-person white space)
  still holds.
- **This run's research sharpened an existing understanding; it did not open a new content
  opportunity.** Per `brain_rules.md` §31, drafting a new asset to "respond" to Allied would
  be a content-factory move. The correct responses are strategic, not a post: (a) the
  named-person decision, (b) whether Mysoft builds its own buyer-journey content set — both
  owner decisions, routed to `current_priorities.md`.
- The other full-sweep areas (platform, audience, industry, government, market, search,
  social) were re-confirmed by the earlier 2026-09-04 pass with nothing material; not
  re-researched this run (same day; `evidence_rules.md` §38).

**Content decision:**
- **Nothing new this run.** No new generation prompt. The evidence changed the competitive
  map, not the content pipeline.
- **LI-C1 (LinkedIn carousel, 9 panels) stays the pending TEST** — unchanged from the
  earlier 2026-09-04 entry. The Allied audit *reinforces* it (format + named-person white
  space confirmed against the sole tracked competitor). Still DRAFT; still gated on the
  owner (a) naming a person and (b) approving a carousel row / standalone test.
- **Routed to `08_DECISIONS/current_priorities.md`:** (1) name a founder / technical lead
  for LinkedIn (blocks LI-C1 and all named-person LinkedIn content); (2) decide whether to
  commission a Mysoft buyer-journey content set to answer Allied's — Mysoft currently has
  zero published assets against Allied's full funnel.

**Confidence:** LOW — `08_DECISIONS/current_priorities.md` is still empty and
`sales_insights.md` records a pre-revenue, zero-customer, zero-demo-notes stage, so nothing
here is validated against Mysoft sales, customer or performance evidence. The Allied audit
is vendor-site + directory sources only, no engagement data, single pass.

**Open questions handed to the next Research run:**
- Logged-in social audit of Allied (`allied-solutions-pte-ltd` on LinkedIn, `alliedsolutionsg`
  on Facebook): cadence, recency, engagement, format mix, any individual employees posting.
- Does Allied's Penang office run local-market / local-language content?
- Any Allied paid advertising (Meta / LinkedIn / Google)?
- Has Allied appeared in a real Mysoft deal? (owner / sales input — competitive implications
  stay HYPOTHESIS without it)
- Has the owner named a founder / technical lead? (carried from the refinement gate)

---

## 2026-09-04

**Research read:** this run's in-place updates — `03_PLATFORM/linkedin.md` (2026-09-04
carousel / employee-advocacy figures), `07_RESEARCH/government_updates.md` #7 (MDEC
SmartMFG+ Incentive Programme), `04_COMPETITORS/aspl-allied-solutions.md` (Siemens FA/Digital
partner; AI/IIoT product language). Prior context: `2026-09-03-competitor-content-activity-first-pass.md`,
`competitor_gaps.md` Gap 1, `08_DECISIONS/content_backlog.md` (shift-handover idea, 2026-09-02).
**Prior refinement applied:** none — first run under the closed loop; no `REFINEMENT:` note exists yet.

**What the findings mean:**
- The two independent signals that matter both point the same way: (a) LinkedIn document/
  carousel posts are now the highest-engagement native format with 8–12 slides optimal, and
  (b) individual-employee posts out-reach the company page several times over. The Brain
  already had the founder/named-expert thesis (2026-08-31) and a carousel idea parked; this
  run turns "worth testing" into "the format and the channel choice are the same bet, made
  twice." The existing test asset **LI-C1** is the correct vehicle — it was just mis-sized
  (6 panels, below the band). Fixed this run to 9.
- **MDEC SmartMFG+** is a *provider-side* incentive (Mysoft could qualify; so could
  competitors). It is not a customer-facing content angle and must not be turned into a
  "grants available" post — that would misrepresent a TSP incentive as a buyer incentive.
  It is an operational item for the owner (`current_priorities.md`), not content.
- **ASPL** adopting "AI-driven optimization / IIoT" platform language (now a named Siemens
  partner) is the global-vendor vocabulary arriving in a local competitor. It makes Mysoft's
  plain-language, shop-floor-story, SME-specific positioning *more* distinct, not less — it
  does not require a response, only monitoring.

**Content decision:**
- **Test** — proceed with **LI-C1** (LinkedIn carousel, Production Manager primary / GM
  secondary, top-of-funnel), revised this run to 9 panels. Derived from
  `03_PLATFORM/linkedin.md` (2026-09-03 + 2026-09-04) and the first-pass competitor audit.
  Hypothesis and success metric already carried in the prompt file (dwell time / saves per
  impression vs the September LinkedIn text-post median; no numeric target until a Mysoft
  baseline exists).
- **No new asset this run.** The evidence sharpened an existing test; it did not open a new
  one. Creating another prompt to "look busy" would violate `brain_rules.md` §31.
- LI-C1 stays DRAFT on approval PR `approvals/2026-09-04` (PR #1) with the revision noted.

**Confidence:** LOW — `01_BUSINESS/swot.md` is populated but `sales_insights.md` records a
pre-revenue, zero-customer stage and `08_DECISIONS/current_priorities.md` is still empty, so
nothing here is validated against Mysoft sales, customer or performance evidence. All
platform figures are external benchmarks (TESTING).

**Open questions handed to the next Research run:**
- Does Mysoft hold Malaysia Digital (MD) status? (Determines whether SmartMFG+ is actionable.)
- Logged-in social audit of the top 5 competitors — cadence, recency, engagement, any
  individual employees posting about MES — still not done.
- Any of the 14 competitors appearing in a real Mysoft deal (needs owner/sales input) —
  every competitive implication remains HYPOTHESIS without it.
