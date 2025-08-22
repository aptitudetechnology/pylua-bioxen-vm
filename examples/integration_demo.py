"""
Integration Demo for pylua_bioxen_vm_lib
Demonstrates the complete AGI bootstrapping workflow:
- Environment setup and validation
- Intelligent package curation
- VM creation with curator integration
- Networking capabilities with automatic package management
- Health monitoring and diagnostics
- Error handling and recovery scenarios

This demo embodies the curator philosophy of intelligent, discerning package management
for AGI development.
"""

import sys
import time
from pathlib import Path
from typing import Dict, List, Any

# Import our components
from pylua_vm.env import EnvironmentManager
from pylua_vm.utils.curator import Curator, get_curator, bootstrap_lua_environment
from pylua_vm.lua_process import LuaProcess
from pylua_vm.networking import NetworkedLuaVM


def print_section(title: str, char: str = "="):
    """Print a formatted section header"""
    print(f"\n{char * 60}")
    print(f" {title.center(58)} ")
    print(f"{char * 60}\n")


def print_status(message: str, status: str = "INFO"):
    """Print a status message with formatting"""
    markers = {
        "SUCCESS": "✓",
        "ERROR": "✗", 
        "WARNING": "⚠",
        "INFO": "ℹ"
    }
    marker = markers.get(status, "•")
    print(f"{marker} {message}")


def demo_environment_setup():
    """Demonstrate environment manager capabilities"""
    print_section("STEP 1: Environment Setup & Validation")
    
    # Test multiple profiles to show flexibility
    profiles_to_test = ['minimal', 'standard', 'networking']
    
    for profile in profiles_to_test:
        print(f"\n--- Testing {profile.title()} Profile ---")
        
        try:
            # Create environment manager
            env = EnvironmentManager(profile=profile, debug_mode=True)
            print_status(f"Created EnvironmentManager with profile: {profile}")
            
            # Show environment info
            print(f"  Lua executable: {env.lua_executable}")
            print(f"  Profile: {env.profile}")
            print(f"  Debug mode: {env.debug_mode}")
            print(f"  Config path: {env.config_file}")
            
            # Validate environment
            print_status("Validating environment...")
            errors = env.validate_environment()
            
            if errors:
                print_status(f"Validation found {len(errors)} issues:", "WARNING")
                for error in errors[:3]:  # Show first 3 errors
                    print(f"    - {error}")
                if len(errors) > 3:
                    print(f"    ... and {len(errors) - 3} more issues")
            else:
                print_status("Environment validation passed!", "SUCCESS")
            
            # Show system info
            if hasattr(env, 'get_system_info'):
                system_info = env.get_system_info()
                print(f"  System: {system_info.get('platform', 'Unknown')}")
                print(f"  Lua version: {system_info.get('lua_version', 'Unknown')}")
            
        except Exception as e:
            print_status(f"Failed to setup {profile} environment: {e}", "ERROR")
            continue
    
    # Return a working environment for subsequent demos
    try:
        return EnvironmentManager(profile='standard', debug_mode=True)
    except Exception as e:
        print_status(f"Could not create standard environment: {e}", "ERROR")
        return None


def demo_curator_intelligence():
    """Demonstrate curator's intelligent package management"""
    print_section("STEP 2: Intelligent Package Curation")
    
    try:
        # Create curator
        curator = get_curator()
        print_status("Created intelligent curator")
        
        # Show curator capabilities
        print("\n--- Curator Health Check ---")
        health = curator.health_check()
        for key, value in health.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        
        # Show available packages in catalog
        print(f"\n--- Package Catalog ({len(curator.catalog)} packages) ---")
        categories = {}
        for name, pkg in curator.catalog.items():
            if pkg.category not in categories:
                categories[pkg.category] = []
            categories[pkg.category].append(f"{name} (priority: {pkg.priority})")
        
        for category, packages in sorted(categories.items()):
            print(f"\n  {category.upper()}:")
            for pkg in sorted(packages):
                print(f"    - {pkg}")
        
        # Show current installed packages
        print("\n--- Currently Installed Packages ---")
        installed = curator.list_installed_packages()
        if installed:
            print_status(f"Found {len(installed)} installed packages:")
            for pkg in installed[:5]:  # Show first 5
                print(f"    - {pkg['name']} v{pkg['version']} ({pkg['category']})")
            if len(installed) > 5:
                print(f"    ... and {len(installed) - 5} more")
        else:
            print_status("No packages currently installed")
        
        # Get intelligent recommendations
        print("\n--- Intelligent Recommendations ---")
        recommendations = curator.get_recommendations()
        if recommendations:
            print_status(f"Curator recommends {len(recommendations)} packages:")
            for pkg in recommendations:
                print(f"    - {pkg.name}: {pkg.description} (priority: {pkg.priority})")
        else:
            print_status("No recommendations - environment looks complete!")
        
        # Demonstrate profile-based curation
        print("\n--- Profile-Based Environment Curation ---")
        profiles = curator.manifest.get('profiles', {})
        print_status(f"Available profiles: {list(profiles.keys())}")
        
        # Try to curate a minimal environment
        print_status("Attempting to curate 'minimal' profile...")
        if 'minimal' in profiles:
            success = curator.curate_environment('minimal')
            if success:
                print_status("Minimal environment curation completed!", "SUCCESS")
            else:
                print_status("Curation encountered some issues", "WARNING")
        
        return curator
        
    except Exception as e:
        print_status(f"Curator demo failed: {e}", "ERROR")
        return None


