# 📖 Installation Guide

## The Bee Brothel - Complete Setup Instructions

This guide will walk you through setting up your bee hive monitoring system from scratch.

---

## 📋 Pre-Installation Checklist

### **Required Hardware** ✅
- [ ] SEEED XIAO ESP32-S3 with camera module
- [ ] Raspberry Pi 3B+ or newer (with SD card, power supply)
- [ ] Broodminder T2 temperature sensor(s)
- [ ] Broodminder W3 scale (includes temp + humidity)
- [ ] WiFi network with internet access
- [ ] Weatherproof enclosure for ESP32 camera
- [ ] USB-C cable and power adapter (ESP32)
- [ ] microSD card (32GB+, Class 10) for Raspberry Pi

### **Required Software** ✅
- [ ] Home Assistant server (OS, Container, or Core)
- [ ] ESPHome dashboard or CLI installed
- [ ] Broodminder account (free tier sufficient)
- [ ] Python 3.9+ on Raspberry Pi
- [ ] Basic Linux/command line familiarity

### **Optional** 📦
- [ ] GreenAPI account (WhatsApp notifications)
- [ ] iPhone with Home Assistant app
- [ ] Solar panel + battery for remote deployment

---

## 🗺️ Installation Overview

**Estimated Time**: 2-3 hours

```
Step 1: Physical Hardware Setup (30 min)
   ↓
Step 2: ESP32 Camera Configuration (30 min)
   ↓
Step 3: Raspberry Pi Motion Detection (45 min)
   ↓
Step 4: Broodminder Integration (15 min)
   ↓
Step 5: Home Assistant Configuration (45 min)
   ↓
Step 6: Dashboard Setup (15 min)
   ↓
Step 7: Testing & Calibration (30 min)
```

---

## 📍 Step 1: Physical Hardware Setup

### **1.1 Position ESP32 Camera**

**Location Requirements:**
- Clear view of hive entrance
- 2-4 feet from hive face
- Protected from direct rain/sun
- WiFi signal strength: >-70 dBm recommended

**Mounting:**
```bash
# Test WiFi signal strength at proposed location
# Use your phone or a WiFi analyzer app
# Ideal: -50 to -65 dBm
# Acceptable: -66 to -75 dBm
# Poor: -76 dBm or weaker
```

**Power Options:**
1. **Wired**: Run USB-C cable to nearby outlet (preferred)
2. **Solar**: 5W panel + 18650 battery bank (for remote apiaries)

**Weatherproofing:**
- Use IP65+ rated enclosure
- Silicone gasket around camera lens opening
- Ensure USB cable entry is sealed
- Test enclosure with garden hose before installing

### **1.2 Place Broodminder Sensors**

**Broodminder-T2 (Temperature):**
- **Lower Sensor**: Between 2nd and 3rd frame from entrance
- **Upper Sensor** (optional): Top brood box, center
- Secure with velcro or wire, avoid blocking bee movement

**Broodminder-W3 (Scale):**
- Level surface under hive
- Calibrate per Broodminder instructions
- Protect from rain if not weatherproof model

**Sensor Sync:**
- Open Broodminder app on phone
- Place phone near hive
- Sensors auto-sync via Bluetooth
- Verify readings in Broodminder app

### **1.3 Set Up Raspberry Pi**

**Physical Setup:**
- Place indoors OR in weatherproof enclosure
- Wired Ethernet connection (most reliable)
- Or: Strong WiFi signal (>-65 dBm)
- Power via official power supply (2.5A+ recommended)

**Why Indoors?**
- Easier troubleshooting
- Stable power
- No weatherproofing needed
- Can run other services (Pi-hole, VPN, etc.)

---

## 🎥 Step 2: ESP32 Camera Configuration

### **2.1 Install ESPHome**

**Option A: ESPHome Dashboard (Easiest)**
```bash
# Install ESPHome on your computer
pip3 install esphome

# Start dashboard
esphome dashboard config/
# Opens web interface at http://localhost:6052
```

**Option B: Home Assistant Add-on**
- Navigate to **Supervisor → Add-on Store**
- Install **ESPHome**
- Start add-on

### **2.2 Use Included ESPHome Configuration**

**The configuration file is already included in this repository!**

📁 **[`config/esphome/bee-hive-monitor.yaml`](config/esphome/bee-hive-monitor.yaml)**

Just copy it and customize the network settings:

```bash
# Copy from repository
cp config/esphome/bee-hive-monitor.yaml ~/esphome/

# Edit the network settings
nano ~/esphome/bee-hive-monitor.yaml
```

**Update these lines in the file:**
```yaml
wifi:
  manual_ip:
    static_ip: 192.168.1.100  # Change to available IP on your network
    gateway: 192.168.1.1      # Change to your router IP
```

