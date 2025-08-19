# pylua-bioxen-vm Interactive Terminal Refactor Plan

## Files to Update for Interactive Terminal Support

### 1. LuaProcess class file (`pylua_vm/lua_process.py`)
- **Current:** Uses `subprocess.run` for one-shot Lua execution.
- **Update:** Refactor to use `subprocess.Popen` with PTY support for persistent, interactive Lua interpreter processes. Add methods for bidirectional I/O and process management.

### 2. VMManager class file (`pylua_vm/vm_manager.py`)
- **Current:** Manages VM lifecycle and orchestration using one-shot execution.
- **Update:** Add interactive session tracking, persistent process registry, and new methods:
  - `attach_to_vm(vm_id)`
  - `send_input(vm_id, input_str)`
  - `read_output(vm_id)`
  - `detach_vm(vm_id)`

### 3. New InteractiveSession class file (`pylua_vm/interactive_session.py`)
- **Purpose:** Encapsulate PTY management, bidirectional I/O, and threading for real-time terminal communication with Lua VMs.
- **Features:**
  - PTY creation and management
  - Threading for non-blocking I/O
  - Session attach/detach logic

### 4. Main `__init__.py` (`pylua_vm/__init__.py`)
- **Update:** Export new interactive terminal classes and methods for public API.

### 5. Exception handling file (`pylua_vm/exceptions.py`)
- **Update:** Add new exceptions for interactive session errors (e.g., `InteractiveSessionError`, `AttachError`, `DetachError`).

---

## Key Functionality to Implement
- Replace one-shot `subprocess.run` with persistent `subprocess.Popen` + PTY
- Add threading for non-blocking I/O handling
- Implement attach/detach terminal session management
- Maintain backward compatibility with existing non-interactive API
- Add process registry to track persistent Lua interpreter instances

---

## Project Structure Reference
- Main package: `pylua_vm/`
  - `__init__.py`
  - `lua_process.py`
  - `networking.py`
  - `vm_manager.py`
  - `exceptions.py`
- Example usage: `examples/basic_usage.py`, README
- Dependencies: `requirements.txt`, `setup.py`

---

## Next Steps
1. Start with refactoring `LuaProcess` for persistent interactive process support.
2. Implement `InteractiveSession` class for PTY and threading.
3. Update `VMManager` for session management and registry.
4. Extend exception handling.
5. Update exports in `__init__.py`.

Let me know if you want to begin with the full code for `LuaProcess` or any other file!
