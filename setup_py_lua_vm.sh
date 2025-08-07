#!/bin/bash

# Create py-lua-vm project structure
echo "Setting up py-lua-vm project structure..."

# Create main project directory
mkdir -p py-lua-vm
cd py-lua-vm

# Create main package directory
mkdir -p pylua_vm

# Create subdirectories
mkdir -p examples
mkdir -p tests
mkdir -p docs

# Create package files
touch pylua_vm/__init__.py
touch pylua_vm/vm_manager.py
touch pylua_vm/networking.py
touch pylua_vm/lua_process.py
touch pylua_vm/exceptions.py

# Create example files
touch examples/basic_usage.py
touch examples/distributed_compute.py
touch examples/p2p_messaging.py

# Create test files
touch tests/__init__.py
touch tests/test_vm_manager.py
touch tests/test_networking.py
touch tests/test_lua_process.py

# Create documentation files
touch docs/api.md
touch docs/examples.md
touch docs/installation.md

# Create root level files
touch setup.py
touch requirements.txt
touch .gitignore
touch LICENSE
touch CHANGELOG.md

echo "✅ Project structure created successfully!"
echo ""
echo "Created directories:"
echo "  py-lua-vm/"
echo "  ├── pylua_vm/"
echo "  ├── examples/"
echo "  ├── tests/"
echo "  └── docs/"
echo ""
echo "Next steps:"
echo "1. Add README.md content"
echo "2. Initialize git repository: git init"
echo "3. Start coding in pylua_vm/"
echo ""
echo "Ready to build py-lua-vm! 🚀"
