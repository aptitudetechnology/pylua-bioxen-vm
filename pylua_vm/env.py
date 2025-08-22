"""
Environment management for PyLua VM Curator system.
Handles environment profiles, configuration validation, cross-platform paths, and development/production profiles.
"""
import os
import json
import platform
from pathlib import Path

class EnvironmentManager:
    def __init__(self, profile='standard', config_path=None):
        self.profile = profile
        self.config_path = config_path or self._default_config_path()
        self.config = self._load_config()
        self.system = platform.system()
        self.lua_version = self._detect_lua_version()

    def _default_config_path(self):
        return Path.home() / '.pylua_env.json'

    def _load_config(self):
        if Path(self.config_path).exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {}

    def _detect_lua_version(self):
        # Simple detection, can be extended
        try:
            import subprocess
            result = subprocess.run(['lua', '-v'], capture_output=True, text=True)
            return result.stdout.strip() or result.stderr.strip()
        except Exception:
            return None

    def validate(self):
        # Validate configuration and environment
        errors = []
        if not self.lua_version:
            errors.append('Lua interpreter not found.')
        # Add more validation as needed
        return errors

    def get_profile(self):
        return self.profile

    def set_profile(self, profile):
        self.profile = profile
        # Optionally reload config or apply changes

    def get_config(self):
        return self.config

    def save_config(self):
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)

    def get_system_info(self):
        return {
            'system': self.system,
            'lua_version': self.lua_version,
            'profile': self.profile,
            'config_path': str(self.config_path)
        }

    def is_development(self):
        return self.profile == 'development'

    def is_production(self):
        return self.profile == 'production'

    def get_cross_platform_path(self, path):
        return str(Path(path).resolve())

# Example usage:
# env = EnvironmentManager(profile='standard')
# print(env.get_system_info())
# errors = env.validate()
# if errors:
#     print('Environment errors:', errors)
