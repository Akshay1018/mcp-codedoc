# 🛡️ CodeDoc MCP Server

**The AI-Powered "Pre-Flight" Documentation & Quality Audit Agent.**

`CodeDoc` is a professional-grade Model Context Protocol (MCP) server that transforms how developers document and review code. Instead of just describing what code does, `CodeDoc` acts as a **local gatekeeper**, identifying logic bugs, security vulnerabilities, and code smells before they ever reach a Pull Request.

* * *

## 🚀 Why CodeDoc?

-   **Invisible Automation:** Works seamlessly within Cursor or Claude Desktop.
    
-   **PR-Ready Audits:** Catches SQL Injections, Race Conditions, and Resource Leaks.
    
-   **Context-Aware:** Reads local files directly from your workspace—no more copy-pasting.
    
-   **Smart Filtering:** Automatically ignores `node_modules`, `.env`, and binary files.

## ⚖️ How CodeDoc is Different

While standard AI chat can explain code, **CodeDoc** is built for a professional "Review-First" workflow. It bridges the gap between temporary chat conversations and permanent repository health.

| Feature | Standard AI Chat | CodeDoc MCP |
| :--- | :--- | :--- |
| **Persistence** | Lost when chat is cleared | Permanent in `/documentation` folder |
| **Context** | Limited to open tabs | Scans entire project structure |
| **Workflow** | Reactive (answering questions) | Proactive (pre-commit style auditing) |
| **Output** | Raw text in chat window | Professional, version-controlled Markdown |
| **System Awareness**| No local file access | Reads & Writes directly to your workspace |

### 🛠️ The "Pre-Commit" Philosophy
CodeDoc isn't just a documentation generator; it's a **quality gatekeeper**. By generating a local audit before you merge code, you ensure that security risks, concurrency bugs, and architectural flaws are caught and documented for the whole team to see—not just hidden in your AI history.

### 🗺️ Future Roadmap
- 🚀 **Smart Refactoring:** Automated suggestions to simplify complex logic.
- ⚡ **Performance Optimization:** Identifying and fixing $O(n^2)$ bottlenecks[in progress].
- 🔒 **Secret Detection:** Scanning for leaked API keys or hardcoded credentials.
- 📈 **Commit Integration:** Automatically updating docs on every local commit.
    

* * *

## 💻 Installation Guide

### 1\. Prerequisites

Ensure you have [Python 3.10+](https://python.org/) and the `uv` package manager installed:

Bash

    pip install uv

### 2\. Adding to your AI Editor

#### **For Cursor Users:**

1.  Open **Settings** > **Cursor Settings**.
    
2.  Navigate to **Features** > **MCP Servers**.
    
3.  Click **\+ Add New MCP Server**.
    
4.  Fill in the details:
    
    -   **Name:** `CodeDoc`
        
    -   **Type:** `command`
        
    -   **Command:** \`\`\`bash uvx --from git+https://www.google.com/search?q=https://github.com/akshay1018/mcp-codedoc.git codedoc
        

#### **For Claude Desktop Users:**

Add this to your `claude_desktop_config.json`:

JSON

    {
      "mcpServers": {
        "codedoc": {
          "command": "uvx",
          "args": [
            "--from",
            "git+https://github.com/akshay1018/mcp-codedoc.git",
            "codedoc"
          ]
        }
      }
    }

* * *

## 📖 How to Use (The Guide)

Once installed, you don't need to learn any special commands. Just talk to the AI in your sidebar.

### Scenario A: Documenting a Local File

If you have a file open (e.g., `auth.py`), simply ask:

> _"Use CodeDoc to document `auth.py` and check for bugs."_

### Scenario B: Documenting Pasted Code

If you have a snippet of code in your chat, ask:

> _"Document this code snippet and perform a quality audit."_

### Scenario C: Project Overview

If you want to see what files can be documented:

> _"Scan my project files using CodeDoc and tell me which ones need documentation."_

* * *

## 📂 Understanding the Output

Every time you run a documentation task, CodeDoc creates a folder named `/documentation` in your project root.

Plaintext

    your-project/
    ├── documentation/
    │   ├── documentation_snippet_20251227_010000.md  <-- Your Report
    ├── auth.py
    └── server.py

### What's inside the report?

Each `.md` file generated includes:

1.  **Technical Documentation:** Overview, Parameters, and Return Values.
    
2.  **Quality Audit:** **The most important section.** This lists potential bugs, security risks, and performance bottlenecks.
    
3.  **Source Code:** A timestamped reference of the code that was audited.

## 🤝 Contributing & Support

# 

If you encounter any issues or have feature requests, please open an issue on the [GitHub Repository](https://github.com/akshay1018/mcp-codedoc).

**License:** MIT