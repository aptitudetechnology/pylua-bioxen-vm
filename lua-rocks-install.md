def install_luarocks_package(package_name):

# LuaRocks Package Installation Plan (Refactored)

## Objective
Enable users to install LuaRocks packages (with optional sudo privileges) into the VM environment, supporting both recommended and custom packages.

---

## Refined Implementation Steps

### 1. Abstract Installation Logic
- Create a shared utility: `pylua_vm/utils/luarocks.py` with an `install_luarocks_package` function.
- VM classes (`LuaProcess`, `NetworkedLuaVM`) delegate to this utility for package installation.

### 2. Pre-checks before Installation
- Verify `luarocks` is installed (`shutil.which("luarocks")`).
- Optionally check if the package is already installed (`luarocks list <pkg>`).

### 3. Logging
- Use the project’s logging system for installation output and errors.
- Optionally store logs in a `logs/` folder or integrate with VMLogger.

### 4. Interactive & Non-interactive Modes
- Interactive: Prompt user to pick recommended packages or enter custom.
- Non-interactive: Allow direct function calls for automated installs.

### 5. Safer Sudo Handling
- Try installing without sudo first.
- Fall back to sudo if permission denied.

### 6. Documentation Additions
- Add README section: "Installing LuaRocks Packages into VM" with CLI and class usage examples.
- Document how to run without sudo (e.g., in containers).

---

## Example Utility Implementation
```python
# pylua_vm/utils/luarocks.py
import subprocess
import shutil
import logging

logger = logging.getLogger(__name__)

def install_luarocks_package(package_name, use_sudo=True):
   if not shutil.which("luarocks"):
      raise RuntimeError("luarocks not found in PATH")
   cmd = ["luarocks", "install", package_name]
   if use_sudo:
      cmd.insert(0, "sudo")
   try:
      result = subprocess.run(cmd, check=True, capture_output=True, text=True)
      logger.info("Installed %s successfully:\n%s", package_name, result.stdout)
      return True
   except subprocess.CalledProcessError as e:
      logger.error("Failed to install %s:\n%s", package_name, e.stderr)
      return False
```

---

## VM Class Integration
```python
from .utils.luarocks import install_luarocks_package
class LuaProcess:
   ...
   def install_package(self, package_name):
      return install_luarocks_package(package_name)
```

---

## Files to Update
- `pylua_vm/utils/luarocks.py` (new utility)
- `pylua_vm/lua_process.py` (add install_package method)
- `pylua_vm/networking.py` (add install_package method)
- CLI/UI scripts for package selection and install triggers
- `README.md` (document LuaRocks installation workflow)

---

## Recommended Packages
- `gabby-lua`
- `luasocket`
- `luafilesystem`
- `inspect`
- `penlight`
- `luajson`

---

This refactored plan enables robust, user-friendly LuaRocks package installation for your VM environment, with shared logic, logging, and both interactive and automated support.
