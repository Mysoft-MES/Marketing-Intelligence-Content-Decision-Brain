import os
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import re
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import datetime, date, timedelta, timezone as datetime_timezone
from typing import Optional
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

mcp = FastMCP(
    "Social Content Engine",
    instructions="Before doing any research, prompting, generation, justification, "
                  "or analysis work, always call know_yourself first to load this "
                  "system's identity, rules, and business context. Let it ground "
                  "every decision you make in this session. Before recommending "
                  "content, call build_recommendation_context so audience, platform, "
                  "SWOT, competitor, performance, creative, and priority evidence are "
                  "considered together. Use route_intelligence before saving new "
                  "findings, and never treat an AI recommendation as an approved decision."
                  " For GitHub synchronization, use check_github_connection, then "
                  "preview_github_api_sync, and only call sync_to_github_atomic after "
                  "explicit human confirmation of the preview and remote SHA. Before "
                  "creating an operational prompt, call build_prompt_context and treat "
                  "00_SYSTEM and 01_BUSINESS as read-only grounding."
)

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(WORKSPACE_DIR, ".mcp_data")

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_OWNER = "Mysoft-MES"
REPO_NAME = "Marketing-Intelligence-Content-Decision-Brain"

print(f"DEBUG: GITHUB_TOKEN loaded = {bool(GITHUB_TOKEN)}", file=sys.stderr)

# ----------------- CHANGE TRACKING -----------------

_pending_changes = []  # tracks (action, filepath) since the last sync

PROTECTED_FILES = {
    "00_SYSTEM/brain_rules.md",
    "00_SYSTEM/decision_framework.md",
    "00_SYSTEM/evidence_rules.md",
    "00_SYSTEM/routing_rules.md",
    "00_SYSTEM/taxonomy.md",
    "00_SYSTEM/update_rules.md",
    "01_BUSINESS/company_profile.md",
    "01_BUSINESS/products.md",
    "01_BUSINESS/positioning.md",
    "01_BUSINESS/customer_objections.md",
    "01_BUSINESS/sales_insights.md",
    "01_BUSINESS/swot.md",
}

def _log_change(action: str, filepath: str):
    _pending_changes.append((action, filepath))


def _file_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _audit_mutation(tool: str, filepath: str, action: str, before: str, after: str, approved: bool) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    record = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "tool": tool,
        "filepath": filepath,
        "action": action,
        "before_sha256": _file_hash(before),
        "after_sha256": _file_hash(after),
        "approved": approved,
    }
    with open(os.path.join(DATA_DIR, "audit_log.jsonl"), "a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")


def _is_protected(filepath: str) -> bool:
    return filepath.replace("\\", "/") in PROTECTED_FILES


def _resolve_workspace_path(filepath: str, require_markdown: bool = True) -> str:
    """Resolve a user-supplied relative path and keep it inside this workspace."""
    if not isinstance(filepath, str) or not filepath.strip():
        raise ValueError("A non-empty relative filepath is required.")
    if os.path.isabs(filepath):
        raise ValueError("Absolute paths are not allowed.")
    normalized = os.path.normpath(filepath.strip())
    full_path = os.path.abspath(os.path.join(WORKSPACE_DIR, normalized))
    if os.path.commonpath([WORKSPACE_DIR, full_path]) != WORKSPACE_DIR:
        raise ValueError("The filepath must remain inside the marketing-brain workspace.")
    if require_markdown and not full_path.lower().endswith(".md"):
        raise ValueError("Only Markdown (.md) files are allowed.")
    return full_path


def _relative_path(full_path: str) -> str:
    return os.path.relpath(full_path, WORKSPACE_DIR).replace("\\", "/")


def _read_markdown(filepath: str) -> str:
    full_path = _resolve_workspace_path(filepath)
    if not os.path.exists(full_path):
        return ""
    with open(full_path, "r", encoding="utf-8") as file:
        return file.read()


def _is_placeholder(content: str) -> bool:
    meaningful = content.strip().lower()
    if not meaningful:
        return True
    cleaned_lines = [
        line for line in content.splitlines()
        if "_(placeholder)_" not in line.lower()
        and "not yet populated" not in line.lower()
    ]
    cleaned = "\n".join(cleaned_lines).strip()
    if not cleaned:
        return True
    level_two_headings = re.findall(r"(?m)^##[ \t]+(.+?)\s*$", cleaned)
    if level_two_headings and all(heading.lower().endswith("template") for heading in level_two_headings):
        return True
    nonblank_lines = [line.strip() for line in cleaned.splitlines() if line.strip()]
    table_lines = [line for line in nonblank_lines if line.startswith("|") and line.endswith("|")]
    non_table_body = [line for line in nonblank_lines[1:] if not (line.startswith("|") and line.endswith("|"))]
    if table_lines and len(table_lines) <= 2 and not non_table_body:
        return True
    return False


# ----------------- 1. CORE FILE TOOLS -----------------

@mcp.tool()
def read_doc(filepath: str) -> str:
    """Reads a markdown file from the marketing-brain knowledge base.
    
    Pass the path relative to the repo root, including its folder, e.g.:
      - "01_BUSINESS/company_profile.md"
      - "07_RESEARCH/market_trends.md"
      - "05_CREATIVE/hook_library.md"
    
    If you pass a folder instead of a file, this returns a message telling
    you to use list_docs on that folder first.
    
    Folder structure:
      00_SYSTEM/      - brain rules, decision framework, evidence rules (reference only)
      01_BUSINESS/    - company profile, products, positioning, objections, SWOT (reference only)
      02_AUDIENCE/    - factory owner, production manager, finance manager, audience matrix
      03_PLATFORM/    - facebook, instagram, linkedin, xiaohongshu, reddit, youtube
      04_COMPETITORS/ - competitor index and individual competitor profiles
      05_CREATIVE/    - hook library, video formats, creative rules, winning patterns
      06_PERFORMANCE/ - campaign history, video/ad performance, learning log
      07_RESEARCH/    - trends, government updates, industry news, customer insights
      08_DECISIONS/   - content backlog, current priorities, experiments, decision log
    """
    try:
        full_path = _resolve_workspace_path(filepath)
    except ValueError as error:
        return f"Invalid filepath: {error}"
    if os.path.isdir(full_path):
        return f"{filepath} is a folder, not a file. Use list_docs('{filepath}') to see what's inside it first."
    if not os.path.exists(full_path):
        return f"File {filepath} does not exist yet."
    with open(full_path, "r", encoding="utf-8") as f:
        return f.read()


@mcp.tool()
def write_doc(filepath: str, content: str, overwrite: bool = False, human_approved: bool = False) -> str:
    """Creates a Markdown file and preserves existing files by default.
    
    Pass the path relative to the repo root, including its folder, e.g.:
      - "07_RESEARCH/market_trends.md"
      - "05_CREATIVE/hook_library.md"
    
    Same folder structure as read_doc. IMPORTANT: 00_SYSTEM/ and 01_BUSINESS/ are
    reference material set by the human, not agent output — do not write to these
    folders unless explicitly instructed to update company/business information.
    Freely write to 02_AUDIENCE/ through 08_DECISIONS/.
    
    Set overwrite=True only after reading the current file. Protected files also
    require human_approved=True. For log-style files such as learning_log.md,
    use append_doc instead — write_doc will destroy their history.
    """
    try:
        full_path = _resolve_workspace_path(filepath)
    except ValueError as error:
        return f"Invalid filepath: {error}"
    rel_path = _relative_path(full_path)
    exists = os.path.exists(full_path)
    if exists and not overwrite:
        return f"Refused: {rel_path} already exists. Use append_doc, update_markdown_section, or explicitly set overwrite=True."
    if _is_protected(rel_path) and not human_approved:
        return f"Refused: {rel_path} is protected. Use propose_brain_update or provide explicit human approval."
    before = _read_markdown(rel_path) if exists else ""
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    _log_change("write", rel_path)
    _audit_mutation("write_doc", rel_path, "overwrite" if exists else "create", before, content, human_approved)
    return f"Successfully saved {rel_path} locally."


@mcp.tool()
def append_doc(filepath: str, content: str, add_timestamp: bool = True, human_approved: bool = False) -> str:
    """Appends content to a markdown file, without erasing what's already there.
    
    Use this instead of write_doc for log-style files that should accumulate
    over time, e.g.:
      - "06_PERFORMANCE/learning_log.md"
      - "06_PERFORMANCE/campaign_history.md"
      - "08_DECISIONS/decision_log.md"
    
    Pass the path relative to the repo root, including its folder, same as
    read_doc/write_doc. If the file doesn't exist yet, it will be created.
    
    add_timestamp (default True) prefixes the appended entry with today's date,
    so log entries stay chronologically traceable. Set to False if your content
    already includes its own date/header.
    
    Do not use on 00_SYSTEM/ or 01_BUSINESS/ files — those are reference
    material set by the human, not agent output.
    """
    try:
        full_path = _resolve_workspace_path(filepath)
    except ValueError as error:
        return f"Invalid filepath: {error}"
    rel_path = _relative_path(full_path)
    if _is_protected(rel_path) and not human_approved:
        return f"Refused: {rel_path} is protected. Use propose_brain_update or provide explicit human approval."
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    if add_timestamp:
        entry = f"\n## {datetime.now().strftime('%Y-%m-%d')}\n{content}\n"
    else:
        entry = f"\n{content}\n"

    before = _read_markdown(rel_path)
    with open(full_path, "a", encoding="utf-8") as f:
        f.write(entry)

    _log_change("append", rel_path)
    _audit_mutation("append_doc", rel_path, "append", before, before + entry, human_approved)
    return f"Appended to {rel_path}"


@mcp.tool()
def create_dated_file(folder: str = "07_RESEARCH", content: str = "") -> str:
    """Creates a markdown file named after today's date (day+month, no separator,
    e.g. 29/8/2026 -> 298.md) inside the given folder, with the given content.
    
    Note: this naming scheme can collide across different years or certain
    day/month combinations — consider using write_doc with an explicit
    YYYY-MM-DD filename instead if long-term uniqueness matters."""
    today = date.today()
    filename = f"{today.day}{today.month}.md"
    rel_path = os.path.join(folder, filename)
    try:
        full_path = _resolve_workspace_path(rel_path)
    except ValueError as error:
        return f"Invalid folder: {error}"
    if os.path.exists(full_path):
        return f"Refused: {_relative_path(full_path)} already exists. Use a unique YYYY-MM-DD filename."
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    rel_path_str = rel_path.replace(os.sep, "/")
    _log_change("create", rel_path_str)
    _audit_mutation("create_dated_file", rel_path_str, "create", "", content, False)
    return f"Created dated file: {rel_path_str}"


@mcp.tool()
def list_docs(folder: str = "", include_archive: bool = False) -> str:
    """Lists markdown files in the marketing-brain knowledge base.
    Pass a folder name (e.g. '07_RESEARCH') to list just that folder,
    or leave empty to list the whole structure."""
    try:
        base = _resolve_workspace_path(folder, require_markdown=False) if folder else WORKSPACE_DIR
    except ValueError as error:
        return f"Invalid folder: {error}"
    if not os.path.exists(base):
        return f"Folder {folder} does not exist yet."
    result = []
    for root, dirs, files in os.walk(base):
        if not include_archive:
            dirs[:] = [directory for directory in dirs if directory != "_archive"]
        if ".git" in root or "__pycache__" in root:
            continue
        for file in sorted(files):
            if file.endswith(".md"):
                rel = os.path.relpath(os.path.join(root, file), WORKSPACE_DIR).replace("\\", "/")
                result.append(rel)
    return "\n".join(result) if result else f"No markdown files found in {folder or 'workspace'}."


@mcp.tool()
def update_markdown_section(
    filepath: str,
    section_heading: str,
    content: str,
    expected_file_sha256: Optional[str] = None,
    create_if_missing: bool = False,
    human_approved: bool = False,
) -> str:
    """Updates one Markdown heading section without replacing the rest of the file.

    Pass the heading text without # characters. For concurrency safety, callers may
    provide the SHA-256 returned by inspect_doc. Protected files require explicit
    human approval. Missing headings are not appended unless create_if_missing=True.
    """
    try:
        full_path = _resolve_workspace_path(filepath)
    except ValueError as error:
        return f"Invalid filepath: {error}"
    rel_path = _relative_path(full_path)
    if not os.path.exists(full_path):
        return f"File {rel_path} does not exist."
    if _is_protected(rel_path) and not human_approved:
        return f"Refused: {rel_path} is protected. Use propose_brain_update or provide explicit human approval."
    before = _read_markdown(rel_path)
    current_hash = _file_hash(before)
    if expected_file_sha256 and expected_file_sha256 != current_hash:
        return f"Refused: {rel_path} changed since inspection. Current SHA-256: {current_hash}"
    heading = section_heading.strip().lstrip("#").strip()
    if not heading or not content.strip():
        return "section_heading and content are required."
    pattern = re.compile(
        rf"(?ms)^(?P<marks>#{{1,6}})[ \t]+{re.escape(heading)}[ \t]*\r?\n.*?(?=^(?P=marks)[ \t]+|\Z)"
    )
    match = pattern.search(before)
    if match:
        marks = match.group("marks")
        replacement = f"{marks} {heading}\n\n{content.strip()}\n\n"
        after = before[:match.start()] + replacement + before[match.end():]
        action = "update_section"
    elif create_if_missing:
        after = before.rstrip() + f"\n\n## {heading}\n\n{content.strip()}\n"
        action = "append_section"
    else:
        return f"Section '{heading}' was not found in {rel_path}. No changes made."
    with open(full_path, "w", encoding="utf-8") as file:
        file.write(after)
    _log_change(action, rel_path)
    _audit_mutation("update_markdown_section", rel_path, action, before, after, human_approved)
    return f"Updated section '{heading}' in {rel_path}. New SHA-256: {_file_hash(after)}"


