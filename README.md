# OS-Level AI Daemon

An intelligent Python-based daemon for operating system monitoring, resource allocation, and anomaly detection using machine learning.

## Features

### 🔍 System Monitoring
- Real-time CPU, memory, disk, and network monitoring
- Process-level resource tracking
- Historical metrics collection and analysis

### 🤖 AI-Powered Anomaly Detection
- Machine learning-based anomaly detection using Isolation Forest
- Automatic baseline establishment
- Severity-based anomaly classification (LOW, MEDIUM, HIGH)

### ⚙️ Intelligent Resource Allocation
- Dynamic resource threshold monitoring
- Automatic optimization recommendations
- Top resource consumer identification

### 📊 Intelligent Logging
- Structured logging with multiple levels
- Anomaly-specific logging with JSON export
- Metric tracking and historical analysis

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/OS-Level-AI-Daemon.git
cd OS-Level-AI-Daemon
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure you have appropriate permissions:
```bash
# The daemon needs permissions to access system metrics
# On Linux, you may need to run with sudo or configure capabilities
```

## Usage

### Running the Daemon

#### Foreground Mode (for testing):
```bash
python os_ai_daemon.py
```

#### Background Mode (production):
```bash
# Using systemd (recommended for Linux)
sudo cp os-ai-daemon.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start os-ai-daemon
sudo systemctl enable os-ai-daemon
```

### Configuration

Edit the daemon parameters in `os_ai_daemon.py`:

```python
# Monitoring interval (seconds)
self.monitor_interval = 10

# Resource thresholds
self.optimization_rules = {
    'cpu_threshold': 80.0,
    'memory_threshold': 85.0,
    'disk_threshold': 90.0,
}
```

### Logs

Logs are stored in `/var/log/os-ai-daemon/` by default:
- `daemon.log` - Main daemon log with all system metrics
- `anomalies.json` - Detected anomalies in JSON format

## Architecture

```
OS-Level-AI-Daemon/
├── os_ai_daemon.py         # Main daemon implementation
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── setup.py               # Installation script
├── os-ai-daemon.service   # Systemd service file
└── tests/                 # Unit tests
    └── test_daemon.py
```

## Components

### AILogger
Intelligent logging system with structured output and anomaly-specific logging.

### SystemMonitor
Real-time system monitoring with ML-powered anomaly detection using Isolation Forest algorithm.

### ResourceAllocator
AI-driven resource analysis and optimization recommendations.

### OSDaemon
Main daemon orchestrator managing all components.

## Requirements

- Python 3.8+
- Linux, macOS, or Windows
- Sufficient permissions for system monitoring

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Style
```bash
# Format code
black os_ai_daemon.py

# Lint
pylint os_ai_daemon.py
```

## Performance

- Lightweight footprint (~20-50MB RAM)
- Configurable monitoring interval
- Efficient metric collection using psutil
- ML model training only after baseline collection

## Security Considerations

- Runs with necessary system privileges
- Logs are protected with appropriate permissions
- No sensitive data is logged by default
- Process information is handled securely

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues, questions, or contributions, please open an issue on GitHub.

## Roadmap

- [ ] Web dashboard for real-time monitoring
- [ ] Email/Slack notifications for critical anomalies
- [ ] Advanced ML models (LSTM, Autoencoders)
- [ ] Multi-host monitoring and aggregation
- [ ] Custom plugin system
- [ ] Performance profiling tools
- [ ] Container-aware monitoring
- [ ] Cloud integration (AWS, Azure, GCP)

## Acknowledgments

Built with:
- psutil for system monitoring
- scikit-learn for machine learning
- Python's built-in logging for structured logs
