"""
InteractiveSession: Persistent interactive Lua VM session with PTY and threading support.
"""
import os
import pty
import threading
import queue
import subprocess
import select
import time
import signal
from typing import Dict, List, Optional, Any, Callable
from .exceptions import InteractiveSessionError, SessionNotFoundError, SessionAlreadyExistsError


class InteractiveSession:
    """
    Manages a persistent interactive Lua interpreter process using PTY.
    Provides bidirectional I/O and real-time output streaming with attach/detach capabilities.
    """
    
    def __init__(self, session_id: str, vm_instance, lua_executable: str = "lua"):
        """
        Initialize an interactive session.
        
        Args:
            session_id: Unique identifier for this session
            vm_instance: The LuaProcess VM instance this session manages
            lua_executable: Path to Lua interpreter
        """
        self.session_id = session_id
        self.vm_instance = vm_instance
        self.lua_executable = lua_executable
        self.name = f"InteractiveSession_{session_id}"
        
        # Process and PTY management
        self.process = None
        self.master_fd = None
        self.slave_fd = None
        
        # Threading and I/O
        self.output_queue = queue.Queue()
        self._output_thread = None
        self._running = False
        self._attached = False
        
        # Session state
        self._lock = threading.RLock()
        self._output_callback = None
        self._last_activity = time.time()
        
        # Output buffer for execute_and_wait
        self._command_output_buffer = []
        self._waiting_for_command = False

    def start(self):
        """Start the interactive Lua process with PTY."""
        if self._running:
            raise InteractiveSessionError("Session already running")
            
        try:
            # Create PTY pair
            self.master_fd, self.slave_fd = pty.openpty()
            
            # Start Lua process with PTY
            self.process = subprocess.Popen(
                [self.lua_executable, "-i"],  # Interactive mode
                stdin=self.slave_fd,
                stdout=self.slave_fd,
                stderr=self.slave_fd,
                bufsize=0,
                close_fds=True,
                preexec_fn=os.setsid  # Create new process group
            )
            
            self._running = True
            self._last_activity = time.time()
            
            # Start output reading thread
            self._output_thread = threading.Thread(target=self._read_output, daemon=True)
            self._output_thread.start()
            
            # Give Lua a moment to start and show prompt
            time.sleep(0.1)
            
        except Exception as e:
            self._cleanup_resources()
            raise InteractiveSessionError(f"Failed to start session: {e}")

    def _read_output(self):
        """Background thread to read output from Lua process."""
        while self._running:
            try:
                # Use select to check if data is available
                rlist, _, _ = select.select([self.master_fd], [], [], 0.1)
                
                if self.master_fd in rlist:
                    data = os.read(self.master_fd, 1024)
                    if data:
                        output = data.decode(errors="replace")
                        self._last_activity = time.time()
                        
                        # Add to output queue
                        self.output_queue.put(output)
                        
                        # Add to command buffer if waiting for command
                        if self._waiting_for_command:
                            self._command_output_buffer.append(output)
                        
                        # Call output callback if attached
                        if self._attached and self._output_callback:
                            try:
                                self._output_callback(output)
                            except Exception:
                                pass  # Don't let callback errors break the session
                    else:
                        # EOF - process terminated
                        break
                        
            except OSError:
                # PTY closed or other I/O error
                break
            except Exception:
                # Unexpected error, but continue trying
                time.sleep(0.01)
                continue
                
            time.sleep(0.01)  # Small delay to prevent busy waiting

    def attach(self, output_callback: Optional[Callable[[str], None]] = None):
        """
        Attach to this session for interactive use.
        
        Args:
            output_callback: Optional callback function for real-time output
        """
        with self._lock:
            if not self._running:
                self.start()
            
            self._attached = True
            self._output_callback = output_callback
            self._last_activity = time.time()

    def detach(self):
        """Detach from this session (keeps process running)."""
        with self._lock:
            self._attached = False
            self._output_callback = None

    def is_attached(self) -> bool:
        """Check if session is currently attached."""
        return self._attached

    def send_input(self, input_str: str):
        """Send raw input to the Lua process."""
        if not self._running:
            raise InteractiveSessionError("Session not running")
            
        try:
            # Ensure input ends with newline for Lua interpreter
            if not input_str.endswith('\n'):
                input_str += '\n'
            os.write(self.master_fd, input_str.encode())
            self._last_activity = time.time()
        except OSError as e:
            raise InteractiveSessionError(f"Failed to send input: {e}")

    def send_command(self, command: str):
        """Send a command to the Lua process (alias for send_input for VMManager compatibility)."""
        self.send_input(command)

    def read_output(self, timeout: float = 0.1) -> str:
        """
        Read available output from the session.
        
        Args:
            timeout: Maximum time to wait for output
            
        Returns:
            Output string or empty string if no output available
        """
        try:
            return self.output_queue.get(timeout=timeout)
        except queue.Empty:
            return ""

    def get_all_output(self, max_items: int = 100) -> str:
        """Get all currently available output."""
        output_parts = []
        count = 0
        
        while count < max_items:
            try:
                output = self.output_queue.get_nowait()
                output_parts.append(output)
                count += 1
            except queue.Empty:
                break
                
        return ''.join(output_parts)

    def execute_and_wait(self, command: str, timeout: float = 5.0) -> str:
        """
        Execute a command and wait for output to stabilize.
        
        Args:
            command: Lua command to execute
            timeout: Maximum time to wait for output
            
        Returns:
            Collected output from the command
        """
        if not self._running:
            raise InteractiveSessionError("Session not running")
            
        with self._lock:
            # Clear any existing output
            self.get_all_output()
            self._command_output_buffer.clear()
            self._waiting_for_command = True
            
            try:
                # Send command
                self.send_command(command)
                
                # Wait for output to stabilize
                start_time = time.time()
                last_output_time = start_time
                stable_duration = 0.2  # Wait for 200ms of no new output
                
                while time.time() - start_time < timeout:
                    # Check for new output
                    try:
                        output = self.output_queue.get(timeout=0.1)
                        if output:
                            self._command_output_buffer.append(output)
                            last_output_time = time.time()
                    except queue.Empty:
                        pass
                    
                    # Check if output has stabilized
                    if time.time() - last_output_time >= stable_duration:
                        break
                        
                    time.sleep(0.05)
                
                # Return collected output
                return ''.join(self._command_output_buffer)
                
            finally:
                self._waiting_for_command = False
                self._command_output_buffer.clear()

    def is_running(self) -> bool:
        """Check if the session process is running."""
        return (self._running and 
                self.process and 
                self.process.poll() is None)

    def get_session_info(self) -> Dict[str, Any]:
        """Get information about this session."""
        return {
            'session_id': self.session_id,
            'vm_name': self.vm_instance.name if self.vm_instance else 'unknown',
            'attached': self._attached,
            'running': self.is_running(),
            'last_activity': self._last_activity,
            'process_pid': self.process.pid if self.process else None,
            'lua_executable': self.lua_executable
        }

    def terminate(self):
        """Terminate the session and clean up all resources."""
        with self._lock:
            self._running = False
            self._attached = False
            
            if self.process:
                try:
                    # Try graceful shutdown first
                    self.process.terminate()
                    self.process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    # Force kill if necessary
                    try:
                        os.killpg(os.getpgid(self.process.pid), signal.SIGKILL)
                    except:
                        pass
                except:
                    pass
            
            self._cleanup_resources()

    def stop(self):
        """Stop the session (alias for terminate for backward compatibility)."""
        self.terminate()

    def _cleanup_resources(self):
        """Clean up PTY and process resources."""
        try:
            if self.master_fd:
                os.close(self.master_fd)
        except:
            pass
        
        try:
            if self.slave_fd:
                os.close(self.slave_fd)
        except:
            pass
        
        self.process = None
        self.master_fd = None
        self.slave_fd = None

    def __enter__(self):
        """Context manager entry."""
        if not self._running:
            self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        self.terminate()

    def __repr__(self):
        return (f"InteractiveSession(id='{self.session_id}', "
                f"attached={self._attached}, running={self.is_running()})")