@mcp.tool()
def inspect_doc(filepath: str) -> str:
    """Returns document metadata, headings, placeholder status, and a concurrency hash."""
    try:
        full_path = _resolve_workspace_path(filepath)
    except ValueError as error:
        return json.dumps({"error": str(error)}, indent=2)
    rel_path = _relative_path(full_path)
    if not os.path.exists(full_path):
        return json.dumps({"filepath": rel_path, "exists": False}, indent=2)
    content = _read_markdown(rel_path)
    headings = re.findall(r"(?m)^(#{1,6})[ \t]+(.+?)\s*$", content)
    return json.dumps({
        "filepath": rel_path,
        "exists": True,
        "protected": _is_protected(rel_path),
        "placeholder": _is_placeholder(content),
        "characters": len(content),
        "lines": len(content.splitlines()),
        "sha256": _file_hash(content),
        "headings": [{"level": len(marks), "text": text} for marks, text in headings],
        "modified_at": datetime.fromtimestamp(os.path.getmtime(full_path)).isoformat(timespec="seconds"),
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def search_knowledge(query: str, folder: str = "", limit: int = 10, include_archive: bool = False) -> str:
    """Searches Markdown knowledge and returns compact, source-linked excerpts."""
    if not query.strip():
        return json.dumps({"error": "query is required"}, indent=2)
    try:
        base = _resolve_workspace_path(folder, require_markdown=False) if folder else WORKSPACE_DIR
    except ValueError as error:
        return json.dumps({"error": str(error)}, indent=2)
    safe_limit = max(1, min(limit, 50))
    needle = query.strip().lower()
    results = []
    for root, dirs, files in os.walk(base):
        excluded = {".git", ".mcp_data", "__pycache__"}
        if not include_archive:
            excluded.add("_archive")
        dirs[:] = [directory for directory in dirs if directory not in excluded]
        for filename in sorted(files):
            if not filename.endswith(".md"):
                continue
            full_path = os.path.join(root, filename)
            with open(full_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
            for line_number, line in enumerate(lines, start=1):
                if needle in line.lower():
                    start = max(0, line_number - 2)
                    end = min(len(lines), line_number + 1)
                    results.append({
                        "filepath": _relative_path(full_path),
                        "line": line_number,
                        "excerpt": " ".join(part.strip() for part in lines[start:end] if part.strip())[:500],
                    })
                    if len(results) >= safe_limit:
                        return json.dumps({"query": query, "results": results, "truncated": True}, ensure_ascii=False, indent=2)
    return json.dumps({"query": query, "results": results, "truncated": False}, ensure_ascii=False, indent=2)


@mcp.tool()
def find_knowledge_conflicts(topic: str, limit: int = 50, include_archive: bool = False) -> str:
    """Collects topic passages carrying potentially conflicting status language.

    This is a triage tool, not an automatic truth judge. The connected LLM must
    compare dates, sources, evidence classes, and context before concluding that
    two passages genuinely contradict each other.
    """
    if not topic.strip():
        return json.dumps({"error": "topic is required"}, indent=2)
    status_terms = {
        "verified": ["verified", "confirmed", "validated", "winning", "approved", "active"],
        "uncertain": ["to verify", "unverified", "hypothesis", "assumption", "low confidence", "unknown"],
        "negative": ["excluded", "rejected", "losing", "outdated", "incorrect", "not a competitor"],
    }
    matches = []
    topic_key = topic.lower()
    for root, dirs, files in os.walk(WORKSPACE_DIR):
        excluded = {".git", ".mcp_data", "__pycache__"}
        if not include_archive:
            excluded.add("_archive")
        dirs[:] = [directory for directory in dirs if directory not in excluded]
        for filename in files:
            if not filename.endswith(".md"):
                continue
            full_path = os.path.join(root, filename)
            with open(full_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
            for index, line in enumerate(lines):
                if topic_key not in line.lower():
                    continue
                start = max(0, index - 2)
                end = min(len(lines), index + 3)
                excerpt = " ".join(part.strip() for part in lines[start:end] if part.strip())
                labels = [
                    label for label, terms in status_terms.items()
                    if any(term in excerpt.lower() for term in terms)
                ]
                matches.append({
                    "filepath": _relative_path(full_path),
                    "line": index + 1,
                    "status_signals": labels or ["neutral"],
                    "excerpt": excerpt[:700],
                })
                if len(matches) >= max(1, min(limit, 200)):
                    break
    present_categories = sorted({label for match in matches for label in match["status_signals"] if label != "neutral"})
    return json.dumps({
        "topic": topic,
        "possible_conflict": len(present_categories) > 1,
        "status_categories_present": present_categories,
        "matches": matches,
        "instruction": "Review source quality and dates; mixed labels are a review signal, not proof of contradiction."
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def audit_knowledge_freshness(folder: str = "", maximum_age_days: int = 90, include_archive: bool = False) -> str:
    """Finds placeholder files and Markdown files with missing or stale YYYY-MM-DD dates."""
    try:
        base = _resolve_workspace_path(folder, require_markdown=False) if folder else WORKSPACE_DIR
    except ValueError as error:
        return json.dumps({"error": str(error)}, indent=2)
    today = date.today()
    stale = []
    missing_dates = []
    placeholders = []
    for root, dirs, files in os.walk(base):
        excluded = {".git", ".mcp_data", "__pycache__"}
        if not include_archive:
            excluded.add("_archive")
        dirs[:] = [directory for directory in dirs if directory not in excluded]
        for filename in files:
            if not filename.endswith(".md"):
                continue
            full_path = os.path.join(root, filename)
            rel_path = _relative_path(full_path)
            content = _read_markdown(rel_path)
            if _is_placeholder(content):
                placeholders.append(rel_path)
            parsed_dates = []
            for value in re.findall(r"\b(20\d{2}-\d{2}-\d{2})\b", content):
                try:
                    parsed_dates.append(datetime.strptime(value, "%Y-%m-%d").date())
                except ValueError:
                    continue
            if not parsed_dates:
                missing_dates.append(rel_path)
            else:
                latest = max(parsed_dates)
                age = (today - latest).days
                if age > maximum_age_days:
                    stale.append({"filepath": rel_path, "latest_date": str(latest), "age_days": age})
    return json.dumps({
        "maximum_age_days": maximum_age_days,
        "placeholder_files": sorted(placeholders),
        "files_without_parseable_dates": sorted(missing_dates),
        "stale_files": sorted(stale, key=lambda item: item["age_days"], reverse=True),
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def health_check(include_git: bool = False) -> str:
    """Runs a fast repository health check.

    Git inspection is disabled by default because credential helpers, file locks,
    or large worktrees can block inside some MCP hosts. Set include_git=True only
    when needed; that optional check has a short timeout and returns a summary.
    """
    required = [
        "00_SYSTEM/brain_rules.md", "00_SYSTEM/decision_framework.md", "00_SYSTEM/evidence_rules.md",
        "00_SYSTEM/routing_rules.md", "00_SYSTEM/taxonomy.md", "00_SYSTEM/update_rules.md",
        "01_BUSINESS/company_profile.md", "01_BUSINESS/products.md", "01_BUSINESS/positioning.md",
        "01_BUSINESS/swot.md", "02_AUDIENCE/audience_index.md", "03_PLATFORM/platform_index.md",
        "04_COMPETITORS/competitor_index.md", "04_COMPETITORS/competitor_patterns.md",
        "05_CREATIVE/creative_strategy.md", "06_PERFORMANCE/performance_framework.md",
        "07_RESEARCH/research_index.md", "08_DECISIONS/recommended_content.md",
    ]
    missing = [filepath for filepath in required if not os.path.exists(_resolve_workspace_path(filepath))]
    placeholders = [filepath for filepath in required if filepath not in missing and _is_placeholder(_read_markdown(filepath))]
    git_summary = {"checked": False, "state": "NOT_CHECKED", "changed_file_count": None}
    if include_git:
        try:
            status = subprocess.run(
                ["git", "status", "--porcelain=v1", "--untracked-files=normal"],
                cwd=WORKSPACE_DIR, capture_output=True, text=True, timeout=3, check=False
            )
            changed_lines = [line for line in status.stdout.splitlines() if line.strip()]
            git_summary = {
                "checked": True,
                "state": "DIRTY" if changed_lines else "CLEAN",
                "changed_file_count": len(changed_lines),
                "changed_files_preview": [line[3:].replace("\\", "/") for line in changed_lines[:25]],
                "truncated": len(changed_lines) > 25,
                "return_code": status.returncode,
            }
        except subprocess.TimeoutExpired:
            git_summary = {"checked": True, "state": "TIMED_OUT", "changed_file_count": None}
        except OSError as error:
            git_summary = {"checked": True, "state": "UNAVAILABLE", "error": str(error)}
    audit_path = os.path.join(DATA_DIR, "audit_log.jsonl")
    sync_log_path = os.path.join(DATA_DIR, "sync_log.jsonl")
    last_sync = None
    if os.path.exists(sync_log_path):
        with open(sync_log_path, "r", encoding="utf-8") as file:
            sync_lines = [line.strip() for line in file if line.strip()]
        if sync_lines:
            try:
                last_sync = json.loads(sync_lines[-1])
            except json.JSONDecodeError:
                last_sync = {"status": "unreadable"}
    return json.dumps({
        "status": "OK" if not missing else "INCOMPLETE",
        "missing_required_files": missing,
        "placeholder_required_files": placeholders,
        "github_token_configured": bool(GITHUB_TOKEN),
        "github_token_value_exposed": False,
        "git_worktree": git_summary,
        "git_guidance": "Use health_check(include_git=true) or sync_changed_files_to_github(dry_run=true) for Git details.",
        "audit_log_exists": os.path.exists(audit_path),
        "last_successful_sync": last_sync,
        "pending_mcp_changes": _pending_changes,
    }, ensure_ascii=False, indent=2)


# ----------------- 2. IDENTITY TOOL -----------------

@mcp.tool()
def know_yourself() -> str:
    """Reads and returns the core identity, rules, and business context that
    should ground every task. Call this FIRST, before doing any research,
    prompting, or analysis work, so your decisions are grounded in who this
    system is and what it's for."""
    files = [
        "00_SYSTEM/brain_rules.md",
        "00_SYSTEM/decision_framework.md",
        "00_SYSTEM/evidence_rules.md",
        "00_SYSTEM/routing_rules.md",
        "00_SYSTEM/taxonomy.md",
        "00_SYSTEM/update_rules.md",
        "01_BUSINESS/company_profile.md",
        "05_CREATIVE/prompting_rules.md"
    ]
    combined = []
    for f in files:
        full_path = _resolve_workspace_path(f)
        if os.path.exists(full_path):
            with open(full_path, "r", encoding="utf-8") as file:
                combined.append(f"--- {f} ---\n{file.read()}")
        else:
            combined.append(f"--- {f} ---\n(not yet created)")
    return "\n\n".join(combined)


# ----------------- 3. PLATFORM RESEARCH TOOL -----------------

@mcp.tool()
def write_platform_findings(findings: dict) -> str:
    """Writes research findings to their matching platform file in one call.
    
    Pass a dict where each key is a platform name and each value is the
    findings text for that platform, e.g.:
      {"facebook": "...", "instagram": "...", "reddit": "..."}
    
    Valid keys: facebook, instagram, linkedin, xiaohongshu, reddit, youtube.
    Each entry gets appended (with today's date) to its matching file in
    03_PLATFORM/. Invalid platform names are skipped and reported.
    """
    valid_platforms = {"facebook", "instagram", "linkedin", "xiaohongshu", "reddit", "youtube"}
    written = []
    skipped = []
    today = datetime.now().strftime("%Y-%m-%d")

    for platform, content in findings.items():
        key = platform.lower().strip()
        if key not in valid_platforms:
            skipped.append(platform)
            continue
        filepath = f"03_PLATFORM/{key}.md"
        full_path = os.path.join(WORKSPACE_DIR, filepath)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "a", encoding="utf-8") as f:
            f.write(f"\n## {today}\n{content}\n")
        _log_change("append", filepath)
        written.append(filepath)

    result = f"Written to: {', '.join(written)}"
    if skipped:
        result += f"\n(Skipped unrecognized platforms: {', '.join(skipped)})"
    return result


# ----------------- 4. BRAIN UPDATE PROPOSAL TOOL -----------------

@mcp.tool()
def propose_brain_update(target_file: str, proposed_change: str, reasoning: str) -> str:
    """Proposes a change to a core identity/business file (00_SYSTEM/ or 01_BUSINESS/)
    WITHOUT applying it. Writes the proposal to 08_DECISIONS/brain_update_proposals.md
    for human review. Never edits 00_SYSTEM/ or 01_BUSINESS/ directly."""
    if not (target_file.startswith("00_SYSTEM/") or target_file.startswith("01_BUSINESS/")):
        return "This tool is only for proposing changes to 00_SYSTEM/ or 01_BUSINESS/ files."

    entry = (f"\n## Proposed update to {target_file}\n"
             f"**Reasoning:** {reasoning}\n\n"
             f"**Proposed change:**\n{proposed_change}\n")
    filepath = "08_DECISIONS/brain_update_proposals.md"
    full_path = os.path.join(WORKSPACE_DIR, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "a", encoding="utf-8") as f:
        f.write(entry)
    _log_change("propose", filepath)
    return f"Proposal logged to {filepath}. This does NOT modify {target_file} — review and apply manually if you agree."


# ----------------- 5. REPO SCAFFOLDING TOOL -----------------

@mcp.tool()
def scaffold_repo_structure() -> str:
    """Creates the standard marketing-brain folders (02_AUDIENCE through 08_DECISIONS)
    with placeholder markdown files, without touching 00_SYSTEM or 01_BUSINESS."""
    structure = {
        "02_AUDIENCE": [
            "audience_index.md", "audience_matrix.md", "factory_owner.md", "finance_manager.md",
            "general_manager.md", "it_manager.md", "operations_manager.md",
            "production_manager.md", "supply_chain_planner.md"
        ],
        "03_PLATFORM": [
            "platform_index.md", "facebook.md", "google_business.md", "instagram.md",
            "linkedin.md", "reddit.md", "website.md", "whatsapp.md", "xiaohongshu.md", "youtube.md"
        ],
        "04_COMPETITORS": [
            "competitor_index.md", "competitor_template.md", "competitor_patterns.md", "competitor_gaps.md"
        ],
        "05_CREATIVE": [
            "creative_strategy.md", "creative_rules.md", "hook_library.md", "video_formats.md",
            "storytelling_patterns.md", "winning_patterns.md", "losing_patterns.md", "creative_experiments.md",
            "prompting_rules.md", "prompt_templates.md", "prompt_library.md"
        ],
        "06_PERFORMANCE": [
            "performance_framework.md", "content_performance.md", "video_performance.md",
            "ad_performance.md", "campaign_history.md", "learning_log.md", "validated_patterns.md"
        ],
        "07_RESEARCH": [
            "research_index.md", "market_trends.md", "social_trends.md", "search_trends.md",
            "industry_news.md", "government_updates.md", "customer_insights.md", "competitor_updates.md"
        ],
        "08_DECISIONS": [
            "current_priorities.md", "content_backlog.md", "recommended_content.md",
            "experiments.md", "decision_log.md", "rejected_ideas.md", "brain_update_proposals.md"
        ],
    }
    created = []
    for folder, files in structure.items():
        folder_path = os.path.join(WORKSPACE_DIR, folder)
        os.makedirs(folder_path, exist_ok=True)
        for fname in files:
            fpath = os.path.join(folder_path, fname)
            if not os.path.exists(fpath):
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(f"# {fname.replace('.md','').replace('_',' ').title()}\n\n_(placeholder)_\n")
                created.append(f"{folder}/{fname}")
    return f"Created {len(created)} new files: {', '.join(created)}" if created else "All folders/files already exist."


# ----------------- 6. INTELLIGENCE ROUTING -----------------

INTELLIGENCE_ROUTES = {
    "platform_finding": "03_PLATFORM/{platform}.md",
    "competitor_observation": "04_COMPETITORS/{competitor}.md",
    "competitor_pattern": "04_COMPETITORS/competitor_patterns.md",
    "competitor_gap": "04_COMPETITORS/competitor_gaps.md",
    "creative_hook": "05_CREATIVE/hook_library.md",
    "creative_pattern": "05_CREATIVE/winning_patterns.md",
    "video_result": "06_PERFORMANCE/video_performance.md",
    "content_result": "06_PERFORMANCE/content_performance.md",
    "ad_result": "06_PERFORMANCE/ad_performance.md",
    "performance_learning": "06_PERFORMANCE/learning_log.md",
    "validated_pattern": "06_PERFORMANCE/validated_patterns.md",
    "market_research": "07_RESEARCH/market_trends.md",
    "social_research": "07_RESEARCH/social_trends.md",
    "search_research": "07_RESEARCH/search_trends.md",
    "industry_news": "07_RESEARCH/industry_news.md",
    "government_update": "07_RESEARCH/government_updates.md",
    "customer_insight": "07_RESEARCH/customer_insights.md",
    "content_idea": "08_DECISIONS/content_backlog.md",
    "content_recommendation": "08_DECISIONS/recommended_content.md",
    "experiment": "08_DECISIONS/experiments.md",
    "approved_decision": "08_DECISIONS/decision_log.md",
    "rejected_idea": "08_DECISIONS/rejected_ideas.md",
}

VALID_PLATFORMS = {
    "facebook", "instagram", "linkedin", "xiaohongshu", "reddit", "youtube",
    "website", "google_business", "whatsapp"
}


def _safe_slug(value: str, field_name: str) -> str:
    slug = value.strip().lower().replace(" ", "-").replace("_", "-")
    if not slug or any(character not in "abcdefghijklmnopqrstuvwxyz0123456789-" for character in slug):
        raise ValueError(f"{field_name} must contain only letters, numbers, spaces, underscores, or hyphens.")
    return slug


def _route_destination(
    intelligence_type: str,
    platform: Optional[str] = None,
    competitor: Optional[str] = None,
) -> str:
    route = INTELLIGENCE_ROUTES.get(intelligence_type.strip().lower())
    if not route:
        valid = ", ".join(sorted(INTELLIGENCE_ROUTES))
        raise ValueError(f"Unknown intelligence_type. Valid values: {valid}")
    if "{platform}" in route:
        if not platform:
            raise ValueError("platform is required for platform_finding.")
        platform_key = platform.strip().lower().replace(" ", "_").replace("-", "_")
        if platform_key not in VALID_PLATFORMS:
            raise ValueError(f"Unsupported platform: {platform}")
        route = route.format(platform=platform_key)
    if "{competitor}" in route:
        if not competitor:
            raise ValueError("competitor is required for competitor_observation.")
        route = route.format(competitor=_safe_slug(competitor, "competitor"))
    _resolve_workspace_path(route)
    return route


@mcp.tool()
def route_intelligence(
    intelligence_type: str,
    platform: Optional[str] = None,
    competitor: Optional[str] = None,
) -> str:
    """Returns the primary Markdown destination for a finding without writing it.

    Use this before saving research. It separates source facts from performance
    learnings, recommendations, experiments, and approved human decisions.
    """
    try:
        destination = _route_destination(intelligence_type, platform, competitor)
    except ValueError as error:
        return json.dumps({"error": str(error)}, ensure_ascii=False, indent=2)

    secondary = None
    if intelligence_type == "competitor_observation" and platform:
        secondary = f"03_PLATFORM/{platform.strip().lower()}.md (strategic platform implication only)"
    return json.dumps({
        "destination": destination,
        "write_mode": "append",
        "reason": "This is the primary home defined by the Marketing Brain taxonomy.",
        "possible_secondary_file": secondary,
        "rule": "Store the original fact once; put only its strategic implication in a secondary file."
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def save_intelligence(
    intelligence_type: str,
    title: str,
    content: str,
    platform: Optional[str] = None,
    competitor: Optional[str] = None,
    source: Optional[str] = None,
    observed_at: Optional[str] = None,
    confidence: str = "LOW",
    evidence_type: str = "AI INFERENCE",
) -> str:
    """Appends a structured intelligence entry to its server-controlled destination.

    This tool never overwrites an existing file. Use approved_decision only after
    explicit human approval. Core 00_SYSTEM and 01_BUSINESS files are intentionally
    excluded; propose their changes with propose_brain_update instead.
    """
    if not title.strip() or not content.strip():
        return "title and content are required."
    confidence_key = confidence.strip().upper()
    if confidence_key not in {"LOW", "MEDIUM", "HIGH"}:
        return "confidence must be LOW, MEDIUM, or HIGH."
    if intelligence_type.strip().lower() == "approved_decision" and evidence_type.strip().upper() == "AI INFERENCE":
        return "Refused: an AI inference cannot be saved as an approved decision without explicit human approval evidence."
    try:
        destination = _route_destination(intelligence_type, platform, competitor)
        full_path = _resolve_workspace_path(destination)
    except ValueError as error:
        return f"Routing error: {error}"

    observation_date = observed_at or datetime.now().strftime("%Y-%m-%d")
    entry = (
        f"\n## {title.strip()}\n\n"
        f"- Date observed: {observation_date}\n"
        f"- Evidence type: {evidence_type.strip().upper()}\n"
        f"- Confidence: {confidence_key}\n"
        f"- Source: {source or 'Not provided'}\n"
        f"- Platform: {platform or 'Not applicable'}\n"
        f"- Competitor: {competitor or 'Not applicable'}\n\n"
        f"{content.strip()}\n"
    )
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    existing_content = _read_markdown(destination)
    if title.strip().lower() in existing_content.lower() and content.strip().lower() in existing_content.lower():
        return f"No change: an identical titled entry already exists in {destination}."
    with open(full_path, "a", encoding="utf-8") as file:
        file.write(entry)
    _log_change("append", destination)
    _audit_mutation("save_intelligence", destination, "append", existing_content, existing_content + entry, False)
    return f"Appended structured intelligence to {destination}. Existing content was preserved."


# ----------------- 7. STRUCTURED PERFORMANCE AND EXPERIMENTS -----------------

def _data_path(filename: str) -> str:
    os.makedirs(DATA_DIR, exist_ok=True)
    return os.path.join(DATA_DIR, filename)


def _append_jsonl(filename: str, record: dict) -> None:
    with open(_data_path(filename), "a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")


def _read_jsonl(filename: str) -> list:
    path = _data_path(filename)
    if not os.path.exists(path):
        return []
    records = []
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records


def _next_id(prefix: str, records: list) -> str:
    year = datetime.now().year
    sequence = 1
    pattern = re.compile(rf"^{re.escape(prefix)}-{year}-(\d+)$")
    for record in records:
        match = pattern.match(str(record.get("id", "")))
        if match:
            sequence = max(sequence, int(match.group(1)) + 1)
    return f"{prefix}-{year}-{sequence:04d}"


def _resolve_timezone(timezone_name: str):
    if timezone_name == "Asia/Kuala_Lumpur":
        return datetime_timezone(timedelta(hours=8), name="MYT")
    if timezone_name in {"UTC", "Etc/UTC"}:
        return datetime_timezone.utc
    try:
        return ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError as error:
        raise ValueError(f"Unknown IANA timezone: {timezone_name}") from error


def _publication_fields(published_at: str, timezone_name: str) -> dict:
    """Normalize a publication timestamp and derive local scheduling dimensions."""
    if not published_at or not published_at.strip():
        raise ValueError("published_at is required and must be an ISO 8601 timestamp.")
    local_zone = _resolve_timezone(timezone_name)
    try:
        parsed = datetime.fromisoformat(published_at.strip().replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError("published_at must use ISO 8601, for example 2026-09-09T16:00:00+08:00.") from error
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=local_zone)
    local_time = parsed.astimezone(local_zone)
    return {
        "published_at": local_time.isoformat(timespec="seconds"),
        "timezone": timezone_name,
        "day_of_week": local_time.strftime("%A"),
        "hour_local": local_time.hour,
        "date_local": local_time.date().isoformat(),
    }


def _numeric_average(records: list, metric: str) -> Optional[float]:
    values = [record.get(metric) for record in records if isinstance(record.get(metric), (int, float))]
    return sum(values) / len(values) if values else None


@mcp.tool()
def record_video_performance(
    platform: str,
    audience: str,
    objective: str,
    hook: str,
    hook_type: str,
    format: str,
    duration_seconds: float,
    video_id: Optional[str] = None,
    published_at: Optional[str] = None,
    funnel_stage: Optional[str] = None,
    pain_point: Optional[str] = None,
    opening_visual: Optional[str] = None,
    story_structure: Optional[str] = None,
    cta: Optional[str] = None,
    views: Optional[float] = None,
    reach: Optional[float] = None,
    three_second_retention: Optional[float] = None,
    average_watch_time: Optional[float] = None,
    completion_rate: Optional[float] = None,
    shares: Optional[float] = None,
    saves: Optional[float] = None,
    clicks: Optional[float] = None,
    leads: Optional[float] = None,
    demo_bookings: Optional[float] = None,
    sales: Optional[float] = None,
    spend: Optional[float] = None,
    notes: Optional[str] = None,
    timezone: str = "Asia/Kuala_Lumpur",
) -> str:
    """Appends one structured video result without modifying prior records."""
    records = _read_jsonl("video_performance.jsonl")
    record_id = video_id or _next_id("VID", records)
    if any(record.get("id") == record_id for record in records):
        return f"Refused: video ID {record_id} already exists."
    try:
        publication = _publication_fields(published_at, timezone) if published_at else {
            "published_at": None, "timezone": timezone, "day_of_week": None,
            "hour_local": None, "date_local": None,
        }
    except ValueError as error:
        return json.dumps({"saved": False, "error": str(error)}, ensure_ascii=False, indent=2)
    record = {
        "id": record_id,
        "recorded_at": datetime.now().isoformat(timespec="seconds"),
        **publication,
        "platform": platform,
        "audience": audience,
        "objective": objective,
        "funnel_stage": funnel_stage,
        "hook": hook,
        "hook_type": hook_type,
        "opening_visual": opening_visual,
        "pain_point": pain_point,
        "format": format,
        "duration_seconds": duration_seconds,
        "story_structure": story_structure,
        "cta": cta,
        "views": views,
        "reach": reach,
        "three_second_retention": three_second_retention,
        "average_watch_time": average_watch_time,
        "completion_rate": completion_rate,
        "shares": shares,
        "saves": saves,
        "clicks": clicks,
        "leads": leads,
        "demo_bookings": demo_bookings,
        "sales": sales,
        "spend": spend,
        "notes": notes,
    }
    _append_jsonl("video_performance.jsonl", record)
    return json.dumps({"saved": True, "video_id": record_id, "record": record}, ensure_ascii=False, indent=2)


@mcp.tool()
def query_video_performance(
    platform: Optional[str] = None,
    audience: Optional[str] = None,
    hook_type: Optional[str] = None,
    format: Optional[str] = None,
    limit: int = 50,
) -> str:
    """Filters structured video results and reports cautious aggregate averages."""
    records = _read_jsonl("video_performance.jsonl")
    filters = {"platform": platform, "audience": audience, "hook_type": hook_type, "format": format}
    for key, value in filters.items():
        if value:
            records = [record for record in records if str(record.get(key, "")).lower() == value.lower()]
    records = records[-max(1, min(limit, 500)):]
    metric_names = [
        "views", "reach", "three_second_retention", "average_watch_time", "completion_rate",
        "shares", "saves", "clicks", "leads", "demo_bookings", "sales", "spend"
    ]
    averages = {}
    sample_sizes = {}
    for metric in metric_names:
        values = [record[metric] for record in records if isinstance(record.get(metric), (int, float))]
        averages[metric] = sum(values) / len(values) if values else None
        sample_sizes[metric] = len(values)
    return json.dumps({
        "filters": {key: value for key, value in filters.items() if value},
        "record_count": len(records),
        "averages": averages,
        "metric_sample_sizes": sample_sizes,
        "warning": "Averages are descriptive. They do not establish causation unless variables were controlled.",
        "records": records,
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def record_post_performance(
    platform: str,
    audience: str,
    content_type: str,
    published_at: str,
    objective: Optional[str] = None,
    funnel_stage: Optional[str] = None,
    topic: Optional[str] = None,
    post_id: Optional[str] = None,
    timezone: str = "Asia/Kuala_Lumpur",
    impressions: Optional[float] = None,
    reach: Optional[float] = None,
    engagements: Optional[float] = None,
    clicks: Optional[float] = None,
    leads: Optional[float] = None,
    saves: Optional[float] = None,
    shares: Optional[float] = None,
    notes: Optional[str] = None,
) -> str:
    """Append one post result with normalized local time fields; never rewrites history."""
    records = _read_jsonl("content_performance.jsonl")
    record_id = post_id or _next_id("POST", records)
    if any(record.get("id") == record_id for record in records):
        return json.dumps({"saved": False, "error": f"Post ID {record_id} already exists."}, indent=2)
    try:
        publication = _publication_fields(published_at, timezone)
    except ValueError as error:
        return json.dumps({"saved": False, "error": str(error)}, ensure_ascii=False, indent=2)
    record = {
        "id": record_id,
        "recorded_at": datetime.now().isoformat(timespec="seconds"),
        **publication,
        "platform": platform.strip().lower(),
        "audience": audience.strip().lower().replace(" ", "_"),
        "content_type": content_type.strip().lower(),
        "objective": objective,
        "funnel_stage": funnel_stage,
        "topic": topic,
        "impressions": impressions,
        "reach": reach,
        "engagements": engagements,
        "clicks": clicks,
        "leads": leads,
        "saves": saves,
        "shares": shares,
        "notes": notes,
    }
    if isinstance(engagements, (int, float)) and isinstance(reach, (int, float)) and reach > 0:
        record["engagement_rate"] = engagements / reach
    else:
        record["engagement_rate"] = None
    _append_jsonl("content_performance.jsonl", record)
    return json.dumps({"saved": True, "post_id": record_id, "record": record}, ensure_ascii=False, indent=2)


@mcp.tool()
def analyze_posting_time_performance(
    platform: Optional[str] = None,
    audience: Optional[str] = None,
    content_type: Optional[str] = None,
    metric: str = "engagement_rate",
    minimum_sample_size: int = 4,
) -> str:
    """Compare local time slots by day+hour and by hour alone, and label only sufficiently sampled slots as validated.

    Two groupings are reported, because a schedule can be designed for either one:

      slots       - grouped by (day_of_week, hour_local). Use when the same slot is
                    held constant, e.g. four posts all on Tuesday 20:00.
      hour_slots  - grouped by hour_local alone. Use when day_of_week was deliberately
                    counterbalanced across weeks so that time-of-day is not confounded
                    with day-of-week. An hour is only validated here when its posts are
                    actually spread evenly across days; otherwise it is reported
                    CONFOUNDED_WITH_DAY and must not be read as a time-of-day result.
    """
    allowed_metrics = {"impressions", "reach", "engagements", "engagement_rate", "clicks", "leads", "saves", "shares"}
    if metric not in allowed_metrics:
        return json.dumps({"error": f"Unsupported metric. Choose one of: {sorted(allowed_metrics)}"}, indent=2)
    minimum_sample_size = max(2, min(int(minimum_sample_size), 100))
    records = _read_jsonl("content_performance.jsonl")
    filters = {"platform": platform, "audience": audience, "content_type": content_type}
    for key, value in filters.items():
        if value:
            normalized = value.strip().lower().replace(" ", "_") if key == "audience" else value.strip().lower()
            records = [record for record in records if str(record.get(key, "")).lower() == normalized]
    usable = [record for record in records if isinstance(record.get(metric), (int, float))]
    slots = {}
    for record in usable:
        key = (record.get("day_of_week", "Unknown"), record.get("hour_local"))
        slots.setdefault(key, []).append(record)
    results = []
    for (day, hour), slot_records in slots.items():
        sample_size = len(slot_records)
        results.append({
            "day_of_week": day,
            "hour_local": hour,
            "sample_size": sample_size,
            "average": _numeric_average(slot_records, metric),
            "status": "VALIDATED" if sample_size >= minimum_sample_size else "TESTING",
        })
    results.sort(key=lambda item: (item["status"] != "VALIDATED", -(item["average"] or 0), -item["sample_size"]))
    validated = [result for result in results if result["status"] == "VALIDATED"]

    hour_groups = {}
    for record in usable:
        hour_groups.setdefault(record.get("hour_local"), []).append(record)
    hour_results = []
    for hour, hour_records in hour_groups.items():
        distribution = {}
        for record in hour_records:
            day = record.get("day_of_week", "Unknown")
            distribution[day] = distribution.get(day, 0) + 1
        counts = list(distribution.values())
        counterbalanced = len(distribution) >= 2 and (max(counts) - min(counts)) <= 1
        sample_size = len(hour_records)
        if sample_size < minimum_sample_size:
            status = "TESTING"
        elif not counterbalanced:
            status = "CONFOUNDED_WITH_DAY"
        else:
            status = "VALIDATED"
        hour_results.append({
            "hour_local": hour,
            "sample_size": sample_size,
            "average": _numeric_average(hour_records, metric),
            "day_distribution": dict(sorted(distribution.items())),
            "day_counterbalanced": counterbalanced,
            "status": status,
        })
    hour_results.sort(key=lambda item: (item["status"] != "VALIDATED", -(item["average"] or 0), -item["sample_size"]))
    validated_hours = [result for result in hour_results if result["status"] == "VALIDATED"]
    comparable_hours = [result for result in hour_results if result["sample_size"] >= minimum_sample_size]
    hour_comparison_is_balanced = len(comparable_hours) >= 2 and all(
        result["day_distribution"] == comparable_hours[0]["day_distribution"] for result in comparable_hours
    )
    return json.dumps({
        "filters": {key: value for key, value in filters.items() if value},
        "metric": metric,
        "record_count": len(records),
        "usable_record_count": len(usable),
        "minimum_sample_size": minimum_sample_size,
        "can_claim_best_time": bool(validated or validated_hours),
        "best_validated_slot": validated[0] if validated else None,
        "best_validated_hour": validated_hours[0] if validated_hours else None,
        "hour_comparison_is_balanced": hour_comparison_is_balanced,
        "slots": results,
        "hour_slots": hour_results,
        "instruction": (
            "Use VALIDATED slots and VALIDATED hour_slots as internal evidence. Treat TESTING slots and external "
            "benchmarks as hypotheses. Do not claim a best time when can_claim_best_time is false. A validated "
            "best_validated_slot is a day-and-time claim; a validated best_validated_hour is a time-of-day claim only, "
            "and is comparable across hours only when hour_comparison_is_balanced is true. Never read a "
            "CONFOUNDED_WITH_DAY hour as a time-of-day result - its posts were not spread evenly across days."
        ),
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def create_experiment(
    question: str,
    hypothesis: str,
    variable: str,
    control: str,
    variant: str,
    platform: str,
    audience: str,
    success_metric: str,
) -> str:
    """Creates an experiment with a stable ID and ACTIVE status."""
    records = _read_jsonl("experiments.jsonl")
    experiment_id = _next_id("EXP", records)
    record = {
        "id": experiment_id,
        "event": "created",
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "status": "ACTIVE",
        "question": question,
        "hypothesis": hypothesis,
        "variable": variable,
        "control": control,
        "variant": variant,
        "platform": platform,
        "audience": audience,
        "success_metric": success_metric,
    }
    _append_jsonl("experiments.jsonl", record)
    return json.dumps(record, ensure_ascii=False, indent=2)


@mcp.tool()
def record_experiment_result(
    experiment_id: str,
    result: str,
    data_summary: str,
    confidence: str = "LOW",
) -> str:
    """Appends an experiment result while preserving its history."""
    records = _read_jsonl("experiments.jsonl")
    if not any(record.get("id") == experiment_id for record in records):
        return f"Experiment {experiment_id} does not exist."
    confidence_key = confidence.upper()
    if confidence_key not in {"LOW", "MEDIUM", "HIGH"}:
        return "confidence must be LOW, MEDIUM, or HIGH."
    event = {
        "id": experiment_id,
        "event": "result",
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "result": result,
        "data_summary": data_summary,
        "confidence": confidence_key,
    }
    _append_jsonl("experiments.jsonl", event)
    return json.dumps(event, ensure_ascii=False, indent=2)


@mcp.tool()
def close_experiment(experiment_id: str, learning: str, outcome: str) -> str:
    """Closes an experiment as VALIDATED, REJECTED, or INCONCLUSIVE."""
    outcome_key = outcome.upper()
    if outcome_key not in {"VALIDATED", "REJECTED", "INCONCLUSIVE"}:
        return "outcome must be VALIDATED, REJECTED, or INCONCLUSIVE."
    records = _read_jsonl("experiments.jsonl")
    if not any(record.get("id") == experiment_id for record in records):
        return f"Experiment {experiment_id} does not exist."
    event = {
        "id": experiment_id,
        "event": "closed",
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "status": outcome_key,
        "learning": learning,
    }
    _append_jsonl("experiments.jsonl", event)
    return json.dumps(event, ensure_ascii=False, indent=2)


# ----------------- 7B. GENERATION PROMPT APPROVAL -----------------

GENERATION_PROMPTS_DIR = "05_CREATIVE/generation_prompts"
GENERATION_PROMPTS_INDEX = f"{GENERATION_PROMPTS_DIR}/README.md"
_PROMPT_TITLE_RE = re.compile(r"(?m)^#\s+(?P<post_id>.+?)\s+[—–-]\s+(?P<platform>.+?)\s+[—–-]\s+(?P<date>\d{4}-\d{2}-\d{2})\b.*$")
_PROMPT_FILENAME_RE = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})-(?P<platform>[a-z]+)-(?P<post_id>.+)$", re.IGNORECASE)
_PROMPT_STATUS_RE = re.compile(r"(?m)^\*\*Status:\*\*[ \t]*(?P<status>.+?)[ \t]*$")


def _parse_prompt_file(rel_path: str) -> dict:
    """Extract post id, platform, date and status from one generation prompt file."""
    content = _read_markdown(rel_path)
    title_match = _PROMPT_TITLE_RE.search(content)
    name_match = _PROMPT_FILENAME_RE.match(os.path.splitext(os.path.basename(rel_path))[0])
    status_match = _PROMPT_STATUS_RE.search(content)
    raw_status = status_match.group("status").strip() if status_match else ""
    status_word = re.split(r"[ \t(]", raw_status, maxsplit=1)[0].upper() if raw_status else "UNKNOWN"
    first_heading = re.search(r"(?m)^#\s+(.+?)\s*$", content)

    def _pick(field: str) -> str:
        if title_match and title_match.group(field).strip():
            return title_match.group(field).strip()
        if name_match:
            return name_match.group(field).strip()
        return ""

    return {
        "post_id": _pick("post_id"),
        "platform": _pick("platform").title() if not title_match and name_match else _pick("platform"),
        "post_date": _pick("date"),
        "file": rel_path,
        "status": status_word,
        "status_text": raw_status,
        "title": (first_heading.group(1).strip() if first_heading else rel_path),
        "characters": len(content),
    }


def _iter_prompt_files() -> list:
    base = _resolve_workspace_path(GENERATION_PROMPTS_DIR, require_markdown=False)
    if not os.path.isdir(base):
        return []
    found = []
    for name in sorted(os.listdir(base)):
        if name.lower().endswith(".md") and name.lower() != "readme.md":
            found.append(f"{GENERATION_PROMPTS_DIR}/{name}")
    return found


def _find_prompt_file_by_id(post_id: str) -> Optional[str]:
    target = post_id.strip().lower()
    for rel_path in _iter_prompt_files():
        parsed = _parse_prompt_file(rel_path)
        if parsed["post_id"].lower() == target:
            return rel_path
    # Fall back to the filename convention YYYY-MM-DD-<platform>-<post-id>.md
    for rel_path in _iter_prompt_files():
        stem = os.path.splitext(os.path.basename(rel_path))[0].lower()
        if stem.endswith(f"-{target}"):
            return rel_path
    return None


def _set_readme_index_status(post_id: str, new_status: str) -> bool:
    """Rewrite the status cell for one post id row in the generation_prompts index. Returns True if changed."""
    full_path = _resolve_workspace_path(GENERATION_PROMPTS_INDEX)
    if not os.path.exists(full_path):
        return False
    before = _read_markdown(GENERATION_PROMPTS_INDEX)
    row_marker = re.compile(rf"\|\s*{re.escape(post_id)}\s*\|")
    changed = False
    out_lines = []
    for line in before.splitlines():
        if line.lstrip().startswith("|") and row_marker.search(line) and "---" not in line:
            new_line = re.sub(r"\|\s*[^|]*\|\s*$", f"| {new_status} |", line)
            if new_line != line:
                changed = True
            out_lines.append(new_line)
        else:
            out_lines.append(line)
    if not changed:
        return False
    after = "\n".join(out_lines) + ("\n" if before.endswith("\n") else "")
    with open(full_path, "w", encoding="utf-8") as file:
        file.write(after)
    _log_change("update_section", GENERATION_PROMPTS_INDEX)
    _audit_mutation("apply_prompt_decision", GENERATION_PROMPTS_INDEX, "index_status", before, after, True)
    return True


@mcp.tool()
def list_generation_prompt_status() -> str:
    """Lists every media generation prompt with its post id, platform, date and status.

    Reads 05_CREATIVE/generation_prompts/*.md (excluding README.md). Use this to seed the
    approval console queue and to reconcile which prompts still await a human decision.
    Status is the first word of the file's `**Status:**` line (DRAFT / APPROVED / REJECTED /
    PRODUCED / PUBLISHED).
    """
    prompts = [_parse_prompt_file(rel_path) for rel_path in _iter_prompt_files()]
    return json.dumps({
        "directory": GENERATION_PROMPTS_DIR,
        "count": len(prompts),
        "draft_post_ids": [item["post_id"] for item in prompts if item["status"] == "DRAFT"],
        "prompts": prompts,
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def apply_prompt_decision(
    post_id: str,
    decision: str,
    reason: str = "",
    decided_at: str = "",
    decided_by: str = "human via approval PR",
) -> str:
    """Applies one human approve/deny decision to a DRAFT generation prompt, locally only.

    This is the "Human checking" node of the daily loop. It does NOT touch git — the caller
    pushes the returned `changed_files` with preview_github_api_sync -> sync_to_github_atomic.

    approve: rewrites the prompt's `**Status:**` line to APPROVED, flips its row in the
             generation_prompts index, and appends a dated entry to 08_DECISIONS/decision_log.md.
    deny:    rewrites `**Status:**` to REJECTED, flips the index row, and appends an entry to
             08_DECISIONS/rejected_ideas.md carrying the reason (the next run regenerates it).

    A decision of "deny" requires a non-empty reason. Refuses if the prompt is not found or is
    not currently DRAFT (nothing is silently overwritten).
    """
    choice_key = decision.strip().lower()
    if choice_key in {"approve", "approved", "accept", "yes"}:
        choice = "approve"
    elif choice_key in {"deny", "denied", "reject", "rejected", "no"}:
        choice = "deny"
    else:
        return json.dumps({"applied": False, "error": "decision must be 'approve' or 'deny'."}, indent=2)
    if choice == "deny" and not reason.strip():
        return json.dumps({"applied": False, "error": "A non-empty reason is required to deny a prompt."}, indent=2)

    decision_date = decided_at.strip() or datetime.now().strftime("%Y-%m-%d")
    rel_path = _find_prompt_file_by_id(post_id)
    if not rel_path:
        return json.dumps({"applied": False, "error": f"No generation prompt found for post id {post_id!r}."}, indent=2)

    parsed = _parse_prompt_file(rel_path)
    if parsed["status"] != "DRAFT":
        return json.dumps({
            "applied": False,
            "post_id": parsed["post_id"] or post_id,
            "error": f"{rel_path} is not DRAFT (current status: {parsed['status_text'] or parsed['status']}). No change made.",
        }, ensure_ascii=False, indent=2)

    resolved_id = parsed["post_id"] or post_id.strip()
    full_path = _resolve_workspace_path(rel_path)
    before = _read_markdown(rel_path)

    if choice == "approve":
        new_status_line = f"**Status:** APPROVED ({decided_by}, {decision_date})"
        index_status = "APPROVED"
    else:
        new_status_line = f"**Status:** REJECTED ({decided_by}, {decision_date}) — see 08_DECISIONS/rejected_ideas.md"
        index_status = "REJECTED"

    after, replaced = _PROMPT_STATUS_RE.subn(lambda _m: new_status_line, before, count=1)
    if not replaced:
        return json.dumps({"applied": False, "error": f"No `**Status:**` line found in {rel_path}."}, indent=2)
    with open(full_path, "w", encoding="utf-8") as file:
        file.write(after)
    _log_change("update_section", rel_path)
    _audit_mutation("apply_prompt_decision", rel_path, choice, before, after, True)

    changed_files = [rel_path]
    if _set_readme_index_status(resolved_id, index_status):
        changed_files.append(GENERATION_PROMPTS_INDEX)

    if choice == "approve":
        log_rel = "08_DECISIONS/decision_log.md"
        entry = (
            f"\n## {decision_date}\n"
            f"## Decision — Generation prompt {resolved_id} ({parsed['platform']}, {parsed['post_date']}): APPROVED ({decision_date})\n\n"
            f"**Date:** {decision_date}\n"
            f"**Decision:** Move generation prompt `{rel_path}` from DRAFT to APPROVED for production.\n"
            f"**Context:** Human approval recorded via the approval Pull Request ({decided_by}).\n"
            f"**Evidence:** As stated in the prompt's Evidence basis section. Approval authorises production of the asset, not publication.\n"
            f"**Approved by:** {decided_by}, {decision_date}.\n"
            + (f"**Note:** {reason.strip()}\n" if reason.strip() else "")
        )
    else:
        log_rel = "08_DECISIONS/rejected_ideas.md"
        entry = (
            f"\n## {resolved_id} — {parsed['platform']} generation prompt — rejected {decision_date}\n\n"
            f"- Date: {decision_date}\n"
            f"- Idea: {parsed['title']}\n"
            f"- Audience/platform/objective: see `{rel_path}`\n"
            f"- Decision maker: {decided_by}\n"
            f"- Reason rejected: {reason.strip()}\n"
            f"- Evidence considered: the prompt's Evidence basis section\n"
            f"- Conditions that could justify reconsideration: regenerate the prompt addressing the reason above, then re-submit for approval\n"
        )
    log_full = _resolve_workspace_path(log_rel)
    log_before = _read_markdown(log_rel)
    os.makedirs(os.path.dirname(log_full), exist_ok=True)
    with open(log_full, "a", encoding="utf-8") as file:
        file.write(entry)
    _log_change("append", log_rel)
    _audit_mutation("apply_prompt_decision", log_rel, "append", log_before, log_before + entry, True)
    changed_files.append(log_rel)

    return json.dumps({
        "applied": True,
        "post_id": resolved_id,
        "choice": choice,
        "prompt_file": rel_path,
        "new_status": index_status,
        "reason": reason.strip() or None,
        "regenerate_required": choice == "deny",
        "changed_files": changed_files,
        "next_step": (
            "Push changed_files: check_github_connection -> preview_github_api_sync -> "
            "sync_to_github_atomic, then git fetch origin && git reset --hard origin/main. "
            + ("Then regenerate this prompt as a fresh DRAFT addressing the reason and re-seed its queue doc."
               if choice == "deny" else "")
        ),
    }, ensure_ascii=False, indent=2)


# ----------------- 8. PROMPT AND RECOMMENDATION CONTEXT -----------------

@mcp.tool()
def build_prompt_context(
    task_type: str,
    task_description: str,
    audience: Optional[str] = None,
    platform: Optional[str] = None,
    product: Optional[str] = None,
) -> str:
    """Returns the mandatory read-only 00/01 grounding manifest for prompt creation.

    This tool does not write files or generate the final prompt. The connected LLM
    must read the returned required files before constructing an operational prompt.
    """
    if not task_type.strip() or not task_description.strip():
        return json.dumps({"error": "task_type and task_description are required"}, indent=2)

    governance_files = [
        "00_SYSTEM/brain_rules.md",
        "00_SYSTEM/decision_framework.md",
        "00_SYSTEM/evidence_rules.md",
        "00_SYSTEM/routing_rules.md",
        "00_SYSTEM/taxonomy.md",
        "00_SYSTEM/update_rules.md",
        "05_CREATIVE/prompting_rules.md",
    ]
    business_files = [
        "01_BUSINESS/company_profile.md",
        "01_BUSINESS/products.md",
        "01_BUSINESS/positioning.md",
        "01_BUSINESS/customer_objections.md",
        "01_BUSINESS/sales_insights.md",
        "01_BUSINESS/swot.md",
    ]
    status = {}
    for filepath in governance_files + business_files:
        content = _read_markdown(filepath)
        status[filepath] = "MISSING" if not content else "TEMPLATE_ONLY" if _is_placeholder(content) else "AVAILABLE"

    task_key = task_type.strip().lower().replace(" ", "_").replace("-", "_")
    if task_key in {"content_recommendation", "content_creation", "campaign", "research", "prompt_creation"}:
        required_business = business_files
    elif task_key in {"competitor_research", "positioning"}:
        required_business = [
            "01_BUSINESS/company_profile.md", "01_BUSINESS/products.md",
            "01_BUSINESS/positioning.md", "01_BUSINESS/swot.md"
        ]
    elif task_key in {"audience_research", "persona"}:
        required_business = [
            "01_BUSINESS/company_profile.md", "01_BUSINESS/products.md",
            "01_BUSINESS/customer_objections.md", "01_BUSINESS/sales_insights.md"
        ]
    else:
        required_business = ["01_BUSINESS/company_profile.md", "01_BUSINESS/positioning.md"]

    evidence_gaps = [filepath for filepath in required_business if status[filepath] != "AVAILABLE"]
    return json.dumps({
        "task_type": task_key,
        "task_description": task_description.strip(),
        "audience": audience,
        "platform": platform,
        "product": product,
        "mandatory_governance_reads": governance_files,
        "required_business_reads": required_business,
        "file_status": status,
        "business_evidence_gaps": evidence_gaps,
        "protection": {
            "00_SYSTEM": "READ_ONLY",
            "01_BUSINESS": "READ_ONLY",
            "protected_change_route": "propose_brain_update",
            "direct_write_allowed": False,
        },
        "permitted_prompt_write_scope": [
            "02_AUDIENCE", "03_PLATFORM", "04_COMPETITORS", "05_CREATIVE",
            "06_PERFORMANCE", "07_RESEARCH", "08_DECISIONS"
        ],
        "required_prompt_sections": [
            "role", "objective", "grounding", "scope", "tool_order", "evidence_rules",
            "routing", "write_authorization", "prohibited_actions", "output",
            "stopping_conditions", "verification", "success_criteria"
        ],
        "instruction": (
            "Read every mandatory_governance_reads and required_business_reads file before creating the prompt. "
            "Use 00/01 as grounding only. Do not authorize direct writes to them. Explicitly label template-only "
            "or missing business inputs as evidence gaps in the resulting prompt."
        )
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def build_recommendation_context(
    audience: str = "production_manager",
    platform: str = "instagram",
    competitor: Optional[str] = None,
    objective: str = "awareness",
    product: str = "Mysoft MES",
    funnel_stage: str = "awareness",
) -> str:
    """Builds the mandatory evidence packet used before recommending content.

    It does not invent a recommendation or approve a decision. It loads business,
    audience, platform, SWOT, competitor, creative, performance, research, and
    current-priority inputs, and explicitly reports missing/placeholder evidence.
    """
    try:
        audience_slug = _safe_slug(audience, "audience").replace("-", "_")
        platform_slug = platform.strip().lower().replace(" ", "_").replace("-", "_")
        if platform_slug not in VALID_PLATFORMS:
            raise ValueError(f"Unsupported platform: {platform}")
    except ValueError as error:
        return json.dumps({"error": str(error)}, ensure_ascii=False, indent=2)

    files = [
        "01_BUSINESS/company_profile.md",
        "01_BUSINESS/products.md",
        "01_BUSINESS/positioning.md",
        "01_BUSINESS/swot.md",
        f"02_AUDIENCE/{audience_slug}.md",
        f"03_PLATFORM/{platform_slug}.md",
        "04_COMPETITORS/competitor_index.md",
        "04_COMPETITORS/competitor_patterns.md",
        "04_COMPETITORS/competitor_gaps.md",
        "05_CREATIVE/creative_strategy.md",
        "05_CREATIVE/hook_library.md",
        "05_CREATIVE/video_formats.md",
        "05_CREATIVE/winning_patterns.md",
        "05_CREATIVE/losing_patterns.md",
        "06_PERFORMANCE/video_performance.md",
        "06_PERFORMANCE/learning_log.md",
        "06_PERFORMANCE/validated_patterns.md",
        "08_DECISIONS/current_priorities.md",
        "08_DECISIONS/experiments.md",
    ]
    if competitor:
        try:
            files.append(f"04_COMPETITORS/{_safe_slug(competitor, 'competitor')}.md")
        except ValueError as error:
            return json.dumps({"error": str(error)}, ensure_ascii=False, indent=2)

    sections = []
    evidence_gaps = []
    input_status = {}
    for filepath in files:
        try:
            content = _read_markdown(filepath)
        except ValueError as error:
            evidence_gaps.append(f"{filepath}: {error}")
            continue
        if not content:
            evidence_gaps.append(f"{filepath}: missing")
            input_status[filepath] = "MISSING"
            continue
        if _is_placeholder(content):
            evidence_gaps.append(f"{filepath}: placeholder or not yet populated")
            input_status[filepath] = "PLACEHOLDER"
        else:
            input_status[filepath] = "AVAILABLE"
        sections.append(f"--- {filepath} ---\n{content}")

    structured_results = _read_jsonl("video_performance.jsonl")
    relevant_results = [
        record for record in structured_results
        if str(record.get("platform", "")).lower() == platform_slug.lower()
        and str(record.get("audience", "")).lower().replace(" ", "_") == audience_slug.lower()
    ]
    critical_files = {
        "01_BUSINESS/swot.md",
        f"02_AUDIENCE/{audience_slug}.md",
        f"03_PLATFORM/{platform_slug}.md",
        "06_PERFORMANCE/video_performance.md",
    }
    critical_gaps = [filepath for filepath in critical_files if input_status.get(filepath) != "AVAILABLE"]
    if critical_gaps or not relevant_results:
        maximum_confidence = "LOW"
        action_class = "TEST"
    elif evidence_gaps or len(relevant_results) < 3:
        maximum_confidence = "MEDIUM"
        action_class = "TEST"
    else:
        maximum_confidence = "HIGH"
        action_class = "ACT NOW"

    header = {
        "audience": audience_slug,
        "platform": platform_slug,
        "objective": objective,
        "product": product,
        "funnel_stage": funnel_stage,
        "competitor_focus": competitor,
        "input_status": input_status,
        "evidence_gaps": evidence_gaps,
        "critical_evidence_gaps": critical_gaps,
        "structured_relevant_video_results": len(relevant_results),
        "maximum_confidence": maximum_confidence,
        "recommended_action_class": action_class,
        "required_output_fields": [
            "priority", "platform", "audience", "objective", "funnel_stage", "product",
            "problem", "content_idea", "hook", "opening_visual", "format", "duration",
            "story_structure", "cta", "swot_relevance", "competitor_gap",
            "supporting_evidence", "risks", "assumptions", "contradictions",
            "evidence_gaps", "confidence", "hypothesis", "success_metric",
            "next_test_if_successful", "next_test_if_unsuccessful"
        ],
        "instruction": (
            "Use the evidence below to produce the decision-framework output. "
            "Label facts, observations, inferences, assumptions, contradictions, "
            "confidence, and success metrics. If material inputs are placeholders, "
            "recommend a bounded TEST rather than claiming a validated conclusion."
        )
    }
    return json.dumps(header, ensure_ascii=False, indent=2) + "\n\n" + "\n\n".join(sections)


@mcp.tool()
def build_posting_schedule_context(
    platforms: str = "linkedin,instagram,facebook",
    audiences: str = "production_manager,general_manager,operations_manager",
    objective: str = "awareness",
    weeks: int = 4,
    timezone: str = "Asia/Kuala_Lumpur",
) -> str:
    """Build evidence for an LLM-authored schedule without inventing dates, topics, or times."""
    try:
        _resolve_timezone(timezone)
    except ValueError as error:
        return json.dumps({"error": str(error)}, indent=2)
    platform_slugs = list(dict.fromkeys(
        item.strip().lower().replace(" ", "_").replace("-", "_")
        for item in platforms.split(",") if item.strip()
    ))
    audience_slugs = list(dict.fromkeys(
        item.strip().lower().replace(" ", "_").replace("-", "_")
        for item in audiences.split(",") if item.strip()
    ))
    unsupported = [item for item in platform_slugs if item not in VALID_PLATFORMS]
    if unsupported:
        return json.dumps({"error": f"Unsupported platforms: {unsupported}"}, indent=2)
    weeks = max(1, min(int(weeks), 12))
    files = [
        "00_SYSTEM/brain_rules.md", "00_SYSTEM/decision_framework.md", "00_SYSTEM/evidence_rules.md",
        "01_BUSINESS/company_profile.md", "01_BUSINESS/products.md", "01_BUSINESS/positioning.md",
        "05_CREATIVE/creative_strategy.md", "05_CREATIVE/hook_library.md", "05_CREATIVE/video_formats.md",
        "05_CREATIVE/winning_patterns.md", "05_CREATIVE/losing_patterns.md",
        "06_PERFORMANCE/content_performance.md", "06_PERFORMANCE/video_performance.md",
        "06_PERFORMANCE/learning_log.md", "06_PERFORMANCE/validated_patterns.md",
        "08_DECISIONS/current_priorities.md", "08_DECISIONS/content_backlog.md", "08_DECISIONS/experiments.md",
    ]
    files.extend(f"02_AUDIENCE/{audience}.md" for audience in audience_slugs)
    files.extend(f"03_PLATFORM/{platform}.md" for platform in platform_slugs)
    sections, evidence_gaps, input_status = [], [], {}
    for filepath in dict.fromkeys(files):
        try:
            content = _read_markdown(filepath)
        except ValueError as error:
            evidence_gaps.append(f"{filepath}: {error}")
            continue
        status = "MISSING" if not content else "PLACEHOLDER" if _is_placeholder(content) else "AVAILABLE"
        input_status[filepath] = status
        if status != "AVAILABLE":
            evidence_gaps.append(f"{filepath}: {status.lower()}")
        if content:
            sections.append(f"--- {filepath} ---\n{content}")
    performance_records = _read_jsonl("content_performance.jsonl")
    relevant_records = [
        record for record in performance_records
        if record.get("platform") in platform_slugs and record.get("audience") in audience_slugs
    ]
    timed_records = [record for record in relevant_records if record.get("day_of_week") and record.get("hour_local") is not None]
    header = {
        "purpose": "Evidence packet for the connected LLM to create its own posting schedule",
        "platforms": platform_slugs,
        "audiences": audience_slugs,
        "objective": objective,
        "weeks": weeks,
        "timezone": timezone,
        "input_status": input_status,
        "evidence_gaps": evidence_gaps,
        "relevant_performance_records": len(relevant_records),
        "records_with_timing": len(timed_records),
        "mysoft_specific_timing_validated": any(
            sum(
                1 for candidate in timed_records
                if candidate.get("platform") == record.get("platform")
                and candidate.get("audience") == record.get("audience")
                and candidate.get("day_of_week") == record.get("day_of_week")
                and candidate.get("hour_local") == record.get("hour_local")
            ) >= 4
            for record in timed_records
        ),
        "required_tool_order": [
            "know_yourself",
            "build_posting_schedule_context",
            "analyze_posting_time_performance for each platform/audience combination",
        ],
        "required_schedule_columns": [
            "date", "day", "time", "timezone", "platform", "audience", "objective", "funnel_stage",
            "topic", "format", "hook", "cta", "evidence_basis", "confidence", "test_metric", "review_date",
        ],
        "instruction": (
            "The LLM must create the schedule itself from this packet. It must not claim Mysoft-specific best timing "
            "unless analyze_posting_time_performance returns can_claim_best_time=true for the relevant segment. "
            "Otherwise it may use current externally sourced benchmarks as TEST hypotheses, cite them, keep them "
            "separate from internal evidence, and design a controlled schedule that can collect comparable results. "
            "Do not write or sync the schedule without explicit human authorization."
        ),
    }
    return json.dumps(header, ensure_ascii=False, indent=2) + "\n\n" + "\n\n".join(sections)


# ----------------- 9. GITHUB API SYNC TOOLS -----------------

GITHUB_API_BASE = "https://api.github.com"
GITHUB_BRANCH = "main"


class GitHubAPIError(RuntimeError):
    def __init__(self, status: Optional[int], message: str):
        super().__init__(message)
        self.status = status


def _github_api_request(path: str, method: str = "GET", payload: Optional[dict] = None, timeout: int = 20) -> dict:
    """Call GitHub without exposing credentials or raw authorization errors."""
    if not GITHUB_TOKEN:
        raise GitHubAPIError(None, "GITHUB_TOKEN is not configured.")
    url = f"{GITHUB_API_BASE}{path}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "Social-Content-Engine-MCP",
    }
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as error:
        safe_messages = {
            401: "GitHub rejected the token. Replace or reauthorize GITHUB_TOKEN.",
            403: "GitHub denied access or rate-limited the request. Check token permissions and rate limits.",
            404: "The repository, branch, or object was not found for this token.",
            409: "GitHub reported a repository or reference conflict.",
            422: "GitHub rejected the requested Git object or reference update.",
        }
        raise GitHubAPIError(error.code, safe_messages.get(error.code, f"GitHub API request failed with HTTP {error.code}."))
    except urllib.error.URLError as error:
        raise GitHubAPIError(None, f"GitHub could not be reached: {getattr(error, 'reason', 'network error')}")
    except TimeoutError:
        raise GitHubAPIError(None, "GitHub API request timed out.")


def _git_blob_sha(content: bytes) -> str:
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()


def _github_repository_state() -> dict:
    repo_path = f"/repos/{REPO_OWNER}/{REPO_NAME}"
    repository = _github_api_request(repo_path)
    reference = _github_api_request(f"{repo_path}/git/ref/heads/{GITHUB_BRANCH}")
    commit_sha = reference.get("object", {}).get("sha")
    if not commit_sha:
        raise GitHubAPIError(None, f"GitHub did not return the {GITHUB_BRANCH} branch SHA.")
    commit = _github_api_request(f"{repo_path}/git/commits/{commit_sha}")
    tree_sha = commit.get("tree", {}).get("sha")
    if not tree_sha:
        raise GitHubAPIError(None, "GitHub did not return the base tree SHA.")
    tree = _github_api_request(f"{repo_path}/git/trees/{tree_sha}?recursive=1")
    if tree.get("truncated"):
        raise GitHubAPIError(None, "The remote repository tree is too large for a safe complete comparison.")
    remote_blobs = {
        item["path"]: item["sha"]
        for item in tree.get("tree", [])
        if item.get("type") == "blob" and item.get("path") and item.get("sha")
    }
    return {
        "repository_private": repository.get("private"),
        "default_branch": repository.get("default_branch"),
        "permissions": repository.get("permissions", {}),
        "remote_commit_sha": commit_sha,
        "remote_tree_sha": tree_sha,
        "remote_blobs": remote_blobs,
    }


def _build_github_api_preview(include_code: bool, include_obsidian: bool) -> dict:
    candidates = _workspace_sync_candidates(include_code, include_obsidian)
    state = _github_repository_state()
    changed = []
    unchanged = []
    for filepath in candidates:
        full_path = _resolve_workspace_path(filepath, require_markdown=False)
        with open(full_path, "rb") as file:
            local_sha = _git_blob_sha(file.read())
        remote_sha = state["remote_blobs"].get(filepath)
        item = {
            "filepath": filepath,
            "status": "NEW" if remote_sha is None else "MODIFIED",
            "local_blob_sha": local_sha,
            "remote_blob_sha": remote_sha,
        }
        if local_sha == remote_sha:
            unchanged.append(filepath)
        else:
            changed.append(item)
    local_paths = set(candidates)
    deletions = sorted(
        filepath for filepath in state["remote_blobs"]
        if _path_is_sync_eligible(filepath, include_code, include_obsidian)
        and filepath not in local_paths
    )
    return {
        "preview_method": "github_git_data_api_hash_comparison",
        "repository": f"{REPO_OWNER}/{REPO_NAME}",
        "branch": GITHUB_BRANCH,
        "remote_commit_sha": state["remote_commit_sha"],
        "remote_tree_sha": state["remote_tree_sha"],
        "token_permissions_reported_by_github": state["permissions"],
        "include_code": include_code,
        "include_obsidian": include_obsidian,
        "eligible_file_count": len(candidates),
        "changed_file_count": len(changed),
        "changed_files": changed,
        "unchanged_file_count": len(unchanged),
        "deletion_count": len(deletions),
        "deletions": deletions,
        "deletion_policy": "Deletions require an exact reviewed list, allow_deletions=true, and a deletion-specific confirmation phrase.",
        "secret_exclusions": {
            ".env": ".env" not in candidates,
            ".mcp_data": not any(path.startswith(".mcp_data/") for path in candidates),
            ".git": not any(path.startswith(".git/") for path in candidates),
            ".uv-cache": not any(path.startswith(".uv-cache/") for path in candidates),
            ".uv-python": not any(path.startswith(".uv-python/") for path in candidates),
            ".obsidian": not any(path.startswith(".obsidian/") for path in candidates),
        },
    }


@mcp.tool()
def check_github_connection() -> str:
    """Validates GitHub token/repository access without modifying local or remote state."""
    started = datetime.now()
    try:
        state = _github_repository_state()
    except GitHubAPIError as error:
        return json.dumps({
            "connected": False,
            "http_status": error.status,
            "error": str(error),
            "token_exposed": False,
        }, ensure_ascii=False, indent=2)
    return json.dumps({
        "connected": True,
        "repository": f"{REPO_OWNER}/{REPO_NAME}",
        "branch": GITHUB_BRANCH,
        "remote_commit_sha": state["remote_commit_sha"],
        "repository_private": state["repository_private"],
        "permissions_reported_by_github": state["permissions"],
        "token_exposed": False,
        "elapsed_ms": round((datetime.now() - started).total_seconds() * 1000, 2),
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def preview_github_api_sync(include_code: bool = True, include_obsidian: bool = False) -> str:
    """Compares local eligible files with GitHub blob hashes without writing anything."""
    try:
        preview = _build_github_api_preview(include_code, include_obsidian)
    except (GitHubAPIError, OSError, ValueError) as error:
        status = error.status if isinstance(error, GitHubAPIError) else None
        return json.dumps({
            "success": False,
            "http_status": status,
            "error": str(error),
            "remote_modified": False,
        }, ensure_ascii=False, indent=2)
    preview.update({
        "success": True,
        "remote_modified": False,
        "next_step": (
            "Review changed_files. For an atomic commit, pass remote_commit_sha as expected_remote_sha "
            "to sync_to_github_atomic with confirmation='CREATE ATOMIC GITHUB COMMIT'."
        )
    })
    return json.dumps(preview, ensure_ascii=False, indent=2)


def _create_github_blob(filepath: str) -> dict:
    full_path = _resolve_workspace_path(filepath, require_markdown=False)
    with open(full_path, "rb") as file:
        content = file.read()
    response = _github_api_request(
        f"/repos/{REPO_OWNER}/{REPO_NAME}/git/blobs",
        method="POST",
        payload={"content": base64.b64encode(content).decode("ascii"), "encoding": "base64"},
        timeout=30,
    )
    sha = response.get("sha")
    if not sha:
        raise GitHubAPIError(None, f"GitHub did not return a blob SHA for {filepath}.")
    return {"path": filepath, "mode": "100644", "type": "blob", "sha": sha}


@mcp.tool()
def sync_to_github_atomic(
    commit_message: str,
    expected_remote_sha: str,
    include_code: bool = True,
    include_obsidian: bool = False,
    confirmation: str = "",
) -> str:
    """Creates one atomic GitHub commit without invoking local Git.

    Requires the exact remote SHA returned by preview_github_api_sync and exact
    confirmation `CREATE ATOMIC GITHUB COMMIT`. Remote deletions are never made.
    If the branch moved after preview, the operation stops before creating a commit.
    """
    if confirmation != "CREATE ATOMIC GITHUB COMMIT":
        return json.dumps({
            "committed": False,
            "error": "Exact confirmation phrase required: CREATE ATOMIC GITHUB COMMIT"
        }, indent=2)
    if not commit_message.strip() or not re.fullmatch(r"[0-9a-fA-F]{40}", expected_remote_sha.strip()):
        return json.dumps({"committed": False, "error": "A commit message and valid 40-character expected_remote_sha are required."}, indent=2)
    try:
        preview = _build_github_api_preview(include_code, include_obsidian)
        current_remote_sha = preview["remote_commit_sha"]
        if current_remote_sha.lower() != expected_remote_sha.strip().lower():
            return json.dumps({
                "committed": False,
                "conflict": True,
                "expected_remote_sha": expected_remote_sha,
                "current_remote_sha": current_remote_sha,
                "error": "The remote branch changed after preview. Run preview_github_api_sync again and review the new diff."
            }, ensure_ascii=False, indent=2)
        changed_paths = [item["filepath"] for item in preview["changed_files"]]
        if not changed_paths:
            return json.dumps({"committed": False, "pushed": False, "result": "No changed or new eligible files."}, indent=2)

        tree_entries = []
        upload_errors = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(_create_github_blob, filepath): filepath for filepath in changed_paths}
            for future in as_completed(futures):
                filepath = futures[future]
                try:
                    tree_entries.append(future.result())
                except (GitHubAPIError, OSError, ValueError) as error:
                    upload_errors.append({"filepath": filepath, "error": str(error)})
        if upload_errors:
            return json.dumps({
                "committed": False,
                "pushed": False,
                "uploaded_blob_count": len(tree_entries),
                "errors": upload_errors,
                "remote_branch_unchanged": True,
            }, ensure_ascii=False, indent=2)

        repo_path = f"/repos/{REPO_OWNER}/{REPO_NAME}"
        tree_response = _github_api_request(
            f"{repo_path}/git/trees", method="POST",
            payload={"base_tree": preview["remote_tree_sha"], "tree": tree_entries}, timeout=30
        )
        new_tree_sha = tree_response.get("sha")
        if not new_tree_sha:
            raise GitHubAPIError(None, "GitHub did not return the new tree SHA.")
        commit_response = _github_api_request(
            f"{repo_path}/git/commits", method="POST",
            payload={
                "message": commit_message.strip(),
                "tree": new_tree_sha,
                "parents": [current_remote_sha],
            }, timeout=30
        )
        new_commit_sha = commit_response.get("sha")
        if not new_commit_sha:
            raise GitHubAPIError(None, "GitHub did not return the new commit SHA.")
        try:
            _github_api_request(
                f"{repo_path}/git/refs/heads/{GITHUB_BRANCH}", method="PATCH",
                payload={"sha": new_commit_sha, "force": False}, timeout=30
            )
        except GitHubAPIError as error:
            return json.dumps({
                "committed": False,
                "commit_object_created": True,
                "branch_updated": False,
                "orphan_commit_sha": new_commit_sha,
                "http_status": error.status,
                "error": (
                    "The commit object was created but main was not updated. The branch may have changed; "
                    "run preview_github_api_sync again."
                ),
                "token_exposed": False,
            }, ensure_ascii=False, indent=2)
        global _pending_changes
        _pending_changes = []
        _append_jsonl("sync_log.jsonl", {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "method": "github_git_data_api",
            "commit_sha": new_commit_sha,
            "parent_sha": current_remote_sha,
            "files": sorted(changed_paths),
            "status": "pushed",
        })
        return json.dumps({
            "committed": True,
            "pushed": True,
            "commit_sha": new_commit_sha,
            "parent_sha": current_remote_sha,
            "changed_file_count": len(changed_paths),
            "changed_files": sorted(changed_paths),
            "commit_url": f"https://github.com/{REPO_OWNER}/{REPO_NAME}/commit/{new_commit_sha}",
        }, ensure_ascii=False, indent=2)
    except GitHubAPIError as error:
        return json.dumps({
            "committed": False,
            "pushed": False,
            "http_status": error.status,
            "error": str(error),
            "token_exposed": False,
        }, ensure_ascii=False, indent=2)


# ----------------- 9B. PULL REQUEST APPROVAL WORKFLOW -----------------

APPROVAL_BRANCH_PREFIX = "approvals"


def _github_ref_sha(ref: str) -> Optional[str]:
    """Return the commit SHA a ref (e.g. 'heads/approvals/2026-09-04') points at, or None."""
    try:
        data = _github_api_request(f"/repos/{REPO_OWNER}/{REPO_NAME}/git/ref/{ref}")
    except GitHubAPIError as error:
        if error.status == 404:
            return None
        raise
    return data.get("object", {}).get("sha")


def _normalize_file_list(files) -> list:
    items = list(files) if isinstance(files, (list, tuple)) else re.split(r"[,\n]", str(files or ""))
    seen = []
    for item in items:
        rel = str(item).strip().strip('"').replace("\\", "/")
        if rel and rel not in seen:
            seen.append(rel)
    return seen


def _prompt_files_changed_vs_main() -> list:
    """generation_prompts/*.md (plus its README) whose local blob differs from remote main."""
    remote_blobs = _github_repository_state()["remote_blobs"]
    changed = []
    for rel_path in _iter_prompt_files() + [GENERATION_PROMPTS_INDEX]:
        full_path = _resolve_workspace_path(rel_path, require_markdown=False)
        if not os.path.exists(full_path):
            continue
        with open(full_path, "rb") as file:
            local_sha = _git_blob_sha(file.read())
        if remote_blobs.get(rel_path) != local_sha:
            changed.append(rel_path)
    return changed


def _default_pr_body(prompts: list, run_date: str) -> str:
    lines = [
        f"Automated daily run {run_date} — {len(prompts)} generation prompt(s) awaiting the "
        f"**human checking** gate (`daily_operating_spec.md` loop diagram).",
        "",
        "## How to respond",
        "- **Approve all:** merge this PR.",
        "- **Reject some:** comment `deny <POST-ID>: <reason>` for each "
        "(e.g. `deny FB-01: hook too similar to FB-03`), then merge. Denied prompts are logged "
        "to `08_DECISIONS/rejected_ideas.md` and regenerated on the next run.",
        "- **Reject all:** close this PR without merging.",
        "",
        "Do not edit files on this branch — comment instead. Merging publishes nothing: prompts "
        "stay DRAFT until the next run flips approved ones to APPROVED and records them in "
        "`08_DECISIONS/decision_log.md`.",
        "",
        "## Prompts in this PR",
    ]
    for prompt in prompts:
        lines.append(f"### {prompt['post_id']} — {prompt['platform']} — {prompt['post_date']}")
        lines.append(f"`{prompt['file']}`")
    return "\n".join(lines)


@mcp.tool()
def open_prompt_approval_pr(
    files: str = "",
    run_date: str = "",
    title: str = "",
    body: str = "",
    confirmation: str = "",
) -> str:
    """Opens (or updates) a GitHub Pull Request carrying DRAFT generation prompts for human approval.

    This is the "human checking" gate: instead of pushing new prompt files straight to main,
    the daily run puts them on a dated branch and opens a PR. The owner merges to approve all,
    comments `deny <POST-ID>: <reason>` to reject specific prompts, or closes the PR to reject all.

    files: comma/newline-separated repo-relative paths. Empty = every file under
           05_CREATIVE/generation_prompts/ (plus its README) whose local content differs from main.
    run_date: YYYY-MM-DD; picks the branch name approvals/<run_date>. Defaults to today.
    Requires confirmation='OPEN APPROVAL PR'. Never writes to main. Never deletes anything.
    If the branch already carries commits that are not children of the current main tip, it
    refuses rather than force-overwriting them.
    """
    if confirmation != "OPEN APPROVAL PR":
        return json.dumps({"opened": False, "error": "Exact confirmation phrase required: OPEN APPROVAL PR"}, indent=2)
    run_date = run_date.strip() or datetime.now().strftime("%Y-%m-%d")
    branch = f"{APPROVAL_BRANCH_PREFIX}/{run_date}"
    ref = f"heads/{branch}"
    repo_path = f"/repos/{REPO_OWNER}/{REPO_NAME}"

    requested = _normalize_file_list(files)
    try:
        file_list = requested or _prompt_files_changed_vs_main()
    except GitHubAPIError as error:
        return json.dumps({"opened": False, "http_status": error.status, "error": str(error)}, indent=2)

    safe_files = []
    for rel_path in file_list:
        try:
            full_path = _resolve_workspace_path(rel_path, require_markdown=False)
        except ValueError:
            continue
        if os.path.exists(full_path) and _path_is_sync_eligible(rel_path, include_code=True, include_obsidian=False):
            safe_files.append(rel_path)
    if not safe_files:
        return json.dumps({"opened": False, "error": "No eligible files to put in the PR."}, indent=2)

    try:
        state = _github_repository_state()
        main_sha = state["remote_commit_sha"]
        base_tree = state["remote_tree_sha"]

        existing_head = _github_ref_sha(ref)
        if existing_head:
            head_commit = _github_api_request(f"{repo_path}/git/commits/{existing_head}")
            parents = [parent.get("sha") for parent in head_commit.get("parents", [])]
            if parents and main_sha not in parents:
                return json.dumps({
                    "opened": False,
                    "error": (
                        f"Branch {branch} has diverged from main (its commit is not a child of the "
                        f"current main tip). Resolve on GitHub before re-running."
                    ),
                    "branch_head_sha": existing_head,
                }, ensure_ascii=False, indent=2)

        tree_entries = []
        errors = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(_create_github_blob, rel_path): rel_path for rel_path in safe_files}
            for future in as_completed(futures):
                try:
                    tree_entries.append(future.result())
                except (GitHubAPIError, OSError, ValueError) as error:
                    errors.append({"filepath": futures[future], "error": str(error)})
        if errors:
            return json.dumps({"opened": False, "errors": errors}, ensure_ascii=False, indent=2)

        tree_response = _github_api_request(
            f"{repo_path}/git/trees", method="POST",
            payload={"base_tree": base_tree, "tree": tree_entries}, timeout=30,
        )
        new_tree_sha = tree_response.get("sha")
        if not new_tree_sha:
            raise GitHubAPIError(None, "GitHub did not return the new tree SHA.")

        commit_message = title.strip() or f"Prompts for approval — {run_date}"
        commit_response = _github_api_request(
            f"{repo_path}/git/commits", method="POST",
            payload={"message": commit_message, "tree": new_tree_sha, "parents": [main_sha]}, timeout=30,
        )
        new_commit_sha = commit_response.get("sha")
        if not new_commit_sha:
            raise GitHubAPIError(None, "GitHub did not return the new commit SHA.")

        if existing_head is None:
            _github_api_request(
                f"{repo_path}/git/refs", method="POST",
                payload={"ref": f"refs/heads/{branch}", "sha": new_commit_sha}, timeout=30,
            )
        else:
            _github_api_request(
                f"{repo_path}/git/refs/{ref}", method="PATCH",
                payload={"sha": new_commit_sha, "force": True}, timeout=30,
            )

        prompts = [_parse_prompt_file(path) for path in safe_files if path != GENERATION_PROMPTS_INDEX]
        pr_body = body.strip() or _default_pr_body(prompts, run_date)

        open_prs = _github_api_request(f"{repo_path}/pulls?head={REPO_OWNER}:{branch}&state=open")
        if isinstance(open_prs, list) and open_prs:
            pr = open_prs[0]
            _github_api_request(
                f"{repo_path}/pulls/{pr['number']}", method="PATCH",
                payload={"title": commit_message, "body": pr_body}, timeout=30,
            )
            pr_number, pr_url, reused = pr["number"], pr["html_url"], True
        else:
            pr = _github_api_request(
                f"{repo_path}/pulls", method="POST",
                payload={"title": commit_message, "head": branch, "base": GITHUB_BRANCH, "body": pr_body},
                timeout=30,
            )
            pr_number, pr_url, reused = pr.get("number"), pr.get("html_url"), False

        _append_jsonl("sync_log.jsonl", {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "method": "approval_pull_request",
            "branch": branch,
            "commit_sha": new_commit_sha,
            "pr_number": pr_number,
            "files": sorted(safe_files),
            "status": "updated" if reused else "opened",
        })
        return json.dumps({
            "opened": True,
            "reused_existing_pr": reused,
            "pr_number": pr_number,
            "pr_url": pr_url,
            "branch": branch,
            "head_commit_sha": new_commit_sha,
            "base": GITHUB_BRANCH,
            "included_files": sorted(safe_files),
            "post_ids": [prompt["post_id"] for prompt in prompts],
            "instruction_for_owner": (
                "Merge this PR to approve every prompt in it. Comment `deny <POST-ID>: <reason>` "
                "to reject specific prompts (then merge), or close the PR to reject all."
            ),
        }, ensure_ascii=False, indent=2)
    except GitHubAPIError as error:
        return json.dumps({
            "opened": False, "http_status": error.status, "error": str(error), "token_exposed": False,
        }, ensure_ascii=False, indent=2)


@mcp.tool()
def get_prompt_approval_pr(pr_number: int = 0, run_date: str = "") -> str:
    """Reports an approval PR's state (open / merged / closed), its prompt files, and every comment.

    The daily run calls this at bootstrap to apply the previous run's decisions:
      merged            -> approve every prompt in the PR
      closed, unmerged  -> deny every prompt (reason "PR closed without merge") and regenerate
      open + `deny <ID>: <reason>` comments -> deny those, leave the rest pending

    Pass pr_number, or leave it 0 to look the PR up by the approvals/<run_date> branch.
    """
    repo_path = f"/repos/{REPO_OWNER}/{REPO_NAME}"
    try:
        if not pr_number:
            branch = f"{APPROVAL_BRANCH_PREFIX}/{(run_date.strip() or datetime.now().strftime('%Y-%m-%d'))}"
            found = _github_api_request(f"{repo_path}/pulls?head={REPO_OWNER}:{branch}&state=all")
            if not (isinstance(found, list) and found):
                return json.dumps({"found": False, "branch": branch}, ensure_ascii=False, indent=2)
            pr_number = found[0]["number"]
        pr = _github_api_request(f"{repo_path}/pulls/{pr_number}")
        files_data = _github_api_request(f"{repo_path}/pulls/{pr_number}/files?per_page=100")
        issue_comments = _github_api_request(f"{repo_path}/issues/{pr_number}/comments?per_page=100")
        review_comments = _github_api_request(f"{repo_path}/pulls/{pr_number}/comments?per_page=100")
    except GitHubAPIError as error:
        return json.dumps({"found": False, "http_status": error.status, "error": str(error)}, ensure_ascii=False, indent=2)

    changed_files = [item.get("filename") for item in files_data] if isinstance(files_data, list) else []
    prompt_files = [
        path for path in changed_files
        if path and path.startswith(GENERATION_PROMPTS_DIR + "/") and path != GENERATION_PROMPTS_INDEX
    ]
    post_ids = []
    for rel_path in prompt_files:
        name_match = _PROMPT_FILENAME_RE.match(os.path.splitext(os.path.basename(rel_path))[0])
        full_path = _resolve_workspace_path(rel_path, require_markdown=False)
        parsed = _parse_prompt_file(rel_path) if os.path.exists(full_path) else {}
        post_ids.append(parsed.get("post_id") or (name_match.group("post_id") if name_match else rel_path))

    def _fmt(comment: dict) -> dict:
        return {
            "user": comment.get("user", {}).get("login"),
            "created_at": comment.get("created_at"),
            "body": comment.get("body", ""),
        }

    state = pr.get("state")
    merged = bool(pr.get("merged"))
    recommended = "approve_all" if merged else "deny_all" if state == "closed" else "pending_or_partial"
    return json.dumps({
        "found": True,
        "pr_number": pr_number,
        "pr_url": pr.get("html_url"),
        "state": state,
        "merged": merged,
        "merged_at": pr.get("merged_at"),
        "mergeable": pr.get("mergeable"),
        "head_sha": pr.get("head", {}).get("sha"),
        "prompt_files": prompt_files,
        "post_ids": post_ids,
        "comments": (
            [_fmt(comment) for comment in (issue_comments or []) if isinstance(comment, dict)]
            + [_fmt(comment) for comment in (review_comments or []) if isinstance(comment, dict)]
        ),
        "recommended_apply_action": recommended,
        "instruction": (
            "approve_all: git fetch origin && git reset --hard origin/main, then apply_prompt_decision(<id>,'approve') "
            "for every post id and push the status flips + decision_log to main. "
            "deny_all: apply_prompt_decision(<id>,'deny', reason='PR closed without merge') and regenerate each. "
            "pending_or_partial: honour only `deny <ID>: <reason>` comments; leave the PR open."
        ),
    }, ensure_ascii=False, indent=2)


# ----------------- 10. LEGACY GIT SYNC TOOLS -----------------

def _git_changed_paths() -> list:
    result = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z"], cwd=WORKSPACE_DIR,
        capture_output=True, timeout=15, check=False
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace").strip() or "git status failed")
    paths = []
    for item in result.stdout.split(b"\0"):
        if not item:
            continue
        text_item = item.decode("utf-8", errors="replace")
        path = text_item[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        normalized = path.replace("\\", "/")
        if normalized and normalized not in paths:
            paths.append(normalized)
    return paths


def _path_is_sync_eligible(filepath: str, include_code: bool, include_obsidian: bool) -> bool:
    normalized = filepath.replace("\\", "/").lstrip("/")
    parts = normalized.split("/")
    if any(part in {".git", ".mcp_data", ".uv-cache", ".uv-python", "__pycache__"} for part in parts):
        return False
    if not include_obsidian and parts[0] == ".obsidian":
        return False
    if normalized == ".env" or normalized.endswith((".pyc", ".pyo")):
        return False
    managed_root = bool(re.match(r"^0[0-8]_[A-Z_]+/", normalized)) or normalized in {
        ".gitignore", "README.md", "prompt.md", "server.py", "APPROVAL_UI.md"
    }
    if not managed_root:
        return False
    extension = os.path.splitext(normalized)[1].lower()
    if not include_code:
        return extension == ".md"
    return extension in {".md", ".py", ".json", ".toml", ".yaml", ".yml", ".txt"} or normalized == ".gitignore"


def _workspace_sync_candidates(include_code: bool, include_obsidian: bool = False) -> list:
    """List bounded, non-secret workspace files without invoking Git."""
    excluded_directories = {".git", ".mcp_data", ".uv-cache", ".uv-python", "__pycache__"}
    if not include_obsidian:
        excluded_directories.add(".obsidian")
    excluded_files = {".env"}
    candidates = []
    for root, dirs, files in os.walk(WORKSPACE_DIR):
        dirs[:] = [directory for directory in dirs if directory not in excluded_directories]
        for filename in files:
            filepath = _relative_path(os.path.join(root, filename))
            if filename in excluded_files or not _path_is_sync_eligible(filepath, include_code, include_obsidian):
                continue
            candidates.append(filepath)
    return sorted(candidates)


@mcp.tool()
def sync_changed_files_to_github(
    commit_message: str,
    include_code: bool = False,
    dry_run: bool = True,
    confirmation: str = "",
    include_obsidian: bool = False,
) -> str:
    """Safely stages, commits, and pushes changed files as one Git commit.

    The default is a read-only preview. Set include_code=True to include server.py
    and other non-Markdown repository files. A real sync requires dry_run=False and
    confirmation exactly equal to `PUSH TO GITHUB`. Secrets and MCP runtime data are
    always excluded. Git authentication must be configured outside this tool.
    """
    if not commit_message.strip():
        return json.dumps({"error": "commit_message is required"}, indent=2)
    if dry_run:
        candidates = _workspace_sync_candidates(include_code, include_obsidian)
        important_files = ["server.py", "prompt.md", "README.md", ".gitignore"]
        return json.dumps({
            "dry_run": True,
            "preview_method": "bounded_filesystem_scan_without_git",
            "candidate_scope": "All eligible workspace files, not confirmed Git changes",
            "include_code": include_code,
            "include_obsidian": include_obsidian,
            "candidate_count": len(candidates),
            "candidate_files": candidates,
            "important_file_inclusion": {filepath: filepath in candidates for filepath in important_files},
            "secret_exclusions": {
                ".env": ".env" not in candidates,
                ".mcp_data": not any(path.startswith(".mcp_data/") for path in candidates),
                ".git": not any(path.startswith(".git/") for path in candidates),
                ".uv-cache": not any(path.startswith(".uv-cache/") for path in candidates),
                ".uv-python": not any(path.startswith(".uv-python/") for path in candidates),
                ".obsidian": not any(path.startswith(".obsidian/") for path in candidates),
            },
            "commit_message": commit_message.strip(),
            "warning": (
                "Git inspection is intentionally skipped because Git subprocesses block in this MCP host. "
                "A real sync will ask Git to stage these eligible paths and may still fail if the host blocks Git."
            ),
            "next_step": "Review candidate_files. A real sync still requires dry_run=false and confirmation='PUSH TO GITHUB'."
        }, ensure_ascii=False, indent=2)

    try:
        changed = _git_changed_paths()
    except (OSError, subprocess.TimeoutExpired, RuntimeError) as error:
        return json.dumps({
            "error": f"Unable to inspect Git changes: {error}",
            "recommendation": "Use the preview for review, then perform the Git commit/push outside this MCP host."
        }, ensure_ascii=False, indent=2)
    excluded_prefixes = (".git/", ".mcp_data/", ".uv-cache/", ".uv-python/")
    if not include_obsidian:
        excluded_prefixes = excluded_prefixes + (".obsidian/",)
    candidates = [
        path for path in changed
        if path != ".env"
        and not path.startswith(excluded_prefixes)
        and (include_code or path.lower().endswith(".md"))
    ]
    preview = {
        "dry_run": dry_run,
        "include_code": include_code,
        "candidate_count": len(candidates),
        "candidate_files": candidates,
        "excluded_changed_files": [path for path in changed if path not in candidates],
        "commit_message": commit_message.strip(),
    }
    if confirmation != "PUSH TO GITHUB":
        preview["error"] = "Exact confirmation phrase required: PUSH TO GITHUB"
        return json.dumps(preview, ensure_ascii=False, indent=2)
    if not candidates:
        preview["result"] = "No eligible changed files to sync."
        return json.dumps(preview, ensure_ascii=False, indent=2)

    try:
        add_result = subprocess.run(
            ["git", "add", "--", *candidates], cwd=WORKSPACE_DIR,
            capture_output=True, text=True, timeout=30, check=False
        )
        if add_result.returncode != 0:
            raise RuntimeError(add_result.stderr.strip() or "git add failed")
        commit_result = subprocess.run(
            ["git", "commit", "-m", commit_message.strip()], cwd=WORKSPACE_DIR,
            capture_output=True, text=True, timeout=60, check=False
        )
        if commit_result.returncode != 0:
            raise RuntimeError(commit_result.stderr.strip() or commit_result.stdout.strip() or "git commit failed")
        commit_sha_result = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=WORKSPACE_DIR,
            capture_output=True, text=True, timeout=10, check=False
        )
        commit_sha = commit_sha_result.stdout.strip()
        push_result = subprocess.run(
            ["git", "push", "origin", "main"], cwd=WORKSPACE_DIR,
            capture_output=True, text=True, timeout=120, check=False
        )
        if push_result.returncode != 0:
            return json.dumps({
                **preview,
                "committed": True,
                "commit_sha": commit_sha,
                "pushed": False,
                "error": "GitHub push failed. Check repository authentication and retry; the commit remains safe locally.",
            }, ensure_ascii=False, indent=2)
        global _pending_changes
        _pending_changes = []
        sync_record = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "commit_sha": commit_sha,
            "files": candidates,
            "status": "pushed",
        }
        _append_jsonl("sync_log.jsonl", sync_record)
        return json.dumps({**preview, "committed": True, "commit_sha": commit_sha, "pushed": True}, ensure_ascii=False, indent=2)
    except (OSError, subprocess.TimeoutExpired, RuntimeError) as error:
        return json.dumps({**preview, "committed": False, "pushed": False, "error": str(error)}, ensure_ascii=False, indent=2)

@mcp.tool()
def sync_to_github(commit_message: str = None, dry_run: bool = True, confirmation: str = "") -> str:
    """Legacy Markdown-only Contents API sync. Defaults to a non-writing preview.

    Prefer sync_changed_files_to_github for a single atomic Git commit. A real
    legacy sync requires dry_run=False and confirmation `SYNC MARKDOWN FILES`.
    """
    global _pending_changes

    if not GITHUB_TOKEN:
        return "GITHUB_TOKEN is not set (checked via .env). Cannot sync."

    markdown_files = []
    for root, dirs, files in os.walk(WORKSPACE_DIR):
        dirs[:] = [directory for directory in dirs if directory not in {".git", ".mcp_data", "__pycache__"}]
        for filename in files:
            if filename.endswith(".md"):
                markdown_files.append(_relative_path(os.path.join(root, filename)))
    if dry_run:
        return json.dumps({
            "deprecated": True,
            "dry_run": True,
            "candidate_count": len(markdown_files),
            "candidate_files": sorted(markdown_files),
            "warning": "This legacy tool creates one GitHub commit per file. Prefer sync_changed_files_to_github.",
            "next_step": "For legacy sync only, call with dry_run=false and confirmation='SYNC MARKDOWN FILES'."
        }, ensure_ascii=False, indent=2)
    if confirmation != "SYNC MARKDOWN FILES":
        return "Refused: exact confirmation phrase required: SYNC MARKDOWN FILES"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "FastMCP-Agent"
    }

    if commit_message is None:
        if _pending_changes:
            parts = [f"{action} {os.path.basename(fp)}" for action, fp in _pending_changes]
            commit_message = "docs: " + ", ".join(parts)
        else:
            commit_message = "docs: update content strategy and prompts"

    synced_files = []
    failed_files = []

    for root, dirs, files in os.walk(WORKSPACE_DIR):
        if ".git" in root or "__pycache__" in root:
            continue
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, WORKSPACE_DIR).replace("\\", "/")

                with open(full_path, "rb") as f:
                    content_encoded = base64.b64encode(f.read()).decode("utf-8")

                url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{rel_path}"

                sha = None
                get_req = urllib.request.Request(url, headers=headers, method="GET")
                try:
                    with urllib.request.urlopen(get_req) as resp:
                        if resp.status == 200:
                            data = json.loads(resp.read().decode("utf-8"))
                            sha = data.get("sha")
                except urllib.error.HTTPError:
                    pass

                payload = {
                    "message": f"{commit_message} [{rel_path}]",
                    "content": content_encoded,
                    "branch": "main"
                }
                if sha:
                    payload["sha"] = sha

                put_req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={**headers, "Content-Type": "application/json"},
                    method="PUT"
                )

                try:
                    with urllib.request.urlopen(put_req) as resp:
                        if resp.status in (200, 201):
                            synced_files.append(rel_path)
                except urllib.error.HTTPError as e:
                    failed_files.append(f"{rel_path}: {e.read().decode('utf-8')}")
                except Exception as e:
                    failed_files.append(f"{rel_path}: {str(e)}")

    if not failed_files:
        _pending_changes = []

    result = f"Pushed {len(synced_files)} files: {', '.join(synced_files)}"
    if failed_files:
        result += f"\n\nFailed ({len(failed_files)}): {'; '.join(failed_files)}"
    return result


# ----------------- 10. DRAFT PREVIEW TOOL -----------------

@mcp.tool()
def generate_draft_preview(visual_prompt: str) -> str:
    """Generates an image preview URL for human review. PLACEHOLDER ONLY —
    this returns a random stock image, not a real generation. Replace with
    an actual Gemini/Veo API call before using in production."""
    return f"https://picsum.photos/seed/{abs(hash(visual_prompt)) % 1000}/800/800"


if __name__ == "__main__":
    mcp.run()