### **2.3 Create secrets.yaml**

**Use the included template:**

```bash
# Copy template from repository
cp config/esphome/secrets.yaml.template ~/esphome/secrets.yaml

# Edit with your WiFi credentials
nano ~/esphome/secrets.yaml
```

Fill in your details:
```yaml
wifi_ssid: "YourWiFiNetworkName"
wifi_password: "YourWiFiPassword"
fallback_password: "BeeMonitor2024"  # Change this!
```

### **2.4 Flash ESP32**

**First Time (USB Connection):**
```bash
# Compile and flash
esphome run bee-hive-monitor.yaml

# Select USB port when prompted
# Wait 2-3 minutes for compilation and upload
```

**Subsequent Updates (Over-The-Air):**
```bash
# After initial flash, can update wirelessly
esphome run bee-hive-monitor.yaml
# Select "bee-hive-monitor.local" or IP address
```

### **2.5 Verify Camera**

**Check Web Interface:**
1. Navigate to `http://192.168.1.100` (your ESP32 IP)
2. Click "Camera" link
3. Should see live stream

**Check Home Assistant:**
1. **Settings → Devices & Services → ESPHome**
2. Should see "Bee Hive Monitor"
3. Click device → Should see camera entity

**Troubleshooting:**
- No stream? Check GPIO pin connections
- Green/purple artifacts? Hardware issue, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Won't connect? Verify WiFi credentials, check signal strength

---

## 🍓 Step 3: Raspberry Pi Setup

### **3.1 Install Raspberry Pi OS**

