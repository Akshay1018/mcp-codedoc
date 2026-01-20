# 🛡️ CodeDoc MCP Server

**CodeDoc** is an AI-powered "Project Guardian" built for Cursor and Claude. CodeDoc is a high-performance architectural sentinel that transforms Cursor into a Project Architect by enforcing security, structural integrity, and production-grade code quality across your entire codebase. Unlike general AI coding assistants, CodeDoc is a context-aware engine designed to enforce structural integrity, SOLID principles, and clean code standards directly within your local environment. CodeDoc goes beyond simple code generation. It acts as a "Guardian" for your project, ensuring that every refactor is secure, every change is understood across the "Radius," and every line of code meets industry-standard health metrics.

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

---

## 🚀 The Guardian Pipeline
CodeDoc doesn't just write code; it follows a professional safety-first workflow:
1. **Security Scan:** Detects hardcoded secrets or API keys before they leak to GitHub.
2. **Impact Analysis:** Maps the ripple effect of your changes across the entire project.
3. **Health Audit:** Scores your code (1-10) based on SOLID, OOPS, and maintainability.
4. **Certified Refactor:** Generates production-ready optimizations with a native side-by-side Diff view.

---

## 🚀 Features

### Smart Documentation
- **Automatic Docs:** Generates technical documentation for any file.
- **Structure Scanning:** Maps out project files and dependencies.

### Guardian Refactoring
- **Refactor & Optimize:** Targeted refactoring using SOLID and OOPS principles.
- **Smart Pathing:** Finds `Middleware.java` even if it's buried in `src/main/resources/internal/`.
- **Custom Rule Injection:** Allows users to pass specific team standards (e.g., "Use Tailwind for styles").

### Security Sentinel (Project-Wide)
Stop leaks before they happen. CodeDoc scans uncommitted files or specific folders for API keys, tokens, and vulnerabilities. 
> **Prompt:** *"codedoc, scan my uncommitted changes for secrets before I push."*

### Impact Analyzer (The Blast Radius)
Understand the ripple effect of your changes. It identifies exactly which files and line numbers will break when you modify a function signature or rename a variable.
> **Prompt:** *"What happens if I change the 'fetchData' argument to an object in apiService.ts?"*

### Architecture Scorecard
Get an instant audit of your code health. CodeDoc provides a 1-10 score, breaks down complexity, and identifies architectural debt.
> **Prompt:** *"Give me a health score for login.tsx and provide the optimised code based on the health."*

### Smart Project Awareness
Language-agnostic support for **Java, TypeScript, Python, C++, C#, and more.** CodeDoc intelligently prunes `node_modules` and heavy folders to provide lightning-fast results without freezing your system.

### Future Roadmap
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

```

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
    ├── # other files

### What's inside the report?

Each `.md` file generated includes:

1.  **Technical Documentation:** Overview, Parameters, and Return Values.
    
2.  **Quality Audit:** **The most important section.** This lists potential bugs, security risks, and performance bottlenecks.
    
3.  **Source Code:** A timestamped reference of the code that was audited.

## 🤝 Contributing & Support

# 

If you encounter any issues or have feature requests, please open an issue on the [GitHub Repository](https://github.com/akshay1018/mcp-codedoc).

**License:** MIT