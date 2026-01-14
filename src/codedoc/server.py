from mcp.server.fastmcp import FastMCP
import os
import sys
import re
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
        # content += f"## 3. Source Code\n```{language}\n{final_code}\n```"

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

# Refactoring & Optimization
@mcp.tool()
async def refactor_and_optimize(file_path: str, custom_rules: str = "") -> str:
    """
    Refactors and optimizes code. 
    Handles case-insensitivity and deep path discovery.
    """
    import os

    # 1. FORCE THE CORRECT PROJECT ROOT
    # We look at the current working directory but prioritize the actual file name
    project_root = os.path.abspath(".")
    target_filename = os.path.basename(file_path).lower() # Case-insensitive
    resolved_path = None
    matches = []

    # 2. AGGRESSIVE SEARCH
    for root, dirs, files in os.walk(project_root):
        # Security: Prune restricted folders
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['venv', 'node_modules', 'Library']]
        
        for f in files:
            if f.lower() == target_filename:
                matches.append(os.path.join(root, f))

    # 3. SMART PATH SELECTION
    if not matches:
        return f"Error: '{file_path}' not found in {project_root}. Please ensure you have the file open in Cursor."
        
    if len(matches) > 1:
        rel_paths = [os.path.relpath(m, project_root) for m in matches]
        return f"Multiple matches found. Which one should I refactor?\n" + "\n".join([f"- {p}" for p in rel_paths])
    
    resolved_path = matches[0]

    # 4. EXECUTE REFACTOR
    try:
        with open(resolved_path, "r", encoding="utf-8") as f:
            code_content = f.read()

        # Build a robust AI Prompt
        return f"""
        TASK: Refactor the code for {os.path.basename(resolved_path)}
        PROJECT_PATH: {os.path.relpath(resolved_path, project_root)}
        
        RULES: {custom_rules if custom_rules else "Apply SOLID, OOPS, and Clean Code standards."}
        
        ORIGINAL_CODE:
        ---
        {code_content}
        ---
        
        INSTRUCTION: Provide the refactored code block only. Cursor will help the user apply changes.
        """
    except Exception as e:
        return f"Access Error: {str(e)}"

# Health Audit and Refactoring
@mcp.tool()
async def evaluate_and_refactor(file_path: str, custom_rules: str = "") -> str:
    """
    Language-agnostic --- health audit AND generates optimized code.
    """
    import os

    # 1. SEARCH
    project_root = os.path.abspath(os.getcwd())
    target_name = os.path.basename(file_path)
    resolved_path = None

    for root, dirs, files in os.walk(project_root):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'venv', 'bin', 'obj']]
        if target_name in files:
            resolved_path = os.path.join(root, target_name)
            break

    if not resolved_path:
        return f"Error: Could not find '{target_name}' in the project."

    # 2. FILE METADATA
    ext = os.path.splitext(resolved_path)[1].lower()
    
    try:
        with open(resolved_path, "r", encoding="utf-8") as f:
            code_content = f.read()

        # 3. UNIFIED ARCHITECT PROMPT
        return f"""
        ROLE: Senior Multi-Language Architect
        TASK: Audit and Refactor the provided {ext} file.
        
        FILE_PATH: {os.path.relpath(resolved_path, project_root)}

        --- STEP 1: HEALTH AUDIT ---
        Analyze the code for SOLID compliance, OOPS patterns, and language-specific best practices.
        Generate a Score (1-10) and a Health Report.

        --- STEP 2: OPTIMIZATION ---
        Refactor the code to address every weakness identified in Step 1.
        USER RULES: {custom_rules if custom_rules else "Apply standard high-quality optimizations."}

        CODE TO PROCESS:
        ---
        {code_content}
        ---

        OUTPUT FORMAT REQUIREMENT:
        1. Start with the "## 🩺 Code Health Report" section (Score, Findings, Risk).
        2. Then provide the "## 🛠️ Optimized Code" section.
        3. Provide the refactored code in a standard markdown block. 
           (Note: Cursor will automatically detect this and show the 'Apply' button).
        4. End with a "## 🏁 Final Verdict" explaining why this version is production-ready.
        """
    except Exception as e:
        return f"Processing Error: {str(e)}"

# impact analysis
@mcp.tool()
async def predict_impact(file_path: str) -> str:
    """
    Scans the entire project to find files that depend on the given file.
    Identifies 'Impacted Files' and potential breaking changes.
    """

    project_root = os.path.abspath(os.getcwd())
    target_name = os.path.basename(file_path)
    # Remove extension to find imports like 'from ./Login' or 'import Login'
    base_name = os.path.splitext(target_name)[0]
    
    impacted_files = []

    # 1. SCAN THE PROJECT
    for root, dirs, files in os.walk(project_root):
        # Skip hidden and heavy folders
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'venv', 'dist', 'bin']]
        
        for file in files:
            if file == target_name: continue # Skip the target itself
            
            file_full_path = os.path.join(root, file)
            try:
                with open(file_full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Check for import patterns (e.g., import ... from './Login')
                    # This regex is language-agnostic enough for JS, TS, Python, etc.
                    if re.search(rf"(['\"/]){base_name}(['\"])", content):
                        impacted_files.append(os.path.relpath(file_full_path, project_root))
            except:
                continue

    if not impacted_files:
        return f"✅ **Low Impact:** No external dependencies found for `{target_name}`. It is safe to refactor."

    # 2. GENERATE THE ANALYSIS REPORT
    report = f"## Analysis for `{target_name}`\n"
    report += f"**Detected {len(impacted_files)} dependent files.** A change here may break the following:\n\n"
    
    for f in impacted_files:
        report += f"- 📁 `{f}`\n"
    
    report += "\n### Architect's Recommendation\n"
    report += "Before applying changes, use `@codedoc` to verify the entry points in the files listed above."
    
    return report

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()