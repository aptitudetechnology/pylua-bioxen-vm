# COPILOT_FIXFLOW.md

⚠️ Important: This runbook describes the step-by-step workflow for auditing, patching, and testing the pylua-bioxen-vm codebase using Copilot (or any LLM assistant) and the provided audit/patch playbooks.

---

## Workflow Steps

### 1. Run the Audit

- Command:
  ```
  /analyze Follow COPILOT_AUDIT.md and produce AUDIT_REPORT.md
  ```
- Output: `AUDIT_REPORT.md` (structured findings in Markdown)

---

### 2. Generate Fixes

- Command:
  ```
  /fix Apply COPILOT_PATCH.md using AUDIT_REPORT.md as input, and produce PATCH_REPORT.md
  ```
- Output: `PATCH_REPORT.md` (proposed code changes, diffs, and rationale)

---

### 3. Apply Patches

- Option 1: Ask Copilot to inline changes into the source files.
- Option 2: Manually review and apply diffs from `PATCH_REPORT.md`.

---

### 4. Re-run Tests

- Command:
  ```
  python3 test_installation4.py
  ```
- Confirm that all issues are resolved and features work as expected.

---

## Notes
- This workflow ensures diagnosis and treatment are separated for clarity and traceability.
- You can repeat the loop as needed for new features or bug fixes.
- For CI/CD, automate steps 1–4 to maintain code health.

---

With this runbook, any team member or automation can follow the audit → patch → test loop with confidence.
