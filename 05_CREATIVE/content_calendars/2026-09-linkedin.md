# LinkedIn Content Calendar — September 2026

**Status: AWAITING HUMAN APPROVAL — NOT AUTHORIZED FOR PUBLICATION**
Built: 2026-09-02 | Cycle: 2026-09-07 to 2026-10-04 | Timezone: MYT (UTC+8)
Index: [calendar_index.md](calendar_index.md)

---

## What this file is, and where the copy lives

This is the **schedule and measurement layer**. It decides when each post goes out, to whom, why that slot, and how it will be measured.

The **post copy lives in `05_CREATIVE/linkedin_content_calendar_2026-09.md`**, referenced below by post number. That file was drafted 2026-09-01 and its copy is carried forward unchanged — it is not reproduced here, to avoid two divergent versions of the same text (Primary File Rule, `00_SYSTEM/routing_rules.md`).

**Decision (human, 2026-09-02):** combine the drafted copy with the counterbalanced timing design. 8 of the 12 drafted posts are scheduled below; 3 are parked in `08_DECISIONS/content_backlog.md`; 1 runs outside the experiment.

---

## Why LinkedIn carries the most weight

Per `03_PLATFORM/linkedin.md` (2026-08-31): the primary B2B research channel for industrial buyers, having overtaken trade publications for buyers under 45. Named-person posts reportedly reach 6–10× company-page posts. Highest-performing MES formats are quantified case studies, non-promotional technical breakdowns, and short founder-commentary video.

**We have no customer proof on file**, so the strongest documented format — the quantified case study — is unavailable. Every post below therefore works from a question or a mechanism, never a claimed outcome. That constraint is why the drafted copy's honesty (refusing to promise zero errors, telling Excel users they may not need to change) is an asset rather than a compromise.

---

## Timing — TESTING, not validated

`analyze_posting_time_performance(platform="linkedin")` returned `record_count: 0`, `usable_record_count: 0`, `can_claim_best_time: false`, `best_validated_slot: null`.

**No Mysoft-specific LinkedIn timing evidence exists.** The external sources also disagree with each other, so rather than pick a winner, the disagreement *is* the experiment.

