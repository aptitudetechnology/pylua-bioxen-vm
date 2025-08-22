"""
Basic usage example for PyLua VM Curator system.
Demonstrates environment setup, package installation, VM creation, and health checks.
"""
from pylua_vm.env import EnvironmentManager
from pylua_vm.utils.curator import Curator
from pylua_vm.lua_process import LuaProcess

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
