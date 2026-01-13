# 🛡️ CodeDoc MCP Server

**CodeDoc** is an AI-powered "Project Guardian" built for Cursor and Claude. Unlike general AI coding assistants, CodeDoc is a context-aware engine designed to enforce structural integrity, SOLID principles, and clean code standards directly within your local environment.

* * *

## 🚀 Why CodeDoc?

-   **Invisible Automation:** Works seamlessly within Cursor or Claude Desktop.
    
-   **PR-Ready Audits:** Catches SQL Injections, Race Conditions, and Resource Leaks.
    
-   **Context-Aware:** Reads local files directly from your workspace—no more copy-pasting.
    
-   **Smart Filtering:** Automatically ignores `node_modules`, `.env`, and binary files.

## ⚖️ How CodeDoc is Different

While standard AI chat can explain code, **CodeDoc** is built for a professional "Review-First" workflow. It bridges the gap between temporary chat conversations and permanent repository health.

### 🛡️ The "Certified Push" Workflow
CodeDoc is the only tool that bridges the gap between **Code Execution** and **Compliance**. 

**The Challenge:** Cursor suggests code, but does it follow your team's specific naming conventions? Does it avoid nested loops?
**The Solution:** With CodeDoc Phase 2, you provide your `Development Manifesto`. CodeDoc then audits your staged files against those specific rules, refactors the logic, and documents the changes in one step.

**It doesn't just write code; it enforces your standards.**

| Feature | Standard AI Chat | CodeDoc MCP |
| :--- | :--- | :--- |
| **Persistence** | Lost when chat is cleared | Permanent in `/documentation` folder |
| **Context** | Limited to open tabs | Scans entire project structure |
| **Workflow** | Reactive (answering questions) | Proactive (pre-commit style auditing) |
| **Output** | Raw text in chat window | Professional, version-controlled Markdown |
| **System Awareness**| No local file access | Reads & Writes directly to your workspace |

### 🛠️ The "Pre-Commit" Philosophy
CodeDoc isn't just a documentation generator; it's a **quality gatekeeper**. By generating a local audit before you merge code, you ensure that security risks, concurrency bugs, and architectural flaws are caught and documented for the whole team to see—not just hidden in your AI history.

## 🚀 Features

### Phase 1: Smart Documentation (Complete)
- **Automatic Docs:** Generates technical documentation for any file.
- **Structure Scanning:** Maps out project files and dependencies.

### Phase 2: Guardian Refactoring (Complete)
- **Refactor & Optimize:** Targeted refactoring using SOLID and OOPS principles.
- **Smart Pathing:** Finds `Middleware.java` even if it's buried in `src/main/resources/internal/`.
- **Custom Rule Injection:** Allows users to pass specific team standards (e.g., "Use Tailwind for styles").

### Phase 3: Architecture Scorecard (Coming Soon)
- **Health Reports:** Get a 1-10 score on code complexity and technical debt.
- **Impact Analysis:** See what components will break before you apply a change.

### 🗺️ Future Roadmap
- 🚀 **Smart Refactoring:** Automated suggestions to simplify complex logic.
- ⚡ **Performance Optimization:** Identifying and fixing $O(n^2)$ bottlenecks. User can ask for the code optimisation and bugfree code before final push to production.[in progress].
- 🔒 **Secret Detection:** Scanning for leaked API keys or hardcoded credentials.
- 📈 **Commit Integration:** Automatically updating docs on every local commit.
    

* * *

## 🛠️ Installation

To add the Guardian Engine to your Cursor IDE:

1. Open **Cursor Settings** (`Cmd+Shift+J` or `Ctrl+Shift+J`).
2. Go to **Features > MCP**.
3. Click **+ Add New MCP Server**.
4. Paste the following:

```json
{
  "mcpServers": {
    "codedoc": {
      "command": "uvx",
      "args": [
        "--refresh",
        "--from",
        "git+[https://github.com/akshay1018/mcp-codedoc.git](https://github.com/akshay1018/mcp-codedoc.git)",
        "codedoc"
      ]
    }
  }
}

* * *

## 📖 How to Use (The Guide)

Once installed, you don't need to learn any special commands. Just talk to the AI in your sidebar.

### The "Auto-Refactor" Prompt
> "@codedoc scan and refactor Login.tsx using SOLID principles. Extract logic into a service file."

### The "Project Map" Prompt
> "@codedoc scan project files and identify any files missing documentation."

### The "Clean Push" Prompt
> "@codedoc refactor Middleware.java for better performance before I push to main."

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