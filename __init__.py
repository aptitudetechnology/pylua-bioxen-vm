"""
pylua_vm.utils - Intelligent utilities for Lua VM management

This package contains sophisticated utilities for managing Lua environments,
with a focus on intelligent curation and bootstrapping capabilities for AGI development.
"""

from .curator import (
    Curator,
    Package,
    get_curator,
    quick_install,
    bootstrap_lua_environment
)

# Public API
__all__ = [
    'Curator',
    'Package', 
    'get_curator',
    'quick_install',
    'bootstrap_lua_environment'
]

# Version info
__version__ = '1.0.0'
__author__ = 'AGI Bootstrap Project'

# Convenience aliases for common operations
def create_curator(lua_path=None, manifest_path=None):
    """Create a new curator instance - alias for get_curator"""
    return get_curator(lua_path, manifest_path)

def install_packages(*packages, profile=None):
    """Install packages or apply profile - alias for quick_install"""
    return quick_install(list(packages), profile)

def setup_environment(profile='standard'):
    """Setup complete Lua environment - alias for bootstrap_lua_environment"""
    return bootstrap_lua_environment(profile)

# Add convenience functions to __all__
__all__.extend(['create_curator', 'install_packages', 'setup_environment'])