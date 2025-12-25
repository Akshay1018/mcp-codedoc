# 🛡️ CodeDoc MCP Server

**The AI-Powered "Pre-Flight" Documentation & Quality Audit Agent.**

`CodeDoc` is a professional-grade Model Context Protocol (MCP) server that transforms how developers document and review code. Instead of just describing what code does, `CodeDoc` acts as a **local gatekeeper**, identifying logic bugs, security vulnerabilities, and code smells before they ever reach a Pull Request.



---

## 🚀 Why CodeDoc?

Most AI tools just chat. `CodeDoc` **automates**. It is designed for developers who want to maintain high code quality without the manual overhead of writing documentation or catching repetitive bugs.

* **Invisible Automation:** Works seamlessly within Cursor or Claude Desktop.
* **PR-Ready Audits:** Catches SQL Injections, Race Conditions, and Resource Leaks.
* **Context-Aware:** Reads local files directly from your workspace—no more copy-pasting.
* **Smart Filtering:** Automatically ignores `node_modules`, `.env`, and binary files to stay focused on your source code.

---

## 🛠️ Features

| Feature | Description |
| :--- | :--- |
| **Technical Docs** | Generates Overview, Parameters, Return Values, and Validation Logic. |
| **Quality Audit** | Performs deep-dives into potential logic bugs and security risks. |
| **Linting & Style** | Identifies ESLint-style issues and variable naming inconsistencies. |
| **DRY Analysis** | Flags redundant code and suggests reusability patterns. |
| **Project Scanning** | Discovers all documentable files in your project automatically. |

---

## 💻 Installation

### 1. Prerequisites
Ensure you have [Python 3.10+](https://python.org) and the `uv` package manager installed:
```bash
pip install uv

### 2. Add to your IDE

#### **For Cursor:**
1.  Go to **Settings** > **Cursor Settings** > **Features** > **MCP Servers**.
2.  Click **+ Add New MCP Server**.
3.  **Name:** `CodeDoc`
4.  **Type:** `command`
5.  **Command:** ```bash
    uv run /absolute/path/to/your/code_doc.py
    ```

#### **For Claude Desktop:**
Edit your `claude_desktop_config.json` (usually located at `~/Library/Application Support/Claude/claude_desktop_config.json` on Mac):

```json
{
  "mcpServers": {
    "codedoc": {
      "command": "uv",
      "args": ["run", "/absolute/path/to/your/code_doc.py"]
    }
  }
}

## 📖 How to Use
Simply prompt your AI naturally. CodeDoc will handle the file operations and folder organization.

**Snippet Mode:**  
"Document this code I just pasted and check for bugs."

**File Mode:**  
"Generate an audit for auth_service.py."

**Project Mode:**  
"Scan my project and document the core logic files."

---

## 📂 Output Structure
All reports are saved to a dedicated `/documentation` folder in your script's directory:

```plaintext
project-root/
├── documentation/
│   ├── audit_auth_service_py_20251225_120000.md
│   └── audit_chat_snippet_20251225_120500.md