| Slot | Time | External support |
|---|---|---|
| **A** | 09:30 MYT | [PostFast](https://postfa.st/blog/best-time-to-post-on-linkedin), 6 Jun 2026 — Tue–Thu 8–11am, synthesising Buffer (4.8M posts) and Sprout (2.7bn engagements / 436k profiles); tech/SaaS 8–9am. Plus [ZenWeb](https://zenweb.my/blog/best-time-to-post-malaysia/), 20 Aug 2026 — 9–11am Tue–Thu MYT, Malaysian client tracking, sample undisclosed. **Two independent sources converge.** |
| **B** | 13:00 MYT | [Sprout Social](https://sproutsocial.com/insights/best-times-to-post-on-social-media/), 31 Mar 2026 — Mon–Fri 11am–5pm local, from ~2bn engagements across ~307,000 profiles, 27 Nov 2025 – 27 Feb 2026. Global, cross-industry. |

None is B2B-manufacturing-specific. **All slots labelled TESTING.**

## Experiment design

Four posts per slot, and **day-of-week is swapped every week** so time-of-day is not confounded with day-of-week:

- Slot A: Tue W1, Thu W2, Tue W3, Thu W4 → 2 Tuesdays, 2 Thursdays
- Slot B: Thu W1, Tue W2, Thu W3, Tue W4 → 2 Tuesdays, 2 Thursdays

**Voice is counterbalanced too.** Since named-person posts reportedly out-reach company-page posts by 6–10×, an uneven voice split across slots would bias the timing result. Each slot carries exactly 2 founder and 2 company-page posts.

Four posts per slot is exactly the tool's `minimum_sample_size` default. **LinkedIn is designed to reach `can_claim_best_time: true` in one cycle** — the only platform in this cycle that can.

---

## Schedule

| Post ID | Date | Day | Time | Slot | Voice | Audience | Source post | Topic |
|---|---|---|---|---|---|---|---|---|
| LI-01 | 2026-09-08 | Tue | 09:30 | A | Founder | Production Manager | Post 1 | "Where is Job #4471" — report accuracy |
| LI-02 | 2026-09-10 | Thu | 13:00 | B | Company | Operations Manager | Post 4 | Planned vs actual — how many hours until you know |
| LI-03 | 2026-09-15 | Tue | 13:00 | B | Founder | Production Manager | Post 7 | "Excel is enough" — when it is, when it stops |
| LI-04 | 2026-09-17 | Thu | 09:30 | A | Company | General Manager | Post 2 | What is an MES, and why isn't it your ERP |
| LI-05 | 2026-09-22 | Tue | 09:30 | A | Founder | Production Manager | Post 3 | Can a digital system stop false reporting? |
| LI-06 | 2026-09-24 | Thu | 13:00 | B | Company | Operations Manager | Post 8 | What is a Digital Job Traveller |
| LI-07 | 2026-09-29 | Tue | 13:00 | B | Founder | Operations Manager | Post 9 | Why MES projects actually fail |
| LI-08 | 2026-10-01 | Thu | 09:30 | A | Company | General Manager | Post 6 | When a factory needs an MES — and when it doesn't |
| LI-09 | 2026-10-02 | Fri | 13:00 | — | Company | All roles | Post 12 | 5-question self-check — **outside the experiment** |

All of LI-01 to LI-08: objective **Awareness**, confidence **LOW**, status **TEST**.

`build_recommendation_context` returned `maximum_confidence: LOW` and `recommended_action_class: TEST` for production_manager × linkedin, general_manager × linkedin and operations_manager × linkedin alike, with the audience profile and `01_BUSINESS/swot.md` flagged as critical gaps in every case.

### Why LI-09 sits outside the experiment

Post 12 is the only drafted post with a direct CTA — objective Consideration → Enquiry, not Awareness. Including it inside the eight would confound the engagement comparison, since a conversion post has a different engagement profile by design. Running it on the Friday after the cycle closes gives the month a conversion opportunity without corrupting the timing data.

**LI-09 must be excluded from the slot analysis.** Flag it in the `notes` field.

---

## Audience rationale

- **Production Manager (LI-01, 03, 05)** — the Problem Owner who lives the pain daily but per `company_profile.md` §18–19 is typically not the budget holder. Gets problem-recognition and objection-handling, no lead-gen push.
- **Operations Manager (LI-02, 06, 07)** — documented frustration is cross-departmental and coordination-shaped, which suits a written argument. Gets plan-vs-actual, the definitional anchor, and the trust-building failure post.
- **General Manager (LI-04, 08)** — the approver. Both posts target the recorded GM rejection trigger: the belief that existing ERP already provides sufficient visibility.

## Parked, not scheduled

Moved to `08_DECISIONS/content_backlog.md`:

- **Post 5** — IT Manager / integration architecture. Strong post, but IT Manager is outside this cycle's three audiences. Also depends on `products.md` §7 (Digiwin upload mechanism, TO VERIFY).
- **Post 10** — traceability depth, Engineering / Continuous Improvement. Outside this cycle's audiences.
- **Post 11** — Penang / Northern Malaysia local specificity. Strong geographic signal; hold for a cycle with a local or event hook.

---

## Publishing prerequisites

1. **Named person confirmed.** Four posts are founder-voice. Per the platform finding, consistency of the same name matters more than which person. The design depends on this — without it, drop to company-page voice throughout and note that the voice variable is removed.
2. **Clear every `[VERIFY / INSERT REAL FIGURE]` marker** in the source copy before publishing. Do not publish with a placeholder in place.
3. **Claim check** against `01_BUSINESS/products.md` §30–31 for any line not already in the source file.
4. Post 2 and Post 8 are the strongest AEO anchors. Mirror both as glossary entries on the website — LinkedIn posts are only lightly indexed, and per `company_profile.md` §26 the website is the owned source of truth.

## Recording results

`record_post_performance` within 72 hours, then again at day 7.

Required: `platform: "linkedin"`, `audience`, `content_type`, `published_at` (**actual** time, `timezone: "Asia/Kuala_Lumpur"`).
Metrics: `impressions`, `engagements`; `clicks`, `shares`, and any DM or enquiry traced to the post as `leads`.
Notes — mandatory for the experiment to work: slot (`slot_A_0930` / `slot_B_1300`), voice (`founder` / `company_page`), and `excluded_from_slot_analysis` on LI-09.

Watch for comments from Plant Manager / Production Manager / Quality Manager job titles specifically, not raw comment volume — that is the audience-fit signal on LinkedIn.

**Cycle review: 2026-10-08.** Re-run `analyze_posting_time_performance(platform="linkedin")`. With 8 clean records it should return `can_claim_best_time: true` — the first validated timing evidence in the brain. Only then may a slot be written to `06_PERFORMANCE/validated_patterns.md`.
