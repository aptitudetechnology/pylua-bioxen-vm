# Updating test_installation.py for Interactive Terminal Support

## Overview
With the recent upgrades to support persistent, interactive Lua VM sessions, your `test_installation.py` should be updated to validate the new features and ensure backward compatibility. This report outlines recommended changes and additions for your test suite.

---

## Key Areas to Test
1. **Basic VM Creation and Execution**
   - Ensure you can create and execute Lua code in both basic and networked VMs.
2. **Interactive Session Management**
   - Test creation, attachment, detachment, and termination of interactive sessions using `VMManager`, `InteractiveSession`, and `SessionManager`.
   - Validate bidirectional I/O: sending input and reading output from Lua VMs interactively.
3. **Exception Handling**
   - Confirm that new exceptions (`InteractiveSessionError`, `AttachError`, `DetachError`, `SessionNotFoundError`, `SessionAlreadyExistsError`, `VMManagerError`, `ProcessRegistryError`) are raised appropriately.
4. **Persistent VM Registry**
   - Test registration, listing, and removal of persistent VMs.
5. **Backward Compatibility**
   - Ensure legacy one-shot execution and cluster management features still work as expected.

---

## Recommended Test Additions
- **Test Interactive Session Lifecycle:**
  - Create a persistent VM, attach to its session, send Lua commands, read output, detach, and terminate.
- **Test Exception Scenarios:**
  - Attempt to attach/detach to non-existent sessions, create duplicate sessions, and trigger registry errors.
- **Test Registry and Listing:**
  - Validate that persistent VMs and sessions are correctly tracked and listed.
- **Test Backward Compatibility:**
  - Run legacy tests for basic execution and cluster operations to ensure no regressions.

---

## Example Test Snippets
```python
from pylua_vm import VMManager, InteractiveSession, SessionManager, \
    InteractiveSessionError, AttachError, DetachError, SessionNotFoundError

def test_interactive_session_lifecycle():
    manager = VMManager()
    vm_id = "test_vm"
    session = manager.create_interactive_vm(vm_id)
    manager.send_input(vm_id, "print('Hello from Lua')\n")
    output = manager.read_output(vm_id)
    assert "Hello from Lua" in output
    manager.detach_from_vm(vm_id)
    manager.terminate_vm_session(vm_id)

def test_exception_handling():
    manager = VMManager()
    try:
        manager.attach_to_vm("nonexistent_vm")
    except SessionNotFoundError:
        pass  # Expected
```

---

## Next Steps
- Update `test_installation.py` to include the above tests and scenarios.
- Run the test suite to validate all new and legacy features.
- Address any failures or regressions promptly.

Let me know if you want full test code examples or help with implementation!
