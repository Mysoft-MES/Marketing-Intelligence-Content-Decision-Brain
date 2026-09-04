# Competitive Benchmark — Stage: Analysis #2 ("Posting")

Running record of the **second** analysis stage in the operating loop: the pass that sits
**after Posting** and compares Mysoft MES's marketing output against what competitors are
doing, to produce concrete suggestions for beating them.

Analysis #2 has two halves:

1. **Our performance** — timing, engagement, format results from `record_post_performance`
   / `analyze_posting_time_performance`. *Empty until the first post is published.*
2. **Competitor comparison** — our posts / ads / cadence / formats / angles vs the 14
   verified MES competitors' content activity (`04_COMPETITORS/`,
   `07_RESEARCH/2026-09-03-competitor-content-activity-first-pass.md` and later audits).

Output each run: **what competitors did, whether it worked, and what Mysoft should do to do
better** — written as suggestions, not decisions. Suggestions feed the **next Research run**
via a refinement note appended to `06_PERFORMANCE/learning_log.md`.

- One dated entry per run. Newest first. Never rewrite a past entry.
- Competitor claims are evidence of what that party claims, not fact (`evidence_rules.md`).
- Nothing here is VALIDATED. Mysoft timing is validated only when
  `analyze_posting_time_performance` returns `can_claim_best_time: true`.

See `00_SYSTEM/daily_operating_spec.md` §9A for the stage definition.

> **Correction (owner, 2026-09-04):** the retired **2026-09-04 (first run)** entry below
> names **DigiwinSoft** as a competitor / "content leader" to beat. That is wrong. **Digiwin /
> DigiwinSoft is a Mysoft MES partner / technology supplier, never a competitor.** Past
> entries are not rewritten (running-log rule), but disregard every Digiwin competitor
> reference. See `04_COMPETITORS/competitor_index.md` NOTES.

---

## Entry template

```
## <YYYY-MM-DD>

### Half 1 — Our performance
<metrics, or "no first-party performance data yet — zero published posts">

### Half 2 — Competitor comparison
| Competitor | What they published / ran | Format & channel | Worked? (evidence) | Recency / cadence |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

**Where Mysoft is behind:** <gaps competitors are filling that we are not>
**Where competitors are weak / white space holds:** <openings>
**What competitors tried that flopped:** <do not copy>

### Suggestions to beat them (feed next Research + Prompting)
1. <specific, actionable>
2. ...

### Refinement written to learning_log.md this run
<the exact self-improvement note appended to 06_PERFORMANCE/learning_log.md>

**Confidence:** <LOW / MEDIUM / HIGH> — <why>
**Needs a logged-in / human pass:** <what could not be measured from public sources>
```

---

<!-- entries below, newest first -->

## 2026-09-04 (third run — post-reconciliation re-sweep)

### Half 1 — Our performance

No change. No first-party performance data — zero published posts.
`analyze_posting_time_performance` returns nothing for every platform;
`record_post_performance` has no records. **New this day:** the owner **merged approval
PR #1**, so LI-C1 (LinkedIn carousel), IG-01, IG-02, FB-03, FB-04 and IG-04 are now
**APPROVED for production** (`apply_prompt_decision` run this session). Production and
publishing are still separate human steps — nothing is live, so there is still nothing to
measure.

### Half 2 — Competitor comparison

Only tracked competitor: **Allied Solutions Global / ASPL**. No logged-in pass was possible
this run either. One public-source addition since the second-run audit:

| Competitor | What they publish / run | Format & channel | Worked? (evidence) | Recency / cadence |
|---|---|---|---|---|
| **Allied Solutions Global / ASPL** | Buyer-education funnel now confirmed to also include an **"MES vs ERP: What's the Difference, and Do You Need Both?"** explainer (early Jul 2026) — one of the most common MES-buyer search queries — alongside what-is-MES, buyer's guides, how-to-choose, implementation guide, ROI/cost, web-based MES. Plus the 8 Jul 2026 "Driving Digital Transformation Together" exec session (with Yonyou Singapore). | Long-form articles on `alliedsolutionsglobal.com/news`; LinkedIn company page + Facebook; region-targeted SEO. Still no short video / carousel / named-person content visible. | **Not measured.** Sustained through Aug 2026 by dated titles. No engagement data (public sources only). | Content ≈ 1–3 posts/month. Social cadence/recency: **still needs a logged-in pass.** |

