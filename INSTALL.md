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

### **2.2 Create ESPHome Configuration**

Create `bee-hive-monitor.yaml`:

```yaml
substitutions:
  device_name: bee-hive-monitor
  friendly_name: "Bee Hive Monitor"
  
esphome:
  name: bee-hive-monitor
  friendly_name: Bee Hive Monitor

esp32:
  board: seeed_xiao_esp32s3
  framework:
    type: arduino
  variant: esp32s3

psram:
  mode: octal
  speed: 80MHz

i2c:
  - id: bus_a
    sda: GPIO40
    scl: GPIO39
    scan: true
    frequency: 400kHz

logger:
  level: INFO

api:
  encryption:
    key: !secret api_encryption_key  # Auto-generated

ota:
  - platform: esphome
    password: !secret ota_password

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password
  
  # Use static IP for reliability (recommended)
  manual_ip:
    static_ip: 192.168.1.100  # Change to match your network
    gateway: 192.168.1.1      # Your router IP
    subnet: 255.255.255.0
  
  ap:
    ssid: "Bee Hive Monitor Fallback"
    password: "BeeMonitor2024"  # Change this!

captive_portal:

web_server:
  port: 80

# Camera Configuration
esp32_camera:
  name: "Camera"
  external_clock:
    pin: GPIO10
    frequency: 20MHz
  i2c_id: bus_a
  data_pins: [GPIO15, GPIO17, GPIO18, GPIO16, GPIO14, GPIO12, GPIO11, GPIO48]
  vsync_pin: GPIO38
  href_pin: GPIO47
  pixel_clock_pin: GPIO13
  
  resolution: 1600x1200
  jpeg_quality: 10
  max_framerate: 5 fps
  idle_framerate: 0.2 fps
  
  # Adjust these based on your camera orientation
  vertical_flip: false
  horizontal_mirror: false

# Sensors
sensor:
  - platform: wifi_signal
    name: "WiFi Signal"
    update_interval: 60s
    
  - platform: uptime
    name: "Uptime"

binary_sensor:
  - platform: status
    name: "Status"

button:
  - platform: restart
    name: "Restart"

switch:
  - platform: template
    name: "Monitoring Enabled"
    id: monitoring_enabled
    optimistic: true
    restore_mode: RESTORE_DEFAULT_ON
```

### **2.3 Create secrets.yaml**

In same directory as `bee-hive-monitor.yaml`:

```yaml
# secrets.yaml
wifi_ssid: "YourWiFiName"
wifi_password: "YourWiFiPassword"
api_encryption_key: "auto-generated-key-will-appear-here"
ota_password: "change-me"
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

### **3.4 Create Python Monitoring Script**

Create `bee_activity_monitor.py`:

```python
#!/usr/bin/env python3
"""
Bee Hive Activity Monitor
Real-time motion detection for ESP32-S3 camera
Optimized for Colorado dry climate
"""

import cv2
import numpy as np
import requests
import time
import logging
from datetime import datetime
from typing import Optional, Tuple

# ============================================================================
# CONFIGURATION - UPDATE THESE VALUES
# ============================================================================
ESP32_IP = "192.168.1.XXX"  # Your ESP32 static IP
HA_URL = "http://192.168.1.XXX:8123"  # Your Home Assistant URL
HA_TOKEN = "YOUR_LONG_LIVED_ACCESS_TOKEN"  # Create in HA → Profile

