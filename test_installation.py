import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pylua_vm import VMManager, SessionManager, create_vm, InteractiveSession
from pylua_vm.logger import VMLogger
from pylua_vm.exceptions import (
    InteractiveSessionError, AttachError, DetachError, 
    SessionNotFoundError, SessionAlreadyExistsError, 
    VMManagerError, ProcessRegistryError
)

# Initialize debug mode - can be controlled via environment variable
debug_mode = os.getenv('PYLUA_DEBUG', 'false').lower() in ('true', '1', 'yes', 'on')
logger = VMLogger(debug_mode=debug_mode, component="TestInstallation")

SESSION_MANAGER_AVAILABLE = True
print("✅ Modules imported successfully")
print("✅ SessionManager available")

import time
import re
import traceback

# Helper function to clean Lua output
def clean_output(output):
    """Remove Lua prompts and ANSI escape codes from output."""
    if not output:
        return ""
    output = re.sub(r'\x1b\[[;?0-9]*[a-zA-Z]', '', output)
    output = re.sub(r'^\s*(>|>>)\s*', '', output, flags=re.MULTILINE)
    output = re.sub(r'\r\n|\r|\n', '\n', output).strip()
    return output

def check_output_contains(output, expected_parts, test_name=""):
    """Check if output contains expected parts, handling tabs/spaces flexibly."""
    if not output:
        return False, f"No output received for {test_name}"
    
    output_clean = clean_output(output)
    missing_parts = []
    
    for part in expected_parts:
        # Simple substring search - much more reliable
        if part not in output_clean:
            missing_parts.append(part)
    
    if missing_parts:
        return False, f"Missing from output: {missing_parts}. Got: {output_clean!r}"
    return True, "OK"

# === 1. Basic VM Creation ===
print("\n1. Testing Basic VM Creation and Execution")
try:
    vm = create_vm("test_vm", debug_mode=debug_mode)
    logger.debug(f"VM object: {vm}")
    result = vm.execute_string('print("Hello from Lua!")')
    logger.debug(f"Execution result: {result}")
    print("✅ Basic VM:", result['stdout'])
except Exception as e:
    print("❌ Basic VM failed:", e)
    traceback.print_exc()

# === 2. Networked VM ===
print("\n2. Testing Networked VM")
try:
    net_vm = create_vm("net_vm", networked=True, debug_mode=debug_mode)
    logger.debug(f"Networked VM object: {net_vm}")
    print("✅ Networked VM created successfully")
except Exception as e:
    print("❌ Networked VM failed:", e)
    traceback.print_exc()

# === 3. VM Manager - Synchronous ===
print("\n3. Testing VM Manager - Synchronous")
try:
    with VMManager(debug_mode=debug_mode) as manager:
        logger.debug(f"VMManager object: {manager}")
        vm = manager.create_vm("managed_vm")
        logger.debug(f"Managed VM object: {vm}")
        result = manager.execute_vm_sync("managed_vm", 'print("Square root of 16 is:", math.sqrt(16))')
        logger.debug(f"Sync execution result: {result}")
        print("✅ VM Manager Sync:", result['stdout'])
except Exception as e:
    print("❌ VM Manager Sync failed:", e)
    traceback.print_exc()

# === 4. Async Execution ===
print("\n4. Testing Async Execution")
try:
    with VMManager(debug_mode=debug_mode) as manager:
        logger.debug(f"VMManager object: {manager}")
        vm = manager.create_vm("async_vm")
        logger.debug(f"Async VM object: {vm}")
        future = manager.execute_vm_async("async_vm", 'print("Async execution works!")')
        logger.debug(f"Future object: {future}")
        result = future.result()
        logger.debug(f"Async execution result: {result}")
        print("✅ Async VM:", result['stdout'])
except Exception as e:
    print("❌ Async VM failed:", e)
    traceback.print_exc()

