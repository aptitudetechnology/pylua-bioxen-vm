"""
PyLua VM Curator CLI
Provides interactive and command-line tools for environment setup, package management, and diagnostics.
"""
import argparse
from pylua_vm.env import EnvironmentManager
from pylua_vm.utils.curator import Curator


def main():
    parser = argparse.ArgumentParser(description="PyLua VM Curator CLI")
    parser.add_argument('--profile', type=str, default='standard', help='Environment profile (minimal, standard, full, development, production, networking)')
    parser.add_argument('--setup', action='store_true', help='Setup environment and install recommended packages')
    parser.add_argument('--install', type=str, help='Install a specific LuaRocks package')
    parser.add_argument('--recommend', action='store_true', help='Show package recommendations')
    parser.add_argument('--health', action='store_true', help='Run environment health check')
    parser.add_argument('--list', action='store_true', help='List installed packages')
    parser.add_argument('--manifest', action='store_true', help='Show current manifest')
    args = parser.parse_args()

    env = EnvironmentManager(profile=args.profile)
    curator = Curator()

    if args.setup:
        print(f"Setting up environment profile: {args.profile}")
        curator.curate_environment(args.profile)
        print("Environment setup complete.")

    if args.install:
        print(f"Installing package: {args.install}")
        curator.install_package(args.install)

    if args.recommend:
        recs = curator.get_recommendations()
        print("Recommended packages:")
        for pkg in recs:
            print(f"- {pkg}")

    if args.health:
        health = curator.health_check()
        print("Environment health:")
        for k, v in health.items():
            print(f"{k}: {v}")

    if args.list:
        pkgs = curator.get_installed_packages()
        print("Installed packages:")
        for pkg in pkgs:
            print(f"- {pkg}")

    if args.manifest:
        manifest = curator.get_manifest()
        print("Current manifest:")
        print(manifest)

if __name__ == "__main__":
    main()