# Motion detection settings
SENSITIVITY = 25  # Lower = more sensitive (15-30 recommended)
MIN_AREA = 20     # Minimum contour area to consider (15-25 recommended)
UPDATE_INTERVAL = 5  # Seconds between updates

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/pi/bee-monitor/bee_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# MOTION DETECTION CLASS
# ============================================================================
class BeeActivityDetector:
    """Detects bee activity using frame differencing"""
    
    def __init__(self, sensitivity: int = 25, min_area: int = 20):
        self.sensitivity = sensitivity
        self.min_area = min_area
        self.previous_frame = None
        
    def preprocess_frame(self, frame: np.ndarray) -> np.ndarray:
        """Convert to grayscale and blur"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (21, 21), 0)
        return blurred
    
    def detect_motion(self, frame: np.ndarray) -> Tuple[float, int]:
        """
        Detect motion between current and previous frame
        Returns: (activity_score, motion_pixels)
        """
        processed = self.preprocess_frame(frame)
        
        # Need previous frame for comparison
        if self.previous_frame is None:
            self.previous_frame = processed
            return 0.0, 0
        
        # Frame differencing
        frame_delta = cv2.absdiff(self.previous_frame, processed)
        thresh = cv2.threshold(frame_delta, self.sensitivity, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        # Find contours (areas of motion)
        contours, _ = cv2.findContours(
            thresh.copy(), 
            cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        # Sum up motion pixels
        motion_pixels = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > self.min_area:
                motion_pixels += area
        
        # Calculate activity score (0-100%)
        frame_area = processed.shape[0] * processed.shape[1]
        activity_score = min(100, (motion_pixels / frame_area) * 100 * 10)
        
        self.previous_frame = processed
        return activity_score, motion_pixels

# ============================================================================
# ESP32 CAMERA CLASS
# ============================================================================
class ESP32Camera:
    """Interface to ESP32 camera via Home Assistant"""
    
    def __init__(self, ha_url: str, ha_token: str, 
                 camera_entity: str = "camera.bee_hive_monitor_camera"):
        self.ha_url = ha_url.rstrip('/')
        self.camera_entity = camera_entity
        self.headers = {'Authorization': f'Bearer {ha_token}'}
        self.snapshot_url = f"{self.ha_url}/api/camera_proxy/{camera_entity}"
        
    def get_frame(self) -> Optional[np.ndarray]:
        """Fetch current frame from camera"""
        try:
            response = requests.get(
                self.snapshot_url, 
                headers=self.headers, 
                timeout=10
            )
            
            if response.status_code == 200:
                img_array = np.frombuffer(response.content, dtype=np.uint8)
                frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                return frame
            else:
                logger.error(f"Failed to get frame: HTTP {response.status_code}")
                
        except Exception as e:
            logger.error(f"Failed to get frame: {e}")
            
        return None

# ============================================================================
# HOME ASSISTANT UPDATER CLASS
# ============================================================================
class HomeAssistantUpdater:
    """Updates Home Assistant sensor states"""
    
    def __init__(self, url: str, token: str):
        self.url = url.rstrip('/')
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
    def update_sensor(self, entity_id: str, state, attributes: dict = None):
        """Update a sensor state in Home Assistant"""
        url = f"{self.url}/api/states/{entity_id}"
        
        # Format state
        if isinstance(state, (int, float)):
            state_value = round(state, 1)
        else:
            state_value = str(state)
        
        data = {
            'state': state_value,
            'attributes': attributes or {}
        }
        
        try:
            response = requests.post(
                url, 
                headers=self.headers, 
                json=data, 
                timeout=5
            )
            response.raise_for_status()
            logger.debug(f"Updated {entity_id} = {state}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update {entity_id}: {e}")
            return False

# ============================================================================
# MAIN MONITORING LOOP
# ============================================================================
def main():
    """Main monitoring loop"""
    
    logger.info("=" * 60)
    logger.info("🐝 Bee Hive Activity Monitor Starting")
    logger.info("=" * 60)
    logger.info(f"ESP32 Camera: {ESP32_IP}")
    logger.info(f"Home Assistant: {HA_URL}")
    logger.info(f"Sensitivity: {SENSITIVITY}, Min Area: {MIN_AREA}")
    logger.info(f"Update Interval: {UPDATE_INTERVAL}s")
    logger.info("=" * 60)
    
    # Initialize components
    camera = ESP32Camera(HA_URL, HA_TOKEN)
    detector = BeeActivityDetector(sensitivity=SENSITIVITY, min_area=MIN_AREA)
    ha_updater = HomeAssistantUpdater(HA_URL, HA_TOKEN)
    
    # Test camera connection
    logger.info("Testing camera connection...")
    test_frame = camera.get_frame()
    if test_frame is None:
        logger.error("❌ Cannot connect to camera! Check ESP32 IP and HA token.")
        return
        
    logger.info(f"✅ Camera connected! Frame size: {test_frame.shape}")
    logger.info("\n🚀 Starting monitoring loop...\n")
    
    # Monitoring loop
    consecutive_failures = 0
    max_failures = 10
    
    try:
        while True:
            # Get frame
            frame = camera.get_frame()
            
            if frame is not None:
                consecutive_failures = 0
                
                # Detect motion
                activity_score, motion_pixels = detector.detect_motion(frame)
                bees_per_minute = int(max(0, motion_pixels // 75))
                
                # Classify activity level
                if activity_score > 80:
                    level = "Very High"
                elif activity_score > 60:
                    level = "High"
                elif activity_score > 40:
                    level = "Moderate"
                elif activity_score > 20:
                    level = "Low"
                else:
                    level = "Very Low"
                
                # Log
                logger.info(
                    f"Activity: {activity_score:5.1f}% | "
                    f"Level: {level:10s} | "
                    f"Bees/min: {bees_per_minute:3d}"
                )
                
                # Update Home Assistant sensors
                ha_updater.update_sensor(
                    'sensor.bee_hive_monitor_activity_score',
                    activity_score,
                    {
                        'motion_pixels': int(motion_pixels),
                        'timestamp': datetime.now().isoformat(),
                        'unit_of_measurement': '%',
                        'state_class': 'measurement',
                        'icon': 'mdi:bee'
                    }
                )
                
                ha_updater.update_sensor(
                    'sensor.bee_hive_monitor_estimated_bees_per_minute',
                    bees_per_minute,
                    {
                        'unit_of_measurement': 'bees/min',
                        'state_class': 'measurement',
                        'icon': 'mdi:bee'
                    }
                )
                
                ha_updater.update_sensor(
                    'sensor.bee_hive_monitor_activity_level',
                    level,
                    {'icon': 'mdi:chart-line'}
                )
                
                ha_updater.update_sensor(
                    'binary_sensor.bee_hive_monitor_high_activity',
                    'on' if activity_score > 80 else 'off',
                    {'device_class': 'motion'}
                )
                
                ha_updater.update_sensor(
                    'binary_sensor.bee_hive_monitor_low_activity_alert',
                    'on' if activity_score < 10 else 'off',
                    {'device_class': 'problem'}
                )
                
            else:
                consecutive_failures += 1
                logger.warning(
                    f"Failed to get frame ({consecutive_failures}/{max_failures})"
                )
                
                if consecutive_failures >= max_failures:
                    logger.error("Too many consecutive failures. Exiting.")
                    break
            
            # Wait before next update
            time.sleep(UPDATE_INTERVAL)
            
    except KeyboardInterrupt:
        logger.info("\n⏹️  Monitoring stopped by user")
        
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)
        
    finally:
        logger.info("🛑 Bee Hive Activity Monitor Stopped")

if __name__ == "__main__":
    main()
```

### **3.5 Configure Script**

Edit the configuration section at top of `bee_activity_monitor.py`:

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

Make script run automatically on boot:

```bash
# Create service file
sudo nano /etc/systemd/system/bee-monitor.service
```

Paste this content:

```ini
[Unit]
Description=Bee Hive Activity Monitor
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/bee-monitor
ExecStart=/usr/bin/python3 /home/pi/bee-monitor/bee_activity_monitor.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
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

**See**: [`HOME_ASSISTANT_SETUP.md`](HOME_ASSISTANT_SETUP.md) for complete configuration files

### **Quick Summary:**

1. **Add to `configuration.yaml`**:
   - Sensor customizations (state_class for statistics)
   - Template sensors (health score, weight compensation, etc.)
   - Binary sensors (alerts)
   - Input helpers (weight snapshot, thresholds)

2. **Add to `automations.yaml`**:
   - Critical health alerts
   - Robbing detection
   - Daily weight snapshot (midnight)
   - Daily summary report (8 PM)
   - Temperature alerts
   - Battery low warnings

3. **Restart Home Assistant**:
   ```bash
   # Developer Tools → YAML → Check Configuration
   # Developer Tools → YAML → Restart
   ```

---

## 📱 Step 6: Dashboard Setup

**See**: Dashboard YAML in repository

1. **Settings → Dashboards**
2. Click **+ Add Dashboard**
3. Name: "Apiary"
4. **⋮ → Raw Configuration Editor**
5. Paste dashboard YAML
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