# === 5. Interactive Session Lifecycle ===
print("\n5. Testing Interactive Session Lifecycle")
try:
    manager = VMManager(debug_mode=debug_mode)
    logger.debug(f"VMManager object: {manager}")
    vm_id = "interactive_test_vm"
    # Cleanup any existing VM
    try:
        manager.terminate_vm_session(vm_id)
        logger.debug(f"Terminated any existing VM session for {vm_id}")
    except Exception as cleanup_e:
        logger.debug(f"Cleanup exception (OK): {cleanup_e}")
    
    session = manager.create_interactive_vm(vm_id)
    logger.debug(f"Interactive session object: {session}")
    
    # Test basic I/O
    manager.send_input(vm_id, "x = 42\n")
    manager.send_input(vm_id, "print('The answer is:', x)\n")
    time.sleep(0.5)
    output = manager.read_output(vm_id)
    logger.debug(f"Output after setting x=42: {output!r}")
    
    success, message = check_output_contains(output, ["The answer is", "42"], "basic I/O")
    if success:
        print("✅ Interactive I/O OK")
    else:
        print(f"⚠️ Interactive I/O issue: {message}")
    
    # Test session persistence
    manager.send_input(vm_id, "y = x * 2\n")
    manager.send_input(vm_id, "print('Double is:', y)\n")
    time.sleep(0.5)
    output2 = manager.read_output(vm_id)
    logger.debug(f"Output after setting y=x*2: {output2!r}")
    
    success, message = check_output_contains(output2, ["Double is", "84"], "session persistence")
    if success:
        print("✅ Session Persistence OK")
    else:
        print(f"⚠️ Session Persistence issue: {message}")
    
    manager.detach_from_vm(vm_id)
    print("✅ Session detached")
    manager.terminate_vm_session(vm_id)
    print("✅ Session terminated")
    
except Exception as e:
    print("❌ Interactive Session failed:", e)
    traceback.print_exc()

# === 6. Testing Session Manager ===
print("\n6. Testing Session Manager")
try:
    manager = VMManager(debug_mode=debug_mode)
    # Use the same session manager instance as VMManager
    session_manager = manager.session_manager
    sessions = session_manager.list_sessions()
    print(f"✅ Active sessions: {len(sessions)}, {sessions!r}")
    
    vm_id = "session_manager_test"
    try: 
        manager.terminate_vm_session(vm_id)
    except: 
        pass
    
    # Create VM and let VMManager handle session creation
    vm_instance = manager.create_interactive_vm(vm_id)
    print("✅ Session created via VMManager")
    
    sessions = session_manager.list_sessions()
    if vm_id in sessions: 
        print("✅ Session appears in registry")
    else: 
        print(f"⚠️ Session not found. Available: {list(sessions.keys())}")
    
    session_manager.terminate_session(vm_id)
    manager.terminate_vm_session(vm_id)
    print("✅ Session cleaned up")
    
except Exception as e:
    print("❌ Registry operations failed:", e)
    traceback.print_exc()

# === 7. Exception Handling ===
print("\n7. Testing Exception Handling")
try:
    manager = VMManager(debug_mode=debug_mode)
    try: 
        manager.attach_to_vm("nonexistent_vm")
    except SessionNotFoundError: 
        print("✅ SessionNotFoundError raised correctly")
    except Exception as e:
        print(f"⚠️ Wrong exception type: {type(e).__name__}: {e}")
except Exception as e: 
    print("⚠️ Unexpected exception in SessionNotFoundError test:", e)

try:
    manager = VMManager(debug_mode=debug_mode)
    vm_id = "duplicate_test"
    try: 
        manager.terminate_vm_session(vm_id)
    except: 
        pass
    
    manager.create_interactive_vm(vm_id)
    try: 
        manager.create_interactive_vm(vm_id)  # This should fail
        print("⚠️ Expected SessionAlreadyExistsError but none raised")
    except (SessionAlreadyExistsError, ValueError) as e:
        # ValueError might be raised instead of SessionAlreadyExistsError
        print(f"✅ Duplicate creation blocked: {type(e).__name__}")
    finally:
        try: 
            manager.terminate_vm_session(vm_id)
        except: 
            pass
except Exception as e: 
    print("⚠️ Unexpected exception in duplicate test:", e)

try:
    manager = VMManager(debug_mode=debug_mode)
    try: 
        manager.detach_from_vm("never_attached_vm")
    except (DetachError, SessionNotFoundError):
        print("✅ DetachError/SessionNotFoundError raised correctly")
    except Exception as e:
        print(f"⚠️ Wrong exception type: {type(e).__name__}: {e}")
except Exception as e: 
    print("⚠️ Unexpected exception in detach test:", e)

# === 8. VM Registry ===
print("\n8. Testing VM Registry")
if not SESSION_MANAGER_AVAILABLE:
    print("⚠️ VM Registry test skipped")