def demo_vm_integration(env_manager, curator):
    """Demonstrate VM creation with curator integration"""
    print_section("STEP 3: VM Creation with Curator Integration")
    
    if not env_manager:
        print_status("Skipping VM demo - no environment manager", "WARNING")
        return None
    
    try:
        # Create basic VM with curator integration
        print_status("Creating LuaProcess with curator integration...")
        vm = LuaProcess(
            name=f"AGI-{env_manager.profile.title()}",
            lua_executable=env_manager.lua_executable,
            debug_mode=env_manager.debug_mode
        )
        
        print_status(f"Created VM: {vm.name}")
        print(f"  Lua path: {vm.lua_executable}")
        print(f"  Debug mode: {vm.debug_mode}")
        
        # Test curator integration methods
        print("\n--- Curator Integration Methods ---")
        
        # Setup packages using curator
        print_status("Setting up packages using curator...")
        try:
            result = vm.setup_packages(env_manager.profile)
            print_status(f"Package setup result: {result.get('success', False)}", 
                        "SUCCESS" if result.get('success') else "WARNING")
            
            if 'packages_installed' in result:
                print(f"  Packages installed: {len(result['packages_installed'])}")
                for pkg in result['packages_installed'][:3]:
                    print(f"    - {pkg}")
        except Exception as e:
            print_status(f"Package setup failed: {e}", "ERROR")
        
        # Get package recommendations through VM
        print_status("Getting package recommendations through VM...")
        try:
            recommendations = vm.get_package_recommendations()
            print(f"  VM recommends {len(recommendations)} packages")
        except Exception as e:
            print_status(f"Failed to get recommendations: {e}", "ERROR")
        
        # Check environment health through VM
        print_status("Checking environment health through VM...")
        try:
            health = vm.check_environment_health()
            if health:
                print(f"  Health check completed - {len(health)} metrics")
                # Show key health indicators
                for key in ['luarocks_available', 'installed_packages', 'critical_packages_ratio']:
                    if key in health:
                        print(f"    {key}: {health[key]}")
        except Exception as e:
            print_status(f"Health check failed: {e}", "ERROR")
        
        # Test basic Lua execution
        print("\n--- Basic Lua Execution Test ---")
        try:
            print_status("Testing basic Lua execution...")
            
            # Simple test
            result = vm.execute_lua('return "Hello from AGI Lua VM!"')
            if result and result.get('success'):
                print_status(f"Execution successful: {result.get('result')}", "SUCCESS")
            else:
                print_status(f"Execution failed: {result.get('error', 'Unknown error')}", "ERROR")
            
            # Test with curator-installed packages (if lua-cjson is available)
            print_status("Testing curator-installed package usage...")
            json_test = '''
            local ok, json = pcall(require, "cjson")
            if ok then
                local data = {message = "Curator package working!", packages = {"lua-cjson", "penlight"}}
                return json.encode(data)
            else
                return "lua-cjson not available"
            end
            '''
            
            result = vm.execute_lua(json_test)
            if result and result.get('success'):
                print_status(f"Package test: {result.get('result')}", "SUCCESS")
            else:
                print_status(f"Package test result: {result.get('result', 'Package not available')}")
                
        except Exception as e:
            print_status(f"Lua execution test failed: {e}", "ERROR")
        
        return vm
        
    except Exception as e:
        print_status(f"VM integration demo failed: {e}", "ERROR")
        return None


