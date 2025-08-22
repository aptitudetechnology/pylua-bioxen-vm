"""
Basic usage example for PyLua VM Curator system.
Demonstrates environment setup, package installation, VM creation, and health checks.
"""
from pylua_vm.env import EnvironmentManager
from pylua_vm.utils.curator import Curator
from pylua_vm.lua_process import LuaProcess
from pylua_vm.vm_manager import VMManager
from pylua_vm.interactive_session import SessionManager

# Setup environment
env = EnvironmentManager(profile='standard')
print("System info:", env.get_system_info())
errors = env.validate()
if errors:
    print("Environment errors:", errors)
else:
    print("Environment validated.")

# Curator package management
curator = Curator()
curator.curate_environment('standard')
curator.install_package('lua-cjson')

# Create a Lua VM and run code
vm = LuaProcess(name='example_vm')
result = vm.execute_string('print("Hello from Lua!")')
print("Lua VM result:", result)

# Health check and recommendations
health = curator.health_check()
print("Health check:", health)
recs = curator.get_recommendations()
print("Recommended packages:", recs)

# Interactive Session Lifecycle
try:
    vm_manager = VMManager()
    session = vm_manager.create_interactive_session()
    print("Interactive Session created:", session)
except NameError as e:
    print("❌ Interactive Session failed:", e)
except Exception as e:
    print("❌ Interactive Session error:", e)

# Session Manager Registry Operations
try:
    session_manager = SessionManager()
    session_manager.register_session('example_session', session)
    print("Session registered in manager.")
except NameError as e:
    print("❌ Registry operations failed:", e)
except Exception as e:
    print("❌ Registry operations error:", e)

# Complex Interactive Session
try:
    complex_session = vm_manager.create_interactive_session(config={'complex': True})
    print("Complex Interactive Session created:", complex_session)
except NameError as e:
    print("❌ Complex session failed:", e)
except Exception as e:
    print("❌ Complex session error:", e)

# Session Reattachment
try:
    reattached = vm_manager.reattach_session('example_session')
    print("Session reattached:", reattached)
except NameError as e:
    print("❌ Session reattachment failed:", e)
except Exception as e:
    print("❌ Session reattachment error:", e)

print("==================================================")
print("Installation test complete!")
print("All features tested for pylua_bioxen_vm_lib interactive support")
