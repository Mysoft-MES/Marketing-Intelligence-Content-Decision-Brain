import os
import base64
import json
import urllib.request
import urllib.error
from datetime import datetime, date
from fastmcp import FastMCP

mcp = FastMCP(
    "Social Content Engine",
    instructions="Before doing any research, prompting, generation, justification, "
                  "or analysis work, always call know_yourself first to load this "
                  "system's identity, rules, and business context. Let it ground "
                  "every decision you make in this session."
)

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))

# GITHUB CREDENTIALS — set GITHUB_TOKEN as an environment variable, never hardcode it here
GITHUB_TOKEN = os.environ.get("Git_Hub")
REPO_OWNER = "Mysoft-MES"
REPO_NAME = "Marketing-Intelligence-Content-Decision-Brain"

# ----------------- CHANGE TRACKING -----------------

_pending_changes = []  # tracks (action, filepath) since the last sync

def _log_change(action: str, filepath: str):
    _pending_changes.append((action, filepath))


# ----------------- 1. CORE FILE TOOLS -----------------

@mcp.tool()
def read_doc(filepath: str) -> str:
    """Reads a markdown file from the marketing-brain knowledge base.
    
    Pass the path relative to the repo root, including its folder, e.g.:
      - "01_BUSINESS/company_profile.md"
      - "07_RESEARCH/trends.md"
      - "05_CREATIVE/hook_library.md"
    
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
    full_path = os.path.join(WORKSPACE_DIR, filepath)
    if not os.path.exists(full_path):
        return f"File {filepath} does not exist yet."
    with open(full_path, "r", encoding="utf-8") as f:
        return f.read()


@mcp.tool()
def write_doc(filepath: str, content: str) -> str:
    """Creates or overwrites a markdown file in the marketing-brain knowledge base.
    
    Pass the path relative to the repo root, including its folder, e.g.:
      - "07_RESEARCH/trends.md"
      - "05_CREATIVE/hook_library.md"
    
    Same folder structure as read_doc. IMPORTANT: 00_SYSTEM/ and 01_BUSINESS/ are
    reference material set by the human, not agent output — do not write to these
    folders unless explicitly instructed to update company/business information.
    Freely write to 02_AUDIENCE/ through 08_DECISIONS/.
    
    Note: this OVERWRITES the entire file. For log-style files that should
    accumulate over time (learning_log.md, decision_log.md, campaign_history.md),
    use append_doc instead — write_doc will destroy their history.
    """
    full_path = os.path.join(WORKSPACE_DIR, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    _log_change("write", filepath)
    return f"Successfully saved {filepath} locally."


@mcp.tool()
def append_doc(filepath: str, content: str, add_timestamp: bool = True) -> str:
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
    full_path = os.path.join(WORKSPACE_DIR, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    if add_timestamp:
        entry = f"\n## {datetime.now().strftime('%Y-%m-%d')}\n{content}\n"
    else:
        entry = f"\n{content}\n"
    
    with open(full_path, "a", encoding="utf-8") as f:
        f.write(entry)
    
    _log_change("append", filepath)
    return f"Appended to {filepath}"


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
    full_path = os.path.join(WORKSPACE_DIR, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    rel_path_str = rel_path.replace(os.sep, "/")
    _log_change("create", rel_path_str)
    return f"Created dated file: {rel_path_str}"


@mcp.tool()
def list_docs(folder: str = "") -> str:
    """Lists markdown files in the marketing-brain knowledge base.
    Pass a folder name (e.g. '07_RESEARCH') to list just that folder,
    or leave empty to list the whole structure."""
    base = os.path.join(WORKSPACE_DIR, folder)
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
        "00_SYSTEM/routing_rules.md",
        "01_BUSINESS/company_profile.md"
    ]
    combined = []
    for f in files:
        full_path = os.path.join(WORKSPACE_DIR, f)
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


# ----------------- 6. GITHUB SYNC TOOL -----------------

@mcp.tool()
def sync_to_github(commit_message: str = None) -> str:
    """Pushes local markdown files to GitHub. If commit_message is not provided,
    one is auto-generated from the actions logged since the last sync (e.g.
    'docs: append learning_log.md, write trends.md')."""
    global _pending_changes

    if not GITHUB_TOKEN:
        return "GITHUB_TOKEN environment variable is not set. Cannot sync."

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

    _pending_changes = []

    result = f"Pushed {len(synced_files)} files: {', '.join(synced_files)}"
    if failed_files:
        result += f"\n\nFailed ({len(failed_files)}): {'; '.join(failed_files)}"
    return result


# ----------------- 7. DRAFT PREVIEW TOOL -----------------

@mcp.tool()
def generate_draft_preview(visual_prompt: str) -> str:
    """Generates an image preview URL for human review. PLACEHOLDER ONLY —
    this returns a random stock image, not a real generation. Replace with
    an actual Gemini/Veo API call before using in production."""
    return f"https://picsum.photos/seed/{abs(hash(visual_prompt)) % 1000}/800/800"


if __name__ == "__main__":
    mcp.run()