**Flash OS:**
1. Download [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
2. Flash "Raspberry Pi OS (64-bit)" to SD card
3. **Enable SSH** in settings before writing

**First Boot:**
```bash
# SSH into Pi (default user: pi, password: raspberry)
ssh pi@raspberrypi.local

# Change default password immediately
passwd

# Update system
sudo apt update && sudo apt upgrade -y
```

### **3.2 Install Dependencies**

```bash
# Install Python and OpenCV
sudo apt install -y python3-pip python3-opencv

# Install Python packages
pip3 install --break-system-packages opencv-python numpy requests
```

### **3.3 Create Monitoring Directory**

```bash
# Create directory structure
mkdir -p ~/bee-monitor
cd ~/bee-monitor
```

### **3.4 Use Included Python Monitoring Script**

**The Python script is already included in this repository!**

📁 **[`config/raspberry-pi/bee_activity_monitor.py`](config/raspberry-pi/bee_activity_monitor.py)**

```bash
# Copy script from repository to Raspberry Pi
scp config/raspberry-pi/bee_activity_monitor.py pi@raspberrypi.local:~/bee-monitor/

# Copy requirements file
scp config/raspberry-pi/requirements.txt pi@raspberrypi.local:~/bee-monitor/

# SSH into Pi
ssh pi@raspberrypi.local

# Install dependencies
cd ~/bee-monitor
pip3 install --break-system-packages -r requirements.txt
```

### **3.5 Configure Script**

Edit the configuration at the top of `bee_activity_monitor.py`:

```bash
nano ~/bee-monitor/bee_activity_monitor.py
```

**Update these values:**
```python
ESP32_IP = "192.168.1.100"  # Change to your ESP32 IP
HA_URL = "http://192.168.1.50:8123"  # Change to your HA URL
HA_TOKEN = "YOUR_TOKEN_HERE"  # See below for how to get
```

**Get Long-Lived Access Token:**
1. Home Assistant → Click your name (bottom left)
2. Scroll to **Long-Lived Access Tokens**
3. Click **Create Token**
4. Name it "Bee Monitor Script"
5. Copy token and paste in script

### **3.6 Test Script Manually**

```bash
cd ~/bee-monitor
python3 bee_activity_monitor.py

# Should see:
# ✅ Camera connected! Frame size: (1200, 1600, 3)
# 🚀 Starting monitoring loop...
# Activity:  15.2% | Level: Low        | Bees/min:  34

# Press Ctrl+C to stop
```

### **3.7 Create Systemd Service**

**The systemd service file is already included in this repository!**

📁 **[`config/raspberry-pi/bee-monitor.service`](config/raspberry-pi/bee-monitor.service)**

```bash
# Copy service file from repository
scp config/raspberry-pi/bee-monitor.service pi@raspberrypi.local:/tmp/

# SSH into Pi and install service
ssh pi@raspberrypi.local
sudo mv /tmp/bee-monitor.service /etc/systemd/system/
```

**Enable and start service:**

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable bee-monitor

# Start service now
sudo systemctl start bee-monitor

# Check status
sudo systemctl status bee-monitor

# View logs
sudo journalctl -u bee-monitor -f
```

---

## 📊 Step 4: Broodminder Integration

### **4.1 Configure Broodminder Cloud Integration**

**In Home Assistant:**
1. **Settings → Devices & Services**
2. Click **+ Add Integration**
3. Search for "Broodminder"
4. Enter Broodminder credentials
5. Select sensors to import

**Verify Sensors:**
- `sensor.broodminder_t_XXXXX_temperature` (internal temp)
- `sensor.broodminder_w_XXXXX_weight_realtime` (scale)
- `sensor.broodminder_w_XXXXX_temperature` (external temp)
- `sensor.broodminder_w_XXXXX_humidity` (humidity)
- Battery sensors for each device

---

## 🏠 Step 5: Home Assistant Configuration

**All configuration files are included in this repository!**

📁 **Configuration Files:**
- [`config/home-assistant/configuration.yaml`](config/home-assistant/configuration.yaml) - Sensors & health scoring
- [`config/home-assistant/automations.yaml`](config/home-assistant/automations.yaml) - Alert automations
- [`config/home-assistant/dashboard.yaml`](config/home-assistant/dashboard.yaml) - Dashboard layout

📖 **Detailed Guide**: [`docs/HOME_ASSISTANT_SETUP.md`](docs/HOME_ASSISTANT_SETUP.md)

### **Quick Setup:**

1. **Backup your current config**:
   ```bash
   cp /config/configuration.yaml /config/configuration.yaml.backup
   cp /config/automations.yaml /config/automations.yaml.backup
   ```

2. **Add bee hive sections**:
   - Copy sensors from `config/home-assistant/configuration.yaml` to your `configuration.yaml`
   - Copy automations from `config/home-assistant/automations.yaml` to your `automations.yaml`
   - **Important**: Update all sensor entity IDs to match YOUR Broodminder sensors!

3. **Restart Home Assistant**:
   ```bash
   # Developer Tools → YAML → Check Configuration
   # Developer Tools → YAML → Restart
   ```

---

## 📱 Step 6: Dashboard Setup

**The complete dashboard configuration is included!**

📁 **[`config/home-assistant/dashboard.yaml`](config/home-assistant/dashboard.yaml)**

1. **Settings → Dashboards**
2. Click **+ Add Dashboard**
3. Name: "Apiary"
4. **⋮ → Raw Configuration Editor**
5. Copy contents from `config/home-assistant/dashboard.yaml` and paste
6. Save

---

## ✅ Step 7: Testing & Calibration

### **7.1 Verify All Sensors**

**Developer Tools → States**, search for:
- ✅ `sensor.bee_hive_monitor_activity_score`
- ✅ `sensor.bee_hive_health_score`
- ✅ `sensor.beehive_weight_compensated`
- ✅ `sensor.broodminder_t_XXXXX_temperature`
- ✅ `binary_sensor.bee_hive_critical_health_alert`

### **7.2 Calibrate Motion Detection**

**Too Sensitive** (activity always >80%):
- Increase `SENSITIVITY` in Python script (try 30)
- Increase `MIN_AREA` (try 25)

**Not Sensitive Enough** (activity always <10%):
- Decrease `SENSITIVITY` (try 20)
- Decrease `MIN_AREA` (try 15)

**Restart service after changes:**
```bash
sudo systemctl restart bee-monitor
```

### **7.3 Adjust Health Score for Your Climate**

Edit humidity ranges in `configuration.yaml` if not in Colorado:

**Humid climates** (Eastern US, Europe):
- Winter: 40-60% optimal
- Summer: 50-70% optimal

**Very dry** (Southwest US):
- Winter: 15-25% optimal
- Summer: 20-30% optimal

### **7.4 Test Notifications**

**Trigger test alert:**
```yaml
# Developer Tools → Services
# Service: notify.mobile_app_YOUR_PHONE
# Data:
title: "Test Alert"
message: "Bee monitoring system online!"
```

---

## 🎉 Installation Complete!

**You should now have:**
- ✅ Live camera feed
- ✅ Real-time activity monitoring
- ✅ Health scoring
- ✅ Automated alerts
- ✅ Beautiful dashboard

**Next Steps:**
1. Monitor for 24-48 hours to verify stability
2. Adjust sensitivity if needed
3. Enable/disable alerts as desired
4. Enjoy your smart hive! 🐝

---

## 📚 Additional Resources

- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues
- [HARDWARE_SETUP.md](HARDWARE_SETUP.md) - Detailed hardware guide
- [HOME_ASSISTANT_SETUP.md](HOME_ASSISTANT_SETUP.md) - Complete HA config
- [GitHub Issues](https://github.com/yourusername/bee-brothel/issues) - Get help

---

**Questions? Open a GitHub issue or discussion!**