**Where Mysoft is behind:** unchanged — Allied has a complete, connected, published
buyer-journey content set (now including MES-vs-ERP); Mysoft has zero published assets.
Allied is on Mysoft's own intended register (plain-language, problem-first) and got there
first, at volume, with a Penang office in Mysoft's city.

**Where competitors are weak / white space holds:** unchanged and re-confirmed against
sharper LinkedIn data — named-person / individual-employee presence (company-page reach
−60–66% since 2024; employee posts ~+561% reach-per-post — a penalty Allied is fully exposed
to); authentic shop-floor storytelling; short vertical video / document carousel built for
the 2026 dwell-time feed (carousels the single highest-engagement format, 8–12 slides).
Allied does none of these.

**What competitors tried that flopped:** nothing observable. The standing caution holds:
Allied's buyer-education content is *good* and directly comparable — Mysoft cannot win that
sub-lane by publishing the same thing later; it has to win on shape (named person /
shop-floor story / short-form / Penang-local) or on a sharper problem frame ("can management
verify what actually happened on the floor?", which Allied does not lead with).

### Suggestions to beat them (feed next Research + Prompting)

1. **The logged-in Allied audit is now overdue** — it has been the top open competitor task
   for three runs. LinkedIn `allied-solutions-pte-ltd` + Facebook `alliedsolutionsg`:
   cadence, recency, engagement, format mix, any individual employees posting, any paid ads.
   Everything in "white space holds" above is still public-sources-only.
2. **LI-C1 is approved — treat its production as the immediate next move into the empty
   lane.** It is format white space (no competitor carousel) and problem-frame white space
   (shift-handover / information survival) against Allied. Run it as a company-page asset if
   no person is named; do not let the named-person block stall the carousel itself.
3. **Do not answer Allied's guides (now incl. MES-vs-ERP) with more guides.** If Mysoft
   builds owned buyer-journey content (`current_priorities.md` item 2), differentiate on
   shape or on the verification/reporting-reliability frame — not OEE / ROI / compliance,
   where Allied is already strong and generic.
4. **Keep positioning plain and problem-first** while Allied and the TrakSYS 14 / Parsec
   line lean on "AI-driven optimisation / IIoT / Connected Worker" language — the
   differentiation is partly linguistic; do not chase the AI vocabulary.
5. **Name the founder / technical lead** (`current_priorities.md` item 1). Still the single
   blocker on the whole named-person LinkedIn direction; still an empty lane vs Allied.

### Refinement written to learning_log.md this run

> **REFINEMENT (2026-09-04, third run):** The 2026-09-04 work is now reconciled onto
> `origin/main` and PR #1 is merged (LI-C1 + 5 others APPROVED). Two operating lessons from
> how today went: (1) **the daily run must verify `git status` shows `main` even with
> `origin/main` before doing any research or writing** — three runs today wrote onto a
> diverged branch and none could push, compounding the mess each time; if `main` is not
> a clean fast-forward of `origin/main`, stop and report, do not research. (2) **When an
> approval PR is merged mid-run or between runs, run `apply_prompt_decision` for its post
> ids in that same run and push the status flips** — do not leave approved prompts sitting
> at DRAFT on `main` waiting for the next run's bootstrap. Next run: the logged-in Allied
> social audit is the priority research task; the named-person gate is a yes/no check only.

**Confidence:** LOW-MEDIUM — Allied side is public sources only, no engagement data, single
competitor; Mysoft side has zero first-party data. Nothing here is VALIDATED.

**Needs a logged-in / human pass:** Allied LinkedIn/Facebook cadence, recency, engagement,
format mix; individual Allied employees posting about MES; Allied paid advertising; whether
Allied has appeared in a real Mysoft deal; whether the owner has named a founder / technical
lead; whether Mysoft holds MD status.

---

## 2026-09-04 (second run — competitor-set reset)

> Competitor set was reset this day (owner deleted the prior 14; supplied one replacement).
> This entry compares Mysoft against the **only tracked competitor now: Allied Solutions
> Global / ASPL**. The 2026-09-04 entry below still reflects the retired 14-vendor set and
> is kept for provenance.

### Half 1 — Our performance

No change. No first-party performance data — zero published posts.
`analyze_posting_time_performance` returns nothing for every platform;
`record_post_performance` has no records. Our side is still only plans: the September
LinkedIn text-post cycle, the September Facebook/Instagram Reel calendars, and LI-C1
(carousel test) — all DRAFT / awaiting approval, none published.

### Half 2 — Competitor comparison

| Competitor | What they publish / run | Format & channel | Worked? (evidence) | Recency / cadence |
|---|---|---|---|---|
| **Allied Solutions Global / ASPL** | Sustained plain-language buyer education — full funnel: "What Is an MES System?", "TrakSYS MES Buyer's Guide", "MES Buyer's Guide: How to Choose", "TrakSYS MES Implementation Guide", "MES ROI & Cost / business case", "Web-Based MES", plus "OEE Calculation: worked examples", "What Is OT Cybersecurity? A Plain-English Guide". Executive sharing sessions / webinars (e.g. 8 Jul 2026 with Yonyou Singapore). Trade-show presence: Penang Manufacturing Expo (Jul 2026), Johor Industrial Fair (Aug 2026), both showcasing "Manufacturing Operations & MES". | Long-form articles / downloadable guides on `alliedsolutionsglobal.com/news`; LinkedIn company page (`allied-solutions-pte-ltd`) + Facebook (`alliedsolutionsg`); regional SEO ("Singapore, Malaysia, Vietnam" in titles). No IG / YouTube / TikTok. No short video or carousel found. | **Not measured.** Operation clearly exists and is sustained through 2026 (≈1–3 posts/month by dated titles). No engagement data from public sources. TrakSYS global customer ROI figures on their pages are **vendor claims**, not verified. | Content: roughly monthly, active as of Aug 2026. Social cadence/recency: **needs a logged-in pass.** |

**Where Mysoft is behind:**
- **Published content: everything.** Allied has a complete, connected buyer-journey content
  set live. Mysoft has zero published assets.
- **On Mysoft's own intended register.** Allied's content is plain-language, problem-first,
  worked-example-led — the register Mysoft's positioning aims for. Allied got there first
  and at volume.
- **Same-city presence.** Allied has a Penang office (George Town) in Mysoft's own city, plus
  KL. It is now the primary same-city competitor on file (Critical Manufacturing and
  Sciengate are no longer tracked).

**Where competitors are weak / white space holds:**
- **Named-person presence — still completely empty.** Allied's content is corporate and
  unbylined; no founder or individual employee posts about MES in anything public. The
  −60–66% 2026 company-page reach penalty is one Allied is fully exposed to.
- **Authentic shop-floor storytelling — absent.** Allied explains MES; it does not *show* a
  shift, a floor, a lost job. Its imagery and framing are corporate/technical.
- **Short vertical video / carousel — absent.** Allied is long-form-article and
  webinar-shaped. Nothing built for the 2026 dwell-time feed.
- **Local-language / local-market content — not found.** Allied's content is English and
  regional, not Penang-specific or Bahasa Malaysia.

**What competitors tried that flopped:** nothing observable flopped. Note the opposite risk:
Allied's buyer-education content is *good* and directly comparable to what Mysoft would
write — Mysoft cannot win this sub-lane by doing the same thing later. It has to win on
named-person + authentic + short-form + local, or on a sharper problem frame (reporting
reliability / "can you verify what happened", which Allied does **not** lead with — Allied
leads with OEE, downtime, compliance, ERP-connectivity).

### Suggestions to beat them (feed next Research + Prompting)

1. **Do the logged-in Allied audit next run — it is now the single highest-value competitor
   task.** One competitor, one focused pass: LinkedIn + Facebook cadence, recency,
   engagement, format mix, any individual employees posting, any paid ads. Every "white
   space holds" line above is still public-sources-only, LOW-MEDIUM confidence.
2. **Do not answer Allied's guides with more guides.** Allied owns "explain MES well" for the
   SG/MY/VN region. Mysoft's edge has to be a *different shape*: named person, shop-floor
   story, short-form, Penang-local — or a *different problem frame* (reporting reliability /
   verifiability, which Allied does not lead with).
3. **If Mysoft does build owned buyer-journey content, frame it around the gap Allied
   leaves:** "can management verify what actually happened on the floor?" — not OEE / ROI /
   compliance, where Allied is already strong and generic. Route the build/no-build decision
   to the owner (`current_priorities.md` item 2).
4. **LI-C1 is still the right first move into the empty lane** — carousel format + shift-
   handover story is white space against Allied too. Unchanged. Gated on the owner naming a
   person and approving the format.
5. **Keep positioning plain and problem-first while Allied and the globals lean on "AI /
   IIoT / TrakSYS 14" language** — the differentiation is partly linguistic; do not chase
   the AI vocabulary.

### Refinement written to learning_log.md this run

> **REFINEMENT (2026-09-04, second run):** The named-person LinkedIn dependency is now
> settled and routed (`current_priorities.md` item 1) — the Brain has re-derived it from
> three evidence lines across two runs. Stop re-analysing it. Next cycle, at the Prompting
> gate, only *check whether the owner has answered* (yes/no); do not rebuild the case. Spend
> the freed effort on the **logged-in Allied Solutions Global social audit**, which is now
> the single highest-value competitor task (one tracked competitor, no engagement data yet).
> Also: drop the retired "top 5 competitors" framing from all analysis — the tracked set is
> one until the owner adds another.

**Confidence:** LOW-MEDIUM — Allied side is web-search + vendor-site + directory only, no
engagement data; Mysoft side has zero first-party data. Single competitor, single pass.
Nothing here is VALIDATED.

**Needs a logged-in / human pass:** Allied LinkedIn/Facebook cadence, recency, engagement,
format mix; individual Allied employees posting about MES; Allied paid advertising; whether
Allied has appeared in a real Mysoft deal; whether the owner has named a founder / technical
lead.

---

## 2026-09-04

### Half 1 — Our performance
No first-party performance data yet — zero published posts. `analyze_posting_time_performance`
returns nothing for every platform; `record_post_performance` has no records. Nothing to
compare on our side except plans: the September LinkedIn text-post cycle (counterbalanced
Tue/Thu two-slot design), the September Facebook/Instagram Reel calendars, and the LI-C1
carousel test — all DRAFT / awaiting approval, none published.

### Half 2 — Competitor comparison

| Competitor | What they publish / run | Format & channel | Worked? (evidence) | Recency / cadence |
|---|---|---|---|---|
| Critical Manufacturing (MY) | Enterprise MES positioning; UST partnership announcement (26 Aug 2026) for SEA+India semiconductor/E&E deployment | Press / independent tech media (TechNode) | Announcement got independent pickup | Event-driven, not a content cadence |
| FSBM MES Elite | Institutional credibility (FMM MBP 2.1 partnership, Smart4wrd listing), named SME pricing ("MES Lite" RM28,888) | Parent (FSBM Holdings) LinkedIn; directories | Not measured; not a thought-leadership cadence | Sparse |
| ASPL / Allied Solutions | "AI-driven optimization, IIoT" platform messaging; now a named Siemens FA/Digital partner | Own website; LinkedIn company page | Not measured | Not measured |
| Bizit, Sciengate, YNY, VISI, Blue Ocean, SOFtronix, TNA, Regaltech, XTS, Zoomo | MES is one line in a broader automation/robotics/consulting business; social identity (where any) is built around the parent business, not MES | Mostly Facebook/company pages tied to the non-MES core business | n/a for MES-buyer content | n/a |

**Where Mysoft is behind:** nothing published at all, so behind everyone with an active
channel — ASPL most of all (real multi-channel operation + named case studies +
official-body webinars). Mysoft also cannot yet run its strongest documented format (the
quantified customer case study) because it is pre-customer.

**Where competitors are weak / white space holds:** no tracked Malaysian MES vendor uses
(a) a named founder / technical lead posting consistently on LinkedIn, (b) authentic
shop-floor storytelling, or (c) short vertical video / carousel built for the 2026
dwell-time algorithm. DigiwinSoft occupies "corporate content"; the *authentic, named-person,
short-form* lane is still empty even against them.

**What competitors tried that flopped:** nothing observable flopped — but the "MES as an
afterthought line" pattern (9–10 of 14 vendors) means most competitors are effectively
absent from MES-buyer content and are not a threat for the content audience even where they
compete for the deal. Do not over-index on beating them; the real bar is "start publishing at all."

### Suggestions to beat them (feed next Research + Prompting)
1. **Stand up one named person on LinkedIn before scaling anything else.** The white space
   is specifically *named-person* content; a company page alone concedes the 2026
   reach penalty (−60–66%) and doesn't touch the gap. Blocked on the owner naming a founder
   / technical lead — carry this as the top open dependency.
2. **Ship LI-C1 (carousel) as the first move into the empty lane** — it is format white
   space (no competitor uses carousels) and now correctly sized (9 panels). Treat its
   result as the first read on whether the dwell-time thesis holds for this audience.
3. **Benchmark against ASPL's case-study structure, not their channel mix** — when
   Mysoft has its first customer, the quantified case study is the format to answer their
   vendor-published ones with; until then, use the "one real production problem, no
   product" technical-breakdown format they are *not* doing.
4. **Do the logged-in competitor social audit** — cadence/recency/engagement on the top 5,
   plus any individual employees posting. Every "white space holds" claim above is still
   web-search-only and LOW-MEDIUM confidence.
5. **Keep positioning plain while ASPL and the globals converge on "AI/IIoT" language** —
   the differentiation is now partly linguistic; do not chase the AI vocabulary.

### Refinement written to learning_log.md this run
> **REFINEMENT (2026-09-04):** Before the next Prompting stage, check whether the owner has
> named a founder / technical lead for LinkedIn. The Brain has now recommended "one named
> person posting consistently" from two independent evidence lines (2026-08-31 founder
> thesis; 2026-09-04 employee-advocacy reach data) and the competitor audit shows the lane
> is empty — but every LinkedIn asset stays a company-page asset until that person exists.
> Make "named person: yes/no" an explicit gate at the top of each run's Prompting stage, and
> if still "no", say so in the run summary and route it to `current_priorities.md` rather
> than drafting more company-page LinkedIn content.

