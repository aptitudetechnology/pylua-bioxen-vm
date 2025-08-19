# COPILOT_PATCH.md

⚠️ Important: For each finding in the audit report, propose a concrete code change (patch) in the format below. Do not summarize or skip steps. Output only in the format described.

---

## Patch Instructions

For each issue in the audit report, provide:
- **Heading** matching the audit finding (e.g., `### 1. Interactive I/O prints Lua banner`)
- **Location**: File and line number(s) to change
- **Current Code**: Relevant code snippet
- **Proposed Patch**: New code or diff
- **Rationale**: Why this change fixes the issue

---

## Example Format

```markdown
### 1. Interactive I/O prints Lua banner
- Location: `pylua_vm/interactive_session.py:67`
- Current Code:
  ```python
  output = data.decode(errors="replace")
  self.output_queue.put(output)
  ```
- Proposed Patch:
  ```python
  # Filter out Lua banner/version info on first output
  if not hasattr(self, '_banner_filtered'):
      if output.strip().startswith('Lua '):
          self._banner_filtered = True
          return  # skip banner
      self._banner_filtered = True
  self.output_queue.put(output)
  ```
- Rationale: Prevents Lua version text from polluting interactive output.
```

---

## Patch Sections

### 1. Interactive I/O prints Lua banner

### 2. Session Persistence not maintained

### 3. Exception Handling mismatch

### 4. Registry Inconsistency

### 5. Complex Interactive Session / Multiline Input

---

For each section, propose a patch as shown above. If a fix requires multiple files, list all affected files and changes. If a fix is not possible, explain why and suggest alternatives.
