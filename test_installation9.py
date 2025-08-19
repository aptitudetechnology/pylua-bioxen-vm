
print("Testing pylua-bioxen-vm installation...")
print("=" * 50)



# === Top-level imports with robust fallback and global assignment ===
import sys, os
try:
    from pylua_vm import VMManager, SessionManager, create_vm, InteractiveSession
    from pylua_vm.exceptions import (
        InteractiveSessionError, AttachError, DetachError, 
        SessionNotFoundError, SessionAlreadyExistsError, 
        VMManagerError, ProcessRegistryError
    )
    print("✅ Modules imported successfully")
except ImportError as e:
    print("❌ Module import failed:", e)
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    try:
        from pylua_vm import VMManager, SessionManager, create_vm, InteractiveSession
        from pylua_vm.exceptions import (
            InteractiveSessionError, AttachError, DetachError, 
            SessionNotFoundError, SessionAlreadyExistsError, 
            VMManagerError, ProcessRegistryError
        )
        print("✅ Modules imported successfully after fallback")
    except ImportError as e2:
        print("❌ Fallback import failed:", e2)
        exit(1)

# Ensure VMManager and SessionManager are available globally
globals()['VMManager'] = VMManager
globals()['SessionManager'] = SessionManager

# Check if SessionManager is available
try:
    _ = SessionManager
    SESSION_MANAGER_AVAILABLE = True
    print("✅ SessionManager available")
except NameError:
    SESSION_MANAGER_AVAILABLE = False
    print("⚠️ SessionManager not available")

import time
import re

# Helper function to clean Lua output
def clean_output(output):
    """Remove Lua prompts and ANSI escape codes from output."""
    if not output:
        return ""
    output = re.sub(r'\x1b\[[;?0-9]*[a-zA-Z]', '', output)
    output = re.sub(r'^\s*(>|>>)\s*', '', output, flags=re.MULTILINE)
    output = re.sub(r'\r\n|\r|\n', '\n', output).strip()
    return output

# === 1. Basic VM Creation ===
print("\n1. Testing Basic VM Creation and Execution")
try:
    vm = create_vm("test_vm")
    result = vm.execute_string('print("Hello from Lua!")')
    print("✅ Basic VM:", result['stdout'])
except Exception as e:
    print("❌ Basic VM failed:", e)

# === 2. Networked VM ===
print("\n2. Testing Networked VM")
try:
    net_vm = create_vm("net_vm", networked=True)
    print("✅ Networked VM created successfully")
except Exception as e:
    print("❌ Networked VM failed:", e)

# === 3. VM Manager - Synchronous ===
print("\n3. Testing VM Manager - Synchronous")
try:
    with VMManager() as manager:
        vm = manager.create_vm("managed_vm")
        result = manager.execute_vm_sync("managed_vm", 'print("Square root of 16 is:", math.sqrt(16))')
        print("✅ VM Manager Sync:", result['stdout'])
except Exception as e:
    print("❌ VM Manager Sync failed:", e)

# === 4. Async Execution ===
print("\n4. Testing Async Execution")
try:
    with VMManager() as manager:
        vm = manager.create_vm("async_vm")
        future = manager.execute_vm_async("async_vm", 'print("Async execution works!")')
        result = future.result()
        print("✅ Async VM:", result['stdout'])
except Exception as e:
    print("❌ Async VM failed:", e)



print("\n5. Testing Interactive Session Lifecycle")
try:
    from pylua_vm import VMManager
    manager = VMManager()
    vm_id = "interactive_test_vm"
    # Cleanup any existing VM
    try: manager.terminate_vm_session(vm_id)
    except: pass
    session = manager.create_interactive_vm(vm_id)
    print("✅ Interactive VM created")
    manager.send_input(vm_id, "x = 42\n")
    manager.send_input(vm_id, "print('The answer is:', x)\n")
    time.sleep(0.5)
    output = clean_output(manager.read_output(vm_id))
    print(f"[DEBUG] Output after setting x=42: {output!r}")
    print(f"[DEBUG] Session state: {session.__dict__}")
    if "The answer is: 42" in output: print("✅ Interactive I/O OK")
    else: print("⚠️ Unexpected output:", output)
    # Session persistence
    manager.send_input(vm_id, "y = x * 2\n")
    manager.send_input(vm_id, "print('Double is:', y)\n")
    time.sleep(0.5)
    output2 = clean_output(manager.read_output(vm_id))
    print(f"[DEBUG] Output after setting y=x*2: {output2!r}")
    print(f"[DEBUG] Session state: {session.__dict__}")
    if "Double is: 84" in output2: print("✅ Session Persistence OK")
    else: print("⚠️ Session Persistence failed")
    manager.detach_from_vm(vm_id)
    print("✅ Session detached")
    manager.terminate_vm_session(vm_id)
    print("✅ Session terminated")
except Exception as e:
    print("❌ Interactive Session failed:", e)


print("\n6. Testing Session Manager")
try:
    from pylua_vm import SessionManager, VMManager
    session_manager = SessionManager()
    sessions = session_manager.list_sessions()
    print(f"✅ Active sessions: {len(sessions)}, {sessions!r}")
    manager = VMManager()
    vm_id = "session_manager_test"
    try: manager.terminate_vm_session(vm_id)
    except: pass
    vm_instance = manager.create_interactive_vm(vm_id)
    session_manager.create_session(vm_id, vm_instance)
    print("✅ Session created via SessionManager")
    sessions = session_manager.list_sessions()
    if vm_id in sessions: print("✅ Session appears in registry")
    else: print("⚠️ Session not found")
    session_manager.terminate_session(vm_id)
    manager.terminate_vm_session(vm_id)
    print("✅ Session cleaned up")
