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
        subprocess.run(["git", "add", "."], cwd=WORKSPACE_DIR, check=True)
        subprocess.run(["git", "commit", "-m", commit_message], cwd=WORKSPACE_DIR, check=True)
        subprocess.run(["git", "push"], cwd=WORKSPACE_DIR, check=True)
        return "Successfully pushed all updates to GitHub repository!"
    except subprocess.CalledProcessError as e:
        return f"Git sync error: {e}"

# ----------------- 3. DRAFT PREVIEW TOOL -----------------

@mcp.tool()
def generate_draft_preview(visual_prompt: str) -> str:
    """Generates an image preview URL for human review."""
    return f"https://picsum.photos/seed/{abs(hash(visual_prompt)) % 1000}/800/800"

if __name__ == "__main__":
    mcp.run()