def demo_networking_vm(env_manager):
    """Demonstrate networked VM with automatic package management"""
    print_section("STEP 4: Networked VM with Automatic Package Management")
    
    if not env_manager:
        print_status("Skipping networking demo - no environment manager", "WARNING")
        return None
    
    try:
        # Create networked VM
        print_status("Creating NetworkedLuaVM...")
        net_vm = NetworkedLuaVM(
            name="AGI-Network",
            lua_executable=env_manager.lua_executable,
            debug_mode=True
        )
        
        print_status(f"Created networked VM: {net_vm.name}")
        
        # Setup networking packages automatically
        print("\n--- Automatic Networking Package Setup ---")
        print_status("Setting up networking packages with curator...")
        
        try:
            result = net_vm.setup_networking_packages(include_advanced=True)
            
            print_status(f"Networking setup completed", 
                        "SUCCESS" if result.get('success', False) else "WARNING")
            
            if 'packages_installed' in result:
                print(f"  Networking packages: {len(result['packages_installed'])}")
                for pkg in result['packages_installed']:
                    print(f"    - {pkg}")
            
            print(f"  Networking ready: {result.get('networking_ready', False)}")
            
        except Exception as e:
            print_status(f"Networking setup failed: {e}", "ERROR")
        
        # Get networking-specific recommendations
        print("\n--- Networking Package Recommendations ---")
        try:
            net_recommendations = net_vm.get_networking_recommendations()
            
            if net_recommendations:
                print_status(f"Found {len(net_recommendations)} networking recommendations:")
                
                # Group by networking category
                by_category = {}
                for rec in net_recommendations:
                    cat = rec.get('networking_category', 'utility')
                    if cat not in by_category:
                        by_category[cat] = []
                    by_category[cat].append(rec)
                
                for category, recs in sorted(by_category.items()):
                    print(f"\n  {category.upper()}:")
                    for rec in recs:
                        print(f"    - {rec['package']}: {rec['description']}")
            else:
                print_status("No networking recommendations available")
                
        except Exception as e:
            print_status(f"Failed to get networking recommendations: {e}", "ERROR")
        
        # Comprehensive networking health check
        print("\n--- Networking Health Diagnostics ---")
        try:
            health = net_vm.check_networking_health()
            
            if health:
                print_status("Networking health check completed")
                
                # Show key networking metrics
                if 'networking' in health:
                    net_health = health['networking']
                    readiness = net_health.get('networking_readiness_percentage', 0)
                    print(f"  Networking readiness: {readiness}%")
                    
                    if 'luasocket_available' in net_health:
                        status = "Available" if net_health['luasocket_available'] else "Not Available"
                        print(f"  LuaSocket: {status}")
                    
                    if 'http_client_ready' in net_health:
                        status = "Ready" if net_health['http_client_ready'] else "Not Ready"
                        print(f"  HTTP Client: {status}")
                
                # Show overall system health
                if 'system' in health:
                    sys_health = health['system']
                    print(f"  System packages: {sys_health.get('installed_packages', 0)}")
                    print(f"  LuaRocks: {sys_health.get('luarocks_available', 'Unknown')}")
        
        except Exception as e:
            print_status(f"Networking health check failed: {e}", "ERROR")
        
        # Test networking capabilities
        print("\n--- Networking Capability Test ---")
        try:
            # Test LuaSocket availability
            socket_test = '''
            local ok, socket = pcall(require, "socket")
            if ok then
                return "LuaSocket available - Version: " .. (socket.VERSION or "unknown")
            else
                return "LuaSocket not available"
            end
            '''
            
            result = net_vm.execute_lua(socket_test)
            if result and result.get('success'):
                print_status(f"Socket test: {result.get('result')}", "SUCCESS")
            else:
                print_status(f"Socket test failed: {result.get('error', 'Unknown error')}", "ERROR")
        
        except Exception as e:
            print_status(f"Networking test failed: {e}", "ERROR")
        
        return net_vm
        
    except Exception as e:
        print_status(f"Networking VM demo failed: {e}", "ERROR")
        return None


def demo_error_scenarios():
    """Demonstrate error handling and recovery scenarios"""
    print_section("STEP 5: Error Handling & Recovery Scenarios")
    
    print_status("Testing error handling capabilities...")
    
    # Test 1: Invalid profile
    print("\n--- Invalid Profile Handling ---")
    try:
        env = EnvironmentManager(profile='nonexistent', debug_mode=True)
        print_status("Created environment with invalid profile - this should have failed", "WARNING")
    except Exception as e:
        print_status(f"Correctly handled invalid profile: {e}", "SUCCESS")
    
    # Test 2: Package installation failure
    print("\n--- Package Installation Error Handling ---")
    try:
        curator = get_curator()
        success = curator.install_package('nonexistent-package-12345')
        if success:
            print_status("Installation of fake package succeeded - unexpected!", "WARNING")
        else:
            print_status("Correctly handled invalid package installation", "SUCCESS")
    except Exception as e:
        print_status(f"Exception during package installation: {e}")
    
    # Test 3: VM execution error
    print("\n--- VM Execution Error Handling ---")
    try:
        env = EnvironmentManager(profile='minimal', debug_mode=True)
        vm = LuaProcess(name="ErrorTest", lua_executable=env.lua_executable)
        
        # Execute invalid Lua code
        result = vm.execute_lua('this is not valid lua code!')
        
        if result:
            if result.get('success'):
                print_status("Invalid Lua code executed successfully - unexpected!", "WARNING")
            else:
                error_msg = result.get('error', 'Unknown error')
                print_status(f"Correctly handled Lua error: {error_msg[:100]}...", "SUCCESS")
        else:
            print_status("VM execution returned None - handled gracefully", "SUCCESS")
            
    except Exception as e:
        print_status(f"Exception during VM execution test: {e}")


