# Knowledge Update Rules

## General Rules

1. Read the destination file before writing.
2. Update an existing entry instead of duplicating it.
3. Preserve the original fact separately from interpretation and action.
4. Record source, observation date, confidence, and last-checked date when relevant.
5. Never promote one result into a validated rule.

## Routing Updates

- Competitor observation -> individual competitor file.
- Repeated competitor behaviour -> `04_COMPETITORS/competitor_patterns.md`.
- Competitor white space -> `04_COMPETITORS/competitor_gaps.md`.
- Customer conversation -> `07_RESEARCH/customer_insights.md`.
- Sales-team learning -> `01_BUSINESS/sales_insights.md`.
- Individual result -> relevant `06_PERFORMANCE/` file.
- Initial performance interpretation -> `06_PERFORMANCE/learning_log.md`.
- Repeated supported result -> `06_PERFORMANCE/validated_patterns.md`.
- Proposed content -> `08_DECISIONS/recommended_content.md` or `content_backlog.md`.
- Approved action -> `08_DECISIONS/decision_log.md`.
- Contradictory evidence -> retain both claims and lower confidence until resolved.

## Protected Knowledge

Changes to `00_SYSTEM/` and foundational `01_BUSINESS/` knowledge require explicit human instruction or a proposal in `08_DECISIONS/brain_update_proposals.md`.

