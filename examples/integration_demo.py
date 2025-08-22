"""
Integration Demo for pylua_bioxen_vm_lib
Demonstrates environment setup, package installation, VM creation, curator usage, and logging.
"""

from pylua_vm.env import EnvironmentManager
from pylua_vm.utils.curator import Curator
from pylua_vm.lua_process import LuaVM
from pylua_vm.logger import VMLogger
import sys

# Initialize logger
logger = VMLogger()
logger.info("Starting integration demo...")

# Step 1: Setup environment
env_manager = EnvironmentManager(logger=logger)
if not env_manager.validate():
    logger.error("Environment validation failed. Exiting.")
    sys.exit(1)
logger.info("Environment validated.")

# Step 2: Curator - recommend and install packages
curator = Curator(env_manager=env_manager, logger=logger)
recommended = curator.recommend_packages()
logger.info(f"Recommended packages: {recommended}")
for pkg in recommended:
    success = curator.install_package(pkg)
    if success:
        logger.info(f"Installed package: {pkg}")
    else:
        logger.warning(f"Failed to install package: {pkg}")

# Step 3: Health check
health = curator.health_check()
logger.info(f"Curator health check: {health}")

# Step 4: Create and use Lua VM
vm = LuaVM(env_manager=env_manager, logger=logger)
result = vm.execute('print("Hello from Lua VM!")')
logger.info(f"Lua VM execution result: {result}")

# Step 5: CLI invocation example (optional)
logger.info("You can also use the CLI tool: python -m pylua_vm.cli --help")

logger.info("Integration demo complete.")
