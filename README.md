#  Vortex - Minecraft Bedrock DDoS Tool

**Professional-grade latency attack tool for Minecraft Bedrock Edition servers**

>  **LEGAL DISCLAIMER**: This tool is for educational and authorized penetration testing purposes only. Unauthorized use against servers you don't own is illegal.

##  Features

- **Real-time Latency Monitoring** - Track server performance before, during, and after attacks
- **Proxy Support** - SOCKS5, SOCKS4, and HTTP proxy integration for anonymity
- **Multi-threaded Attacks** - Configurable bot threads for maximum impact
- **Live Progress Tracking** - Real-time statistics and latency visualization
- **Server Reconnaissance** - Pre-attack server information gathering
- **Impact Analysis** - Detailed effectiveness reporting with color-coded ratings

##  Installation

### Requirements
```bash
pip install mcstatus pyfiglet pysocks
```

### Quick Start
```bash
python vortex.py
```

## 🚀 Usage

### Basic Attack
1. Run the script
2. Enter target server IP and port (default: 19132)
3. Configure threads and duration
4. Monitor real-time impact

### Advanced Features
- **Proxy Integration**: Route attacks through SOCKS/HTTP proxies
- **Custom Delays**: Fine-tune packet timing for optimal impact
- **Live Metrics**: Watch latency spikes in real-time

##  Target Compatibility

-  **Minecraft Bedrock Edition**
-  **Windows 10/11 Edition**
-  **Mobile Editions** (iOS/Android)
-  **Console Editions** (Xbox, PlayStation, Switch)

##  Attack Metrics

The tool provides comprehensive performance analysis:

- **Baseline Latency** - Pre-attack server performance
- **Peak Latency** - Maximum latency achieved during attack
- **Latency Increase** - Percentage-based impact measurement
- **Effectiveness Rating** - Color-coded success assessment

##  Proxy Configuration

### Supported Proxy Types
- **SOCKS5** (Recommended)
- **SOCKS4**
- **HTTP**

### Example Proxy Setup
```
Proxy Type: socks5
Proxy IP: 127.0.0.1
Proxy Port: 9050
```

##  Effectiveness Ratings

- ** DEVASTATING** (500%+ latency increase)
- ** HIGH IMPACT** (200-500% latency increase)
- ** MODERATE IMPACT** (50-200% latency increase)
- ** MINIMAL IMPACT** (Below 50% latency increase)

##  Interface Preview

```
Yb    dP  dP"Yb  88""Yb 888888 888888 Yb  dP 
 Yb  dP  dP   Yb 88__dP   88   88__    YbdP  
  YbdP   Yb   dP 88"Yb    88   88""    dPYb  
   YP     YbodP  88  Yb   88   888888 dP  Yb 

        Minecraft DDoS Tool

Creator: S-K1DD13
Compatibility: Bedrock Edition

🌐 Server IP: 192.168.1.100
🔌 Server port [default: 19132]: 19132
```

## ⚙️ Configuration Options

### Attack Parameters
- **Threads**: Number of concurrent attack bots (1-1000+)
- **Duration**: Attack length in seconds
- **Delay**: Time between packets (lower = more aggressive)

### Monitoring Features
- Real-time latency tracking
- Packet count monitoring
- Progress visualization
- Impact assessment

##  Technical Details

### Protocol
Uses Minecraft Bedrock's native ping protocol for maximum compatibility

### Packet Structure
```python
PING_PACKET = b'\x01' + b'\x00' * 17
```

### Performance Optimization
- Multi-threaded design
- Non-blocking socket operations
- Efficient resource management

##  Output Example

```
📡 Baseline Latency: 45.2 ms
💥 Peak Latency: 1250.8 ms
📉 Final Latency: 320.6 ms
🚀 Latency Increase: 2767.3%
🎯 Attack Effectiveness: 💀 DEVASTATING (100.0%)
```

##  Legal & Ethical Use

### Authorized Scenarios
- Testing your own servers
- Educational purposes
- Authorized penetration testing
- Security research

### Prohibited Use
- Attacking servers without permission
- Malicious disruption of services
- Harassment or griefing
- Any illegal activities

##  Troubleshooting

### Common Issues
1. **Server appears offline** - Verify IP/port and server status
2. **Proxy connection failed** - Check proxy settings and connectivity
3. **Low effectiveness** - Increase threads or adjust delay timing

### Performance Tips
- Use higher thread counts for better impact
- Lower delays increase packet frequency
- Proxy usage may reduce attack speed

##  Contributing

This tool is maintained for educational purposes. Responsible disclosure and ethical use are mandatory.

##  License

Educational Use Only - No funny business...

---

**Vortex** - Professional Minecraft Bedrock Edition server testing tool  
**Creator**: S-K1DD13  
**Version**: 1.0  
**Category**: Network Security Testing
