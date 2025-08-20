# Failing Imports Debug Report

## Overview
This report analyzes why Tests 5, 6, 9, and 10 in `test_installation8.py` fail with `name 'VMManager' is not defined` and `name 'SessionManager' is not defined`, despite successful top-level imports from `pylua_vm`.

---

## Symptoms
- Top-level import of `pylua_vm.VMManager` and `pylua_vm.SessionManager` succeeds.
- Tests 5, 6, 9, and 10 fail with `NameError` for `VMManager` and `SessionManager`.
- Debug output confirms `SessionManager` is found in `pylua_vm`.

---

## Likely Causes
1. **Local Variable Scope:**
   - The imports may not be available in the local scope of the test functions.
   - Possible missing or incorrect import statements inside the test script or functions.
2. **Module Caching / Reload Issues:**
   - Python's import system may cache or shadow names, especially in interactive environments.
3. **Incorrect or Shadowed Imports:**
   - Using `import pylua_vm` but referencing `VMManager` directly instead of `pylua_vm.VMManager`.
   - Accidental redefinition or deletion of `VMManager` or `SessionManager` in the script.

---

## Debug Steps
1. **Check Export in `pylua_vm/__init__.py`:**
   - Ensure `VMManager` and `SessionManager` are imported and listed in `__all__`.
2. **Check Import in Test Script:**
   - Use `from pylua_vm import VMManager, SessionManager` at the top of the test file.
   - If using `import pylua_vm`, reference as `pylua_vm.VMManager`.
3. **Add Debug Code Before Test 5:**
   ```python
   print("Debug: VMManager in globals?", 'VMManager' in globals())
   print("Debug: pylua_vm.VMManager?", hasattr(pylua_vm, 'VMManager'))
   try:
       print("Debug: VMManager type:", type(VMManager))
   except Exception as e:
       print("Debug: VMManager not available:", e)
   ```
4. **Use importlib.reload if Needed:**
   ```python
   import importlib
   import pylua_vm
   importlib.reload(pylua_vm)
   ```
5. **Check for Shadowing:**
   - Ensure `VMManager` and `SessionManager` are not redefined or deleted in the script.

---

## Recommendations
- Verify and correct all import statements in the test script.
- Add debug prints before Test 5 to confirm availability of `VMManager` and `SessionManager`.
- If issues persist, reload the module and check for shadowing.
- Review `pylua_vm/__init__.py` to ensure proper exports.

---

## Conclusion
The `NameError` is most likely due to missing or incorrect imports, local scope issues, or module caching. Following the debug steps above will help pinpoint and resolve the problem.
