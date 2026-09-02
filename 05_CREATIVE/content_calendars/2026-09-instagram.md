# Instagram Content Calendar — September 2026

**Status: AWAITING HUMAN APPROVAL — NOT AUTHORIZED FOR PUBLICATION**
Built: 2026-09-02 | Cycle: 2026-09-07 to 2026-10-04 | Timezone: MYT (UTC+8)
Index: [calendar_index.md](calendar_index.md)

---

## Why Instagram stays small

Per `03_PLATFORM/instagram.md` (2026-08-31): Instagram in Malaysia is an extension of the Meta/Reels ecosystem rather than a separate strategy, and should remain a **secondary channel behind Facebook** for Malaysian MES lead-gen. It skews younger and more visual — junior engineers, plant digitalisation champions, younger second-generation SME owners who *influence* MES purchases but don't sign off.

So Instagram gets 4 posts, targets the Production Manager rather than the budget holder, and carries **no hard CTA**.

The opportunity is real though: very little organic MES or industrial-software content exists on Instagram in Malaysia — most local vendors treat it as a contact-info page. That is a genuine content gap, noted as an OBSERVATION rather than a verified competitor audit, since social activity has never been audited for any of the 14 tracked competitors.

Format choice follows the 2026-09-02 entry in the same file: Instagram's algorithm reportedly favours watch-through rate and saves over posting frequency, and a "process breakdown" Reel format is the indicated direction. That source is Tier 4, non-Malaysia, non-MES, single case study — **LOW-MEDIUM confidence, treat as format hypothesis, not proven.**

## Timing — TESTING, not validated

`analyze_posting_time_performance(platform="instagram")` returned `record_count: 0`, `can_claim_best_time: false`. **No Mysoft-specific Instagram timing evidence exists.**

Slot: **Wednesday 20:00 MYT**, where the two source families overlap:

- [Sprout Social, Best Times to Post on Instagram](https://sproutsocial.com/insights/best-times-to-post-on-instagram/), 31 Mar 2026 — Wednesday 12–9pm is the widest weekly peak; weekends and 3–7am worst. ~2bn engagements, ~307,000 profiles, 27 Nov 2025 – 27 Feb 2026. Global, cross-industry.
- [ZenWeb, Best Time to Post in Malaysia](https://zenweb.my/blog/best-time-to-post-malaysia/), 20 Aug 2026 — Instagram 9–11pm Wed–Fri MYT, Malaysian client tracking, sample size undisclosed.

**Label all four as TESTING.**

### Known weakness in this cycle

**Malaysia Day falls on Wednesday 16 September 2026**, displacing the Week 2 slot. IG-02 moves to Thursday 17 September and must be **excluded from the Wednesday-20:00 timing sample** — a public holiday confounds the comparison.

That leaves the Wednesday slot at **n=3 against a minimum sample size of 4. Instagram timing will not validate this cycle.** Stated up front rather than discovered at review. It needs one more cycle.

---

## Schedule

| Post ID | Date | Day | Time (MYT) | Audience | Funnel stage | Confidence | Status |
|---|---|---|---|---|---|---|---|
| IG-01 | 2026-09-09 | Wed | 20:00 | Production Manager | Problem Aware | LOW | TEST |
| IG-02 | 2026-09-17 | **Thu** | 20:00 | Production Manager | Solution Aware | LOW | TEST — excluded from Wed sample |
| IG-03 | 2026-09-23 | Wed | 20:00 | Production Manager | Solution Aware | LOW | TEST |
| IG-04 | 2026-09-30 | Wed | 20:00 | Production Manager | Solution Aware | LOW | TEST |

Confidence is LOW because `build_recommendation_context(audience="production_manager", platform="instagram")` returned `maximum_confidence: LOW`, `recommended_action_class: TEST`, with `02_AUDIENCE/production_manager.md` and `01_BUSINESS/swot.md` as critical gaps.

---

## IG-01 — 2026-09-09

**Topic:** A job passes six stations. Here's where the record breaks.
**Format:** 60–90s process-breakdown Reel, station by station, 9:16
**Hook:** "Six stations. Five handwritten records. One number reaches your office." Hook type: Problem
**CTA:** "Save this if it's your floor." No hard CTA.
**Evidence basis:** The recording chain in `01_BUSINESS/company_profile.md` §20 — shop-floor activity → manual recording → supervisor consolidation → report → management, with gaps between what happened, what was recorded and what was reported.
**Platform adaptation note:** Shares a shoot with FB-01 but is a **different asset** — FB-01 is a 30–45s dramatised single moment ending in a WhatsApp CTA for a decision-maker; this is a 60–90s station-by-station breakdown ending in a save prompt for a practitioner. Identical cross-posting is prohibited by `brain_rules.md` §7.
**Test metric:** Watch-through rate (primary), saves, reach
**Review date:** 2026-09-14

## IG-02 — 2026-09-17 (moved from Wed 16 Sep, Malaysia Day)

**Topic:** What a Digital Job Order screen actually shows
**Format:** 45–60s clean screen recording, no voiceover, text-on-screen
**Hook:** "One job. One screen. Station, operator, timestamp." Hook type: Demonstration
**CTA:** "Save for your next floor walk."
**Evidence basis:** Digital Job Order recording is MYSOFT VERIFIED per `products.md` §5. `03_PLATFORM/instagram.md` names dashboard-UI aesthetic content as an open content gap in Malaysia. Claim safety: show the screen, do not narrate integration — the Digiwin upload mechanism is TO VERIFY per `products.md` §7.
**Test metric:** Watch-through rate, saves
**Note:** `notes` field on the performance record must carry `excluded_from_wed_slot_sample_malaysia_day`.
**Review date:** 2026-09-21

## IG-03 — 2026-09-23

**Topic:** Traceability check, step by step: what happened to one job last Tuesday
**Format:** 60–90s process-breakdown Reel
**Hook:** "Customer asks what happened on job 4471 last Tuesday. Go." Hook type: Scenario
**CTA:** "Save this."
**Evidence basis:** Traceability and production-history questions in `company_profile.md` §4 and §12. Claim safety: a digital record can only trace what it was configured to capture — do not imply total traceability as a checkbox feature.
**Test metric:** Watch-through rate, saves
**Review date:** 2026-09-28

## IG-04 — 2026-09-30

**Topic:** Paperless production: what changes at each station
**Format:** 60–90s process-breakdown Reel
**Hook:** "Station 1: no more clipboard. Here's what replaces it." Hook type: Demonstration
**CTA:** "Save this."
**Evidence basis:** Paperless production is a listed solution area in `company_profile.md` §6 and `products.md` §21. Frame as a more structured, retrievable record — not as paperless for its own sake.
**Test metric:** Watch-through rate, saves
**Review date:** 2026-10-05

---

## Recording results

Log with `record_post_performance` within 72 hours, then again at day 7.

Required: `platform: "instagram"`, `audience: "production_manager"`, `content_type`, `published_at` (**actual** time, `timezone: "Asia/Kuala_Lumpur"`).
Metrics: `impressions`, `reach`, `engagements`, and **`saves`** — saves matter most here per the 2026 algorithm finding.
Notes: format label, and the Malaysia Day exclusion flag on IG-02.

**Cycle review: 2026-10-08.** Instagram will sit at n=3 and stay unvalidated. Expected, not a failure.
