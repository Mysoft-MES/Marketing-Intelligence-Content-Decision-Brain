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
from datetime import datetime, date
from typing import Optional
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
                  "explicit human confirmation of the preview and remote SHA."
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
    if not meaningful or "_(placeholder)_" in meaningful or "not yet populated" in meaningful:
        return True
    level_two_headings = re.findall(r"(?m)^##[ \t]+(.+?)\s*$", content)
    if level_two_headings and all(heading.lower().endswith("template") for heading in level_two_headings):
        return True
    nonblank_lines = [line.strip() for line in content.splitlines() if line.strip()]
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
      - "07_RESEARCH/trends.md"
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
      - "07_RESEARCH/trends.md"
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
def list_docs(folder: str = "") -> str:
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
def search_knowledge(query: str, folder: str = "", limit: int = 10) -> str:
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
        dirs[:] = [directory for directory in dirs if directory not in {".git", ".mcp_data", "__pycache__"}]
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
def find_knowledge_conflicts(topic: str, limit: int = 50) -> str:
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
        dirs[:] = [directory for directory in dirs if directory not in {".git", ".mcp_data", "__pycache__"}]
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
def audit_knowledge_freshness(folder: str = "", maximum_age_days: int = 90) -> str:
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
        dirs[:] = [directory for directory in dirs if directory not in {".git", ".mcp_data", "__pycache__"}]
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
        "01_BUSINESS/company_profile.md"
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
        "02_AUDIENCE": ["factory_owner.md", "production_manager.md", "finance_manager.md", "audience_matrix.md"],
        "03_PLATFORM": ["facebook.md", "instagram.md", "linkedin.md", "xiaohongshu.md", "reddit.md", "youtube.md"],
        "04_COMPETITORS": ["competitor_index.md"],
        "05_CREATIVE": ["hook_library.md", "video_formats.md", "creative_rules.md", "winning_patterns.md"],
        "06_PERFORMANCE": ["campaign_history.md", "video_performance.md", "ad_performance.md", "learning_log.md"],
        "07_RESEARCH": ["trends.md", "government_updates.md", "industry_news.md", "customer_insights.md"],
        "08_DECISIONS": ["content_backlog.md", "current_priorities.md", "experiments.md", "decision_log.md", "brain_update_proposals.md"],
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
) -> str:
    """Appends one structured video result without modifying prior records."""
    records = _read_jsonl("video_performance.jsonl")
    record_id = video_id or _next_id("VID", records)
    if any(record.get("id") == record_id for record in records):
        return f"Refused: video ID {record_id} already exists."
    record = {
        "id": record_id,
        "recorded_at": datetime.now().isoformat(timespec="seconds"),
        "published_at": published_at,
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


# ----------------- 8. RECOMMENDATION CONTEXT -----------------

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
        "deletions": [],
        "deletion_policy": "Remote files are never deleted by this tool.",
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


def _workspace_sync_candidates(include_code: bool, include_obsidian: bool = False) -> list:
    """List bounded, non-secret workspace files without invoking Git."""
    excluded_directories = {".git", ".mcp_data", ".uv-cache", ".uv-python", "__pycache__"}
    if not include_obsidian:
        excluded_directories.add(".obsidian")
    excluded_files = {".env"}
    allowed_code_extensions = {".md", ".py", ".json", ".toml", ".yaml", ".yml", ".txt"}
    candidates = []
    for root, dirs, files in os.walk(WORKSPACE_DIR):
        dirs[:] = [directory for directory in dirs if directory not in excluded_directories]
        for filename in files:
            if filename in excluded_files or filename.endswith((".pyc", ".pyo")):
                continue
            extension = os.path.splitext(filename)[1].lower()
            if not include_code and extension != ".md":
                continue
            if include_code and extension not in allowed_code_extensions and filename != ".gitignore":
                continue
            candidates.append(_relative_path(os.path.join(root, filename)))
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
