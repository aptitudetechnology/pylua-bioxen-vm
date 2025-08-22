# pylua_bioxen_vm_lib Debug Mode Implementation Plan

## Overview
Based on the audit, debug output is hardcoded throughout the library. This implementation plan will make debug mode optional and clean up terminal output.

## Phase 1: Core Infrastructure Changes

### 1.1 Add Logging Infrastructure
Create a new file: `pylua_vm/logger.py`

```python
import logging
import os
from typing import Optional

class VMLogger:
    def __init__(self, name: str, debug_mode: Optional[bool] = None):
        self.logger = logging.getLogger(name)
        
        # Check debug mode from environment or parameter
        if debug_mode is None:
            debug_mode = os.environ.get('PYLUA_DEBUG', 'false').lower() == 'true'
        
        level = logging.DEBUG if debug_mode else logging.INFO
        self.logger.setLevel(level)
        
        # Create formatter
        formatter = logging.Formatter(
            '[%(levelname)s][%(name)s] %(message)s'
        )
        
        # Console handler (only if debug mode)
        if debug_mode:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        self.debug_mode = debug_mode
    
    def debug(self, message: str):
        self.logger.debug(message)
    
    def info(self, message: str):
        self.logger.info(message)
    
    def warning(self, message: str):
        self.logger.warning(message)
    
    def error(self, message: str):
        self.logger.error(message)
```

### 1.2 Update InteractiveSession Class
Modify `pylua_vm/interactive_session.py`:

```python
# Add at top of file
from .logger import VMLogger

class InteractiveSession:
    def __init__(self, vm, debug_mode: bool = False):
        self.vm = vm
        self.debug_mode = debug_mode
        self.logger = VMLogger(f"InteractiveSession-{vm.vm_id}", debug_mode)
        # ... rest of existing __init__
    
    def _read_output(self):
        """Read output from PTY with optional debug logging"""
        try:
            # ... existing PTY reading code ...
            output = self.pty_master.read(4096).decode('utf-8', errors='ignore')
            
            # Replace: print(f"[DEBUG][_read_output] PTY output: {repr(output)}")
            self.logger.debug(f"PTY output: {repr(output)}")
            
            return output
        except Exception as e:
            # Replace: print(f"[DEBUG][PTY] Error during read: {e}")
            self.logger.error(f"PTY read error: {e}")
            return ""
    
    def read_output(self):
        """Read and drain PTY output with optional debug logging"""
        all_output = ""
        # ... existing logic ...
        
        # Replace: print(f"[DEBUG][read_output] Drained output: {repr(all_output)}")
        self.logger.debug(f"Drained output: {repr(all_output)}")
        
        return all_output
    
    def send_command(self, command: str):
        """Send command with optional debug logging"""
        # ... existing command sending logic ...
        
        # Replace: print(f"[DEBUG][PTY] Output after send_command: {output}")
        self.logger.debug(f"Output after send_command: {output}")
        
        return output
```

### 1.3 Update VMManager Class
Modify `pylua_vm/vm_manager.py`:

```python
from .logger import VMLogger

class VMManager:
    def __init__(self, debug_mode: bool = False):
        self.debug_mode = debug_mode
        self.logger = VMLogger("VMManager", debug_mode)
        # ... rest of existing __init__
    
    def create_interactive_session(self, vm_id: str):
        """Create interactive session with debug mode inheritance"""
        vm = self.get_vm(vm_id)
        return InteractiveSession(vm, debug_mode=self.debug_mode)
```

### 1.4 Update LuaProcess Class
Modify `pylua_vm/lua_process.py`:

```python
from .logger import VMLogger

class LuaProcess:
    def __init__(self, vm_id: str, debug_mode: bool = False):
        self.vm_id = vm_id
        self.debug_mode = debug_mode
        self.logger = VMLogger(f"LuaProcess-{vm_id}", debug_mode)
        # ... rest of existing __init__
```

## Phase 2: Configuration Options

### 2.1 Environment Variable Support
Users can enable debug mode via:
```bash
export PYLUA_DEBUG=true
python your_bioxen_script.py
```

### 2.2 Programmatic Control
```python
# Enable debug for specific components
manager = VMManager(debug_mode=True)
session = manager.create_interactive_session("vm1")

# Or disable globally
manager = VMManager(debug_mode=False)
```

### 2.3 Configuration File Support (Optional)
Create `pylua_vm/config.py`:

```python
import os
import json
from pathlib import Path

class Config:
    def __init__(self):
        self.debug_mode = self._get_debug_mode()
    
    def _get_debug_mode(self) -> bool:
        # Check environment variable first
        env_debug = os.environ.get('PYLUA_DEBUG', '').lower()
        if env_debug in ['true', '1', 'yes']:
            return True
        
        # Check config file
        config_path = Path.home() / '.pylua_config.json'
        if config_path.exists():
            try:
                with open(config_path) as f:
                    config = json.load(f)
                    return config.get('debug_mode', False)
            except:
                pass
        
        return False  # Default: no debug
```

## Phase 3: BioXen Integration

### 3.1 Command Line Arguments
In the BioXen-luavm main script, add:

```python
import argparse

parser = argparse.ArgumentParser(description='BioXen Lua VM Manager')
parser.add_argument('--debug', action='store_true', 
                   help='Enable debug output from pylua_bioxen_vm_lib')
parser.add_argument('--quiet', action='store_true',
                   help='Suppress all non-essential output')

args = parser.parse_args()

# Pass debug mode to VMManager
vm_manager = VMManager(debug_mode=args.debug)
```

### 3.2 Interactive Menu Option
Add debug toggle to the BioXen menu:

```
======================================================================
🌙 BioXen Lua VM Manager - Enhanced Hypervisor Interface
======================================================================
📊 Status: 3 VMs running, 0 attached
----------------------------------------------------------------------
1. 🖥️  List Persistent VMs
2. 🔗 Attach to VM Terminal  
3. 📊 VM Detailed Status
4. 🐛 Toggle Debug Mode [Currently: OFF]
5. ⚙️  Settings
```

## Phase 4: Testing and Validation

### 4.1 Test Cases
1. **Default behavior**: No debug output visible
2. **Environment variable**: `PYLUA_DEBUG=true` shows debug
3. **Command line flag**: `--debug` shows debug
4. **Programmatic control**: Debug mode parameter works
5. **Clean terminal**: No escape sequences in normal mode

### 4.2 Backwards Compatibility
- Existing code without debug parameters should work unchanged
- Default behavior should be clean (no debug output)
- All existing functionality should remain intact

## Phase 5: Documentation Updates

### 5.1 README Updates
Add section on debug mode:

```markdown
## Debug Mode

Enable debug output to troubleshoot VM communication issues:

### Environment Variable
```bash
export PYLUA_DEBUG=true
python your_script.py
```

### Command Line (BioXen)
```bash
python bioxen_manager.py --debug
```

### Programmatic
```python
manager = VMManager(debug_mode=True)
```
```

## Implementation Priority

1. **High Priority**: InteractiveSession debug cleanup (fixes immediate terminal issues)
2. **Medium Priority**: VMManager and LuaProcess updates
3. **Low Priority**: Configuration file support, advanced logging features

## Rollback Plan

If issues arise, the changes can be easily reverted by:
1. Keeping original print statements commented out initially
2. Using feature flags to switch between old/new behavior
3. Maintaining separate branches during development

This implementation will make the BioXen terminal experience much cleaner while preserving debug capabilities when needed.