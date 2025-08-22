We are continuing a debug mode refactor for a PyLua VM project. The goal is to replace scattered debug print statements with a centralized VMLogger class and add debug_mode control throughout the system.

COMPLETED SO FAR:
✅ interactive_session.py - Refactored to use VMLogger with debug_mode parameter
✅ vm_manager.py - Refactored to use VMLogger and pass debug_mode down the chain

IMPLEMENTATION PATTERN:
1. Add debug_mode parameter to class constructors
2. Initialize VMLogger(debug_mode=debug_mode, component="ClassName") 
3. Replace print(f"[DEBUG]...") statements with self.logger.debug(...)
4. Add strategic debug logging for key operations
5. Import VMLogger from .logger

The VMLogger class expects this interface:
- VMLogger(debug_mode: bool, component: str)
- logger.debug(message: str) - only outputs when debug_mode=True

Please continue the refactor with the remaining files. I'll provide each file that needs refactoring and say "please" when ready for code changes.