def demo_complete_workflow():
    """Demonstrate complete AGI bootstrapping workflow"""
    print_section("STEP 6: Complete AGI Bootstrapping Workflow")
    
    print_status("Demonstrating complete AGI development workflow...")
    
    try:
        # 1. Environment Detection and Setup
        print("\n--- Automated Environment Bootstrap ---")
        success = bootstrap_lua_environment(profile='development')
        
        if success:
            print_status("AGI environment bootstrap completed!", "SUCCESS")
        else:
            print_status("Bootstrap encountered issues but continued", "WARNING")
        
        # 2. Create production-ready VM
        print("\n--- Production VM Setup ---")
        env = EnvironmentManager(profile='full', debug_mode=False)  # Production mode
        
        # Create both regular and networked VMs
        main_vm = LuaProcess(name="AGI-Main", lua_executable=env.lua_executable)
        network_vm = NetworkedLuaVM(name="AGI-Network", lua_executable=env.lua_executable)
        
        # Setup both VMs with appropriate packages
        main_result = main_vm.setup_packages('full')
        network_result = network_vm.setup_networking_packages(include_advanced=True)
        
        print_status(f"Main VM setup: {'Success' if main_result.get('success') else 'Partial'}")
        print_status(f"Network VM setup: {'Success' if network_result.get('success') else 'Partial'}")
        
        # 3. Demonstrate coordinated operation
        print("\n--- Coordinated VM Operation ---")
        
        # Main VM: Data processing
        data_processing = '''
        local inspect = require("inspect")
        local data = {
            system = "AGI Bootstrapping Demo",
            timestamp = os.time(),
            components = {"environment", "curator", "vm", "networking"},
            status = "operational"
        }
        return inspect(data)
        '''
        
        main_result = main_vm.execute_lua(data_processing)
        if main_result and main_result.get('success'):
            print_status("Main VM data processing: SUCCESS", "SUCCESS")
            print(f"  Result: {main_result.get('result', '')[:100]}...")
        
        # Network VM: Capability check
        network_check = '''
        local socket = require("socket")
        return "Network VM operational - Socket version: " .. (socket.VERSION or "unknown")
        '''
        
        network_result = network_vm.execute_lua(network_check)
        if network_result and network_result.get('success'):
            print_status("Network VM capability check: SUCCESS", "SUCCESS")
            print(f"  Result: {network_result.get('result', '')}")
        
        print_status("AGI bootstrapping workflow completed!", "SUCCESS")
        
    except Exception as e:
        print_status(f"Complete workflow demo failed: {e}", "ERROR")


def main():
    """Main integration demo"""
    print_section("PyLua VM AGI Bootstrapping Integration Demo", "=")
    
    print("This demo showcases the complete AGI bootstrapping system:")
    print("• Intelligent environment management")  
    print("• Curator-based package curation")
    print("• Integrated VM creation and management")
    print("• Automated networking setup")
    print("• Comprehensive health monitoring")
    print("• Error handling and recovery")
    print("")
    
    start_time = time.time()
    
    # Run demonstration steps
    env_manager = demo_environment_setup()
    curator = demo_curator_intelligence() 
    vm = demo_vm_integration(env_manager, curator)
    network_vm = demo_networking_vm(env_manager)
    demo_error_scenarios()
    demo_complete_workflow()
    
    # Final summary
    print_section("Demo Summary & Next Steps")
    
    duration = time.time() - start_time
    print_status(f"Integration demo completed in {duration:.2f} seconds")
    
    print("\n--- System Status ---")
    if env_manager:
        print_status(f"Environment: {env_manager.profile} profile ready", "SUCCESS")
    
    if curator:
        health = curator.health_check()
        packages = len(curator.list_installed_packages())
        print_status(f"Curator: {packages} packages managed", "SUCCESS")
    
    if vm:
        print_status(f"Main VM: {vm.name} operational", "SUCCESS")
    
    if network_vm:
        print_status(f"Network VM: {network_vm.name} operational", "SUCCESS")
    
    print("\n--- What You Can Do Next ---")
    print("• Use the CLI: python -m pylua_vm.cli --interactive")
    print("• Create custom profiles with specific package sets") 
    print("• Develop Lua scripts using the curated package ecosystem")
    print("• Build networked applications with automatic dependency management")
    print("• Monitor system health and get intelligent package recommendations")
    
    print_section("Packaing System Ready!", "=")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user. Goodbye!")
        sys.exit(130)
    except Exception as e:
        print(f"\n\nDemo failed with unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)py