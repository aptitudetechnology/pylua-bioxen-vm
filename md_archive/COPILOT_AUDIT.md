# 🔍 Audit Instructions for Copilot

You are auditing the **pylua-bioxen-vm** codebase.
Focus on **session lifecycle management, interactive VM handling, and registry operations**.

## 1. Locate Key Components

* Find all definitions of:
  * `VMManager`
  * `SessionManager`
  * `SessionRegistry` (if present)
  * Custom exceptions (`DetachError`, `SessionNotFoundError`, etc.)
* Identify where interactive sessions (`interactive_eval`, `attach`, `detach`, etc.) are implemented.

---

## 2. Check for Known Issues

Compare the code against these reported problems from `test_installation4.py`:

1. **Interactive I/O prints Lua banner**
   * Does the VM spawn Lua in a way that automatically prints version text?
   * Suggest how to suppress/filter this.

2. **Session Persistence not maintained**
   * When `detach()` is called, is the Lua state destroyed or preserved?
   * On `reattach()`, is a new Lua state created instead of reconnecting to the old one?
   * Suggest how to persist session state.

3. **Exception Handling mismatch**
   * In `SessionManager.create_session()`, what happens if a session ID already exists?
   * Does it raise the wrong exception (`duplicate VM exists`) instead of `DetachError`?

4. **Registry Inconsistency**
   * Verify that all sessions created are correctly registered.
   * Check cleanup logic: is the registry prematurely deleting entries?

5. **Complex Interactive Session / Multiline Input**
   * Review how `interactive_eval()` handles multi-line Lua code (functions, loops).
   * Is there buffering logic, or does it send incomplete statements straight to Lua?

---

## 3. Write an Audit Report

Produce a structured report with these sections:

* **Summary**: One-paragraph overview of code quality and test coverage.
* **Findings**: For each issue above, note:
  * Relevant code snippets (with file + line numbers).
  * Why the issue happens.
  * Suggested fix.
* **Recommendations**:
  * Steps to improve persistence, registry accuracy, and REPL behavior.
  * Any missing unit tests Copilot thinks should be added.

---

## 4. Output Format

Use **Markdown** with headings:

```markdown
# pylua-bioxen-vm Audit Report

## Summary
...

## Findings

### 1. Interactive I/O prints Lua banner
- Location: `vm_manager.py:123`
- Cause: ...
- Fix: ...

### 2. Session Persistence
...

## Recommendations
- ...
```

---

👉 With this, Copilot should crawl the repo, map issues to code, and produce a detailed audit report.
