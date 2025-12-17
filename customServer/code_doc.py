from mcp.server.fastmcp import FastMCP
import os
from datetime import datetime

mcp = FastMCP("CodeDoc")

@mcp.tool()
def generate_doc_file(code: str, doc_content: str, language: str = "python") -> str:
    """
    Creates a technical documentation file in the 'documentation' folder.
    """
    try:
        # 1. Define and create the documentation directory
        # This will create a folder named 'documentation' in the same 
        # directory where this script is located.
        base_dir = os.path.dirname(os.path.abspath(__file__))
        target_folder = os.path.join(base_dir, "documentation")
        
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
            
        # 2. Create the timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"doc_{timestamp}.md"
        file_path = os.path.join(target_folder, filename)
        
        # 3. Build the markdown content
        content = f"# Technical Documentation ({language.upper()})\n"
        content += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
        content += f"## Source Code\n```{language}\n{code}\n```\n\n"
        content += f"## Analysis\n{doc_content}"
        
        # 4. Save the file to the specific folder
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        return f"Successfully created {filename} in the documentation folder."
    
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()