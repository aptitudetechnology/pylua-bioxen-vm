# test_installation.py
# Start with minimal imports to test what's available
try:
    from pylua_vm import create_vm
    print("✅ create_vm imported successfully")
except ImportError as e:
    print("❌ create_vm import failed:", e)

try:
    from pylua_vm import VMManager
    print("✅ VMManager imported successfully")
except ImportError as e:
    print("❌ VMManager import failed:", e)

try:
    from pylua_vm import InteractiveSession
    print("✅ InteractiveSession imported successfully")
except ImportError as e:
    print("❌ InteractiveSession import failed:", e)

try:
    from pylua_vm import SessionManager
    print("✅ SessionManager imported successfully")
except ImportError as e:
    print("❌ SessionManager import failed:", e)

# Try importing exceptions
try:
    from pylua_vm.exceptions import (
        InteractiveSessionError, AttachError, DetachError, 
        SessionNotFoundError, SessionAlreadyExistsError, 
        VMManagerError, ProcessRegistryError
    )
    print("✅ All exceptions imported successfully")
except ImportError as e:
    print("❌ Exception imports failed:", e)

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
    manager.send_input(vm_id, "x = 42\n")
    manager.send_input(vm_id, "print('The answer is:', x)\n")
    time.sleep(0.1)  # Brief pause for execution
    output = manager.read_output(vm_id)
    
    if "The answer is: 42" in output:
        print("✅ Interactive I/O:", "Commands executed successfully")
    else:
        print("⚠️ Interactive I/O: Unexpected output:", output)
    
    # Test session persistence
    manager.send_input(vm_id, "y = x * 2\n")
    manager.send_input(vm_id, "print('Double is:', y)\n")
    time.sleep(0.1)
    output2 = manager.read_output(vm_id)
    
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
try:
    session_manager = SessionManager()
    
    # List sessions (should be empty initially)
    sessions = session_manager.list_sessions()
    print(f"✅ Session listing: {len(sessions)} active sessions")
    
    # Create a session through SessionManager
    vm_id = "session_manager_test"
    session_manager.create_session(vm_id)
    print("✅ Session created via SessionManager")
    
    # Verify it appears in listing
    sessions = session_manager.list_sessions()
    if vm_id in [s['vm_id'] for s in sessions]:
        print("✅ Session appears in registry")
    else:
        print("⚠️ Session not found in registry")
    
    # Cleanup
    session_manager.terminate_session(vm_id)
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
    manager.create_interactive_vm(vm_id)  # Should fail
    print("❌ Should have raised SessionAlreadyExistsError")
    manager.terminate_vm_session(vm_id)  # Cleanup
except SessionAlreadyExistsError:
    print("✅ SessionAlreadyExistsError raised correctly")
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
try:
    manager = VMManager()
    
    # Create multiple VMs
    vm_ids = ["registry_vm_1", "registry_vm_2", "registry_vm_3"]
    for vm_id in vm_ids:
        manager.create_interactive_vm(vm_id)
    
    # List all VMs
    active_vms = manager.list_active_vms()
    print(f"✅ Registry listing: {len(active_vms)} active VMs")
    
    # Verify our VMs are in the list
    found_vms = [vm for vm in active_vms if vm['vm_id'] in vm_ids]
    if len(found_vms) == 3:
        print("✅ All test VMs found in registry")
    else:
        print(f"⚠️ Only {len(found_vms)}/3 VMs found in registry")
    
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
    time.sleep(0.2)  # Allow execution time
    
    output = manager.read_output(vm_id)
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
    time.sleep(0.1)
    
    output = manager.read_output(vm_id)
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
    time.sleep(0.1)
    
    # Detach
    manager.detach_from_vm(vm_id)
    print("✅ Detached from session")
    
    # Reattach
    manager.attach_to_vm(vm_id)
    print("✅ Reattached to session")
    
    # Verify persistence
    manager.send_input(vm_id, "print('Variable still exists:', persistent_var)\n")
    time.sleep(0.1)
    output = manager.read_output(vm_id)
    
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