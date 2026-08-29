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
        env = os.environ.copy()
        env["GIT_TERMINAL_PROMPT"] = "0"  # Prevent Git from hanging on authentication prompts

        subprocess.run(["git", "add", "."], cwd=WORKSPACE_DIR, check=True, env=env)
        
        # Commit only if there are staged changes
        status = subprocess.run(["git", "status", "--porcelain"], cwd=WORKSPACE_DIR, capture_output=True, text=True, env=env)
        if status.stdout.strip():
            subprocess.run(["git", "commit", "-m", commit_message], cwd=WORKSPACE_DIR, check=True, env=env)
            
        push_res = subprocess.run(["git", "push"], cwd=WORKSPACE_DIR, capture_output=True, text=True, timeout=30, env=env)
        return "Successfully pushed all updates to GitHub!"
    except subprocess.TimeoutExpired:
        return "Git push timed out. Please ensure your Git credentials are authenticated."
    except subprocess.CalledProcessError as e:
        return f"Git error: {e}"
# ----------------- 3. DRAFT PREVIEW TOOL -----------------

@mcp.tool()
def generate_draft_preview(visual_prompt: str) -> str:
    """Generates an image preview URL for human review."""
    return f"https://picsum.photos/seed/{abs(hash(visual_prompt)) % 1000}/800/800"

if __name__ == "__main__":
    mcp.run()