# Configuration Files

This directory contains all configuration files for The Bee Brothel monitoring system.

## 📁 Directory Structure

```
config/
├── esphome/
│   ├── bee-hive-monitor.yaml          # ESP32 camera configuration
│   └── secrets.yaml.template          # Template for WiFi credentials
│
├── home-assistant/
│   ├── configuration.yaml             # Sensors, templates, and health scoring
│   ├── automations.yaml               # Alert automations
│   └── dashboard.yaml                 # Lovelace dashboard configuration
│
└── raspberry-pi/
    ├── bee_activity_monitor.py        # Motion detection Python script
    ├── bee-monitor.service            # Systemd service file
    └── requirements.txt               # Python dependencies
```

## ⚙️ Setup Instructions

### 1. ESPHome Configuration

```bash
# Copy secrets template
cp config/esphome/secrets.yaml.template config/esphome/secrets.yaml

# Edit with your details
nano config/esphome/secrets.yaml

# Flash to ESP32
esphome run config/esphome/bee-hive-monitor.yaml
```

### 2. Raspberry Pi Setup

```bash
# Install dependencies
pip3 install --break-system-packages -r config/raspberry-pi/requirements.txt

# Copy script to Raspberry Pi
scp config/raspberry-pi/bee_activity_monitor.py pi@raspberrypi.local:~/bee-monitor/

# Edit configuration in script
nano ~/bee-monitor/bee_activity_monitor.py
# Update: ESP32_IP, HA_URL, HA_TOKEN

# Copy systemd service
sudo cp config/raspberry-pi/bee-monitor.service /etc/systemd/system/

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable bee-monitor
sudo systemctl start bee-monitor
```

### 3. Home Assistant Configuration

```bash
# Backup your current configuration first!
cp /config/configuration.yaml /config/configuration.yaml.backup

# Add bee hive sections from:
config/home-assistant/configuration.yaml

# Add automations from:
config/home-assistant/automations.yaml

# Check configuration
# Home Assistant -> Developer Tools -> YAML -> Check Configuration

# Restart Home Assistant
```

### 4. Dashboard

```bash
# In Home Assistant:
# Settings -> Dashboards -> + Add Dashboard
# Name: "Apiary"
# Three dots menu -> Raw Configuration Editor
# Paste contents from: config/home-assistant/dashboard.yaml
```

## 🔧 Customization Required

### Update Sensor Entity IDs

Replace `XXXXX` with your actual Broodminder sensor serial numbers:

- `sensor.broodminder_t_XXXXX_temperature` (internal temp)
- `sensor.broodminder_w_XXXXX_weight_realtime` (scale)
- `sensor.broodminder_w_XXXXX_temperature` (external temp)
- `sensor.broodminder_w_XXXXX_humidity` (humidity)

Find your actual sensor IDs:
1. Home Assistant -> Developer Tools -> States
2. Search for "broodminder"
3. Copy exact entity IDs

### Update Network Settings

**ESP32 (esphome/bee-hive-monitor.yaml):**
```yaml
manual_ip:
  static_ip: 192.168.1.100  # Change to available IP on your network
  gateway: 192.168.1.1      # Change to your router IP
```

**Raspberry Pi (raspberry-pi/bee_activity_monitor.py):**
```python
ESP32_IP = "192.168.1.100"            # Match ESP32 IP above
HA_URL = "http://192.168.1.50:8123"   # Your Home Assistant URL
HA_TOKEN = "YOUR_TOKEN_HERE"          # Long-lived access token
```

### Adjust for Your Climate

If not in Colorado's dry climate, update humidity ranges in `configuration.yaml`:

**Humid climates (Eastern US, Europe):**
- Winter: 40-60% optimal
- Summer: 50-70% optimal

**Very dry (Southwest US):**
- Winter: 15-25% optimal
- Summer: 20-30% optimal

## 🔒 Security Notes

**Never commit these to GitHub:**
- `secrets.yaml` (WiFi passwords)
- Home Assistant tokens
- API keys
- Your network IPs

These are already in `.gitignore` to prevent accidental commits.

## 📚 Documentation

- [Full Installation Guide](../INSTALL.md)
- [Home Assistant Setup Details](../docs/HOME_ASSISTANT_SETUP.md)
- [Troubleshooting Guide](../TROUBLESHOOTING.md)
- [Hardware Requirements](../HARDWARE.md)
