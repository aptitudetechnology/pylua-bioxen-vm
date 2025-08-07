"""
High-level VM manager for orchestrating multiple Lua VMs.

This module provides the main interface for creating, managing, and coordinating
multiple networked Lua VMs.
"""

import threading
import time
from typing import Dict, List, Optional, Any, Callable
from concurrent.futures import ThreadPoolExecutor, Future

from .lua_process import LuaProcess
from .networking import NetworkedLuaVM
from .exceptions import LuaVMError, VMConnectionError


class VMManager:
    """
    High-level manager for multiple Lua VMs.
    
    Handles creation, lifecycle management, and coordination of Lua VMs
    with support for both basic and networked VMs.
    """
    
    def __init__(self, max_workers: int = 10, lua_executable: str = "lua"):
        """
        Initialize the VM manager.
        
        Args:
            max_workers: Maximum number of concurrent VM executions
            lua_executable: Path to Lua interpreter
        """
        self.max_workers = max_workers
        self.lua_executable = lua_executable
        self.vms: Dict[str, LuaProcess] = {}
        self.futures: Dict[str, Future] = {}
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self._lock = threading.Lock()
    
    def create_vm(self, vm_id: str, networked: bool = False) -> LuaProcess:
        """
        Create a new Lua VM.
        
        Args:
            vm_id: Unique identifier for the VM
            networked: Whether to create a networked VM with socket support
            
        Returns:
            The created VM instance
        """
        if vm_id in self.vms:
            raise ValueError(f"VM with ID '{vm_id}' already exists")
        
        with self._lock:
            if networked:
                vm = NetworkedLuaVM(name=vm_id, lua_executable=self.lua_executable)
            else:
                vm = LuaProcess(name=vm_id, lua_executable=self.lua_executable)
            
            self.vms[vm_id] = vm
            return vm
    
    def get_vm(self, vm_id: str) -> Optional[LuaProcess]:
        """Get a VM by ID."""
        return self.vms.get(vm_id)
    
    def list_vms(self) -> List[str]:
        """Get list of all VM IDs."""
        return list(self.vms.keys())
    
    def remove_vm(self, vm_id: str) -> bool:
        """
        Remove a VM and clean up its resources.
        
        Args:
            vm_id: ID of VM to remove
            
        Returns:
            True if VM was removed, False if VM didn't exist
        """
        with self._lock:
            vm = self.vms.pop(vm_id, None)
            if vm:
                vm.cleanup()
                
                # Cancel any running futures for this VM
                future = self.futures.pop(vm_id, None)
                if future and not future.done():
                    future.cancel()
                
                return True
            return False
    
    def execute_vm_async(self, vm_id: str, lua_code: str, 
                        timeout: Optional[float] = None) -> Future:
        """
        Execute Lua code on a VM asynchronously.
        
        Args:
            vm_id: ID of VM to execute on
            lua_code: Lua code to execute
            timeout: Maximum execution time
            
        Returns:
            Future object representing the execution
        """
        vm = self.get_vm(vm_id)
        if not vm:
            raise ValueError(f"VM '{vm_id}' not found")
        
        def execute():
            return vm.execute_string(lua_code, timeout=timeout)
        
        future = self.executor.submit(execute)
        self.futures[vm_id] = future
        return future
    
    def execute_vm_sync(self, vm_id: str, lua_code: str, 
                       timeout: Optional[float] = None) -> Dict[str, Any]:
        """
        Execute Lua code on a VM synchronously.
        
        Args:
            vm_id: ID of VM to execute on
            lua_code: Lua code to execute  
            timeout: Maximum execution time
            
        Returns:
            Execution result dictionary
        """
        vm = self.get_vm(vm_id)
        if not vm:
            raise ValueError(f"VM '{vm_id}' not found")
        
        return vm.execute_string(lua_code, timeout=timeout)
    
    def start_server_vm(self, vm_id: str, port: int, 
                       timeout: Optional[float] = None) -> Future:
        """
        Start a VM as a socket server asynchronously.
        
        Args:
            vm_id: ID of VM to use as server
            port: Port to bind to
            timeout: Maximum execution time
            
        Returns:
            Future object representing the server execution
        """
        vm = self.get_vm(vm_id)
        if not vm or not isinstance(vm, NetworkedLuaVM):
            raise ValueError(f"Networked VM '{vm_id}' not found")
        
        def start_server():
            return vm.start_server(port, timeout=timeout)
        
        future = self.executor.submit(start_server)
        self.futures[vm_id] = future
        return future
    
    def start_client_vm(self, vm_id: str, host: str, port: int, 
                       message: str = "Hello from client!", 
                       timeout: Optional[float] = None) -> Future:
        """
        Start a VM as a socket client asynchronously.
        
        Args:
            vm_id: ID of VM to use as client
            host: Server host to connect to
            port: Server port to connect to
            message: Message to send to server
            timeout: Maximum execution time
            
        Returns:
            Future object representing the client execution
        """
        vm = self.get_vm(vm_id)
        if not vm or not isinstance(vm, NetworkedLuaVM):
            raise ValueError(f"Networked VM '{vm_id}' not found")
        
        def start_client():
            return vm.start_client(host, port, message, timeout=timeout)
        
        future = self.executor.submit(start_client)
        self.futures[vm_id] = future
        return future
    
    def start_p2p_vm(self, vm_id: str, local_port: int,
                     peer_host: Optional[str] = None, peer_port: Optional[int] = None,
                     run_duration: int = 30, timeout: Optional[float] = None) -> Future:
        """
        Start a VM in P2P mode asynchronously.
        
        Args:
            vm_id: ID of VM to use for P2P
            local_port: Port to listen on
            peer_host: Optional peer host to connect to
            peer_port: Optional peer port to connect to  
            run_duration: How long to run P2P mode
            timeout: Maximum execution time
            
        Returns:
            Future object representing the P2P execution
        """
        vm = self.get_vm(vm_id)
        if not vm or not isinstance(vm, NetworkedLuaVM):
            raise ValueError(f"Networked VM '{vm_id}' not found")
        
        def start_p2p():
            return vm.start_p2p(local_port, peer_host, peer_port, run_duration, timeout=timeout)
        
        future = self.executor.submit(start_p2p)
        self.futures[vm_id] = future
        return future
    
    def wait_for_vm(self, vm_id: str, timeout: Optional[float] = None) -> Dict[str, Any]:
        """
        Wait for an asynchronous VM operation to complete.
        
        Args:
            vm_id: ID of VM to wait for
            timeout: Maximum time to wait
            
        Returns:
            Result of the VM execution
        """
        future = self.futures.get(vm_id)
        if not future:
            raise ValueError(f"No running operation found for VM '{vm_id}'")
        
        return future.result(timeout=timeout)
    
    def cancel_vm(self, vm_id: str) -> bool:
        """
        Cancel a running VM operation.
        
        Args:
            vm_id: ID of VM to cancel
            
        Returns:
            True if operation was cancelled, False otherwise
        """
        future = self.futures.get(vm_id)
        if future and not future.done():
            return future.cancel()
        return False
    
    def get_vm_status(self, vm_id: str) -> Optional[str]:
        """
        Get the status of a VM's current operation.
        
        Args:
            vm_id: ID of VM to check
            
        Returns:
            Status string: 'running', 'done', 'cancelled', or None if no operation
        """
        future = self.futures.get(vm_id)
        if not future:
            return None
        
        if future.cancelled():
            return 'cancelled'
        elif future.done():
            return 'done'
        else:
            return 'running'
    
    def create_vm_cluster(self, cluster_id: str, vm_count: int, 
                         networked: bool = True) -> List[str]:
        """
        Create a cluster of VMs with consistent naming.
        
        Args:
            cluster_id: Base name for the cluster
            vm_count: Number of VMs to create
            networke