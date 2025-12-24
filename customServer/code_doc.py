from mcp.server.fastmcp import FastMCP
import os
from datetime import datetime

mcp = FastMCP("CodeDoc")

@mcp.tool()
def generate_doc_file(code: str, doc_content: str, audit_results: str, language: str = "auto") -> str:
    """
    Creates a documentation and quality audit file.
    'doc_content' should cover: Overview, Parameters, Return Values, Validation Logic, and Notes.
    'audit_results' should cover: Potential Bugs, Linting/Style issues, and Reusability suggestions.
    """
    try:
        # Determine the directory of the script and point to the /documentation folder
        base_dir = os.path.dirname(os.path.abspath(__file__))
        target_folder = os.path.join(base_dir, "documentation")
        
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"doc_{timestamp}.md"
        file_path = os.path.join(target_folder, filename)
        
        # Strictly structured Markdown output
        content = f"# Technical Documentation & Quality Audit\n"
        content += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
        
        content += f"## 1. Documentation\n{doc_content}\n\n"
        
        content += f"## 2. Quality Audit (Pre-Commit Check)\n"
        content += f"> [!IMPORTANT]\n"
        content += f"> Review these points before pushing to GitHub to avoid PR failure.\n\n"
        content += f"{audit_results}\n\n"
        
        content += f"## 3. Source Code Reference\n```{language}\n{code}\n```\n"
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        return f"Audit and Documentation saved to: documentation/{filename}"
    
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()