except Exception as e:
    print("❌ Registry operations failed:", e)

# === 7. Exception Handling ===
print("\n7. Testing Exception Handling")
try:
    manager = VMManager()
    try: manager.attach_to_vm("nonexistent_vm")
    except SessionNotFoundError: print("✅ SessionNotFoundError raised correctly")
except Exception as e: print("⚠️ Unexpected exception:", e)

try:
    manager = VMManager()
    vm_id = "duplicate_test"
    try: manager.terminate_vm_session(vm_id)
    except: pass
    manager.create_interactive_vm(vm_id)
    try: manager.create_interactive_vm(vm_id)
    except SessionAlreadyExistsError: print("✅ SessionAlreadyExistsError raised correctly")
    finally:
        try: manager.terminate_vm_session(vm_id)
        except: pass
except Exception as e: print("⚠️ Unexpected exception:", e)

try:
    manager = VMManager()
    try: manager.detach_from_vm("never_attached_vm")
    except DetachError: print("✅ DetachError raised correctly")
except Exception as e: print("⚠️ Unexpected exception:", e)

# === 8. VM Registry ===
print("\n8. Testing VM Registry")
if not SESSION_MANAGER_AVAILABLE:
    print("⚠️ VM Registry test skipped")
else:
    try:
        manager = VMManager()
        vm_ids = ["registry_vm_1", "registry_vm_2", "registry_vm_3"]
        for vm_id in vm_ids:
            try: manager.terminate_vm_session(vm_id)
            except: pass
            manager.create_interactive_vm(vm_id)
        
        session_manager = SessionManager()
        active_sessions = session_manager.list_sessions()
        print(f"✅ Registry listing: {len(active_sessions)}, {active_sessions!r}")
        created_count = sum(1 for vm_id in vm_ids if vm_id in active_sessions)
        if created_count == 3: print("✅ All test VMs found")
        else: print(f"⚠️ Only {created_count}/3 VMs found")
        
        for vm_id in vm_ids:
            try: manager.terminate_vm_session(vm_id)
            except: pass
        print("✅ Registry cleanup completed")
    except Exception as e: print("❌ Registry operations failed:", e)


print("\n9. Testing Complex Interactive Session")
try:
    from pylua_vm import VMManager
    manager = VMManager()
    vm_id = "complex_session"
    try: manager.terminate_vm_session(vm_id)
    except: pass
    session = manager.create_interactive_vm(vm_id)
    manager.send_input(vm_id, """
function fibonacci(n)
    if n <= 1 then return n else return fibonacci(n-1)+fibonacci(n-2) end
end
""")
    manager.send_input(vm_id, "print('Fibonacci 10:', fibonacci(10))\n")
    time.sleep(1.0)
    output = clean_output(manager.read_output(vm_id))
    print(f"[DEBUG] Output after fibonacci(10): {output!r}")
    print(f"[DEBUG] Session state: {session.__dict__}")
    if "Fibonacci 10: 55" in output: print("✅ Complex session OK")
    else: print("⚠️ Unexpected output:", output)
    manager.send_input(vm_id, """
for i=1,5 do print('Count:', i) end
""")
    time.sleep(1.0)
    output = clean_output(manager.read_output(vm_id))
    print(f"[DEBUG] Output after for loop: {output!r}")
    print(f"[DEBUG] Session state: {session.__dict__}")
    if "Count: 5" in output: print("✅ Multi-line input OK")
    else: print("⚠️ Multi-line input failed")
    manager.terminate_vm_session(vm_id)
except Exception as e: print("❌ Complex session failed:", e)


print("\n10. Testing Session Reattachment")
try:
    from pylua_vm import VMManager
    manager = VMManager()
    vm_id = "reattach_test"
    try: manager.terminate_vm_session(vm_id)
    except: pass
    session = manager.create_interactive_vm(vm_id)
    manager.send_input(vm_id, "persistent_var = 'I persist!'\n")
    time.sleep(0.5)
    output1 = clean_output(manager.read_output(vm_id))
    print(f"[DEBUG] Output after setting persistent_var: {output1!r}")
    print(f"[DEBUG] Session state before detach: {session.__dict__}")
    manager.detach_from_vm(vm_id)
    print("✅ Detached from session")
    manager.attach_to_vm(vm_id)
    print("✅ Reattached to session")
    manager.send_input(vm_id, "print('Variable still exists:', persistent_var)\n")
    time.sleep(0.5)
    output2 = clean_output(manager.read_output(vm_id))
    print(f"[DEBUG] Output after reattach and print: {output2!r}")
    print(f"[DEBUG] Session state after reattach: {session.__dict__}")
    if "I persist!" in output2: print("✅ Session persistence OK")
    else: print("⚠️ Variables lost after reattachment")
    manager.terminate_vm_session(vm_id)
except Exception as e: print("❌ Session reattachment failed:", e)

print("\n" + "=" * 50)
print("Installation test complete!")
print("All features tested for pylua-bioxen")

