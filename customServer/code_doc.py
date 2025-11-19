

from mcp.server.fastmcp import FastMCP
import os
import ast
import re
import json
from datetime import datetime
from pygments.lexers import guess_lexer
from pygments.util import ClassNotFound
from typing import List, Tuple, Dict, Any

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
# Helpers: Markdown builders
# ================================
def md_section(title: str, content: str, level: int = 3) -> str:
    return f"{'#' * level} {title}\n{content}\n\n"


def code_block(lang: str, content: str) -> str:
    return f"```{lang}\n{content}\n```\n\n"


def safe_join(lines: List[str]) -> str:
    return "\n".join(lines)


# ================================
# Language detection
# ================================
EXT_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".java": "java",
    ".go": "go",
    ".cpp": "cpp",
    ".c": "c",
    ".cs": "csharp",
    ".php": "php",
    ".rb": "ruby",
    ".rs": "rust",
    ".swift": "swift",
    ".kt": "kotlin",
    ".scala": "scala",
}


def detect_language_from_code(code: str) -> str:
    try:
        name = guess_lexer(code).name.lower()
        # Pygments returns names like "Python", "JavaScript", "TypeScript"
        return name
    except ClassNotFound:
        return "unknown"


def detect_language_from_path(path: str) -> str:
    _, ext = os.path.splitext(path)
    return EXT_MAP.get(ext.lower(), "unknown")


# ================================
# Python AST parsing (detailed)
# ================================
def parse_python(code: str) -> Tuple[List[str], List[str]]:
    """
    Return (docs_lines, notes_lines)
    - docs_lines: markdown sections describing classes, methods, functions
    - notes_lines: summary notes (short per-item lines)
    """
    docs: List[str] = []
    notes: List[str] = []

    try:
        tree = ast.parse(code)
    except Exception as e:
        notes.append("Python AST parse error.")
        notes.append(str(e))
        docs.append(md_section("Parse Error", f"Failed to parse Python code: `{e}`", level=2))
        return docs, notes

    module_doc = ast.get_docstring(tree) or "No module-level description provided."
    docs.append(md_section("Module Description", module_doc, level=2))

    # Build class map for inheritance summary
    classes_info: Dict[str, Dict[str, Any]] = {}

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            cls_name = node.name
            bases = []
            for b in node.bases:
                try:
                    bases.append(ast.unparse(b))
                except Exception:
                    # fallback to ast.Name if possible
                    if isinstance(b, ast.Name):
                        bases.append(b.id)
                    else:
                        bases.append("unknown")
            cls_doc = ast.get_docstring(node) or "No class docstring provided."
            methods: List[Dict[str, Any]] = []

            # scan for methods inside class
            for cnode in node.body:
                if isinstance(cnode, ast.FunctionDef):
                    m_name = cnode.name
                    # parameters (skip 'self' if present)
                    params = []
                    for arg in cnode.args.args:
                        params.append(arg.arg)
                    # attempt to detect return annotation
                    try:
                        ret = ast.unparse(cnode.returns) if cnode.returns else "varies"
                    except Exception:
                        ret = "varies"
                    m_doc = ast.get_docstring(cnode) or "No method docstring provided."
                    methods.append({
                        "name": m_name,
                        "params": params,
                        "returns": ret,
                        "doc": m_doc
                    })

            classes_info[cls_name] = {
                "name": cls_name,
                "bases": bases,
                "doc": cls_doc,
                "methods": methods
            }

    # Document classes
    if classes_info:
        for cname, info in classes_info.items():
            header = f"{cname}"
            if info["bases"]:
                header = f"{cname}({', '.join(info['bases'])})"
            docs.append(md_section(f"Class: {header}", info["doc"], level=3))

            notes.append(f"- Class: {cname} | Inherits: {', '.join(info['bases']) or 'None'}")

            if info["methods"]:
                docs.append("#### Methods\n\n")
                for m in info["methods"]:
                    # signature: skip 'self' in display params
                    display_params = [p for p in m["params"] if p != "self"]
                    docs.append(md_section(f"`{m['name']}({', '.join(display_params)})`", m["doc"], level=4))
                    # Parameters block
                    if display_params:
                        docs.append("**Parameters:**\n\n")
                        for p in display_params:
                            docs.append(f"- **{p}** (`variable`): Parameter used by this method.\n\n")
                    else:
                        docs.append("**Parameters:**\n\n- None\n\n")
                    # Returns
                    docs.append("**Returns:**\n\n")
                    docs.append(f"- `{m['returns']}`: Return value (inferred or 'varies').\n\n")
                    # Example usage (method call examples)
                    example_params = ", ".join("..." for _ in display_params)
                    example = (
                        f"# Example usage of {m['name']}()\n"
                        f"instance = {cname}(...)\n"
                        f"result = instance.{m['name']}({example_params})\n"
                        f"print(result)"
                    )
                    docs.append(code_block("python", example))
                    notes.append(f"  - Method: {m['name']} | Params: {', '.join(display_params) or 'None'} | Returns: {m['returns']}")
            else:
                docs.append("No methods detected in this class.\n\n")
                notes.append("  - No methods detected.")
            docs.append("---\n")
    else:
        docs.append("No classes detected in module.\n\n")

    # Top-level functions (not in classes)
    top_funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
    if top_funcs:
        docs.append(md_section("Top-level Functions", "The following are module-level functions.", level=2))
        for fn in top_funcs:
            fname = fn.name
            params = [a.arg for a in fn.args.args]
            fdoc = ast.get_docstring(fn) or "No function docstring provided."
            try:
                ret = ast.unparse(fn.returns) if fn.returns else "varies"
            except Exception:
                ret = "varies"

            docs.append(md_section(f"`{fname}({', '.join(params)})`", fdoc, level=4))
            docs.append("**Parameters:**\n\n")
            if params:
                for p in params:
                    docs.append(f"- **{p}** (`variable`)\n\n")
            else:
                docs.append("- None\n\n")
            docs.append("**Returns:**\n\n")
            docs.append(f"- `{ret}`\n\n")
            example = (
                f"# Example usage of {fname}()\n"
                f"result = {fname}({', '.join('...' for _ in params)})\n"
                f"print(result)"
            )
            docs.append(code_block("python", example))
            notes.append(f"- Function: {fname} | Params: {', '.join(params) or 'None'} | Returns: {ret}")
            docs.append("---\n")
    else:
        # if no top-level functions, mention it
        docs.append("No top-level functions detected.\n\n")

    # Inheritance summary (compact)
    if classes_info:
        docs.append(md_section("Class Inheritance Summary", "\n".join(
            f"- **{n}** inherits from: {', '.join(info['bases']) or 'None'}" for n, info in classes_info.items()
        ), level=2))

    return docs, notes


