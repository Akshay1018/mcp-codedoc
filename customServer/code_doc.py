import os
import ast
import textwrap
from datetime import datetime
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("CodeDoc")

# === Create documentation directory ===
BASE_DIR = os.path.dirname(__file__)
DOCS_DIR = os.path.join(BASE_DIR, "documentation")
os.makedirs(DOCS_DIR, exist_ok=True)

# === Generate timestamped doc filename ===
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
DOC_FILE = os.path.join(DOCS_DIR, f"documentation_{timestamp}.md")



def md_section(title: str, content: str) -> str:
    """Format text into markdown section."""
    wrapped = textwrap.fill(content, width=100)
    return f"### {title}\n\n{wrapped}\n\n"


@mcp.tool()
def generate_documentation(code: str) -> str:
    """
    Generate **professional Markdown documentation** for the given Python code.
    """

    try:
        tree = ast.parse(code)
    except Exception as e:
        return f"❌ Error parsing code: {e}"

    # === Header ===
    docs = []
    module_name = "Documentation"
    docs.append(f"# {module_name}\n")
    docs.append("---\n")

    module_doc = ast.get_docstring(tree)
    overview = (
        module_doc
        or "This module provides core functionalities and reusable components for business logic."
    )
    docs.append(md_section("Overview", overview))

    # === Function sections ===
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            params = [arg.arg for arg in node.args.args]
            docstring = ast.get_docstring(node) or "No description provided."

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
            ret = getattr(node, 'returns', None)
            ret_type = ast.unparse(ret) if ret else "varies"
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
                f"The `{func_name}` function was auto-documented using static code analysis. "
                "Please validate return types, exceptions, and examples based on your project’s actual behavior."
            )
            docs.append(md_section("Notes", note_text))

            docs.append("---\n")

    # === Error Handling Section ===
    docs.append("## Error Handling\n")
    docs.append(
        "All functions should perform **input validation** and raise meaningful errors (e.g., "
        "`ValueError`, `TypeError`) where applicable.\n"
    )
    docs.append(
        "Example:\n\n```python\n"
        "try:\n"
        "    result = your_function(...)\n"
        "except ValueError as e:\n"
        "    print(e)\n```\n"
    )

    # === Save the documentation ===
    full_doc = "\n".join(docs)
    with open(DOC_FILE, "w") as f:
        f.write(full_doc)

    return f"✅ Markdown documentation successfully generated.\n📄 Saved at: {DOC_FILE}"