**Confidence:** LOW-MEDIUM — competitor side is web-search-only; our side has zero
first-party data. Nothing here is VALIDATED.
**Needs a logged-in / human pass:** competitor post cadence/recency/engagement; individual
employees posting about MES; whether any competitor appears in a real Mysoft deal; whether
Mysoft holds MD status (for SmartMFG+).


---

## 2026-09-04 (fourth run — platform copy-style / audience-age synthesis + Allied comparison)

> This run produced one new reference doc — `03_PLATFORM/copywriting_style_and_audience_age.md`
> (how the copy should sound and which age / seniority band it addresses on each channel) —
> and compares that against the one tracked competitor, Allied Solutions Global / ASPL, on
> **copywriting register and audience targeting** specifically. It is a synthesis pass, no
> new external research.

### Half 1 — Our performance

No change. No first-party performance data — zero published posts.
`analyze_posting_time_performance` returns nothing for every platform;
`record_post_performance` has no records. Approved-for-production (PR #1, merged
2026-09-04): LI-C1, IG-01, IG-02, FB-03, FB-04, IG-04 — none produced, none published, so
nothing to measure. No new generation prompt this run and no approval PR opened (the
synthesis did not open a content opportunity — see `08_DECISIONS/analysis_log.md`).

### Half 2 — Competitor comparison — copywriting style & audience targeting