# ================================
# Generic non-Python parsing
# (lightweight structured output)
# ================================
GENERIC_CLASS_RE = re.compile(r"\bclass\s+([A-Za-z_][A-Za-z0-9_]*)")
# capture common function patterns with name and param-list (JS/TS/Java/C-like)
GENERIC_FUNC_RE = re.compile(
    r"(?:function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\((.*?)\))|"
    r"(?:([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\(.*?\)\s*=>)|"  # arrow assigned to variable
    r"(?:([A-Za-z_][A-Za-z0-9_]*)\s*\((.*?)\)\s*\{)"  # C-style functions
    , re.S
)


def parse_generic(code: str, language_name: str) -> Tuple[List[str], List[str]]:
    docs: List[str] = []
    notes: List[str] = []

    docs.append(md_section("Module Description", f"Auto-generated documentation for {language_name}.", level=2))

    classes = GENERIC_CLASS_RE.findall(code)
    if classes:
        for c in classes:
            docs.append(md_section(f"Class: {c}", "Auto-detected class. Please verify attributes and methods.", level=3))
            example = f"{c} instance = new {c}();"
            docs.append(code_block(language_name.split()[0].lower() if language_name != "unknown" else "", example))
            notes.append(f"- Class: {c}")
            docs.append("---\n")
    else:
        notes.append("No classes detected (generic parsing).")

    # functions
    func_matches = GENERIC_FUNC_RE.findall(code)
    found_funcs = []
    for match in func_matches:
        # match groups vary; pick the non-empty ones
        name = None
        params = ""
        # group order: (g1, g2, g3, g4, g5, g6?) depending on regex; simplify
        for grp in match:
            if grp and "(" not in grp:  # crude filter to find names
                # some groups contain names, some params; better to inspect positions
                pass
        # fallback: try JS/TS style function names
    # simpler generic fallback: capture tokens like "name(" occurrences
    simple_funcs = re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)\s*\{", code)
    if simple_funcs:
        for name, params in simple_funcs:
            param_list = [p.strip() for p in params.split(",") if p.strip()]
            docs.append(md_section(f"`{name}({', '.join(param_list)})`", "Auto-detected function.", level=4))
            if param_list:
                docs.append("**Parameters:**\n\n")
                for p in param_list:
                    docs.append(f"- **{p}** (`variable`)\n\n")
            else:
                docs.append("**Parameters:**\n\n- None\n\n")
            docs.append("**Returns:**\n\n- Depends on implementation.\n\n")
            example = f"{name}({', '.join('...' for _ in param_list)});"
            docs.append(code_block(language_name.split()[0].lower() if language_name != "unknown" else "", example))
            notes.append(f"- Function: {name} | Params: {', '.join(param_list) or 'None'}")
            docs.append("---\n")
    else:
        notes.append("No functions detected (generic parsing).")

    return docs, notes


# ================================
# Main generator: language-agnostic
# ================================
def build_documentation_for_code(code: str, source_hint: str = "") -> Tuple[str, str]:
    """
    Returns (doc_markdown, note_text)
    Always returns non-empty notes.
    """
    # metadata
    detected = detect_language_from_code(code)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    header_lines = [
        f"# {detected.capitalize()} Module Documentation",
        "\n---\n",
    ]
    docs_lines: List[str] = header_lines.copy()
    notes_lines: List[str] = []

    # always include meta notes
    notes_lines.append(f"Detected Language: {detected}")
    notes_lines.append(f"Source hint: {source_hint or 'N/A'}")
    notes_lines.append(f"Character count: {len(code)}")
    notes_lines.append(f"Line count: {len(code.splitlines())}")
    notes_lines.append(f"Generated at: {timestamp}\n")

    # Python -> rich AST
    if "python" in detected.lower():
        p_docs, p_notes = parse_python(code)
        docs_lines.extend(p_docs)
        notes_lines.extend(p_notes)
    else:
        # generic parsing (best-effort)
        g_docs, g_notes = parse_generic(code, detected)
        docs_lines.extend(g_docs)
        notes_lines.extend(g_notes)

    # universal error-handling section
    docs_lines.append(md_section("Error Handling", "Validate inputs and handle exceptions consistently. See examples in your language docs.", level=2))
    notes_lines.append("Static analysis completed.")

    # ensure notes always non-empty
    if not notes_lines:
        notes_lines.append("No items detected; empty analysis result.")

    return safe_join(docs_lines), safe_join(notes_lines)


# ================================
# MCP tool: main entry - accepts code string
# ================================
@mcp.tool()
def generate_documentation(code: str, source_hint: str = "") -> str:
    """
    Generate documentation markdown and notes from a code string.
    Returns user-facing string pointing to saved files.
    """
    detected = detect_language_from_code(code)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    doc_filename = f"documentation_{detected}_{timestamp}.md"
    note_filename = f"notes_{detected}_{timestamp}.txt"
    doc_path = os.path.join(DOCS_DIR, doc_filename)
    note_path = os.path.join(NOTES_DIR, note_filename)

    doc_md, notes_text = build_documentation_for_code(code, source_hint)

    # write files (utf-8)
    with open(doc_path, "w", encoding="utf-8") as f:
        f.write(doc_md)
    with open(note_path, "w", encoding="utf-8") as f:
        f.write(notes_text)

    return f"✅ Documentation saved to `{doc_path}`\n🗒️ Notes saved to `{note_path}`"


# ================================
# MCP command: generate docs from file path
# ================================
@mcp.command()
def generate_from_path(path: str) -> dict:
    """
    Read a file on disk and generate documentation + notes.
    Returns metadata JSON with paths.
    """
    if not os.path.exists(path):
        return {"status": "error", "message": f"Path not found: {path}"}
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            code = fh.read()
    except Exception as e:
        return {"status": "error", "message": f"Unable to read file: {e}"}

    doc_md, notes_text = build_documentation_for_code(code, source_hint=path)

    detected = detect_language_from_path(path)
    if detected == "unknown":
        detected = detect_language_from_code(code)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    doc_filename = f"documentation_{os.path.basename(path)}_{detected}_{timestamp}.md"
    note_filename = f"notes_{os.path.basename(path)}_{detected}_{timestamp}.txt"
    doc_path = os.path.join(DOCS_DIR, doc_filename)
    note_path = os.path.join(NOTES_DIR, note_filename)

    with open(doc_path, "w", encoding="utf-8") as f:
        f.write(doc_md)
    with open(note_path, "w", encoding="utf-8") as f:
        f.write(notes_text)

    return {"status": "success", "doc": doc_path, "notes": note_path, "language": detected}


# ================================
# Run server (if executed directly)
# ================================
if __name__ == "__main__":
    mcp.run()
