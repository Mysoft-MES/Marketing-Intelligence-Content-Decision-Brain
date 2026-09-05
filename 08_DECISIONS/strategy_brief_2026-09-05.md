# Strategy Brief — 2026-09-05

**What this is.** The strategist read of this run's research, written the way a marketing lead
would brief the owner: what it means, where the gap is, what to do, what to make, where it
goes, when to post, what to research next. `08_DECISIONS/analysis_log.md` holds the short
decision record; this file holds the reasoning.

**Confidence on everything below: LOW.** Unchanged from every prior brief:
`08_DECISIONS/current_priorities.md` has no owner-set business priority to rank against;
`01_BUSINESS/sales_insights.md` records pre-revenue, zero customers, demos in progress, zero
demo notes captured; there is no first-party performance or audience data on any channel;
every platform and competitor figure is an external benchmark → TESTING.

**Inputs read:** this run's research (commit `2b6b150`) — `07_RESEARCH/industry_news.md` #4
addendum (West Asia war supply-chain stressor), `07_RESEARCH/research_index.md`; re-checks of
`03_PLATFORM/linkedin.md`, `07_RESEARCH/government_updates.md`, `04_COMPETITORS/allied-solutions-global.md`
(no material change found in any of the three). Context: `08_DECISIONS/strategy_brief_2026-09-04.md`
(yesterday's full brief — its Opportunity/Gap and Platform Strategy sections stand unchanged
and are not repeated in full here), `06_PERFORMANCE/learning_log.md` (sixth-run refinement),
`06_PERFORMANCE/competitive_benchmark.md` (2026-09-04 sixth run), `list_generation_prompt_status`,
`get_prompt_approval_pr` for PR #1 and PR #2 (both merged and already applied — see
`08_DECISIONS/analysis_log.md` 2026-09-05).
**Prior refinement applied:** `learning_log.md` REFINEMENT (2026-09-04, sixth run) — a repeat
same-day pass with an open PR should short-circuit; that condition does not apply today (this
is the first run of a new calendar day and both prior PRs are already closed/merged), so a
normal full-sweep run applies. **Named-person gate checked this run: still NO** (nothing in
`sales_insights.md` or `current_priorities.md` names a founder / technical lead). Not rebuilt.
**Logged-in Allied audit: still not possible** (no authenticated access in this run) — now 7
runs overdue.

---

## 1. MEANING — what this research actually tells us about Mysoft

**Today added one new data point and confirmed everything else.** A 2026-09-03 industry
survey (Malay Mail) found 96% of Malaysian manufacturers report being affected by the West
Asia war, with 74% citing raw-material shortages and rising costs as the most pressing
concern — firms are shifting sourcing toward Singapore and China. This is a distinct pressure
from the US-tariff picture already on file: it is an **input-cost / supply-continuity** risk,
not an export-market risk.

**What it means for Mysoft:** it sharpens, rather than changes, the register already
recommended. A manufacturer absorbing a supply shock has more reason to want to see what is
actually happening on its shop floor in real time — WIP, material consumption, where a job
is stuck — than to hear a growth or efficiency pitch. This supports the existing "production
truth / verify what actually happened" frame (`positioning.md` §32) with a second, independent
reason beyond the original visibility/traceability argument: **operational resilience under
cost pressure.** It does not change platform choice, format, or audience — it is a usable line
inside copy that is already planned (e.g. LI-C2's "what number are you actually running your
schedule on"), not a reason for a new asset.

**Everything else re-confirmed with no directional change:** Malaysia manufacturing PMI
(50.2 August, third month of expansion), e-Invoice / SME digitalisation grant landscape,
LinkedIn algorithm (dwell/"Depth Score", carousel advantage, company-page reach penalty,
engagement-bait down-ranking), and Allied Solutions Global's public footprint (Penang/KL
offices, TrakSYS + Proficy distribution, PMAX 2026 booth, no visible short-form/carousel/
named-person content). None of this opens a new content opportunity beyond what yesterday's
brief already identified.

**The four binding gates are unchanged:** no named founder/technical lead, no customer proof,
no owner-set business priority, lean execution capacity. Yesterday's Opportunity/Gap and
Marketing Decision (§2–3 of `strategy_brief_2026-09-04.md`) still hold in full and are not
restated here.

---

## 2. OPPORTUNITY / GAP

Unchanged from `strategy_brief_2026-09-04.md` §2 — no new evidence today moves this table.
One addition: the West Asia war supply-chain stressor is a second, independent "why now"
argument (operational resilience) alongside the original visibility/traceability one. It
strengthens the existing verification-frame opportunity; it does not open a new one.

---

## 3. WHAT I RECOMMEND MYSOFT DO

**Primary direction (unchanged):** hold the plain-language, problem-first, verification-frame
position; ship the already-designed September social cycle and the two approved LinkedIn
carousels as the first data-generating moves; do not chase Allied's AI/IIoT vocabulary.

