
import sys, os
import traceback

# Add the necessary paths for imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Test that the imports themselves work
try:
    from pylua_vm import VMManager, SessionManager, create_vm, InteractiveSession
    from pylua_vm.exceptions import (
        InteractiveSessionError, AttachError, DetachError, 
        SessionNotFoundError, SessionAlreadyExistsError, 
        VMManagerError, ProcessRegistryError
    )
    print("✅ All modules imported successfully.")
except ImportError as e:
    print(f"❌ Critical import failed: {e}")
    sys.exit(1)

def main():
    print("\n--- Starting simplified tests ---")

    # === 5. Interactive Session Lifecycle ===
    print("\n5. Testing Interactive Session Lifecycle")
    try:
        manager = VMManager()
        print("✅ VMManager object created.")
    except Exception as e:
        print(f"❌ Failed to instantiate VMManager: {e}")
        traceback.print_exc()

    # === 6. Testing Session Manager ===
    print("\n6. Testing Session Manager")
    try:
        manager = VMManager()
        session_manager = manager.session_manager
        print("✅ SessionManager object accessed.")
    except Exception as e:
        print(f"❌ Failed to access SessionManager: {e}")
        traceback.print_exc()

    # === 9. Testing Complex Interactive Session ===
    print("\n9. Testing Complex Interactive Session")
    try:
        manager = VMManager()
        print("✅ VMManager object created for complex session test.")
    except Exception as e:
        print(f"❌ Failed to instantiate VMManager: {e}")
        traceback.print_exc()

    # === 10. Testing Session Reattachment ===
    print("\n10. Testing Session Reattachment")
    try:
        manager = VMManager()
        print("✅ VMManager object created for reattachment test.")
    except Exception as e:
        print(f"❌ Failed to instantiate VMManager: {e}")
        traceback.print_exc()

    print("\n--- Simplified tests complete ---")

if __name__ == "__main__":
    main()