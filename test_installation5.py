from pylua_vm import VMManager, create_vm, InteractiveSession
try:
    from pylua_vm import SessionManager
    SESSION_MANAGER_AVAILABLE = True
except ImportError:
    SESSION_MANAGER_AVAILABLE = False
from pylua_vm.exceptions import (
    InteractiveSessionError, AttachError, DetachError, 
    SessionNotFoundError, SessionAlreadyExistsError, 
    VMManagerError, ProcessRegistryError
)
import time

print("Testing pylua-bioxen-vm installation...")
print("=" * 50)

# Test 1: Basic VM Creation and Execution (Legacy)
print("\n1. Testing Basic VM Creation and Execution")
try:
    vm = create_vm("test_vm")
    result = vm.execute_string('print("Hello from Lua!")')
    print("✅ Basic VM:", result['stdout'])
except Exception as e:
    print("❌ Basic VM failed:", e)

# Test 2: Networked VM (Legacy)
print("\n2. Testing Networked VM")
try:
    net_vm = create_vm("net_vm", networked=True)
    print("✅ Networked VM created successfully")
except Exception as e:
    print("❌ Networked VM failed:", e)

# Test 3: VM Manager - Synchronous Execution (Legacy)
print("\n3. Testing VM Manager - Synchronous")
try:
    with VMManager() as manager:
        vm = manager.create_vm("managed_vm")
        result = manager.execute_vm_sync("managed_vm", 'print("Square root of 16 is:", math.sqrt(16))')
        print("✅ VM Manager Sync:", result['stdout'])
except Exception as e:
    print("❌ VM Manager Sync failed:", e)

# Test 4: Async Execution (Legacy)
print("\n4. Testing Async Execution")
try:
    with VMManager() as manager:
        vm = manager.create_vm("async_vm")
        future = manager.execute_vm_async("async_vm", 'print("Async execution works!")')
        result = future.result()  # Wait for completion
        print("✅ Async VM:", result['stdout'])
except Exception as e:
    print("❌ Async VM failed:", e)

# Test 5: Interactive Session Lifecycle
print("\n5. Testing Interactive Session Lifecycle")
try:
    manager = VMManager()
    vm_id = "interactive_test_vm"
    
    # Create interactive session
    session = manager.create_interactive_vm(vm_id)
    print("✅ Interactive VM created")
    
    # Send commands and read output
    manager.send_input(vm_id "x = 42\n")
    manager.send_input(vm_id, "print('The answer is:', x)\n")
    time.sleep(0.2)  # Increased for stability
    output = manager.read_output(vm_id)
    print(f"Debug output: {output!r}")  # Log raw output
    
    if "The answer is: 42" in output:
        print("✅ Interactive I/O: Commands executed successfully")
    else:
        print("⚠️ Interactive I/O: Unexpected output:", output)
    
    # Test session persistence
    manager.send_input(vm_id, "y = x * 2\n")
    manager.send_input(vm_id, "print('Double is:', y)\n")
    time.sleep(0.2)
    output2 = manager.read_output(vm_id)
    print(f"Debug output: {output2!r}")
    
    if "Double is: 84" in output2:
        print("✅ Session Persistence: Variables maintained between commands")
    else:
        print("⚠️ Session Persistence: Variables not maintained")
    
    # Detach and terminate
    manager.detach_from_vm(vm_id)
    print("✅ Session detached")
    
    manager.terminate_vm_session(vm_id)
    print("✅ Session terminated")
    
except Exception as e:
    print("❌ Interactive Session failed:", e)

# Test 6: Session Manager Operations
print("\n6. Testing Session Manager")
if not SESSION_MANAGER_AVAILABLE:
    print("⚠️ Session Manager test skipped: SessionManager not found in pylua_vm")
else:
    try:
        session_manager = SessionManager()
        
        # List sessions (should be empty initially)
        sessions = session_manager.list_sessions()
        print(f"✅ Session listing: {len(sessions)} active sessions, sessions: {sessions!r}")
        
        # Create a VM first, then create session with VM instance
        manager = VMManager()
        vm_id = "session_manager_test"
        vm_instance = manager.create_interactive_vm(vm_id)
        
        # Create session through SessionManager with VM instance
        session_manager.create_session(vm_id, vm_instance)
        print("✅ Session created via SessionManager")
        
        # Verify it appears in listing
        sessions = session_manager.list_sessions()
        print(f"Debug sessions: {sessions!r}")
        if vm_id in sessions:
            print("✅ Session appears in registry")
        else:
            print("⚠️ Session not found in registry")
        
        # Cleanup
        session_manager.terminate_session(vm_id)
        manager.terminate_vm_session(vm_id)
        print("✅ Session cleaned up")
        
    except Exception as e:
        print("❌ Session Manager failed:", e)

# Test 7: Exception Handling
print("\n7. Testing Exception Handling")

# Test SessionNotFoundError
try:
    manager = VMManager()
    manager.attach_to_vm("nonexistent_vm")
    print("❌ Should have raised SessionNotFoundError")
