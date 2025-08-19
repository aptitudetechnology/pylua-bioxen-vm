"""
pylua-bioxen-vm: A Python library for orchestrating networked Lua virtual machines.
This library provides process-isolated Lua VMs managed from Python with built-in
networking capabilities using LuaSocket and full interactive terminal support.
Perfect for distributed computing, microservices, game servers, and sandboxed scripting.
"""

# Core VM management
from .lua_process import LuaProcess
from .vm_manager import VMManager, VMCluster
from .vm_manager import VMManager, VMCluster
from .interactive_session import InteractiveSession, SessionManager
# Interactive terminal support  
from .interactive_session import InteractiveSession, SessionManager

# Networking
from .networking import NetworkedLuaVM, LuaScriptTemplate, validate_port, validate_host

# Exception classes - maintain backward compatibility with existing names
from .exceptions import (
    # Keep existing exception names for backward compatibility
    LuaVMError,
    LuaProcessError, 
    NetworkingError,
    LuaNotFoundError,
    LuaSocketNotFoundError,
    VMConnectionError,
    VMTimeoutError,
    ScriptGenerationError,
    
    # New interactive session exceptions
    InteractiveSessionError,
    AttachError,
    DetachError,
    PTYError,
    SessionNotFoundError,
    SessionAlreadyExistsError,
    SessionStateError,
    IOThreadError,
    ProcessRegistryError,
    VMManagerError
)

# Version info
__version__ = "0.2.0"
__author__ = "pylua-bioxen-vm contributors"  
__email__ = ""
__description__ = "Process-isolated networked Lua VMs with interactive terminal support"
__url__ = "https://github.com/yourusername/pylua-bioxen-vm"

# Main exports for easy importing
__all__ = [
    # Core classes
    "LuaProcess",
    "NetworkedLuaVM", 
    "VMManager",
    "VMCluster",
    
    # Interactive terminal classes
    "InteractiveSession",
    "SessionManager",
    
    # Utilities
    "LuaScriptTemplate",
    "validate_port",
    "validate_host",
    
    # Existing exceptions (backward compatibility)
    "LuaVMError",
    "LuaProcessError",
    "NetworkingError", 
    "LuaNotFoundError",
    "LuaSocketNotFoundError",
    "VMConnectionError",
    "VMTimeoutError",
    "ScriptGenerationError",
    
    # New interactive session exceptions
    "InteractiveSessionError",
    "AttachError", 
    "DetachError",
    "PTYError",
    "SessionNotFoundError",
    "SessionAlreadyExistsError",
    "SessionStateError",
    "IOThreadError",
    "ProcessRegistryError",
    "VMManagerError",
    
    # Metadata
    "__version__",
    
    # Convenience functions
    "create_vm",
    "create_manager",
    "create_interactive_manager",
    "create_interactive_session"
]


# Convenience function for quick VM creation (backward compatible)
def create_vm(vm_id: str = "default", networked: bool = False, lua_executable: str = "lua") -> LuaProcess:
    """
    Quick VM creation function.
    
    Args:
        vm_id: Unique identifier for the VM
        networked: Whether to create a networked VM with socket support  
        lua_executable: Path to Lua interpreter
        
    Returns:
        The created VM instance
    """
    if networked:
        return NetworkedLuaVM(name=vm_id, lua_executable=lua_executable)
    else:
        return LuaProcess(name=vm_id, lua_executable=lua_executable)


def create_manager(max_workers: int = 10, lua_executable: str = "lua") -> VMManager:
    """
    Quick VMManager creation function (backward compatible).
    
    Args:
        max_workers: Maximum number of concurrent VM executions
        lua_executable: Path to Lua interpreter
        
    Returns:
        A new VMManager instance
    """
    return VMManager(max_workers=max_workers, lua_executable=lua_executable)


def create_interactive_manager(max_workers: int = 10, lua_executable: str = "lua") -> VMManager:
    """
    Create a VMManager optimized for interactive terminal usage.
    
    Args:
        max_workers: Maximum number of concurrent VM executions
        lua_executable: Path to Lua interpreter
        
    Returns:
        A new VMManager instance with interactive capabilities
        
    Example:
        >>> manager = create_interactive_manager()
        >>> session = manager.create_interactive_vm("my_vm", auto_attach=True)
        >>> session.send_command("print('Hello from interactive Lua!')")
        >>> output = session.read_output()
    """
    return VMManager(max_workers=max_workers, lua_executable=lua_executable)


def create_interactive_session(vm_id: str = "interactive", networked: bool = False, 
                             lua_executable: str = "lua", auto_attach: bool = True) -> InteractiveSession:
    """
    Quick interactive session creation function.
    
    Args:
        vm_id: Unique identifier for the VM
        networked: Whether to create a networked VM
        lua_executable: Path to Lua interpreter  
        auto_attach: Whether to automatically attach to the session
        
    Returns:
        InteractiveSession object ready for use
        
    Example:
        >>> session = create_interactive_session("test")
        >>> session.send_command("x = 42")
        >>> session.send_command("print(x)")
        >>> print(session.read_output())
    """
    manager = VMManager(lua_executable=lua_executable)
    return manager.create_interactive_vm(vm_id, networked=networked, auto_attach=auto_attach)