Only tracked competitor: **Allied Solutions Global / ASPL**. Public sources only; no
logged-in pass (still the top open competitor task, now four runs overdue).

| Dimension | Allied Solutions Global (observed) | Mysoft intended (per Brain) | Read |
|---|---|---|---|
| **Voice / register** | Corporate, unbylined, plain-English explainer. Competent and clear. "Monitor, Control, Optimise" / "One platform, every operations challenge". Increasingly leans on "no-code", "web-native", "AI-driven optimisation", "IIoT". | Plain-spoken, problem-first, shop-floor-colleague tone; deliberately *underplays* the technology (`hook_library.md` — "you don't need a new ERP, you need one clear answer"). | Mysoft's intended voice is **more distinct the more Allied leans on platform/AI vocabulary.** Do not converge on that language. |
| **Audience addressed** | Regional buyer in general — "manufacturers in Singapore, Malaysia, Vietnam". Role-agnostic. Compliance / OEE / ROI framing implies a manager-to-exec reader. | Explicitly role- and age-split by channel (new reference doc): FB = 35+ owners/GMs, Mandarin; LI = under-45 researchers, carousel; IG = younger influencers, visual. | Allied does **not** segment copy by platform or age. That segmentation is open space for Mysoft — if Mysoft actually executes it. |
| **Language** | English only. No Mandarin, no BM, no Penang-local content found. | English + Mandarin (FB), English/BM (IG), Mandarin (XHS white space). | **Mandarin / BM / Penang-local is uncontested.** Allied's KL+Penang offices publish in English only from public sources. |
| **Format range** | Long-form articles + downloadable guides + webinars. No short vertical video, no carousel, no named-person posts. | Short vertical video (FB/IG), 8–12-slide LinkedIn carousel, named-person LinkedIn (blocked on owner). | Format white space holds — carousel and short-form are both empty against Allied. |
| **Funnel coverage** | Complete, connected: what-is-MES → MES-vs-ERP → buyer's guide → how-to-choose → implementation guide → ROI/cost. | Zero published assets. | Allied owns "explain MES well for the region". Mysoft cannot win that by publishing the same later. |

