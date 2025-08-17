# MVP Software Defined Air Quality Monitor - Requirements Specification

## Project Overview

Build a minimum viable prototype of a software-defined air quality monitoring system using pylua-bioxen-vm for distributed Lua VM orchestration. The system should demonstrate real-time sensor data processing, aggregation, and monitoring through a Python command-line interface.

## Architecture Requirements

### System Components
- **2 Sensor Node VMs** (Lua processes) - Generate and process mock air quality data
- **1 Data Gateway VM** (Lua process) - Aggregate sensor data and calculate metrics
- **1 Python Control Center** - Orchestrate VMs and provide user interface

### Communication Pattern
- Sensor VMs connect to Gateway VM using client-server socket communication
- Gateway VM acts as central data aggregation point
- Python control center manages VM lifecycle and queries data from Gateway

## Functional Requirements

### Python Control Center
**Primary Functions:**
- Initialize and manage VM lifecycle using pylua-bioxen-vm VMManager
- Provide interactive command-line menu system using questionary library
- Display real-time air quality data in formatted console output
- Monitor system health and VM status
- Allow user to start/stop monitoring processes
- View real-time status with rich

**Menu System Requirements:**
- Main menu with options: View Current Data, System Status, Start/Stop Monitoring, Exit
- Real-time data display with formatted metrics (PM2.5, PM10, temperature, humidity)
- System status showing VM health, communication status, and active sensors
- Graceful shutdown of all VMs on exit

### Sensor Node VMs (Lua)
**Data Generation:**
- Generate realistic mock air quality sensor readings every 3-5 seconds
- Include measurements: PM2.5, PM10, temperature, humidity
- Add realistic variation/noise to simulate real sensor behavior
- Include sensor health status and data quality indicators

**Data Processing:**
- Apply basic data validation (range checking, outlier detection)
- Format data into standardized message structure with timestamp and sensor ID
- Handle connection failures and retry logic
- Transmit processed data to Gateway VM via socket communication

### Gateway VM (Lua)
**Data Aggregation:**
- Receive data from multiple sensor VMs simultaneously
- Store latest readings from each sensor node
- Calculate real-time averages across all active sensors
- Track sensor health and connectivity status

**Analytics:**
- Calculate simplified Air Quality Index (AQI) based on PM2.5 levels
- Detect basic patterns or anomalies in readings
- Maintain running statistics (min, max, average)
- Provide data export functionality for Python queries

## Technical Requirements

### Dependencies
- Python 3.7+ with pylua-bioxen-vm library installed
- questionary library for interactive CLI menus
- Lua 5.3+ with LuaSocket extension
- JSON handling capability in Lua (lua-cjson or equivalent)

### Data Format Specifications
**Sensor Message Structure:**
- Sensor ID (string identifier)
- Timestamp (Unix timestamp)
- Measurements object with PM2.5, PM10, temperature, humidity values
- Status indicators (calibrated, validated, confidence level)
- Data quality flags

**Gateway Response Structure:**
- Aggregated averages for all measurements
- Individual sensor readings
- Active sensor count and health status
- Air quality index calculation
- Last update timestamp

### Performance Requirements
- Support concurrent operation of 3 VMs (2 sensors + 1 gateway)
- Data latency under 1 second from sensor to display
- Stable operation for extended periods (hours)
- Graceful handling of VM failures or communication issues

## User Experience Requirements

### Command Line Interface
- Clear, intuitive menu navigation using questionary
- Real-time data display with appropriate units and formatting
- Color coding for different air quality levels (good/moderate/unhealthy)
- System status indicators showing VM health and communication status
- Responsive interface that updates without blocking user interaction

### Data Display
- Formatted tables showing current sensor readings
- Historical context (trend indicators, previous readings)
- Clear air quality interpretation (AQI level descriptions)
- Sensor-specific status information
- System performance metrics (uptime, message count, error rates)

## Testing and Validation Criteria

### System Integration
- All VMs start successfully and establish network connections
- Sensor data flows from generators through gateway to Python interface
- Menu system responds correctly to all user inputs
- System handles VM restarts and network interruptions gracefully

### Data Accuracy
- Mock sensor data falls within realistic ranges for air quality measurements
- Aggregation calculations produce mathematically correct averages
- AQI calculations follow standard air quality index formulas
- Timestamps and data sequencing remain consistent across VMs

### Reliability Requirements
- System runs continuously for at least 30 minutes without crashes
- Handles network disconnections and VM communication failures
- Provides clear error messages for troubleshooting
- Allows clean shutdown without leaving orphaned processes

## Success Metrics

### Demonstration Goals
- **Process Isolation**: Show independent VM operation with fault tolerance
- **Network Communication**: Demonstrate socket-based VM-to-VM messaging
- **Real-time Processing**: Display live data updates from distributed sources
- **Orchestration**: Showcase Python control of multiple Lua VMs
- **Scalability**: Easy to add additional sensor VMs

### Learning Outcomes
- Understanding of pylua-bioxen-vm architecture and capabilities
- Experience with distributed system design patterns
- Knowledge of real-time data processing and aggregation
- Familiarity with Lua networking and JSON handling
- CLI application development with Python

## Development Phases

### Phase 1: Core Infrastructure (Day 1-2)
- Set up Python VM manager with basic VM creation
- Implement simple Lua scripts for sensor and gateway
- Establish basic socket communication between VMs
- Create minimal questionary-based menu system

### Phase 2: Data Processing (Day 3-4)  
- Add realistic sensor data generation with proper variation
- Implement data validation and error handling in Lua VMs
- Create aggregation logic in gateway VM
- Add formatted data display in Python interface

### Phase 3: Polish and Testing (Day 5)
- Add comprehensive error handling and logging
- Implement graceful shutdown and cleanup
- Create user documentation and setup instructions
- Test system reliability and performance

## Expected Deliverables

1. **Source Code Package** with all Python and Lua scripts
2. **Setup Instructions** for dependencies and configuration
3. **User Guide** for operating the CLI interface
4. **Technical Documentation** explaining VM architecture and communication
5. **Demo Script** showing key features and capabilities

This MVP will serve as a compelling demonstration of pylua-bioxen-vm's capabilities for distributed real-time data processing applications.