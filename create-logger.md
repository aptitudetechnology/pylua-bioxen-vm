The error shows that the `VMLogger` class doesn't exist yet! We've been refactoring files to use `VMLogger`, but we haven't actually created the `logger.py` file that contains the `VMLogger` class.

We need to create the `pylua_vm/logger.py` file with the `VMLogger` implementation. Based on the usage pattern we've been following, it should have:

- `VMLogger(debug_mode: bool, component: str)` constructor
- `logger.debug(message: str)` method that only outputs when `debug_mode=True`

Would you like me to create the missing `logger.py` file with the `VMLogger` class implementation?

The VMLogger should probably:
1. Store the `debug_mode` and `component` settings
2. Only print debug messages when `debug_mode=True`
3. Format messages consistently (maybe with timestamps and component names)
4. Provide a clean interface for the debug logging we've been implementing

