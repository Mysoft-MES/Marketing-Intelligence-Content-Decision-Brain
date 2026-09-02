# Prompting Rules

## Purpose

Create prompts that are executable, evidence-aware, safe for the Marketing Brain, and grounded in Mysoft's actual business context.

This file controls prompt construction only. It does not replace the governance in `00_SYSTEM/` or the business truth in `01_BUSINESS/`.

## Mandatory Grounding

Before producing any operational prompt, retrieve the relevant foundations from:

### System governance

- `00_SYSTEM/brain_rules.md`
- `00_SYSTEM/decision_framework.md`
- `00_SYSTEM/evidence_rules.md`
- `00_SYSTEM/routing_rules.md`
- `00_SYSTEM/taxonomy.md`
- `00_SYSTEM/update_rules.md`

### Business foundations

- `01_BUSINESS/company_profile.md`
- `01_BUSINESS/products.md`
- `01_BUSINESS/positioning.md`
- `01_BUSINESS/customer_objections.md`
- `01_BUSINESS/sales_insights.md`
- `01_BUSINESS/swot.md`

Load only the files relevant to the requested task after the mandatory governance layer. Reading these files does not authorize modifying them.

## Protected-Layer Rule

Prompts may read and cite `00_SYSTEM/` and `01_BUSINESS/`, but must treat them as read-only foundations.

If downstream research suggests a change to those folders, the operational prompt must route it through `propose_brain_update`. It must never authorize direct writes to 00 or 01.

## Prompt Construction Checklist

Every operational prompt should define, where relevant:

1. Role
2. Objective
3. Business context to retrieve
4. Required MCP tools and calling order
5. Relevant source files
6. Evidence requirements
7. Writing authorization
8. Protected files
9. Routing rules
10. Output format
11. Stopping conditions
12. Verification and success criteria

## Construction Process

Before writing the prompt, determine:

- What outcome does the human want?
- Is the task read-only, write-enabled, a protected-file proposal, external research, or external synchronization?
- Which business facts from 01 apply?
- Which governance rules from 00 constrain the work?
- Which files under 02–08 may be written?
- What evidence is required?
- What could be overwritten, duplicated, misrouted, or falsely promoted?
- Does the work need phases to avoid tool or context limits?
- How will completion be verified?

## Writing Style

Prompts should:

- Use direct instructions and ordered steps.
- Name exact MCP tools and repository paths.
- Define ambiguous terms.
- Separate requirements from examples.
- State prohibited actions explicitly.
- Explain where results must be stored.
- Require sources, dates, evidence classes, confidence, contradictions, and evidence gaps.
- Break large work into reviewable phases.
- Prevent claims of success without tool confirmation.
- Avoid repeated or decorative instructions.

## Knowledge-Safety Rules

- Preserve existing content.
- Inspect before writing.
- Never enable whole-file overwrite by default.
- Keep facts, insights, recommendations, experiments, results, learnings, validated patterns, and approved decisions separate.
- Populate only fields supported by evidence.
- Leave unknown information unknown.
- Do not turn external research into internal performance or customer evidence.
- Do not treat AI recommendations as approved decisions.
- Do not synchronize to GitHub unless the human explicitly requests and approves it.

## Required Research Metadata

- Source title
- Source URL
- Publication date
- Access date
- Geography
- Evidence type
- Confidence
- Contradicting evidence
- Evidence gaps
- Last checked

## Large-Task Rule

For large tasks:

1. Divide the work into phases.
2. Complete and save one phase at a time.
3. Report files inspected and written.
4. Record unfinished work and evidence gaps.
5. Stop at the defined review boundary.

## Verification Rule

Operational prompts should require appropriate verification, such as:

- Reinspect updated files.
- Confirm SHA-256 changes only where intended.
- Confirm protected files remain unchanged.
- Confirm no duplicate entry was created.
- Confirm sources and dates are recorded.
- Confirm external systems were not modified without approval.

## Anti-Patterns

Do not produce vague prompts such as:

- "Research this topic."
- "Fill every file."
- "Update everything."
- "Use your best judgment."
- "Push it when finished."

These instructions are unsafe unless scope, evidence, routing, permissions, stopping conditions, and verification are defined.

