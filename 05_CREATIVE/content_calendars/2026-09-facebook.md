# Facebook Content Calendar — September 2026

**Status: AWAITING HUMAN APPROVAL — NOT AUTHORIZED FOR PUBLICATION**
Built: 2026-09-02 | Cycle: 2026-09-07 to 2026-10-04 | Timezone: MYT (UTC+8)
Index: [calendar_index.md](calendar_index.md)

---

## Why Facebook carries this audience

Per `03_PLATFORM/facebook.md` (2026-08-31): highest-reach platform in Malaysia, still the top-converting channel for B2B/industrial SME lead-gen, skews 35+ which matches the owner/GM demographic that `01_BUSINESS/company_profile.md` §17 identifies as Final Decision Maker and Budget Owner. Video over static. Click-to-WhatsApp is the current standard CTA. Mandarin creative builds trust with Chinese-Malaysian SME owners.

So Facebook is the only platform in this cycle carrying a direct lead-gen CTA, and the only one leading in Mandarin.

## Timing — TESTING, not validated

`analyze_posting_time_performance(platform="facebook")` returned `record_count: 0`, `can_claim_best_time: false`. **There is no Mysoft-specific Facebook timing evidence.**

Slot: **Tuesday 20:00 MYT**, held constant for all four posts. Constant rather than split because 4 posts across 2 slots gives n=2 each, which validates nothing; one slot at n=4 reaches the minimum sample size and establishes a baseline. The A/B split belongs in cycle 2.

20:00 is where the two external source families overlap:

- [ZenWeb, Best Time to Post in Malaysia](https://zenweb.my/blog/best-time-to-post-malaysia/), 20 Aug 2026 — Facebook 8–10pm Tue–Thu MYT, from the agency's own 2024–2026 Malaysian client tracking. Sample size not disclosed. Malaysia-specific but consumer/SME-skewed. Tier 4–5.
- [Sprout Social, Best Times to Post on Facebook](https://sproutsocial.com/insights/best-times-to-post-on-facebook/), 31 Mar 2026 — Tue/Wed 12–8pm local, from ~2bn engagements across ~307,000 profiles, 27 Nov 2025 – 27 Feb 2026. Global, cross-industry, not B2B manufacturing.

Neither source is B2B-manufacturing-specific. **Label all four as TESTING.**

---

## Schedule

| Post ID | Date | Day | Time (MYT) | Audience | Funnel stage | Confidence | Status |
|---|---|---|---|---|---|---|---|
| FB-01 | 2026-09-08 | Tue | 20:00 | General Manager / Owner | Problem Aware | LOW | TEST |
| FB-02 | 2026-09-15 | Tue | 20:00 | General Manager / Owner | Problem → Solution Aware | LOW | TEST |
| FB-03 | 2026-09-22 | Tue | 20:00 | General Manager / Owner | Problem Aware | LOW | TEST |
| FB-04 | 2026-09-29 | Tue | 20:00 | General Manager / Owner | Problem Aware | LOW | TEST |

Confidence is LOW on all four because `build_recommendation_context(audience="general_manager", platform="facebook")` returned `maximum_confidence: LOW` and `recommended_action_class: TEST`, with `02_AUDIENCE/general_manager.md` and `01_BUSINESS/swot.md` flagged as critical evidence gaps.

---

## FB-01 — 2026-09-08

**Topic:** The 4pm question every boss asks and nobody can answer fast
**Format:** 30–45s vertical Reel, 9:16. Mandarin-first VO, BM/EN subtitles
**Hook:** 「这批货做到哪里了？」— asked on the floor, followed by silence. Hook type: Problem / relatable situation
**CTA:** Click-to-WhatsApp — "Message us"
**Evidence basis:** `05_CREATIVE/hook_library.md` (2026-08-31) established the "where is this job" moment as a candidate angle, sourced from job-shop owner distrust of big-vendor MES/ERP. That entry is a proposed test asset, not an approved one.
**Test metric:** 3-second video retention (primary), reach, WhatsApp conversations initiated
**Review date:** 2026-09-14

## FB-02 — 2026-09-15

**Topic:** Paper Job Traveller vs Digital Job Order — the same job, two records
**Format:** 30–45s Reel, side-by-side split screen
**Hook:** "Same job. Two records. Only one can be checked." Hook type: Comparison
**CTA:** Click-to-WhatsApp — "Message us"
**Evidence basis:** Digital Job Order recording is MYSOFT VERIFIED per `01_BUSINESS/products.md` §5. Safe to demonstrate. Do **not** describe the Digiwin upload mechanism — `products.md` §7 marks the fields, method, architecture and frequency as TO VERIFY.
**Test metric:** 3-second retention, reach, WhatsApp conversations initiated
**Review date:** 2026-09-21

## FB-03 — 2026-09-22

**Topic:** 从经验管理，到数据管理 — before/after on a real floor
**Format:** 30–45s Reel, Mandarin VO, before/after shop floor
**Hook:** 「看不见的损失，才是最昂贵的损失。」Hook type: Fear/Risk
**CTA:** Click-to-WhatsApp — "Message us"
**Evidence basis:** Both lines are existing brand assets per `01_BUSINESS/company_profile.md` §31, which explicitly states their effectiveness has **not** been measured and they should not automatically be used in every campaign. **This post is therefore a message test as much as a timing test.**
**Test metric:** 3-second retention, reach, WhatsApp conversations initiated. Compare engagement against FB-01/02/04 to isolate whether brand-line framing helps or hurts.
**Review date:** 2026-09-28

## FB-04 — 2026-09-29

**Topic:** Can the report be checked? Traceability without blaming anyone
**Format:** 30–45s Reel, calm neutral tone, no dramatisation
**Hook:** "Nobody's lying. The record just can't be checked." Hook type: Contrarian
**CTA:** Click-to-WhatsApp — "Message us"
**Evidence basis:** `01_BUSINESS/positioning.md` §5 permits the "what people say happened vs what the record shows" direction but warns it must not imply employees are dishonest. The hook is written to defuse that read explicitly. Claim safety: do not promise elimination of error — `products.md` §31 prohibits zero-human-error and 100%-accuracy claims.
**Test metric:** 3-second retention, reach, WhatsApp conversations initiated
**Review date:** 2026-10-05

---

## Recording results

Log every post with `record_post_performance` within 72 hours, then again at day 7.

Required: `platform: "facebook"`, `audience: "general_manager"`, `content_type` (consistent labels), `published_at` (**actual** time, `timezone: "Asia/Kuala_Lumpur"`).
Metrics: `reach`, `impressions`, `engagements`; log WhatsApp conversations initiated as `leads`.
Notes: language used, organic vs boosted, and any deviation from the 20:00 slot.

An inaccurate `published_at` silently corrupts the timing analysis. Log the real time, not the planned one.

**Cycle review: 2026-10-08.** Re-run `analyze_posting_time_performance(platform="facebook")` — with 4 clean records the Tuesday 20:00 slot should reach the minimum sample size.