**The one new action this run is operational, not creative:** three DRAFT prompts — **FB-01**
(2026-09-08), **FB-02** (2026-09-15), **IG-03** (2026-09-23) — have been sitting on `main`
with no open approval PR since 2026-09-04 (a side effect of that day's six same-day passes).
They are valid, evidence-backed drafts, not new content. This run carries them into a fresh
approval PR so the owner can decide on them alongside everything else already pending
production (LI-C1, LI-C2, FB-05, and the four already-approved Reels).

**What should be avoided:** manufacturing a new asset in response to the West Asia war finding.
One LOW-MEDIUM-confidence survey, indirect relevance, and an audience (owners/GMs under cost
pressure) already targeted by existing copy is not sufficient evidence for a dedicated post —
it is a line to fold into copy already planned. Per `brain_rules.md` §31, the correct move on
a quiet-evidence day is to clear the process backlog (the orphaned PR), not add volume.

---

## 4. RECOMMENDED CONTENT PLAN

No new CREATE or TEST this run. Status of the existing plan:

| Priority | Asset | Platform | Status | Action this run |
|---|---|---|---|---|
| — | LI-C1, LI-C2 | LinkedIn | APPROVED (production not yet done) | None — awaiting production |
| — | FB-03, FB-04, FB-05 | Facebook | APPROVED (production not yet done) | None — awaiting production |
| — | IG-01, IG-02, IG-04 | Instagram | APPROVED (production not yet done) | None — awaiting production |
| CONTINUE | FB-01 | Facebook (2026-09-08) | DRAFT, orphaned (no open PR) | **Carry into today's approval PR** |
| CONTINUE | FB-02 | Facebook (2026-09-15) | DRAFT, orphaned (no open PR) | **Carry into today's approval PR** |
| CONTINUE | IG-03 | Instagram (2026-09-23) | DRAFT, orphaned (no open PR) | **Carry into today's approval PR** |
| HOLD | REC-6 website explainer | Website | Gated on owner (`current_priorities.md` item 2) | No prompt |

No prompt regeneration was needed for FB-01/FB-02/IG-03 — their evidence and claim-safety
checks remain valid; only their approval routing needed fixing.

---

## 5. PLATFORM-SPECIFIC TREATMENT

Unchanged from `strategy_brief_2026-09-04.md` §5 for every asset above — FB-01/02 keep the
plain, concrete, problem-first Facebook voice (Click-to-WhatsApp CTA); IG-03 keeps the
visual-first, SEO-caption, save/DM Instagram voice. No cross-platform duplication introduced.

---

## 6. WHEN TO POST

Unchanged dates: FB-01 → 2026-09-08, FB-02 → 2026-09-15, IG-03 → 2026-09-23, all still
`AWAITING HUMAN APPROVAL` and gated on the new approval PR. The counterbalanced LinkedIn
cycle and the LI-C1 → LI-C2 sequencing rule from yesterday's brief are unchanged. Cycle review
remains **2026-10-08**.

---

## 7. WHAT NOT TO DO

- Do not draft a new asset off the West Asia war survey — fold the line into existing copy
  instead (see §1).
- Do not regenerate FB-01/FB-02/IG-03 — their content is still valid; only routing was broken.
- Do not re-litigate the named-person gate or the logged-in Allied audit gap — both are
  standing, already-routed open items, not new analysis.
- Do not open a second research thread on Budget 2027 — nothing new until 9 October.

---

## 8. NEXT RESEARCH

Unchanged priority order from `strategy_brief_2026-09-04.md` §7:

1. **Logged-in Allied social audit** — 7 runs overdue. `allied-solutions-pte-ltd` (LinkedIn),
   `alliedsolutionsg` (Facebook): cadence, recency, engagement, format mix, individual
   employees, paid ads. LOGIN/HUMAN REVIEW required.
2. **First demo notes** (`sales_insights.md` §4). INTERNAL OWNER VERIFICATION.
3. **Owner business priority** (`current_priorities.md`). INTERNAL OWNER VERIFICATION.
4. **Named person: yes/no.** INTERNAL OWNER VERIFICATION.
5. **Malaysia Digital (MD) status** — determines SmartMFG+ actionability. INTERNAL OWNER
   VERIFICATION.
6. **Keyword-tool verification** of the search clusters before REC-6 is written. WEB SEARCH /
   dedicated keyword tool.
7. **First-party audience-age data** once any channel produces some. INTERNAL (post-launch).

---

## 9. CONFIDENCE / LIMITATIONS

**Overall confidence: LOW**, unchanged. Strongest evidence today: the PMI and West Asia
survey figures (PRIMARY / INDUSTRY SOURCE, dated, HIGH-confidence on the numbers themselves).
Weakest: everything about Mysoft's own audience and performance (zero first-party data) and
the Allied social-engagement picture (public sources only). First-party evidence status:
**FIRST-PARTY EVIDENCE LIMITED — external research remains hypothesis-generating**, per
`sales_insights.md` and `customer_insights.md`. Assumption carried forward: the West Asia
survey's relevance to MES buying is inferential (the survey measures general manufacturer
sentiment, not MES purchase intent) — treated as INFERENCE, not FACT, and used only as a
copy line, not a claim. Digiwin vs Mysoft-owned capability boundaries: unchanged, no new
information this run. Nothing here is VALIDATED.