**Where Mysoft is behind:** publishing at all; complete buyer-journey funnel; being first on
the plain-language register in this region.

**Where competitors are weak / white space holds (copy & audience angle):**
1. **Platform- and age-specific copy.** Allied writes one register for one generic buyer.
   Mysoft's new reference doc defines a different voice, format and CTA per channel and age
   band — a real differentiator *if produced*, worthless as a document alone.
2. **Mandarin / Bahasa Malaysia / Penang-local.** Completely uncontested by Allied.
3. **Named-person voice.** Allied is 100% corporate/unbylined and fully exposed to the 2026
   company-page reach penalty (−60–66%; employee posts ~+561%). Still blocked on the owner
   naming a person (`current_priorities.md` item 1).
4. **A sharper problem frame.** Allied leads with OEE / downtime / compliance / ERP-connectivity.
   It does **not** lead with "can management verify what actually happened on the floor?" —
   Mysoft's intended reporting-reliability / verifiability territory (`swot.md` §12, `positioning.md` §32).

**What competitors tried that flopped:** nothing observable. Standing caution unchanged —
Allied's explainer content is genuinely good; Mysoft must win on *shape* (named person /
short-form / carousel / Mandarin / Penang-local) or *problem frame* (verifiability), not by
re-publishing guides.

### Suggestions to beat them (feed next Research + Prompting)

