# Grok Diagnostic Report: pylua_bioxen_vm_lib Import Issues

## Overview
This report documents the root cause and recommended solutions for Python import errors encountered when using the `pylua_bioxen_vm_lib` package from external scripts, specifically:
- `test_pylua-bioxen-vm.py`
- `interactive-bioxen-lua.py`

Both scripts are located in `/home/chris/BioXen-luavm` and use a virtual environment at `/home/chris/BioXen-luavm/venv` (Python 3.10, Linux). The package is installed in editable mode from the GitHub repository `aptitudetechnology/pylua_bioxen_vm_lib`.

## Issue Summary
**Error:**
```
ModuleNotFoundError: No module named 'pylua_bioxen_vm_lib.utils'
```
This error occurs when importing from `pylua_bioxen_vm_lib.utils.curator` in `lua_process.py`:
```python
from .utils.curator import Curator
```

## Root Cause
- The package uses **relative imports** (e.g., `from .utils.curator import Curator`) in its modules.
- When scripts are run outside the package context (not as part of the package), Python cannot resolve these relative imports.
- Editable install (`pip install -e .`) does not change import resolution for relative imports in standalone scripts.

## Solution
### 1. Use Absolute Imports
Change all relative imports in the package to absolute imports. For example, in `lua_process.py`:
```python
from pylua_bioxen_vm_lib.utils.curator import Curator
```
This ensures imports work regardless of how the package is used or where scripts are run.

### 2. General Best Practices
- Use absolute imports for all top-level package modules.
- Reserve relative imports for intra-package usage only when running as a module (e.g., `python -m pylua_bioxen_vm_lib.module`).
- After making changes, reinstall the package in editable mode:
  ```bash
  pip install -e .
  ```

## Action Items
- [ ] Update all relative imports in `pylua_bioxen_vm_lib` to absolute imports.
- [ ] Test external scripts after changes to confirm resolution.
- [ ] Document import strategy in project README for future contributors.

## References
- [Python Packaging User Guide: Imports](https://packaging.python.org/en/latest/guides/packaging-namespace-packages/#imports)
- [PEP 328: Absolute and Relative Imports](https://peps.python.org/pep-0328/)

---
**Prepared by:** GitHub Copilot
**Date:** 24 August 2025
