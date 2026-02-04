# 📁 GitHub Repository Setup Guide

Quick guide for organizing your Bee Brothel repository.

---

## 📂 Recommended Repository Structure

```
bee-brothel/
├── README.md                          # Main overview (already created)
├── LICENSE                            # MIT License
├── INSTALL.md                         # Step-by-step installation
├── HARDWARE.md                        # Hardware shopping list
├── TROUBLESHOOTING.md                 # Common issues & solutions
│
├── docs/
│   ├── HOME_ASSISTANT_SETUP.md       # HA configuration details
│   └── images/                        # Screenshots for documentation
│       ├── dashboard.png
│       ├── camera-mounted.jpg
│       └── health-score-example.png
│
├── config/
│   ├── esphome/
│   │   └── bee-hive-monitor.yaml     # ESP32 configuration
│   │
│   ├── home-assistant/
│   │   ├── configuration.yaml        # HA sensors & templates
│   │   ├── automations.yaml          # Alert automations
│   │   └── dashboard.yaml            # Lovelace dashboard
│   │
│   └── raspberry-pi/
│       ├── bee_activity_monitor.py   # Motion detection script
│       ├── bee-monitor.service       # Systemd service
│       └── requirements.txt          # Python dependencies
│
├── examples/
│   ├── solar-power-setup/
│   │   ├── README.md
│   │   └── wiring-diagram.png
│   │
│   └── multi-hive-setup/
│       ├── README.md
│       └── configuration-example.yaml
│
└── .github/
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.md
    │   └── feature_request.md
    └── CONTRIBUTING.md
```

---

## 🚀 Quick Setup Steps

### **1. Create Repository**

```bash
# On GitHub
# Click "New Repository"
# Name: "bee-brothel"
# Description: "🐝 Smart bee hive monitoring with Home Assistant"
# Public or Private
# Initialize with README ✓
```

### **2. Clone & Add Files**

```bash
# Clone your repo
git clone https://github.com/YOUR_USERNAME/bee-brothel.git
cd bee-brothel

# Copy all the files I created into the repo
# - README.md (replace default)
# - INSTALL.md
# - HARDWARE.md
# - TROUBLESHOOTING.md
# - LICENSE

# Create directories
mkdir -p docs config/esphome config/home-assistant config/raspberry-pi examples

# Move HOME_ASSISTANT_SETUP.md to docs/
mv HOME_ASSISTANT_SETUP.md docs/

# Add your configuration files
# (copy from your actual system)
```

### **3. Add Configuration Files**

```bash
# ESPHome
cp /path/to/your/bee-hive-monitor.yaml config/esphome/

# Home Assistant (extract only bee-related sections)
# Create these files with only the bee hive specific parts:
config/home-assistant/configuration.yaml
config/home-assistant/automations.yaml
config/home-assistant/dashboard.yaml

# Raspberry Pi
cp /home/pi/bee-monitor/bee_activity_monitor.py config/raspberry-pi/
cp /etc/systemd/system/bee-monitor.service config/raspberry-pi/

# Create requirements.txt
echo "opencv-python==4.8.1.78" > config/raspberry-pi/requirements.txt
echo "numpy==1.24.3" >> config/raspberry-pi/requirements.txt
echo "requests==2.31.0" >> config/raspberry-pi/requirements.txt
```

### **4. Add Images**

```bash
# Take screenshots of:
mkdir docs/images

# Recommended screenshots:
# - Dashboard overview
# - Health score breakdown
# - Live camera feed
# - Example notifications
# - Physical installation (camera, sensors)
# - Weatherproof enclosure
```

### **5. Update README.md**

Add image links:
```markdown
## 📸 Dashboard Preview

![Dashboard Overview](docs/images/dashboard.png)
![Camera Feed](docs/images/camera-feed.png)
```

### **6. Commit & Push**

```bash
git add .
git commit -m "Initial commit: Complete bee monitoring system"
git push origin main
```

---

## ⚙️ Configuration Files to Include

### **✅ DO Include (Generic)**
- ESPHome YAML (with secrets removed)
- Python script (with tokens removed)
- Systemd service file
- Home Assistant sensors/templates
- Automations (generic alerts)
- Dashboard layout

