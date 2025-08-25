pylua_bioxen_vm_lib Specification
Overview
The pylua_bioxen_vm_lib (version 0.1.6) is a Python library for managing Lua virtual machines (VMs) within the BioXen framework, enabling biological computation and genomic data virtualization. It supports synchronous and asynchronous Lua code execution, interactive sessions, and package management for Lua environments. This library is ideal for applications integrating lightweight, sandboxed Lua VMs with biological workflows.
This updated specification reflects the development branch of the codebase, addressing compliance findings and providing clear guidance for developers.
Key Components
1. VM Creation

Module: pylua_bioxen_vm_lib
Key Function: create_vm(vm_id: str, networked: bool = False, persistent: bool = False, debug_mode: bool = False, lua_executable: str = "lua") -> LuaProcess
Creates a Lua VM instance with a unique identifier.
Parameters:
vm_id: Unique VM identifier.
networked: Enables experimental networking if True.
persistent: If True, creates a VM that persists for multiple sessions.
debug_mode: Enables verbose logging if True.
lua_executable: Path to the Lua executable (defaults to "lua").


Returns: A LuaProcess object for executing Lua code.
Example:from pylua_bioxen_vm_lib import create_vm
vm = create_vm("test_vm", debug_mode=True)
result = vm.execute_string('print("Hello, BioXen!")')
print(result['stdout'])  # Output: Hello, BioXen!





2. VM Manager

Class: VMManager
Manages multiple Lua VMs and sessions.
Key Methods:
create_vm(vm_id: str, networked: bool = False, persistent: bool = False) -> LuaProcess: Creates a managed VM.
execute_vm_sync(vm_id: str, code: str) -> dict: Executes Lua code synchronously, returning a dictionary with stdout and metadata.
execute_vm_async(vm_id: str, code: str) -> Future: Executes Lua code asynchronously, returning a Future object.
create_interactive_vm(vm_id: str) -> InteractiveSession: Creates a persistent interactive VM session.
attach_to_vm(vm_id: str) -> InteractiveSession: Attaches to an existing session.
detach_from_vm(vm_id: str): Detaches from a session without terminating it.
terminate_vm_session(vm_id: str): Terminates a VM session.
send_input(vm_id: str, input: str): Sends input to an interactive session.
read_output(vm_id: str) -> str: Reads output from an interactive session.
list_sessions() -> List[dict]: Lists active sessions with their details.


Usage:from pylua_bioxen_vm_lib import VMManager
with VMManager(debug_mode=True) as manager:
    vm = manager.create_vm("managed_vm")
    result = manager.execute_vm_sync("managed_vm", 'print("Result:", 2 + 2)')
    print(result['stdout'])  # Output: Result: 4





3. Interactive Session

Class: InteractiveSession
Manages interactive Lua VM sessions for real-time input/output.
Key Methods:
send_input(input: str): Sends Lua code to the session (alternative to load_package for package loading).
read_output() -> str: Retrieves session output.
interactive_loop(): Starts an interactive REPL loop (may be implemented as send_input/read_output sequences).
load_package(package_name: str): Loads a Lua package (may use send_input internally).
set_environment(env_name: str): Sets the Lua environment for the session.


Note: Some implementations may use send_input/read_output instead of load_package or interactive_loop.
Usage:from pylua_bioxen_vm_lib import VMManager
manager = VMManager(debug_mode=True)
session = manager.create_interactive_vm("interactive_vm")
manager.send_input("interactive_vm", "x = 42\nprint('Value:', x)\n")
import time
time.sleep(0.5)
print(manager.read_output("interactive_vm"))  # Output: Value: 42





4. Session Manager

Class: SessionManager
Manages the lifecycle of interactive VM sessions.
Key Methods:
list_sessions() -> dict: Returns a dictionary of active session IDs and details.
terminate_session(vm_id: str): Terminates a specific session.


Usage:from pylua_bioxen_vm_lib import VMManager
manager = VMManager(debug_mode=True)
session_manager = manager.session_manager
session = manager.create_interactive_vm("test_session")
sessions = session_manager.list_sessions()
print(sessions)  # Output: {'test_session': <session_details>}
session_manager.terminate_session("test_session")





5. Package Management

Modules: pylua_bioxen_vm_lib.utils.curator, pylua_bioxen_vm_lib.env, pylua_bioxen_vm_lib.package_manager
Manages Lua packages and environments.
Key Classes/Functions:
Curator and get_curator(): Manages package metadata and repositories.
PackageRegistry: Tracks installed packages (may be part of Curator).
PackageInstaller: Handles package installation, updates, and removal.
EnvironmentManager: Manages isolated Lua environments.
PackageManager: Orchestrates package operations.
RepositoryManager: Manages package repositories.
search_packages(query: str) -> List[Package]: Searches for available packages.
bootstrap_lua_environment(env_name: str) -> bool: Bootstraps a Lua environment.


