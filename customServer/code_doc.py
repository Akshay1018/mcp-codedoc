import os
import ast
from datetime import datetime
from mcp.server.fastmcp import FastMCP

#=====================================================
# CodeDoc MCP Server
#=====================================================

mcp = FastMCP("CodeDoc")

# Directory setup
BASE_DIR = os.path.dirname(__file__)
DOCS_DIR = os.path.join(BASE_DIR, "documentation")
NOTES_DIR = os.path.join(BASE_DIR, "documentation_notes")

# Ensure directories exist
os.makedirs(DOCS_DIR, exist_ok=True)
os.makedirs(NOTES_DIR, exist_ok=True)

@mcp.tool()
def generate_documentation(code: str) -> str:
    """
    Generate professional documentation and store notes automatically.
    """

    # Parse code safely
    try:
        tree = ast.parse(code)
    except Exception as e:
        return f"❌ Error parsing code: {e}"

    # Generate timestamped filenames
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    doc_filename = f"documentation_{timestamp}.md"
    note_filename = f"notes_{timestamp}.txt"

    doc_path = os.path.join(DOCS_DIR, doc_filename)
    note_path = os.path.join(NOTES_DIR, note_filename)

    docs = ["# 📘 Documentation\n"]
    notes = ["# 🗒️ Documentation Notes\n"]

    # Process each function in code
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            docstring = ast.get_docstring(node) or "No description provided."
            params = [arg.arg for arg in node.args.args]
            ret = getattr(node, 'returns', None)
            returns = ast.unparse(ret) if ret else "None"

            # Add to main documentation
            docs.extend([
                f"## Function: `{func_name}`",
                f"**Description:** {docstring}",
                f"**Parameters:** {', '.join(params) or 'None'}",
                f"**Returns:** {returns}",
                "---\n"
            ])

            # Add important notes
            notes.extend([
                f"- Function: {func_name}",
                f"- Summary: {docstring}",
                f"- Parameters: {', '.join(params) or 'None'}",
                f"- Returns: {returns}",
                ""
            ])

    # Save both documentation and notes
    with open(doc_path, "w") as f:
        f.write("\n".join(docs))

    with open(note_path, "w") as f:
        f.write("\n".join(notes))

    return f"✅ Documentation saved to `{doc_path}` and notes saved to `{note_path}`"
