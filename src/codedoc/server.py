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
        1. Start with the "## Code Health Report" section (Score, Findings, Risk).
        2. Then provide the "##  Optimized Code" section.
        3. Provide the refactored code in a standard markdown block. 
           (Note: Cursor will automatically detect this and show the 'Apply' button).
        4. End with a "## 🏁 Final Verdict" explaining why this version is production-ready.
        """
    except Exception as e:
        return f"Processing Error: {str(e)}"

# impact analysis
@mcp.tool()
async def predict_impact(file_path: str, symbol: str = None) -> str:
    """
    Analyzes the impact of changing a specific symbol (variable, function, or class).
    If no symbol is provided, it analyzes dependencies on the file itself.
    """
    import os
    # import re

    project_root = os.path.abspath(os.getcwd())
    target_name = os.path.basename(file_path)
    
    # If the user says "rename fetchData", symbol will be "fetchData"
    # If no symbol, we default to the file name (base_name)
    search_query = symbol if symbol else os.path.splitext(target_name)[0]
    
    impacted_locations = []
    ALLOWED_EXTS = {'.ts', '.tsx', '.js', '.py', '.java', '.cs', '.cpp', '.h'}

    for root, dirs, files in os.walk(project_root):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'dist', 'bin']]
        
        for file in files:
            if os.path.splitext(file)[1].lower() not in ALLOWED_EXTS:
                continue
            
            full_path = os.path.join(root, file)
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    # Search line-by-line to give the user exact line numbers
                    for i, line in enumerate(f, 1):
                        if search_query in line:
                            rel_path = os.path.relpath(full_path, project_root)
                            impacted_locations.append(f"{rel_path} (Line {i})")
            except:
                continue

    if not impacted_locations:
        return f" No external references to `{search_query}` found. Change appears safe."

    # deduplicate and format
    unique_files = list(set([loc.split(' (')[0] for loc in impacted_locations]))
    
    report = f"## Impact Analysis for `{search_query}`\n"
    report += f"Found **{len(impacted_locations)}** references in **{len(unique_files)}** files.\n\n"
    report += "**Affected Files:**\n" + "\n".join([f"- {f}" for f in unique_files[:5]])
    
    if len(unique_files) > 5:
        report += f"\n...and {len(unique_files)-5} more files."
        
    report += "\n\n**Architect Note:** Changing this symbol will break these references. Ensure you use a 'Global Rename' or update these call-sites."
    return report

# security scan
@mcp.tool()
async def global_security_audit() -> str:
    """
    Scans the ENTIRE project for secrets, keys, and vulnerabilities.
    Use this before pushing code to GitHub/GitLab.
    """
    import os
    import re

    project_root = os.path.abspath(os.getcwd())
    
    # Define what we are looking for
    RULES = {
        "Cloud API Key": r"(AIzaSy[0-9A-Za-z-_]{33}|AKIA[0-9A-Z]{16})",
        "Sensitive Variable": r"(?i)(password|secret|token|apikey|api_key|private_key)\s*[:=]\s*['\"].{8,}?['\"]",
        "Connection String": r"(mongodb|postgres|mysql):\/\/[^\s'\"@]+:[^\s'\"@]+@[^\s'\"]+",
        "Private Key": r"-----BEGIN [A-Z ]+ PRIVATE KEY-----"
    }

    critical_findings = []
    
    # Walk through every file in the project
    for root, dirs, files in os.walk(project_root):
        # SKIP heavy/irrelevant folders
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'venv', 'dist', 'build']]
        
        for file in files:
            # Only scan code files
            if not file.endswith(('.ts', '.tsx', '.js', '.py', '.java', '.cs', '.cpp', '.h', '.env', '.yaml', '.yml')):
                continue
                
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line_num, line in enumerate(f, 1):
                        for name, pattern in RULES.items():
                            if re.search(pattern, line):
                                rel_path = os.path.relpath(file_path, project_root)
                                critical_findings.append(f"📁 `{rel_path}` | Line {line_num}: **{name}**")
            except:
                continue

    if not critical_findings:
        return "**Project Scan Complete:** No secrets found. You are safe to push!"

    # 3. FORMAT THE REPORT
    report = "## Global Security Audit Results\n"
    report += f"Found **{len(critical_findings)}** potential security leaks:\n\n"
    report += "\n".join(critical_findings[:15]) # Cap at 15 to prevent text overflow
    
    if len(critical_findings) > 15:
        report += f"\n\n...and {len(critical_findings) - 15} more leaks."
        
    report += "\n\n**Action Required:** Neutralize these secrets or move them to a `.gitignore`'d environment file."
    return report

# Scan Uncommitted Files for Security Risks and Vulnerabilities
@mcp.tool()
async def guardian_scan(target_path: str = None, scan_uncommitted: bool = False) -> str:
    """
    Versatile security scanner.
    - If scan_uncommitted is True: Scans only changed files in Git.
    - If target_path is provided: Scans that specific file or folder.
    - Default: Scans current working directory.
    """
    import os
    import re
    import subprocess

    project_root = os.path.abspath(os.getcwd())
    files_to_scan = []

    # 1. STRATEGY: Find the files to scan
    if scan_uncommitted:
        try:
            # Get list of modified and untracked files from Git
            cmd = "git ls-files --others --modified --exclude-standard"
            output = subprocess.check_output(cmd, shell=True, cwd=project_root).decode()
            files_to_scan = [os.path.join(project_root, f) for f in output.splitlines()]
        except Exception:
            return "Error: This project doesn't seem to be a Git repository."
    
    elif target_path:
        # User specified a file or folder
        full_path = os.path.abspath(target_path)
        if os.path.isdir(full_path):
            for root, dirs, files in os.walk(full_path):
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'venv']]
                for f in files:
                    files_to_scan.append(os.path.join(root, f))
        else:
            files_to_scan.append(full_path)
            
    else:
        # Default: Fast walk of the current root
        for root, dirs, files in os.walk(project_root):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'venv']]
            for f in files:
                files_to_scan.append(os.path.join(root, f))

    # 2. THE SCAN (Optimized)
    RULES = {
        "Hardcoded Secret": r"(?i)(api[_-]?key|secret|token|passwd)[\s]*[:=][\s]*['\"][a-zA-Z0-9_\-\.]{10,}['\"]",
        "Private Key": r"-----BEGIN [A-Z ]+ PRIVATE KEY-----",
        "Connection String": r"(mongodb|postgres|mysql):\/\/[^\s'\"@]+:[^\s'\"@]+@[^\s'\"]+",
    }

    findings = []
    for f_path in files_to_scan:
        if not f_path.endswith(('.ts', '.tsx', '.js', '.py', '.java', '.cs', '.cpp', '.env')):
            continue
        try:
            with open(f_path, "r", encoding="utf-8", errors="ignore") as f:
                for line_num, line in enumerate(f, 1):
                    for name, pattern in RULES.items():
                        if re.search(pattern, line):
                            rel = os.path.relpath(f_path, project_root)
                            findings.append(f" **{name}** in `{rel}` (Line {line_num})")
        except: continue

    if not findings:
        return "No secrets found in the requested files. Ready to go!"

    return "## Guardian Scan Results\n" + "\n".join(findings)

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()