1. **Make the new copy-style / audience-age reference the standing spec for every prompt.**
   Its value is only realised when a caption or a generation prompt is actually written to
   the right voice + age band + CTA friction for its channel. Add it to the Prompting-stage
   read list alongside `build_prompt_context`.
2. **When the FB/IG September Reels are produced, hold the line on the register split:** FB
   copy plain + Mandarin + Click-to-WhatsApp; IG copy minimal + visual-led + save/DM ask;
   never the same caption on both (`brain_rules.md` §7). This is a direct, cheap
   differentiator vs Allied's single-register approach.
3. **Prioritise one Mandarin or Penang-local asset** in the next content cycle — it is the
   most defensible uncontested space and Allied has a Penang office but no local-language
   content on public record.
4. **Logged-in Allied audit is now four runs overdue** — cadence, recency, engagement,
   format mix, individual employees, paid ads on `allied-solutions-pte-ltd` /
   `alliedsolutionsg`. Every "white space holds" line is still public-sources-only.
5. **Name the founder / technical lead** (`current_priorities.md` item 1) — unchanged, still
   the single blocker on the named-person LinkedIn direction and still an empty lane vs Allied.

### Refinement written to learning_log.md this run

> **REFINEMENT (2026-09-04, fourth run):** A per-channel copy-style + audience-age reference
> now exists (`03_PLATFORM/copywriting_style_and_audience_age.md`). From next cycle, the
> Prompting stage must read it before writing any caption or generation prompt, and every
> drafted asset must state, in the prompt file, which platform voice / age band / CTA-friction
> row it is written to — so the evidence-to-creative chain (`daily_operating_spec.md` §9.4)
> includes *audience fit*, not just the derived-from research entry. A prompt that does not
> name its target row is not finished. This does not add a content asset; it tightens how the
> existing prompting gate is run.
> Source: `06_PERFORMANCE/competitive_benchmark.md` 2026-09-04 (fourth run).

