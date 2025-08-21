# Python Import Error Deep-Dive & Action Plan

## Current State
Despite all import strategies and Python path adjustments, `NameError: name 'VMManager' is not defined` and `SessionManager` errors persist in `test_installation9.py`. This is a Python environment/module resolution issue, not a code bug.

## sys.path Output
Your current `sys.path` is:
```
['', '/usr/lib/python310.zip', '/usr/lib/python3.10', '/usr/lib/python3.10/lib-dynload', '/home/chris/pylua_bioxen_vm_lib/venv/lib/python3.10/site-packages']
```
- The project root `/home/chris/pylua_bioxen_vm_lib` is missing from `sys.path`.
- Only site-packages and system paths are present.

## Why This Matters
- Python cannot find your local `pylua_vm` package unless the project root is in `sys.path`.
- This causes `NameError` for any classes not imported via site-packages.

## Action Plan
1. **Verify Package Structure**
   - Ensure `/home/chris/pylua_bioxen_vm_lib/pylua_vm/__init__.py` exists and is not empty.
   - Confirm there is no file named `pylua_vm.py` in your project root (it should be a directory).
2. **Check for Shadowing**
   - Run:
     ```bash
     python3 -c "import pylua_vm; print(pylua_vm.__file__)"
     ```
   - The output should be a path inside `/home/chris/pylua_bioxen_vm_lib/pylua_vm/`. If not, you have a shadowing/conflict issue.
3. **Direct Import Test**
   - In a Python shell:
     ```python
     from pylua_vm import VMManager, SessionManager
     print(VMManager, SessionManager)
     ```
   - If this fails, your package is not discoverable.
4. **Force Project Root in sys.path**
   - Add at the very top of `test_installation9.py`:
     ```python
     import sys, os
     sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
     sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
     ```
5. **Absolute Import in Failing Blocks**
   - In each failing block, use:
     ```python
     import pylua_vm
     VMManager = pylua_vm.VMManager
     SessionManager = pylua_vm.SessionManager
     ```

## If Error Persists
- Share the output of `python3 -c "import pylua_vm; print(pylua_vm.__file__)"` for further diagnosis.
- This will pinpoint whether Python is loading the correct package.

## Conclusion
This is a Python environment/package discovery issue. Fixing the path and shadowing will resolve the import errors for `VMManager` and `SessionManager`.
