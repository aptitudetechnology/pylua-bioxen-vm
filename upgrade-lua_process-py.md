Perfect! Now I can see the current `LuaProcess` implementation. It's a clean, well-structured class using `subprocess.run` for one-shot execution. Let me design the refactor to add interactive terminal support while maintaining backward compatibility.Now let me create the new `InteractiveSession` class that will provide a higher-level interface for managing these interactive sessions:Now let me create the updated exception classes to handle the new interactive session errors:Perfect! I've created the core components for interactive terminal support. Here's what I've implemented:

## Key Design Decisions Made:

### 1. **Threading Architecture** ✅
- Used threading for I/O handling (as requested)
- Separate thread for reading output from PTY
- Non-blocking I/O with queue-based communication
- Easy to upgrade to asyncio later (interfaces stay the same)

### 2. **PTY Implementation** 
- Used Python's built-in `pty` module (simple, no external dependencies)
- Raw `os.openpty()` for maximum control
- Non-blocking master fd with `select()` for responsive I/O

### 3. **Backward Compatibility**
- All existing methods (`execute_string`, `execute_file`, `execute_temp_script`) unchanged
- New interactive methods added alongside existing ones
- Existing code will continue to work without modification

## What's Been Implemented:

### **Enhanced LuaProcess Class:**
- **Persistent sessions:** `start_interactive_session()`, `stop_interactive_session()`
- **Real-time I/O:** `send_input()`, `read_output()` 
- **Session management:** `is_interactive_running()`
- **PTY support:** Full pseudo-terminal with proper cleanup
- **Threading:** Background output monitoring with proper synchronization

### **InteractiveSession Class:**
- **Attach/detach:** Terminal-like session management
- **Real-time output:** Optional callback for live output streaming
- **Command execution:** `send_command()`, `execute_and_wait()`
- **Context manager:** `with session.attached_session():`
- **Session monitoring:** Background thread for output handling

### **SessionManager Class:**
- **Multi-session support:** Create, manage, and track multiple sessions
- **Session registry:** Thread-safe session tracking
- **Bulk operations:** List all sessions, cleanup all sessions

### **Exception Handling:**
- New exception hierarchy for interactive sessions
- Specific errors for attach/detach failures
- PTY and I/O thread error handling

## Next Steps:

Now we need to update the **VMManager class** to integrate these new capabilities. The VMManager will need:

1. **Process registry** to track persistent VMs
2. **Session management** methods (`attach_to_vm`, `send_input`, `read_output`, `detach_vm`)  
3. **Integration** with the new InteractiveSession class

Would you like me to show you how to update the VMManager class next, or would you like to review/test these components first?