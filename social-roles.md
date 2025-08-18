# Social Roles for Air Quality Monitoring System

| Role | Agent | Primary Responsibilities | Key Competencies | Communication Patterns | Authority Boundaries |
|------|-------|-------------------------|------------------|----------------------|---------------------|
| **Field Technician** | Sensor Node VMs | - Generate accurate sensor readings<br>- Validate data quality<br>- Monitor equipment health<br>- Report anomalies | - Domain expertise in air quality measurement<br>- Equipment calibration knowledge<br>- Data validation skills<br>- Fault detection abilities | - Regular data reports to Data Analyst<br>- Exception alerts for anomalies<br>- Status updates to Operations Supervisor<br>- Peer communication for calibration | - Can reject bad readings<br>- Can flag equipment issues<br>- Cannot modify reporting protocols<br>- Cannot override safety thresholds |
| **Data Analyst** | Gateway VM | - Aggregate multi-source data<br>- Calculate derived metrics (AQI)<br>- Quality assurance across sensors<br>- Generate analytical reports | - Statistical analysis skills<br>- Pattern recognition<br>- Quality control expertise<br>- Report generation abilities | - Receives reports from Field Technicians<br>- Provides summaries to Operations Supervisor<br>- Requests clarification on anomalous data<br>- Coordinates between multiple technicians | - Can request data re-validation<br>- Can calculate derived metrics<br>- Cannot directly control sensors<br>- Cannot change data collection protocols |
| **Operations Supervisor** | Python Control Center | - Oversee system operations<br>- Manage staff (VM) lifecycle<br>- Interface with external stakeholders<br>- Coordinate response to issues | - System management expertise<br>- Resource allocation skills<br>- Stakeholder communication<br>- Problem escalation judgment | - Issues directives to all staff<br>- Receives status reports from Data Analyst<br>- Communicates with human users<br>- Coordinates system-wide responses | - Can start/stop operations<br>- Can reassign resources<br>- Can modify operational parameters<br>- Full system oversight authority |

## Role Interaction Patterns

| Interaction | Frequency | Protocol | Purpose |
|-------------|-----------|----------|---------|
| Field Technician → Data Analyst | Every 3-5 seconds | Structured data transmission | Regular data reporting |
| Data Analyst → Operations Supervisor | On-demand queries | Request/response pattern | Status updates and summaries |
| Operations Supervisor → Field Technician | Startup/shutdown | Direct commands | Lifecycle management |
| Operations Supervisor → Data Analyst | Real-time queries | Interactive requests | Monitoring and control |
| Field Technician ↔ Field Technician | As needed | Peer coordination | Cross-validation and calibration |

## Social Behaviors by Role

### Field Technician Behaviors
- **Professional Pride**: Maintains high data quality standards
- **Reliability**: Consistent reporting schedule adherence
- **Expertise Recognition**: Defers to Data Analyst for aggregation decisions
- **Peer Collaboration**: Coordinates with other sensors for validation
- **Escalation Awareness**: Knows when to alert supervisor about issues

### Data Analyst Behaviors
- **Analytical Objectivity**: Processes all data without bias
- **Quality Focus**: Maintains standards across all inputs
- **Synthesis Skills**: Combines multiple data sources meaningfully
- **Communication Clarity**: Provides clear summaries to management
- **Curiosity**: Investigates anomalies and patterns

### Operations Supervisor Behaviors
- **Leadership Responsibility**: Takes accountability for system performance
- **Resource Management**: Efficiently allocates computational resources
- **Stakeholder Service**: Responsive to human user needs
- **Decision Authority**: Makes system-level operational choices
- **Team Coordination**: Facilitates effective collaboration between roles