except SessionNotFoundError:
    print("✅ SessionNotFoundError raised correctly")
except Exception as e:
    print("⚠️ Unexpected exception:", e)

# Test SessionAlreadyExistsError
try:
    manager = VMManager()
    vm_id = "duplicate_test"
    manager.create_interactive_vm(vm_id)
    try:
        manager.create_interactive_vm(vm_id)  # Should fail
        print("❌ Should have raised SessionAlreadyExistsError")
    except SessionAlreadyExistsError:
        print("✅ SessionAlreadyExistsError raised correctly")
    finally:
        try:
            manager.terminate_vm_session(vm_id)  # Cleanup
        except:
            pass
except Exception as e:
    print("⚠️ Unexpected exception:", e)

# Test DetachError
try:
    manager = VMManager()
    manager.detach_from_vm("never_attached_vm")
    print("❌ Should have raised DetachError")
except DetachError:
    print("✅ DetachError raised correctly")
except Exception as e:
    print("⚠️ Unexpected exception:", e)

# Test 8: VM Registry Operations
print("\n8. Testing VM Registry")
if not SESSION_MANAGER_AVAILABLE:
    print("⚠️ VM Registry test skipped: SessionManager not found in pylua_vm")
else:
    try:
        manager = VMManager()
        
        # Create multiple VMs
        vm_ids = ["registry_vm_1", "registry_vm_2", "registry_vm_3"]
        for vm_id in vm_ids:
            manager.create_interactive_vm(vm_id)
        
        # Check if we can access session manager to list VMs
        session_manager = SessionManager()
        active_sessions = session_manager.list_sessions()
        print(f"✅ Registry listing: {len(active_sessions)} active sessions, sessions: {active_sessions!r}")
        
        # Verify our VMs are accessible
        created_count = sum(1 for vm_id in vm_ids if vm_id in active_sessions)
        
        if created_count == 3:
            print("✅ All test VMs found in registry")
        else:
            print(f"⚠️ Only {created_count}/3 VMs found in registry")
        
        # Cleanup all test VMs
        for vm_id in vm_ids:
            try:
                manager.terminate_vm_session(vm_id)
            except:
                pass
        
        print("✅ Registry cleanup completed")
        
    except Exception as e:
        print("❌ Registry operations failed:", e)

# Test 9: Complex Interactive Session
print("\n9. Testing Complex Interactive Session")
try:
    manager = VMManager()
    vm_id = "complex_session"
    
    # Create session
    session = manager.create_interactive_vm(vm_id)
    
    # Define a function in Lua
    manager.send_input(vm_id, """
function fibonacci(n)
    if n <= 1 then
        return n
    else
        return fibonacci(n-1) + fibonacci(n-2)
    end
end
""")
    
    # Use the function
    manager.send_input(vm_id, "print('Fibonacci 10:', fibonacci(10))\n")
    time.sleep(0.5)  # Increased for complex operation
    output = manager.read_output(vm_id)
    print(f"Debug output: {output!r}")
    
    if "Fibonacci 10: 55" in output:
        print("✅ Complex session: Function definition and execution")
    else:
        print("⚠️ Complex session: Unexpected output:", output)
    
    # Test multi-line input
    manager.send_input(vm_id, """
for i = 1, 5 do
    print('Count:', i)
end
""")
    time.sleep(0.5)
    output = manager.read_output(vm_id)
    print(f"Debug output: {output!r}")
    
    if "Count: 5" in output:
        print("✅ Multi-line input: Loop executed successfully")
    else:
        print("⚠️ Multi-line input: Unexpected output")
    
    # Cleanup
    manager.terminate_vm_session(vm_id)
    
except Exception as e:
    print("❌ Complex session failed:", e)

# Test 10: Session Reattachment
print("\n10. Testing Session Reattachment")
try:
    manager = VMManager()
    vm_id = "reattach_test"
    
    # Create and populate session
    session = manager.create_interactive_vm(vm_id)
    manager.send_input(vm_id, "persistent_var = 'I persist!'\n")
    time.sleep(0.2)
    
    # Detach
    manager.detach_from_vm(vm_id)
    print("✅ Detached from session")
    
    # Reattach
    manager.attach_to_vm(vm_id)
    print("✅ Reattached to session")
    
    # Verify persistence
    manager.send_input(vm_id, "print('Variable still exists:', persistent_var)\n")
    time.sleep(0.2)
    output = manager.read_output(vm_id)
    print(f"Debug output: {output!r}")
    
    if "I persist!" in output:
        print("✅ Session persistence: Variables maintained after reattachment")
    else:
        print("⚠️ Session persistence: Variables lost")
    
    # Cleanup
    manager.terminate_vm_session(vm_id)
    
except Exception as e:
    print("❌ Session reattachment failed:", e)

print("\n" + "=" * 50)
print("Installation test complete!")
print("All features tested for pylua-bioxen-vm interactive support")