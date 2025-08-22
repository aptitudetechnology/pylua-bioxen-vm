# Debug Output Audit Report for pylua_bioxen_vm_lib

## 1. Debug Output Sources
- **[DEBUG] print statements** are present in several files, especially in `pylua_vm/interactive_session.py` and `test_installation.py`.
- Functions named `_read_output` and `read_output` are found in `pylua_vm/interactive_session.py`, `pylua_vm/lua_process.py`, and `pylua_vm/vm_manager.py`.
- PTY output handling and debug prints are concentrated in `pylua_vm/interactive_session.py`.
- Hardcoded debug prints (e.g., `[DEBUG][_read_output] PTY output: ...`, `[DEBUG][read_output] Drained output: ...`) are used for tracing PTY and session output.

## 2. Key Files and Classes
- **VMManager**: `pylua_vm/vm_manager.py` (contains `read_output` and session management)
- **InteractiveSession**: `pylua_vm/interactive_session.py` (contains `_read_output`, PTY handling, and debug prints)
- **LuaProcess**: `pylua_vm/lua_process.py` (delegates to interactive session for output)
- **Test scripts**: `test_installation.py` (contains many `[DEBUG]` prints for test output)

## 3. Debug Output Pattern
- Debug output is consistently formatted as:
  - `[DEBUG][_read_output] PTY output: ...`
  - `[DEBUG][read_output] Drained output: ...`
  - `[DEBUG][PTY] Output after send_command: ...`
  - `[DEBUG][PTY] Error during flush: ...`
- These prints are used for tracing PTY reads, command execution, and error handling.

## 4. Recommendations for Optional Debug Mode
- Replace hardcoded debug prints with a configurable debug flag or use Python's `logging` module.
- Example approach:
  - Add a `debug` parameter to `InteractiveSession`, `VMManager`, etc.
  - Use `if self.debug: print(...)` or `logging.debug(...)` instead of direct prints.
  - Allow global or per-session debug control via environment variable or config.
- For production, set debug mode off by default to avoid noisy output.

## 5. Next Steps
- Refactor debug prints to use a standard logging approach.
- Document debug mode usage in README and developer docs.
- Optionally, add log level control for more granular output.
