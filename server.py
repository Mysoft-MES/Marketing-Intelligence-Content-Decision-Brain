import os
import subprocess
from fastmcp import FastMCP

mcp = FastMCP("Social Content Engine")
WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))

# ----------------- 1. RESEARCH & FILE TOOLS -----------------

@mcp.tool()
def read_doc(filename: str) -> str:
    """Reads content from markdown files like Refinement.md, research.md, or prompt.md."""
    filepath = os.path.join(WORKSPACE_DIR, filename)
    if not os.path.exists(filepath):
        return f"File {filename} does not exist yet."
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

@mcp.tool()
def write_doc(filename: str, content: str) -> str:
    """Creates or updates markdown files like research.md, prompt.md, or Refinement.md."""
    filepath = os.path.join(WORKSPACE_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Successfully saved {filename} locally."

# ----------------- 2. GITHUB SYNC TOOL -----------------

@mcp.tool()
def sync_to_github(commit_message: str = "docs: update content strategy and prompts") -> str:
    """Commits and pushes all updated local markdown files directly to GitHub."""
    try:
        # 1. Add all modified files
        add_res = subprocess.run(["git", "add", "."], cwd=WORKSPACE_DIR, capture_output=True, text=True)
        if add_res.returncode != 0:
            return f"Git add error: {add_res.stderr}"

        # 2. Check if there are changes to commit
        status = subprocess.run(["git", "status", "--porcelain"], cwd=WORKSPACE_DIR, capture_output=True, text=True)
        if status.stdout.strip():
            commit_res = subprocess.run(["git", "commit", "-m", commit_message], cwd=WORKSPACE_DIR, capture_output=True, text=True)
            if commit_res.returncode != 0:
                return f"Git commit error: {commit_res.stderr}"

        # 3. Push to remote
        push_res = subprocess.run(["git", "push", "origin", "main"], cwd=WORKSPACE_DIR, capture_output=True, text=True)
        if push_res.returncode != 0:
            return f"Git push error: {push_res.stderr}"

        return "Successfully pushed all updates to GitHub repository!"
    except Exception as e:
        return f"Unexpected error during sync: {str(e)}"
# ----------------- 3. DRAFT PREVIEW TOOL -----------------

@mcp.tool()
def generate_draft_preview(visual_prompt: str) -> str:
    """Generates an image preview URL for human review."""
    return f"https://picsum.photos/seed/{abs(hash(visual_prompt)) % 1000}/800/800"

if __name__ == "__main__":
    mcp.run()