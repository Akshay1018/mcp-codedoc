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

@mcp.tool()
async def refactor_and_optimize(file_path: str, custom_rules: str = "") -> str:
    """
    Refactors and optimizes a file within the current project.
    Only accesses the directory where the server was started to avoid OS popups.
    """
    import os

    # 1. STRICT SECURITY BOUNDARY
    # We use the absolute path of the current directory to lock the search.
    project_root = os.path.abspath(os.getcwd())
    resolved_path = None

    # 2. FILE SEARCH (Restricted to project_root)
    target_name = os.path.basename(file_path)
    
    # Check if the file is directly in the root first
    direct_path = os.path.join(project_root, target_name)
    if os.path.exists(direct_path) and os.path.isfile(direct_path):
        resolved_path = direct_path
    else:
        # Search subdirectories only
        matches = []
        for root, dirs, files in os.walk(project_root):
            # SECURITY: Instantly prune hidden folders and system-heavy folders
            # This prevents triggering OS security warnings for system files.
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['Library', 'Documents', 'Downloads']]
            
            if target_name in files:
                matches.append(os.path.join(root, target_name))
        
        if not matches:
            return f"Error: '{target_name}' not found in the project directory: {project_root}"
        
        if len(matches) > 1:
            rel_paths = [os.path.relpath(m, project_root) for m in matches]
            return f"⚠️ Multiple files found. Please specify the path:\n" + "\n".join([f"- {p}" for p in rel_paths])
        
        resolved_path = matches[0]

    # 3. REFACTORING PAYLOAD
    try:
        with open(resolved_path, "r") as f:
            code_content = f.read()

        ext = os.path.splitext(resolved_path)[1]
        
        # We wrap the response in a clear instruction for the AI (Claude)
        return f"""
        ACT AS: Senior Software Architect
        TASK: Refactor the provided code file.
        FILE_NAME: {os.path.relpath(resolved_path, project_root)}
        
        RULES TO FOLLOW:
        {custom_rules if custom_rules else "Apply SOLID principles, OOPS patterns, and Clean Code standards."}
        
        CODE_CONTENT:
        ---
        {code_content}
        ---
        
        INSTRUCTION: 
        Provide only the refactored code. Do not generate documentation unless explicitly asked in a separate prompt.
        """

    except Exception as e:
        return f"Access Error: {str(e)}"

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()