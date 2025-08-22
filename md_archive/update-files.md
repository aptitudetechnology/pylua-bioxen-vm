# Files to Update for Debug Mode Refactor (claude-plan.md)

## Required Updates

### 1. pylua_vm/interactive_session.py
- Refactor all debug print statements to use the new `VMLogger` class and a `debug_mode` flag.
- Update the constructor to accept `debug_mode` and initialize `VMLogger`.

### 2. pylua_vm/vm_manager.py
- Add a `debug_mode` parameter to the constructor.
- Initialize `VMLogger`.
- Pass `debug_mode` to `InteractiveSession` when creating sessions.

### 3. pylua_vm/lua_process.py
- Add a `debug_mode` parameter to the constructor.
- Initialize `VMLogger`.

## New Files to Add

### 4. pylua_vm/logger.py
- Implement the `VMLogger` class for structured logging and debug output control.

### 5. (Optional) pylua_vm/config.py
- Add configuration file and environment variable support for debug mode.

## Other Updates
- If you have a main script (e.g., BioXen manager), update it to support the `--debug` CLI flag and pass `debug_mode` to `VMManager`.
- Update your README to document debug mode usage and configuration options.

## Summary
You need to update `interactive_session.py`, `vm_manager.py`, and `lua_process.py`, and add `logger.py` (and optionally `config.py`). No existing logging infrastructure is present, so these changes are required for the plan to work.

This checklist is based on the implementation plan in `claude-plan.md` and will enable optional debug mode and cleaner output throughout the library.
