# Prompt Library

Store only reviewed prompt examples that demonstrate the desired construction standard.

## Entry Format

- Prompt ID:
- Title:
- Status: DRAFT / APPROVED / RETIRED
- Task type:
- Intended user:
- Required MCP tools:
- Read scope:
- Write scope:
- Protected scope:
- Why this prompt is useful:
- Known limitations:
- Last reviewed:

### Prompt

```text
[Prompt text]
```

## Approved Example — Safe Repository Understanding Audit

- Prompt ID: PRM-2026-0001
- Title: Repository Purpose Audit
- Status: APPROVED
- Task type: Read-only audit
- Intended user: Marketing Brain administrator
- Required MCP tools: `know_yourself`, `build_prompt_context`, `list_docs`, `inspect_doc`, `read_doc`
- Read scope: Active repository files
- Write scope: None
- Protected scope: `00_SYSTEM/`, `01_BUSINESS/`
- Why this prompt is useful: Tests whether the connected LLM understands file purposes without changing the knowledge base.
- Known limitations: Large repositories should be audited folder by folder to avoid tool limits.
- Last reviewed: 2026-09-02

### Prompt

```text
Use the Social Content Engine MCP to explain the purpose of the active Marketing Brain files.

1. Call know_yourself.
2. Call build_prompt_context with task_type="repository_audit".
3. Call list_docs with include_archive=false.
4. Read routing_rules.md, update_rules.md and README.md.
5. Do not write or synchronize anything.
6. Group named competitor profiles under their shared governed purpose rather than reading every profile.
7. Report each folder's purpose, file boundaries, template-only files, overlaps, evidence gaps and confidence.
8. Do not infer a purpose from a filename when the rules or contents do not support it.
```

## Bad Example

```text
Research everything and fill all the files. Push it when finished.
```

Why it is rejected:

- No grounding in 00/01
- No evidence standard
- No routing boundaries
- No overwrite protection
- No distinction between proposals and approved decisions
- No stopping condition
- Unauthorized external synchronization