**Confidence:** LOW-MEDIUM — Allied side is public sources only, no engagement data, single
competitor; Mysoft side has zero first-party audience or performance data, and the copy-style
reference is entirely external → TESTING. Nothing here is VALIDATED.

**Needs a logged-in / human pass:** Allied LinkedIn/Facebook cadence, recency, engagement,
format mix; individual Allied employees posting about MES; Allied paid advertising; whether
Allied publishes any Mandarin / BM / Penang-local content behind a login; whether the owner
has named a founder / technical lead; Mysoft's own audience age data once a channel produces any.



---

## 2026-09-04 (fifth run — full sweep + strategist brief + Allied comparison)

> This run ran a live web sweep of platform trends / copywriting styles (LinkedIn, Facebook,
> Instagram, Xiaohongshu), the macro (PMI, grants, Budget 2027), and Allied Solutions Global
> (public sources). It produced `08_DECISIONS/strategy_brief_2026-09-04.md` and two new DRAFT
> prompts (LI-C2, FB-05 — approval PR #2). This entry is the Analysis #2 competitor comparison.

### Half 1 — Our performance

No change. `analyze_posting_time_performance` → `record_count: 0`, `can_claim_best_time: false`
for every platform. `record_post_performance` has no records. Zero published posts.
Our side is still all plans: the September LinkedIn text experiment (counterbalanced Tue/Thu),
the September FB/IG Reel calendars, LI-C1 (approved), and now LI-C2 + FB-05 (DRAFT, PR #2) —
none produced, none published.

### Half 2 — Competitor comparison (Allied Solutions Global / ASPL)

Public sources only. Logged-in pass **still outstanding — 5 runs overdue.**

| Dimension | Allied Solutions Global (2026-09-04) | Mysoft (planned pipeline) | Read |
|---|---|---|---|
| Published output | Full buyer-education funnel, now confirmed to include **"MES vs ERP: What's the Difference, and Do You Need Both?"** — one of the highest-volume MES-buyer queries. ~1–3 pieces/month, sustained through 2026. | Zero published. Pipeline: LI-C1, LI-C2, FB-05, September LinkedIn text ×8, FB Reels ×4, IG Reels ×4 — all DRAFT / AWAITING APPROVAL. | Allied owns "explain MES for the region". Mysoft's job is not to race that funnel. |
| Format | Long-form articles + downloadable guides + webinars. No carousel, no short video, no named-person content on public record. | Document carousel (LI-C1, LI-C2), short vertical video (FB/IG Reels). | Format white space holds and is now being built against. |
| Voice / register | Corporate, unbylined. "Monitor, Control, Optimise"; increasingly "no-code / web-native / AI-driven / IIoT". Parsec's new **Connected Worker** (May 2026) adds a "start small → scalable path to full MES" line to the product Allied sells. | Plain, problem-first, shop-floor-colleague; deliberately underplays the tech. | Mysoft's register is *more* distinct as Allied/Parsec lean further into platform/AI language. Hold the line. |
| Problem frame | OEE, downtime, micro-stoppages, compliance, ERP-connectivity. | "Can management verify what actually happened?" / plan vs actual (LI-C2 is exactly this). | Verification frame is white space against Allied's positioning — LI-C2 tests it directly. |
| Language / locality | English only. No Mandarin / BM / Penang-local on public record, despite a Penang office. | Mandarin (FB-05), Penang-local parked. | Uncontested. FB-05 is the first move into it. |
| Named person | None. Fully exposed to the 2026 company-page reach penalty (−60–66%; employee posts ~+561%). | Blocked — owner has not named a person. | Still the single biggest unrealised advantage. |
| Proof | Global TrakSYS logos (vendor proof); vendor ROI figures (claims, not fact). | None — pre-customer. Cannot run the quantified case study. | Mysoft leads with problem + concept, not proof, until an implementation exists. |

**Where Mysoft is behind:** published volume, regional SEO, product maturity/breadth, global
logos, trade-show reach, same-city sales presence. Unchanged.

**Where white space holds (and is now being built against):**
1. LinkedIn document carousel — LI-C1 (shift handover) + LI-C2 (plan vs actual). No Allied carousel.
2. The verification / plan-vs-actual problem frame — LI-C2. Allied leads with OEE.
3. Mandarin / Penang-local — FB-05. Allied publishes English only.
4. Named-person voice — still blocked on the owner.
5. Short vertical video for the 2026 dwell-time / SEO-caption feed — the September Reels.

**What competitors tried that flopped:** nothing observable. Standing caution holds — Allied's
buyer-education content is genuinely good and directly comparable; Mysoft wins on *shape*
(carousel / short-form / Mandarin / named person) and *frame* (verification), not by
publishing the same guides later.

### Suggestions to beat them (feed next Research + Prompting)

1. **Produce LI-C1 and run it inside the September LinkedIn cycle** so its dwell/saves read
   against the text-post median from the same weeks — that comparison is the point.
2. **Hold LI-C2 until LI-C1 has a first read**, then run it — LI-C1 vs LI-C2 tests *frame*
   (shift-handover vs plan-vs-actual) with format held constant. Do not run both cold.
3. **Shoot FB-05 alongside FB-01…04** to keep the first Mandarin asset cheap (lean-team
   constraint). It is the only move into the fully uncontested Mandarin lane.
4. **Do the logged-in Allied audit — now 5 runs overdue.** Everything in the table above on
   Allied's social side is public-sources-only. Cadence, recency, engagement, format mix,
   individual employees, paid ads, any Mandarin/BM/Penang-local behind a login.
5. **Decide REC-6 (website explainer on the verification frame).** Allied's funnel now
   includes MES-vs-ERP; if Mysoft builds owned buyer-education it must be on the verification
   frame and its own register, timed to budget season (9 Oct) as context — not another OEE/ROI guide.
6. **Name the founder / technical lead.** Unchanged. Still the single blocker on the whole
   named-person direction and still an empty lane vs Allied.

### Refinement written to learning_log.md this run

> **REFINEMENT (2026-09-04, fifth run):** The strategist output now lives in a dedicated
> `08_DECISIONS/strategy_brief_YYYY-MM-DD.md` (Research → Meaning → Opportunity/Gap →
> Marketing Decision → Content → Platform/Voice → Timing → Next Research), with
> `analysis_log.md` carrying only the short decision record and pointing to it. From next
> run, Analysis #1 writes the brief in that structure every run (not just the log entry), and
> the Prompting stage executes the brief's Content Recommendation + Platform Strategy + Timing
> sections directly — a prompt must cite which REC number and which platform-voice row it
> comes from. Propose the corresponding `daily_operating_spec.md` §4A wording change in
> `brain_update_proposals.md` (00_SYSTEM is read-only to the run). Also unchanged and carried:
> the logged-in Allied social audit is the top research task (5 runs overdue); the
> named-person gate is a yes/no owner check only.
> Source: `06_PERFORMANCE/competitive_benchmark.md` 2026-09-04 (fifth run).

**Confidence:** LOW-MEDIUM — Allied side is public sources only, no engagement data, single
competitor; Mysoft side has zero first-party data; all platform figures external → TESTING.
Nothing VALIDATED.

**Needs a logged-in / human pass:** Allied LinkedIn (`allied-solutions-pte-ltd`) + Facebook
(`alliedsolutionsg`) cadence / recency / engagement / format mix; individual Allied employees
posting about MES; Allied paid ads; any Mandarin / BM / Penang-local Allied content behind a
login; whether Allied has appeared in a real Mysoft deal; whether the owner has named a
founder / technical lead; whether Mysoft holds MD status.

