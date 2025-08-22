# GitHub Copilot Instructions: pylua_bioxen_vm_lib Debug Output Analysis

## Objective
Analyze the pylua_bioxen_vm_lib source code to identify where debug output is generated and provide recommendations for making debug mode optional.

## Primary Tasks

### 1. Locate Debug Output Sources
Please search the codebase for:
- All instances of `[DEBUG]` strings in print statements or logging
- Functions containing `_read_output` and `read_output`
- PTY (pseudo-terminal) handling code
- Any hardcoded debug print statements

**Search patterns to use:**
```
"[DEBUG]"
"_read_output"
"read_output" 
"PTY output"
"Drained output"
print.*debug
logging.*debug
```

### 2. Identify Key Files and Classes
Focus on files that likely contain:
- VM management classes (`VMManager`, `InteractiveSession`, etc.)
- Subprocess/PTY handling code
- Terminal communication logic
- Session management

### 3. Analyze Debug Output Pattern
The debug output appears in this format:
```
[DEBUG][_read_output] PTY output: "..."
[DEBUG][read_output] Drained output: "..."
```

Please identify:
- Which functions generate these specific messages
- How the PTY output reading is implemented
- Whether debug output is controlled by any existing flags/variables

### 4. Interactive Session Analysis
Look specifically at the `InteractiveSession` class and related code:
- How does `attach()` work?
- Where does terminal input/output processing happen?
- How are escape sequences handled?

## Report Structure

Please provide a report with these sections:

### A. Debug Output Locations
List all files and functions that contain debug output, with:
- File path and line numbers
- Function names
- Exact debug statements found
- Context of when these are triggered

### B. PTY/Terminal Handling
- Which classes/functions handle PTY communication
- How terminal input/output is processed  
- Where escape sequences might be causing display issues
- Current terminal state management

### C. Configuration/Control Points
- Any existing debug flags or configuration options
- How debug mode could be controlled (class constructor parameters, environment variables, etc.)
- Current logging setup (if any)

### D. Recommendations
Suggest specific code changes to:
1. Make debug output optional
2. Clean up terminal display issues
3. Separate debug logging from user output
4. Add configuration options for debug modes

### E. Implementation Plan
Provide a step-by-step plan for:
1. Adding debug mode controls
2. Refactoring debug output
3. Maintaining backward compatibility
4. Testing the changes

## Code Analysis Focus Areas

### Primary Files to Examine:
- Main VM management modules
- Interactive session handling
- Subprocess/PTY communication
- Any terminal or console utilities

### Key Questions to Answer:
1. Is debug output hardcoded or configurable?
2. Can debug mode be disabled without breaking functionality?
3. Where are the escape sequences coming from?
4. How is terminal state managed during attach/detach?
5. Are there any existing logging frameworks being used?

## Output Format
Please format your analysis as a comprehensive technical report with:
- Clear section headers
- Code snippets with file paths and line numbers
- Specific function signatures
- Concrete implementation suggestions
- Priority levels for different fixes

## Additional Context
This analysis is for improving user experience in the BioXen Lua VM Manager, which uses pylua_bioxen_vm_lib for managing interactive Lua VM sessions. The current debug output makes the terminal very difficult to use during interactive sessions.