Note: Dependency resolution and validation may be handled within Curator or PackageInstaller.
Usage:from pylua_bioxen_vm_lib.utils.curator import PackageInstaller, search_packages
installer = PackageInstaller()
packages = search_packages("math")
installer.install_package("math_package")





6. Exception Handling

Module: pylua_bioxen_vm_lib.exceptions
Key Exceptions:
InteractiveSessionError: General interactive session errors.
AttachError: Errors during session attachment.
DetachError: Errors during session detachment.
SessionNotFoundError: Raised for invalid session IDs.
SessionAlreadyExistsError: Raised for duplicate session creation.
VMManagerError: General VM manager errors.
LuaVMError: Errors during Lua execution.


Usage:from pylua_bioxen_vm_lib import VMManager
from pylua_bioxen_vm_lib.exceptions import SessionNotFoundError
try:
    VMManager().attach_to_vm("nonexistent")
except SessionNotFoundError:
    print("Session not found, as expected")





7. Logging

Class: VMLogger
Provides configurable logging.
Parameters:
debug_mode: bool: Enables verbose logging.
component: str: Identifies the logging component (e.g., "MyApp").


Usage:from pylua_bioxen_vm_lib.logger import VMLogger
logger = VMLogger(debug_mode=True, component="MyApp")
logger.debug("Debug message")





Usage Patterns
Basic VM Execution
Execute simple Lua code:
from pylua_bioxen_vm_lib import create_vm
vm = create_vm("simple_vm", debug_mode=True)
result = vm.execute_string('print("Hello!")')
print(result['stdout'])  # Output: Hello!

Managed VMs
Use context manager for automatic cleanup:
from pylua_bioxen_vm_lib import VMManager
with VMManager(debug_mode=True) as manager:
    vm = manager.create_vm("managed_vm")
    result = manager.execute_vm_sync("managed_vm", 'return 2 + 2')
    print(result['stdout'])  # Output: 4

Interactive Sessions
Manage persistent sessions:
from pylua_bioxen_vm_lib import VMManager
manager = VMManager(debug_mode=True)
session = manager.create_interactive_vm("interactive_vm")
manager.send_input("interactive_vm", "x = 10\nprint('Value:', x)\n")
import time
time.sleep(0.5)
print(manager.read_output("interactive_vm"))  # Output: Value: 10
manager.detach_from_vm("interactive_vm")
manager.attach_to_vm("interactive_vm")
manager.terminate_vm_session("interactive_vm")

Package Management
Install and use Lua packages:
from pylua_bioxen_vm_lib.utils.curator import PackageInstaller
from pylua_bioxen_vm_lib import VMManager
installer = PackageInstaller()
installer.install_package("math_package")
with VMManager() as manager:
    session = manager.create_interactive_vm("package_vm")
    session.load_package("math_package")
    manager.send_input("package_vm", "print(math_package.compute(10))")
    time.sleep(0.5)
    print(manager.read_output("package_vm"))

Best Practices

Use Context Managers: Use VMManager with with statements for automatic resource cleanup.
Handle Exceptions: Catch specific exceptions (e.g., SessionNotFoundError) for robust error handling.
Enable Debug Mode: Set PYLUA_DEBUG=true for detailed logging:export PYLUA_DEBUG=true


Session Lifecycle: Explicitly detach and terminate interactive sessions to free resources.
Package Isolation: Use EnvironmentManager for isolated Lua environments.
Validate Inputs: Check session IDs before creation to avoid SessionAlreadyExistsError.

Example Application
A simple application integrating Lua VMs and packages:
import os
from pylua_bioxen_vm_lib import VMManager, VMLogger
from pylua_bioxen_vm_lib.utils.curator import PackageInstaller
logger = VMLogger(debug_mode=os.getenv('PYLUA_DEBUG', 'false').lower() == 'true', component="App")
installer = PackageInstaller()
installer.install_package("math_package")
with VMManager(debug_mode=True) as manager:
    session = manager.create_interactive_vm("app_vm")
    session.load_package("math_package")
    manager.send_input("app_vm", 'print("Result:", math_package.compute(10))\n')
    import time
    time.sleep(0.5)
    print(manager.read_output("app_vm"))
    manager.terminate_vm_session("app_vm")

Dependencies

Python 3.6+
pylua-bioxen-vm-lib (install via pip install pylua-bioxen-vm-lib)

Notes

Integrates with the BioXen framework for biological computing.
Networking (networked=True) is experimental and may require configuration.
Package management may merge dependency resolution and validation into Curator or PackageInstaller.
Interactive sessions may use send_input/read_output instead of load_package/interactive_loop in some implementations.
For API access, visit xAI API.
