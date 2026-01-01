from mcp.server.fastmcp import FastMCP
import os
import sys
from datetime import datetime

mcp = FastMCP("CodeDoc", log_level="ERROR")

IGNORE_DIRS = {'node_modules', '.git', '__pycache__', 'venv', '.env', 'dist', 'build'}

@mcp.tool()
def generate_smart_doc(doc_content: str, audit_results: str, code_snippet: str = None, file_path: str = None, language: str = "auto") -> str:
    """
    Universal tool for documentation and audits.
    - file_path: Path to local file.
    - code_snippet: Pasted code from chat.
    """
    try:
        # 1. SETUP TARGET DIRECTORY
        cwd = os.getcwd()
        base_path = cwd if (cwd and cwd != "/") else os.path.dirname(os.path.abspath(__file__))
        
        target_folder = os.path.join(base_path, "documentation")
        os.makedirs(target_folder, exist_ok=True)

        display_name = ""
        final_code = ""

        if file_path:
            full_file_path = file_path if os.path.isabs(file_path) else os.path.join(base_path, file_path)
            
            if not os.path.exists(full_file_path):
                return f"Error: File not found at {full_file_path}"
                
            with open(full_file_path, "r", encoding="utf-8") as f:
                final_code = f.read()
            display_name = os.path.basename(file_path)
            
        elif code_snippet:
            final_code = code_snippet
            display_name = "snippet"
        else:
            return "Error: Provide either 'file_path' or 'code_snippet'."

        # 2. Create the output file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"documentation_{display_name.replace('.', '_')}_{timestamp}.md"
        full_path = os.path.join(target_folder, filename)

        # 3. Build Markdown
        content = f"# Technical Audit & Docs: {display_name}\n"
        content += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
        content += f"## 1. Documentation\n{doc_content}\n\n"
        content += f"## 2. Quality Audit\n{audit_results}\n\n"
        content += f"## 3. Source Code\n```{language}\n{final_code}\n```"

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f"Successfully generated at: {full_path}"

    except Exception as e:
        print(f"Server Error: {str(e)}", file=sys.stderr)
        return f"System Error: {str(e)}"

@mcp.tool()
def scan_project_files() -> list:
    """Returns a list of all documentable source files in the current project root."""
    documentable = []
    cwd = os.getcwd()
    base_path = cwd if (cwd and cwd != "/") else os.path.dirname(os.path.abspath(__file__))
    
    for root, dirs, files in os.walk(base_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file in files:
            if file.endswith(('.py', '.js', '.ts', '.java', '.cpp', '.cs')):
                rel_path = os.path.relpath(os.path.join(root, file), base_path)
                documentable.append(rel_path)
    return documentable

# New Phase 2 Tool: Refactoring & Optimization
@mcp.tool()
async def refactor_and_optimize(file_path: str, custom_rules: str = "") -> str:
    """
    Refactors and optimizes code. Automatically finds files in subdirectories.
    Supports SOLID, OOPS, and custom development rules.
    """
    import os

    # --- START SMART PATH RESOLUTION ---
    resolved_path = None
    
    # Check if the path is already correct/absolute
    if os.path.exists(file_path) and os.path.isfile(file_path):
        resolved_path = file_path
    else:
        # Recursive search for the filename
        matches = []
        filename_to_find = os.path.basename(file_path)
        
        for root, _, files in os.walk("."):
            # Exclude hidden/system dirs like .git or .venv
            if any(part.startswith('.') for part in root.split(os.sep)):
                continue
                
            if filename_to_find in files:
                matches.append(os.path.join(root, filename_to_find))
        
        if not matches:
            return f"Error: File '{file_path}' not found in the project."
            
        if len(matches) > 1:
            file_list = "\n".join([f"- {m}" for m in matches])
            return f"⚠️ Warning: Multiple files found for '{filename_to_find}':\n{file_list}\n\nPlease provide the full path to continue."
        
        resolved_path = matches[0]
    # --- END SMART PATH RESOLUTION ---

    try:
        with open(resolved_path, "r") as f:
            code_content = f.read()

        ext = os.path.splitext(resolved_path)[1]
        default_rules = """
        1. Performance: Optimize loops and reduce redundant computations.
        2. Clean Code: Meaningful names, Single Responsibility Principle.
        3. Readability: Simplify complex nested logic and remove duplicate code.
        """

        refactor_payload = f"""
        FILE: {resolved_path} (Language: {ext})
        
        ACTION: Refactor and optimize the code below.
        
        USER SPECIFIED RULES:
        {custom_rules if custom_rules else "No specific rules provided. Use default optimizations."}
        
        DEFAULT QUALITY GUARDRAILS:
        {default_rules}
        
        CODE TO PROCESS:
        ---
        {code_content}
        ---
        
        OUTPUT REQUIREMENT:
        Provide ONLY the refactored code block. Ensure it is bug-free and follows requested principles (SOLID, OOPS, etc.).
        """
        
        return refactor_payload

    except Exception as e:
        return f"Refactoring Error: {str(e)}"

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()