class SessionManager:
    """
    Manages multiple interactive sessions with registry and lifecycle tracking.
    """
    
    def __init__(self):
        """Initialize the session manager."""
        self._sessions: Dict[str, InteractiveSession] = {}
        self._lock = threading.RLock()

    def create_session(self, session_id: str, vm_instance, 
                      lua_executable: str = "lua") -> InteractiveSession:
        """
        Create a new interactive session.
        
        Args:
            session_id: Unique identifier for the session
            vm_instance: The LuaProcess VM instance
            lua_executable: Path to Lua interpreter
            
        Returns:
            The created InteractiveSession
        """
        with self._lock:
            if session_id in self._sessions:
                raise SessionAlreadyExistsError(f"Session '{session_id}' already exists")
            
            session = InteractiveSession(session_id, vm_instance, lua_executable)
            self._sessions[session_id] = session
            return session

    def get_session(self, session_id: str) -> Optional[InteractiveSession]:
        """Get a session by ID."""
        return self._sessions.get(session_id)

    def remove_session(self, session_id: str) -> bool:
        """
        Remove and terminate a session.
        
        Args:
            session_id: ID of session to remove
            
        Returns:
            True if session was removed, False if not found
        """
        with self._lock:
            session = self._sessions.pop(session_id, None)
            if session:
                try:
                    session.terminate()
                except:
                    pass
                return True
            return False

    def list_sessions(self) -> Dict[str, Dict[str, Any]]:
        """
        List all sessions and their information.
        
        Returns:
            Dictionary mapping session IDs to session info
        """
        with self._lock:
            return {
                session_id: session.get_session_info()
                for session_id, session in self._sessions.items()
            }

    def cleanup_dead_sessions(self) -> List[str]:
        """
        Clean up sessions with dead processes.
        
        Returns:
            List of session IDs that were cleaned up
        """
        cleaned_up = []
        with self._lock:
            dead_sessions = []
            
            for session_id, session in self._sessions.items():
                if not session.is_running():
                    dead_sessions.append(session_id)
            
            for session_id in dead_sessions:
                if self.remove_session(session_id):
                    cleaned_up.append(session_id)
                    
        return cleaned_up

    def cleanup_all(self):
        """Terminate and remove all sessions."""
        with self._lock:
            session_ids = list(self._sessions.keys())
            for session_id in session_ids:
                self.remove_session(session_id)

    def get_attached_sessions(self) -> Dict[str, InteractiveSession]:
        """Get all currently attached sessions."""
        with self._lock:
            return {
                session_id: session 
                for session_id, session in self._sessions.items()
                if session.is_attached()
            }

    def detach_all_sessions(self):
        """Detach from all sessions (but keep them running)."""
        with self._lock:
            for session in self._sessions.values():
                if session.is_attached():
                    session.detach()

    def get_session_count(self) -> int:
        """Get total number of managed sessions."""
        return len(self._sessions)

    def find_sessions_by_pattern(self, pattern: str) -> Dict[str, InteractiveSession]:
        """
        Find sessions matching a pattern.
        
        Args:
            pattern: Pattern to match against session IDs (supports wildcards)
            
        Returns:
            Dictionary of matching sessions
        """
        import fnmatch
        with self._lock:
            return {
                session_id: session
                for session_id, session in self._sessions.items()
                if fnmatch.fnmatch(session_id, pattern)
            }

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about managed sessions."""
        with self._lock:
            total = len(self._sessions)
            running = sum(1 for s in self._sessions.values() if s.is_running())
            attached = sum(1 for s in self._sessions.values() if s.is_attached())
            
            return {
                'total_sessions': total,
                'running_sessions': running,
                'attached_sessions': attached,
                'idle_sessions': total - attached,
                'dead_sessions': total - running
            }

    def __len__(self):
        """Return number of managed sessions."""
        return len(self._sessions)

    def __contains__(self, session_id: str):
        """Check if session ID exists."""
        return session_id in self._sessions

    def __iter__(self):
        """Iterate over session IDs."""
        return iter(self._sessions.keys())

    def __repr__(self):
        stats = self.get_stats()
        return (f"SessionManager(sessions={stats['total_sessions']}, "
                f"running={stats['running_sessions']}, "
                f"attached={stats['attached_sessions']})")


# Additional utility functions for session management
def create_session_with_auto_start(session_id: str, vm_instance, 
                                 lua_executable: str = "lua",
                                 auto_attach: bool = True,
                                 output_callback: Optional[Callable[[str], None]] = None) -> InteractiveSession:
    """
    Convenience function to create and start a session in one call.
    
    Args:
        session_id: Unique identifier for the session
        vm_instance: The LuaProcess VM instance
        lua_executable: Path to Lua interpreter
        auto_attach: Whether to automatically attach to the session
        output_callback: Optional callback for real-time output
        
    Returns:
        The created and started InteractiveSession
    """
    session = InteractiveSession(session_id, vm_instance, lua_executable)
    session.start()
    
    if auto_attach:
        session.attach(output_callback)
    
    return session


def batch_execute_on_sessions(sessions: Dict[str, InteractiveSession], 
                            command: str, 
                            timeout: float = 5.0) -> Dict[str, str]:
    """
    Execute a command on multiple sessions in parallel.
    
    Args:
        sessions: Dictionary of session_id -> InteractiveSession
        command: Lua command to execute
        timeout: Timeout for each session
        
    Returns:
        Dictionary mapping session_id to output
    """
    import concurrent.futures
    
    def execute_on_session(session_item):
        session_id, session = session_item
        try:
            return session_id, session.execute_and_wait(command, timeout=timeout)
        except Exception as e:
            return session_id, f"Error: {e}"
    
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(sessions)) as executor:
        future_to_session = {
            executor.submit(execute_on_session, item): item[0] 
            for item in sessions.items()
        }
        
        for future in concurrent.futures.as_completed(future_to_session):
            session_id, output = future.result()
            results[session_id] = output
    
    return results


# Export classes and functions
__all__ = [
    'InteractiveSession',
    'SessionManager', 
    'create_session_with_auto_start',
    'batch_execute_on_sessions'
]