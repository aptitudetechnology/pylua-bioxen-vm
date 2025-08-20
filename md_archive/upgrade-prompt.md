I'm implementing interactive terminal support for Lua VMs to work like a hypervisor. Based on previous analysis, I need to modify these core files in the pylua-bioxen-vm library:

REQUIRED FILES TO UPDATE:
1. LuaProcess class file - Convert from subprocess.run to subprocess.Popen with PTY support for persistent interactive processes
2. VMManager class file - Add interactive session tracking, persistent process registry, and new methods (attach_to_vm, send_input, read_output, detach_vm)
3. Create new InteractiveSession class file - Handle PTY management, bidirectional I/O, threading for real-time terminal communication
4. Update main __init__.py - Export new interactive terminal classes and methods
5. Any existing exception handling files - Add new exceptions for interactive session errors

KEY FUNCTIONALITY TO IMPLEMENT:
- Replace one-shot subprocess.run with persistent subprocess.Popen + PTY
- Add threading for non-blocking I/O handling
- Implement attach/detach terminal session management
- Maintain backward compatibility with existing non-interactive API
- Add process registry to track persistent Lua interpreter instances

Please help me implement these changes to transform the library from one-shot execution to persistent interactive VM management.