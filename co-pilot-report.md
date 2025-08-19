# pylua-bioxen-vm Library Analysis & Extension Recommendations

## 1. Subprocess Management Implementation
- **Class:** `LuaProcess`
- **How Lua VMs are spawned:** Each Lua VM is managed as a separate subprocess using Python’s `subprocess.run`. The VM is started by running the Lua interpreter (`lua_executable`) with either a code string (`-e`) or a script file. Temporary Lua scripts are created for multi-line code and executed as files.
- **Lifecycle:** The process is not persistent; each code execution spawns a new subprocess. No long-running Lua process is maintained for interactive sessions (currently).

## 2. Socket Communication Architecture
- **Class:** `NetworkedLuaVM`
- **How communication works:** Uses LuaSocket (Lua-side) for TCP socket communication. Python orchestrates by generating Lua scripts that act as servers, clients, or P2P nodes. Communication is between Lua processes (not Python ↔ Lua directly via sockets). Python triggers Lua scripts that open sockets, accept connections, send/receive messages, etc.
- **Python ↔ Lua communication:** Only via subprocess stdout/stderr, not via sockets or pipes.

## 3. Process Lifecycle Management
- **Manager:** `VMManager`
- **Methods for lifecycle:**
  - `create_vm(vm_id, networked=False)`: Spawns a new Lua VM (subprocess).
  - `remove_vm(vm_id)`: Cleans up resources, cancels futures, deletes temp files.
  - `shutdown_all()`: Shuts down all VMs and cleans up.
  - `cleanup()`: Cleans up temp files for a VM.
  - `wait_for_vm(vm_id)`, `cancel_vm(vm_id)`, `get_vm_status(vm_id)`: Monitor and control execution.
- **Async execution:** Uses `ThreadPoolExecutor` for concurrent execution of Lua code (not persistent Lua processes).

## 4. Inter-process Communication Mechanisms
- **Mechanisms used:**
  - **Subprocess stdout/stderr:** For Python ↔ Lua communication.
  - **TCP sockets (LuaSocket):** For Lua ↔ Lua communication (server/client/P2P).
  - **No pipes or shared memory** between Python and Lua processes.
- **No interactive stdin:** Lua subprocesses are not started with stdin pipes for interactive input.

## 5. Terminal or Console Interaction Capabilities
- **Current capabilities:** No support for interactive terminal sessions (like attaching to a running process). All Lua code is executed non-interactively; input must be provided up front. Output is captured after execution completes.
- **No PTY or console emulation** for Lua VMs.

## 6. Error Handling and Process Monitoring Patterns
- **Error handling:** Custom exceptions (`LuaProcessError`, `LuaNotFoundError`, `NetworkingError`, etc.). Errors in subprocess execution are caught and wrapped in custom exceptions. Networking errors (LuaSocket not found, connection errors) are handled in Python and Lua.
- **Monitoring:** Status via `get_vm_status(vm_id)` (running, done, cancelled). Futures are tracked for async operations.

## 7. API Surface for VM Control
- **Public methods (main ones):**
  - `create_vm`, `remove_vm`, `list_vms`, `get_vm`, `execute_vm_sync`, `execute_vm_async`
  - `start_server_vm`, `start_client_vm`, `start_p2p_vm`
  - `wait_for_vm`, `cancel_vm`, `get_vm_status`
  - Cluster management: `create_vm_cluster`, `setup_p2p_cluster`, `broadcast_to_cluster`, `cleanup_cluster`
  - `shutdown_all`, `get_stats`
- **Direct VM methods:** `execute_string`, `execute_file`, `execute_temp_script`, `cleanup`

---

## How to Extend for Interactive Terminal Sessions

To support interactive terminal sessions (like attaching to a Docker container or VM console):

### Key Classes/Methods to Modify or Extend
- **`LuaProcess`**
  - Change subprocess spawning to use `subprocess.Popen` with `stdin`, `stdout`, and `stderr` pipes.
  - Optionally, use a PTY (pseudo-terminal) for true console emulation (`pty` module).
  - Add methods for sending input to the running Lua process and reading output in real time.
  - Maintain a persistent Lua process for each VM, rather than spawning a new process per command.
- **`VMManager`**
  - Track persistent Lua processes, not just futures for one-off executions.
  - Add methods to "attach" to a running VM, send input, and receive output interactively.
- **API Additions**
  - `attach_to_vm(vm_id)`: Returns a handle for interactive session.
  - `send_input(vm_id, input_str)`: Sends input to the Lua process.
  - `read_output(vm_id)`: Reads output from the Lua process.
  - `detach_vm(vm_id)`: Ends interactive session.
- **Considerations**
  - Use threads or async IO to handle real-time input/output.
  - For true terminal emulation, use PTY so Lua process behaves like a console.

---

## Summary Table

| Area                        | Current Implementation                | Needed for Interactive Terminal |
|-----------------------------|---------------------------------------|---------------------------------|
| Subprocess Management       | `subprocess.run` (one-shot)           | `subprocess.Popen` (persistent) |
| Socket Communication        | Lua ↔ Lua via LuaSocket               | (Unchanged, unless Python ↔ Lua sockets needed) |
| Lifecycle Management        | VMManager tracks one-shot executions  | Track persistent processes      |
| IPC Mechanisms              | stdout/stderr, TCP sockets (Lua)      | Add stdin/PTY for interactive   |
| Terminal/Console Interaction| None                                  | Add PTY, interactive stdin/out  |
| Error Handling/Monitoring   | Custom exceptions, status via futures | Extend to handle interactive errors, process exit |
| API Surface                 | VM creation, execution, cluster mgmt  | Add attach/send/read/detach     |

---

## Next Steps for Extension
1. Refactor `LuaProcess` to optionally start Lua interpreter in interactive mode using `subprocess.Popen` with pipes or PTY.
2. Add methods for interactive input/output.
3. Update `VMManager` to manage persistent processes and interactive sessions.
4. Expose new API methods for terminal-like access.

---

Let me know if you want a code prototype for interactive session support or a more detailed design for any part!
