from mcp.server.fastmcp import FastMCP
import os
import ast
import re
from datetime import datetime
from pygments.lexers import guess_lexer
from pygments.util import ClassNotFound

mcp = FastMCP("CodeDoc")

# ================================
# Base directories
# ================================
BASE_DIR = os.path.dirname(__file__)
DOCS_DIR = os.path.join(BASE_DIR, "documentation")
NOTES_DIR = os.path.join(BASE_DIR, "documentation_notes")

os.makedirs(DOCS_DIR, exist_ok=True)
os.makedirs(NOTES_DIR, exist_ok=True)


# ================================
# Helper: Markdown section builder
# ================================
def md_section(title: str, content: str) -> str:
    return f"### {title}\n{content}\n"


# ================================
# Helper: Detect language
# ================================
def detect_language(code: str) -> str:
    try:
        return guess_lexer(code).name
    except ClassNotFound:
        return "Unknown"


# ================================
# Helper: Extract functions/classes for non-Python languages
# ================================
def extract_generic(code: str):
    classes = re.findall(r"\bclass\s+([A-Za-z_]\w*)", code)

    # Matches many languages: JS, TS, C, C++, Java, Go, PHP
    funcs = re.findall(
        r"(?:public|private|protected)?\s*(?:static)?\s*[A-Za-z0-9_<>\[\]]+\s+([A-Za-z_]\w*)\s*\((.*?)\)",
        code
    )

    return classes, funcs


# ================================
# TOOL: Generate Documentation
# ================================
@mcp.tool()
def generate_documentation(code: str) -> str:
    """
    Generate comprehensive documentation for ANY programming language.
    Creates:
    - 📘 Full markdown documentation
    - 🗒️ Summary notes
    """

    language = detect_language(code)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

    doc_path = os.path.join(DOCS_DIR, f"documentation_{language}_{timestamp}.md")
    note_path = os.path.join(NOTES_DIR, f"notes_{timestamp}.txt")

    docs = []
    notes = []

    # ================================
    # HEADER + OVERVIEW
    # ================================
    docs.append(f"# {language} Module Documentation\n")
    docs.append("---\n")

    docs.append(md_section(
        "Overview",
        f"This automatically generated documentation provides a comprehensive summary of "
        f"the structure and functionality of the detected **{language}** source code."
    ))

    # ================================
    # PYTHON HANDLING (AST)
    # ================================
    if language.lower() == "python":
        try:
            tree = ast.parse(code)
        except Exception as e:
            return f"❌ Unable to parse Python code: {e}"

        module_doc = ast.get_docstring(tree) or "General-purpose Python module."
        docs.append(md_section("Module Description", module_doc))

        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                func_name = node.name
                params = [a.arg for a in node.args.args]
                docstring = ast.get_docstring(node) or "No description provided."

                ret = getattr(node, "returns", None)
                ret_type = ast.unparse(ret) if ret else "varies"

                # Function block
                docs.append(f"## `{func_name}({', '.join(params)})`\n")
                docs.append(md_section("Description", docstring))

                # Parameters
                if params:
                    docs.append("#### Parameters\n")
                    for p in params:
                        docs.append(f"- **{p}** (`variable`): Parameter for this function.\n")
                else:
                    docs.append("#### Parameters\n- None\n")

                # Returns
                docs.append("#### Returns\n")
                docs.append(f"- `{ret_type}`: Output of the function.\n")

                # Example
                example = f"""```python
result = {func_name}({', '.join('...' for _ in params)})
```"""
                docs.append(md_section("Example Usage", example))

                # Notes
                docs.append(md_section(
                    "Notes",
                    f"The `{func_name}` function was auto-documented using static AST analysis."
                ))
                docs.append("---\n")

                # Short notes
                notes.extend([
                    f"- Function: {func_name}",
                    f"- Params: {', '.join(params) or 'None'}",
                    f"- Returns: {ret_type}",
                    ""
                ])

    # ================================
    # GENERIC HANDLING (All Other Languages)
    # ================================
    else:
        classes, funcs = extract_generic(code)

        # Classes
        if classes:
            docs.append("## Classes\n")
            for c in classes:
                docs.append(f"- **{c}**: A class defined in the module.\n")
                notes.append(f"- Class: {c}")

        # Functions
        if funcs:
            docs.append("\n## Functions / Methods\n")
            for func_name, params in funcs:
                param_list = [p.strip() for p in params.split(",") if p.strip()]

                docs.append(f"### `{func_name}({', '.join(param_list)})`\n")
                docs.append("**Description:** Auto-detected function.\n")

                docs.append("#### Parameters\n")
                if param_list:
                    for p in param_list:
                        docs.append(f"- **{p}**: Function parameter.\n")
                else:
                    docs.append("- None\n")

                docs.append("#### Returns\n- Depends on implementation.\n")

                example = f"""```{language.lower()}
{func_name}({', '.join('...' for _ in param_list)});
```"""
                docs.append(md_section("Example Usage", example))

                docs.append(md_section(
                    "Notes",
                    f"The `{func_name}` function was parsed using generic static analysis."
                ))

                docs.append("---\n")

                notes.extend([
                    f"- Function: {func_name}",
                    f"- Params: {', '.join(param_list) or 'None'}",
                    ""
                ])

    # ================================
    # ERROR HANDLING SECTION
    # ================================
    docs.append("## Error Handling\n")
    docs.append(
        "Ensure proper error and exception handling using techniques such as "
        "`try/catch`, `throw`, validation guards, or equivalent constructs "
        "depending on the programming language.\n"
    )

    # ================================
    # SAVE FILES
    # ================================
    with open(doc_path, "w") as f:
        f.write("\n".join(docs))

    with open(note_path, "w") as f:
        f.write("\n".join(notes))

    return (
        f"✅ Comprehensive documentation saved to `{doc_path}`\n"
        f"🗒️ Notes saved to `{note_path}`"
    )
