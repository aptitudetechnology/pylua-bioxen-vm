# NetworkedLuaVM Debug Mode & Logger Integration Report

## Issues Identified

1. **Missing `logger` Attribute**
   - The `NetworkedLuaVM` class does not initialize a `logger` attribute, causing an `AttributeError` during cleanup.

2. **Unexpected `debug_mode` Argument**
   - The `NetworkedLuaVM.__init__()` method does not accept a `debug_mode` parameter, but it is passed from the factory function (`create_vm`).

## Required Fixes

- Update `pylua_vm/networking.py`:
  - Add a `debug_mode` parameter to the `NetworkedLuaVM.__init__` method.
  - Initialize `self.logger = VMLogger(debug_mode=debug_mode, component="NetworkedLuaVM")` in the constructor.
  - Pass `debug_mode` to the superclass (`LuaProcess`) if needed.

## Next Steps
- Refactor `NetworkedLuaVM` to support debug logging and proper cleanup.
- Ensure all VM types in the codebase consistently support `debug_mode` and logger integration.
- Test networked VM creation and cleanup to confirm the fix.

---

This report documents the required changes for debug mode and logger support in the networked VM implementation.