### **❌ DO NOT Include (Sensitive)**
- WiFi passwords
- Home Assistant tokens
- API keys
- GreenAPI credentials
- Broodminder passwords
- Static IP addresses (your network)
- Sensor serial numbers

### **🔒 Use Secrets Files**

**In ESPHome:**
```yaml
# bee-hive-monitor.yaml
wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password

# secrets.yaml (NOT in repo)
wifi_ssid: "YourNetwork"
wifi_password: "YourPassword"
```

**In Python:**
```python
# bee_activity_monitor.py
ESP32_IP = "192.168.x.x"  # UPDATE THIS
HA_TOKEN = "YOUR_TOKEN"   # UPDATE THIS
```

**Add to .gitignore:**
```bash
echo "secrets.yaml" >> .gitignore
echo "*.log" >> .gitignore
echo "__pycache__/" >> .gitignore
```

---

## 📝 Good README Practices

### **Badges** (Optional but Nice)
```markdown
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2024.1+-blue.svg)
![Python](https://img.shields.io/badge/Python-3.9+-green.svg)
![Stars](https://img.shields.io/github/stars/YOUR_USERNAME/bee-brothel?style=social)
```

### **Table of Contents**
```markdown
## 📑 Table of Contents

- [Features](#features)
- [Hardware Requirements](#hardware-requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
```

### **Demo GIF** (Optional)
```markdown
![Demo](docs/images/demo.gif)
```

Create with:
- Screen recording software
- GIF converter
- Or: Use Claude in Chrome's GIF recorder! 📹

---

## 🤝 Issue Templates

### **Bug Report Template**

Create `.github/ISSUE_TEMPLATE/bug_report.md`:

```markdown
---
name: Bug Report
about: Create a report to help improve the system
title: '[BUG] '
labels: bug
assignees: ''
---

**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen.

**System Info:**
 - Home Assistant Version: [e.g. 2024.1.0]
 - ESP32 Model: [e.g. XIAO ESP32-S3]
 - Raspberry Pi Model: [e.g. Pi 4 4GB]

**Logs:**
```
Paste relevant logs here
```

**Additional context**
Screenshots, configuration files, etc.
```

### **Feature Request Template**

Create `.github/ISSUE_TEMPLATE/feature_request.md`:

```markdown
---
name: Feature Request
about: Suggest an enhancement
title: '[FEATURE] '
labels: enhancement
assignees: ''
---

**Feature Description**
Clear description of what you want.

**Use Case**
Why would this be useful?

**Proposed Solution**
How you envision it working.

**Alternatives Considered**
Other approaches you've thought about.
```

---

## 🎯 Topics & Keywords

**Add to GitHub repository settings:**

```
Topics (tags):
- home-assistant
- beekeeping
- iot
- esp32
- raspberry-pi
- computer-vision
- smart-hive
- bee-monitoring
- opencv
- automation
- sensors
- esphome
```

---

## 🌟 After Publishing

### **Share on:**
- Home Assistant Community Forums
- Reddit: r/homeassistant, r/Beekeeping
- Beekeeping forums
- Twitter/X with #homeassistant #beekeeping
- YouTube (if you make a video)

### **Encourage Contributions:**
```markdown
## 🤝 Contributing

We welcome contributions! Areas where help is needed:

- AI-powered bee counting
- Additional climate profiles
- Dashboard improvements
- Documentation translations
- Bug fixes

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
```

### **Star This Project!**
```markdown
## ⭐ Star This Project

If you find this helpful, please star it on GitHub!
It helps others discover the project.
```

---

## 📊 GitHub Insights

**Enable:**
- ✅ Issues
- ✅ Discussions (for questions)
- ✅ Wiki (optional)
- ✅ Releases (for versioning)

**First Release:**
```bash
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0
```

---

## ✅ Pre-Publication Checklist

- [ ] All sensitive data removed
- [ ] Configuration examples tested
- [ ] README links work
- [ ] License file included
- [ ] Issue templates added
- [ ] Images optimized (< 500KB each)
- [ ] Code formatted consistently
- [ ] Comments explain non-obvious code
- [ ] Installation tested from scratch
- [ ] Troubleshooting covers common issues

---

## 🎉 You're Ready!

Your repository is now ready to help other beekeepers! 🐝

**Questions?** Open an issue in your own repo!

---

**Made with 💚 for bees everywhere**