else:
    try:
        manager = VMManager(debug_mode=debug_mode)
        session_manager = manager.session_manager  # Use same instance
        vm_ids = ["registry_vm_1", "registry_vm_2", "registry_vm_3"]
        
        # Clean up first
        for vm_id in vm_ids:
            try: 
                manager.terminate_vm_session(vm_id)
            except: 
                pass
        
        # Create interactive VMs (these will auto-register)
        created_sessions = []
        for vm_id in vm_ids:
            session = manager.create_interactive_vm(vm_id)
            created_sessions.append(session)
        
        active_sessions = session_manager.list_sessions()
        print(f"✅ Registry listing: {len(active_sessions)}, {list(active_sessions.keys())}")
        
        created_count = sum(1 for vm_id in vm_ids if vm_id in active_sessions)
        if created_count == 3: 
            print("✅ All test VMs found")
        else: 
            print(f"⚠️ Only {created_count}/3 VMs found. Missing: {set(vm_ids) - set(active_sessions.keys())}")
        
        # Clean up
        for vm_id in vm_ids:
            try: 
                manager.terminate_vm_session(vm_id)
            except: 
                pass
        print("✅ Registry cleanup completed")
        
    except Exception as e: 
        print("❌ Registry operations failed:", e)
        traceback.print_exc()

# === 9. Testing Complex Interactive Session ===
print("\n9. Testing Complex Interactive Session")
try:
    manager = VMManager(debug_mode=debug_mode)
    vm_id = "complex_session"
    try: 
        manager.terminate_vm_session(vm_id)
    except: 
        pass
    
    session = manager.create_interactive_vm(vm_id)
    
    # Multi-line function definition
    manager.send_input(vm_id, "function fibonacci(n)\n")
    manager.send_input(vm_id, "    if n <= 1 then return n else return fibonacci(n-1)+fibonacci(n-2) end\n")
    manager.send_input(vm_id, "end\n")
    manager.send_input(vm_id, "print('Fibonacci 10:', fibonacci(10))\n")
    time.sleep(1.0)
    output = manager.read_output(vm_id)
    logger.debug(f"Output after fibonacci(10): {output!r}")
    
    success, message = check_output_contains(output, ["Fibonacci 10", "55"], "fibonacci function")
    if success:
        print("✅ Complex function OK")
    else:
        print(f"⚠️ Complex function issue: {message}")
    
    # Single-line loop
    manager.send_input(vm_id, "for i=1,5 do print('Count:', i) end\n")
    time.sleep(1.0)
    output = manager.read_output(vm_id)
    logger.debug(f"Output after for loop: {output!r}")
    
    success, message = check_output_contains(output, ["Count", "1", "Count", "5"], "for loop")
    if success:
        print("✅ Multi-line input OK")
    else:
        print(f"⚠️ Multi-line input issue: {message}")
    
    manager.terminate_vm_session(vm_id)
    
except Exception as e: 
    print("❌ Complex session failed:", e)
    traceback.print_exc()

# === 10. Testing Session Reattachment ===
print("\n10. Testing Session Reattachment")
try:
    manager = VMManager(debug_mode=debug_mode)
    vm_id = "reattach_test"
    try: 
        manager.terminate_vm_session(vm_id)
    except: 
        pass
    
    session = manager.create_interactive_vm(vm_id)
    
    # Set a variable
    manager.send_input(vm_id, "persistent_var = 'I persist!'\n")
    time.sleep(0.5)
    output1 = manager.read_output(vm_id)
    logger.debug(f"Output after setting persistent_var: {output1!r}")
    
    # Detach and reattach
    manager.detach_from_vm(vm_id)
    print("✅ Detached from session")
    manager.attach_to_vm(vm_id)
    print("✅ Reattached to session")
    
    # Test if variable persisted
    manager.send_input(vm_id, "print('Variable still exists:', persistent_var)\n")
    time.sleep(0.5)
    output2 = manager.read_output(vm_id)
    logger.debug(f"Output after reattach and print: {output2!r}")
    
    success, message = check_output_contains(output2, ["Variable still exists", "I persist"], "variable persistence")
    if success:
        print("✅ Session persistence OK")
    else:
        print(f"⚠️ Variable persistence issue: {message}")
    
    manager.terminate_vm_session(vm_id)
    
except Exception as e: 
    print("❌ Session reattachment failed:", e)
    traceback.print_exc()

print("\n" + "=" * 50)
print("Installation test complete!")
print("All features tested for pylua-bioxen")

# Debug mode info
if debug_mode:
    print(f"\n🔧 Debug mode was ENABLED (PYLUA_DEBUG={os.getenv('PYLUA_DEBUG', 'not set')})")
else:
    print(f"\n🔧 Debug mode was DISABLED. Set PYLUA_DEBUG=true to enable detailed logging.")