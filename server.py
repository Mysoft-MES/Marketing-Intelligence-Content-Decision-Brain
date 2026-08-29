import os
import requests
from fastmcp import FastMCP

# Initialize MCP Server
mcp = FastMCP("Social Content Engine")

# Base directory for storing markdown workflows
WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))

# ----------------- 1. RESEARCH & FILE STORAGE TOOLS -----------------

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
    return f"Successfully saved {filename}."

# ----------------- 2. DRAFT PREVIEW TOOL -----------------

@mcp.tool()
def generate_draft_preview(visual_prompt: str) -> str:
    """Generates an image preview URL for human review before publishing."""
    return f"https://picsum.photos/seed/{abs(hash(visual_prompt)) % 1000}/800/800"


if __name__ == "__main__":
    mcp.run()