# 🐝 The Bee Brothel - Smart Hive Monitoring System

A comprehensive, self-hosted bee hive monitoring system using computer vision, environmental sensors, and Home Assistant automation. Designed for Colorado's dry climate with seasonal winter/summer health scoring.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2024.1+-blue.svg)
![Python](https://img.shields.io/badge/Python-3.9+-green.svg)
![ESPHome](https://img.shields.io/badge/ESPHome-2024.1+-purple.svg)

---

## 📸 System Overview

**Real-time monitoring of:**
- 🐝 Bee activity via computer vision (motion detection)
- 🌡️ Internal hive temperature (dual probes)
- ⚖️ Hive weight with temperature compensation
- 💧 Humidity levels
- 🎯 Comprehensive health scoring (0-100%)
- 📊 Nectar flow detection
- 🚨 Robbing alerts
- 👑 Queen health indicators

---

## ✨ Key Features

### **Seasonal Intelligence**
- **Winter Mode** (Nov 1 - Mar 31): Optimized for cluster temps (50-70°F), low activity normal
- **Summer Mode** (Apr 1 - Oct 31): Optimized for brood rearing (93-95°F), high foraging expected
- **Colorado Climate Adjusted**: Humidity ranges calibrated for dry climate (20-40% optimal)

### **Real-Time Monitoring**
- Live camera feed with 5-second motion detection updates
- Activity percentage calculated from pixel-level motion analysis
- Estimated bees-per-minute count
- 24-hour trend graphs

### **Smart Alerts**
- Critical health score (<30%) with 15-min delay
- Robbing detection (high activity + weight loss)
- Temperature alerts (too hot/cold)
- Low activity warnings during warm weather
- Nectar flow detection
- Daily summary reports (8 PM)

### **Temperature-Compensated Weight**
- Raw scale readings corrected for thermal expansion (-0.0558 kg/°C)
- Accurate daily weight change calculations
- Nectar flow vs. consumption tracking

---

## 🛠️ Hardware Requirements

### **Core Components (~$250-300)**
- **Camera**: Seeed XIAO ESP32-S3 with camera (~$15)
- **Computer Vision**: Raspberry Pi 3/4 (~$35-55)
- **Sensors**: Broodminder-T2 + W3 (~$200)
- **Hub**: Home Assistant server (any platform)

### **Optional**
- iPhone + WhatsApp (via GreenAPI)
- Solar panel + battery for remote deployment

📋 **[Complete Hardware Shopping List →](HARDWARE.md)**

---

## 📂 Repository Structure

```
bee-brothel/
├── README.md                          # This file
├── INSTALL.md                         # Step-by-step installation guide
├── HARDWARE.md                        # Detailed shopping list & specs
├── TROUBLESHOOTING.md                 # Common issues & solutions
├── LICENSE                            # MIT License
│
├── config/                            # ⭐ All configuration files included!
│   ├── README.md                      # Config setup instructions
│   │
│   ├── esphome/
│   │   ├── bee-hive-monitor.yaml     # ESP32 camera configuration
│   │   └── secrets.yaml.template     # WiFi credentials template
│   │
│   ├── home-assistant/
│   │   ├── configuration.yaml        # Sensors, health scoring, templates
│   │   ├── automations.yaml          # 11 alert automations
│   │   └── dashboard.yaml            # Complete Lovelace dashboard
│   │
│   └── raspberry-pi/
│       ├── bee_activity_monitor.py   # Motion detection script
│       ├── bee-monitor.service       # Systemd auto-start service
│       └── requirements.txt          # Python dependencies
│
└── docs/
    ├── HOME_ASSISTANT_SETUP.md       # Detailed HA configuration guide
    └── images/                        # Screenshots & photos
```

---

## 🚀 Quick Start

### **1. Get the Hardware**
📋 [Hardware Shopping List](HARDWARE.md) - Complete list with links (~$250-300 total)

### **2. Install the Software**
📖 [Installation Guide](INSTALL.md) - Step-by-step setup for:
- ESP32 camera (ESPHome)
- Raspberry Pi motion detection
- Home Assistant configuration
- Broodminder sensor integration

### **3. Configure Your System**
⚙️ [Configuration Files](config/) - All configs included, just customize:
- Update sensor entity IDs (your Broodminder serials)
- Set network IPs (ESP32, Raspberry Pi, Home Assistant)
- Adjust humidity ranges (if not in Colorado)

### **4. Deploy & Monitor**
📱 Access your dashboard and start monitoring!

---

## 🎯 Health Scoring System

### **Winter Mode** (November 1 - March 31)
| Component | Points | Optimal Range |
|-----------|--------|---------------|
| Temperature | 30 | 50-70°F (cluster) |
| Activity | 25 | 10-30% (low normal) |
| Weight | 25 | -0.1 to 0.1 kg/day (stable) |
| Humidity | 20 | 20-35% (CO dry climate) |

### **Summer Mode** (April 1 - October 31)
| Component | Points | Optimal Range |
|-----------|--------|---------------|
| Temperature | 30 | 93-95°F (brood rearing) |
| Activity | 25 | 60%+ (high foraging) |
| Weight | 25 | >0.5 kg/day (nectar flow) |
| Humidity | 20 | 30-40% (CO dry climate) |

**Health Status:**
- 85-100%: ✅ Excellent - Hive thriving!
- 70-84%: 🟡 Good - Normal conditions
- 50-69%: 🟠 Fair - Monitor closely
- 30-49%: 🔴 Poor - Intervention may be needed
- 0-29%: 🚨 Critical - Immediate attention required

---

## 🔔 Automated Alerts

**Notifications via iPhone + WhatsApp:**
- 🚨 Critical health (<30%) after 15 min
- 🐝 Robbing detected (high activity + weight loss)
- 🌡️ Temperature alerts (too hot/cold)
- ⚖️ Significant weight loss (>0.5 kg/day)
- 📊 Daily summary at 8 PM
- 🔋 Sensor battery low (<20%)
- 📷 Camera offline (10 min)
- 🎉 Excellent health achieved (>85%)

---

## 📊 Dashboard Preview

**Features:**
- Health score with seasonal breakdown
- Live camera feed (16:9 aspect ratio)
- Activity, temperature, weight, humidity cards
- 24-hour trend graphs
- System status monitoring
- Manual controls (restart, snapshot)

*Screenshots coming soon - add yours to `docs/images/`!*

---

## 🌍 Climate Customization

**Designed for Colorado but easily adaptable:**

Humidity ranges in [`config/home-assistant/configuration.yaml`](config/home-assistant/configuration.yaml):

```yaml
# For humid climates (e.g., Eastern US)
# Change winter optimal from 20-35% to 40-60%
# Change summer optimal from 30-40% to 50-60%

# For very dry climates (e.g., Southwest)
# Keep ranges as-is or adjust lower (15-25% winter, 20-30% summer)
```

---

## 💾 Data Storage

**Home Assistant automatically tracks:**
- Activity levels (1-hour, 24-hour averages)
- Weight changes (24-hour, 7-day averages)
- Temperature trends (24-hour average)
- Health score history
- Peak activity times

**Retention**: Configurable (default 10+ days)

---

## 🔒 Privacy & Security

- **100% self-hosted** - No cloud dependencies except Broodminder sensors
- **Local processing** - Computer vision runs on your Raspberry Pi
- **Secure communications** - Home Assistant uses encrypted API
- **Optional cloud** - Broodminder cloud can be disabled

---

## 🐛 Troubleshooting

Common issues and solutions in [TROUBLESHOOTING.md](TROUBLESHOOTING.md):
- ESP32 camera connection problems
- Python script errors
- Sensor unavailable states
- Health score showing "unknown"
- Motion detection calibration

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

**Ideas for enhancement:**
- AI-powered bee counting (YOLO/TensorFlow)
- Varroa mite detection via camera
- Audio analysis (buzzing patterns)
- Weather forecast integration
- Multi-hive support
- Mobile app (standalone)

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file

---

## 🙏 Credits

**Inspiration & Components:**
- [Broodminder](https://broodminder.com/) - Professional hive sensors
- [ESPHome](https://esphome.io/) - ESP32 firmware framework
- [Home Assistant](https://www.home-assistant.io/) - Home automation platform
- [OpenCV](https://opencv.org/) - Computer vision library

---

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/bee-brothel/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/bee-brothel/discussions)

---

## ⭐ Star This Project

If you find this project helpful, please star it on GitHub to help others discover it!

---

**Made with 💚 for bees in Colorado**

*Note: This system is designed for monitoring and educational purposes. Always follow local beekeeping regulations and best practices.*
