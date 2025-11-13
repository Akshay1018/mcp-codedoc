from mcp.server.fastmcp import FastMCP
import os
import ast
from datetime import datetime

mcp = FastMCP("CodeDoc")

# Base directories
BASE_DIR = os.path.dirname(__file__)
DOCS_DIR = os.path.join(BASE_DIR, "documentation")
NOTES_DIR = os.path.join(BASE_DIR, "documentation_notes")

# Ensure folders exist
os.makedirs(DOCS_DIR, exist_ok=True)
os.makedirs(NOTES_DIR, exist_ok=True)

# -----------------------------------------------------------
# Helper: Markdown Section
# -----------------------------------------------------------
def md_section(title: str, content: str) -> str:
    return f"### {title}\n{content}\n"

# -----------------------------------------------------------
# Tool: Generate Comprehensive Documentation
# -----------------------------------------------------------
@mcp.tool()
def generate_documentation(code: str) -> str:
    """
    Generate **comprehensive Markdown documentation** for the given Python code.

    Creates:
    - 📘 Full documentation under `/documentation/`
    - 🗒️ Summary notes under `/documentation_notes/`
    """

    # === Parse code safely ===
    try:
        tree = ast.parse(code)
    except Exception as e:
        return f"❌ Error parsing code: {e}"

    # === Prepare file paths ===
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    doc_filename = f"documentation_{timestamp}.md"
    note_filename = f"notes_{timestamp}.txt"

    doc_path = os.path.join(DOCS_DIR, doc_filename)
    note_path = os.path.join(NOTES_DIR, note_filename)

    # === Build Documentation ===
    docs = []
    notes = []

    module_name = "Python Module Documentation"
    docs.append(f"# {module_name}\n")
    docs.append("---\n")

    # Overview
    module_doc = ast.get_docstring(tree)
    overview = module_doc or (
        "This module provides essential functionalities with reusable components for business logic."
    )
    docs.append(md_section("Overview", overview))

    # === Process Each Function ===
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            params = [arg.arg for arg in node.args.args]
            docstring = ast.get_docstring(node) or "No description provided."
            ret = getattr(node, 'returns', None)
            ret_type = ast.unparse(ret) if ret else "varies"

            docs.append(f"## `{func_name}({', '.join(params)})`\n")
            docs.append(md_section("Description", docstring))

            # Parameters
            if params:
                docs.append("#### Parameters\n")
                for p in params:
                    docs.append(f"- **{p}** (`variable`): Parameter used in this function.\n")
            else:
                docs.append("#### Parameters\n- None\n")

            # Returns
            docs.append("\n#### Returns\n")
            docs.append(f"- `{ret_type}`: Output value of the function.\n")

            # Example usage
            example = f"""```python
# Example usage of {func_name}()
result = {func_name}({', '.join('...' for _ in params)})
print(result)
```"""
            docs.append(md_section("Example Usage", example))

            # Notes
            note_text = (
                f"The `{func_name}` function was auto-documented using static analysis. "
                "Please verify return types, exceptions, and examples for accuracy."
            )
            docs.append(md_section("Notes", note_text))
            docs.append("---\n")

            # Add to notes
            notes.extend([
                f"- Function: {func_name}",
                f"- Description: {docstring}",
                f"- Params: {', '.join(params) or 'None'}",
                f"- Returns: {ret_type}",
                ""
            ])

    # === Error Handling Section ===
    docs.append("## Error Handling\n")
    docs.append(
        "All functions should validate inputs and raise appropriate exceptions "
        "(e.g., `ValueError`, `TypeError`) when invalid data is provided.\n"
    )
    docs.append(
        "Example:\n\n```python\n"
        "try:\n"
        "    result = your_function(...)\n"
        "except ValueError as e:\n"
        "    print(e)\n"
        "```\n"
    )

    # === Save Outputs ===
    with open(doc_path, "w") as f:
        f.write("\n".join(docs))

    with open(note_path, "w") as f:
        f.write("\n".join(notes))

    return (
        f"✅ Comprehensive documentation saved to `{doc_path}`\n"
        f"🗒️ Documentation notes saved to `{note_path}`"
    )
