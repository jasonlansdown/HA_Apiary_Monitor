# 🔧 Troubleshooting Guide

Common issues and solutions for The Bee Brothel monitoring system.

---

## 📷 ESP32 Camera Issues

### **Camera Won't Connect to WiFi**

**Symptoms:**
- Device not showing in Home Assistant
- Can't access web interface at ESP32 IP
- Fallback AP active

**Solutions:**

1. **Check WiFi Credentials**
   ```yaml
   # In bee-hive-monitor.yaml secrets.yaml
   wifi_ssid: "YourNetworkName"  # Exactly as shown in WiFi settings
   wifi_password: "YourPassword"  # Case-sensitive!
   ```

2. **Check WiFi Signal Strength**
   ```bash
   # From computer, check signal at camera location
   # Use WiFi analyzer app or phone
   # Need > -75 dBm for reliability
   ```

3. **Use Static IP**
   ```yaml
   wifi:
     ssid: !secret wifi_ssid
     password: !secret wifi_password
     manual_ip:
       static_ip: 192.168.1.100
       gateway: 192.168.1.1
       subnet: 255.255.255.0
   ```

4. **Connect to Fallback AP**
   - Look for WiFi network "Bee Hive Monitor Fallback"
   - Connect with password from config
   - Configure WiFi through captive portal

### **Camera Stream Shows Green/Purple Lines**

**Symptoms:**
- Vertical lines in image
- Distorted colors
- Image artifacts

**Cause:** Camera hardware issue (common with replacement modules)

**Solution:**
1. Try original camera module if you replaced it
2. Check cable connection between ESP32 and camera
3. Try different camera module
4. Add ferrite bead to camera cable

### **Camera Image Is Black/Too Dark**

**Symptoms:**
- Black image
- Very dark image even in daylight

**Solutions:**

1. **Adjust Camera Settings**
   ```yaml
   esp32_camera:
     brightness: 1    # Try 1 or 2
     contrast: 1
     saturation: 0
   ```

2. **Check Lens Focus**
   - Rotate lens gently to adjust focus
   - Some modules have fixed focus

3. **Verify Power Supply**
   - Use quality USB-C cable
   - 5V 2A+ power supply
   - Insufficient power causes image issues

### **Camera Keeps Disconnecting**

**Symptoms:**
- "Unavailable" status in Home Assistant
- Frequent reconnections

**Solutions:**

1. **Improve WiFi Signal**
   - Move closer to router
   - Add WiFi extender
   - Use directional antenna

2. **Check Power Supply**
   - Quality USB cable
   - Stable power source
   - Not powered from computer USB (insufficient)

3. **Reduce Framerate**
   ```yaml
   esp32_camera:
     max_framerate: 3 fps  # Reduce from 5
   ```

---

## 🍓 Raspberry Pi Issues

### **Python Script Won't Start**

**Symptoms:**
- Service fails immediately
- `systemctl status bee-monitor` shows errors

**Common Errors:**

**1. "ModuleNotFoundError: No module named 'cv2'"**
```bash
# Solution: Install OpenCV
pip3 install --break-system-packages opencv-python
```

**2. "Connection refused" or "Failed to get frame"**

**Check ESP32 IP:**
```python
# In bee_activity_monitor.py
ESP32_IP = "192.168.1.100"  # Update to correct IP
```

**Verify Home Assistant Token:**
```bash
# Test HA API manually
curl -X GET \
  -H "Authorization: Bearer YOUR_TOKEN" \
  http://192.168.1.50:8123/api/states/camera.bee_hive_monitor_camera
```

**3. "Permission denied" on log file**
```bash
# Fix permissions
sudo chown pi:pi /home/pi/bee-monitor/bee_monitor.log
sudo chmod 644 /home/pi/bee-monitor/bee_monitor.log
```

### **Script Runs But No Updates in Home Assistant**

**Symptoms:**
- Script logs show activity
- Home Assistant sensors stay "unknown"

**Solutions:**

1. **Check Sensor Entity IDs**
   ```python
   # In Python script, verify entity IDs match HA
   'sensor.bee_hive_monitor_activity_score'
   # Not:
   'sensor.activity_score'
   ```

2. **Check Home Assistant Token**
   - Token expired? Create new one
   - Token has correct permissions?

3. **Check Home Assistant URL**
   ```python
   HA_URL = "http://192.168.1.50:8123"  # Include http://
   ```

### **Motion Detection Too Sensitive**

**Symptoms:**
- Activity always 80-100%
- Triggered by wind, shadows, clouds

**Solutions:**

1. **Increase Sensitivity Threshold**
   ```python
   SENSITIVITY = 30  # Was 25, try 30-35
   ```

2. **Increase Minimum Area**
   ```python
   MIN_AREA = 25  # Was 20, try 25-30
   ```

3. **Restart Service**
   ```bash
   sudo systemctl restart bee-monitor
   ```

### **Motion Detection Not Sensitive Enough**

**Symptoms:**
- Activity always 0-10%
- Missing obvious bee activity

**Solutions:**

1. **Decrease Sensitivity**
   ```python
   SENSITIVITY = 20  # Was 25, try 15-20
   ```

2. **Decrease Minimum Area**
   ```python
   MIN_AREA = 15  # Was 20
   ```

3. **Check Camera Angle**
   - Camera too far? Move closer (2-4 feet optimal)
   - Poor lighting? Adjust position

4. **Check Frame Rate**
   - Higher FPS = better motion detection
   - Try 5 fps on ESP32

---

## 📊 Home Assistant Issues

### **Health Score Shows "Unknown"**

**Symptoms:**
- `sensor.bee_hive_health_score` is "unknown"
- Dashboard shows "unavailable"

**Causes & Solutions:**

**1. Missing Dependency Sensors**

Check in Developer Tools → States:
```
✅ sensor.bee_hive_monitor_activity_score
✅ sensor.broodminder_t_47_50_96_temperature
✅ sensor.beehive_weight_compensated
✅ sensor.broodminder_w_57_41_5e_humidity
✅ sensor.broodminder_w_57_41_5e_temperature
✅ sensor.bee_hive_daily_weight_change
```

If any are missing:
- Check Raspberry Pi script is running
- Verify Broodminder integration configured
- Check sensor entity IDs match your sensors

**2. Template Syntax Error**

Test in Developer Tools → Template:
```jinja2
{% set activity = states('sensor.bee_hive_monitor_activity_score') | float(0) %}
{% set temp = states('sensor.broodminder_t_47_50_96_temperature') | float(0) %}
Activity: {{ activity }}
Temp: {{ temp }}
```

Should return numbers, not errors.

**3. Sensor Entity IDs Don't Match**

Your Broodminder sensors might have different IDs:
```yaml
# Find actual IDs in Developer Tools → States
# Update in configuration.yaml template sensors
sensor.broodminder_t_XXXXX_temperature  # Your actual ID
```

### **Weight Compensation Not Working**

**Symptoms:**
- `sensor.beehive_weight_compensated` is "unknown"
- Weight shows same as raw reading

**Solutions:**

1. **Check Broodminder Sensors Available**
   - Weight sensor: `sensor.broodminder_w_XXXXX_weight_realtime`
   - Temperature sensor: `sensor.broodminder_w_XXXXX_temperature`

2. **Update Entity IDs**
   ```yaml
   # In template, replace with your actual sensor IDs
   {% set raw_weight = states('sensor.broodminder_w_57_41_5e_weight_realtime') | float(0) %}
   {% set temperature = states('sensor.broodminder_w_57_41_5e_temperature') | float(30) %}
   ```

### **Automations Not Triggering**

**Symptoms:**
- No notifications received
- Automation shows "Triggered 0 times"

**Solutions:**

1. **Check Automation Enabled**
   - Settings → Automations → Find automation
   - Ensure toggle is ON

2. **Check Trigger Conditions**
   ```yaml
   # Example: Temperature alert
   triggers:
   - trigger: numeric_state
     entity_id: sensor.bee_hive_health_score
     below: 30  # Is health score actually below 30?
     for:
       minutes: 15  # Must stay below for 15 minutes
   ```

3. **Test Manually**
   - Settings → Automations → Select automation
   - Click "Run"
   - Check if notification received

4. **Check Traces**
   - Settings → Automations → Select automation
   - Click "Traces"
   - See why automation didn't trigger

### **Sensors Not Recording Statistics**

**Symptoms:**
- No history graphs
- Long-term statistics missing

**Solution:**

Add `state_class` to sensors:
```yaml
homeassistant:
  customize:
    sensor.bee_hive_monitor_activity_score:
      state_class: measurement  # Critical!
```

Restart Home Assistant after adding.

---

## 🌡️ Broodminder Sensor Issues

### **Sensors Not Appearing in Home Assistant**

**Symptoms:**
- Integration shows "No devices"
- Sensors are "unavailable"

**Solutions:**

1. **Check Broodminder Account**
   - Log into [broodminder.com](https://broodminder.com)
   - Verify sensors are syncing
   - Check last sync time

2. **Re-sync Sensors**
   - Open Broodminder app
   - Place phone near hive
   - Wait for Bluetooth sync
   - Check broodminder.com for new data

3. **Reconfigure Integration**
   - Settings → Integrations → Broodminder
   - Remove integration
   - Add again with correct credentials

### **Temperature Readings Seem Wrong**

**Symptoms:**
- Temperature doesn't match expectations
- Sudden jumps in temperature

**Notes:**

1. **Sensor Placement Matters**
   - Lower brood box sensor: NOT in cluster center
   - Reads 50-70°F in winter (correct!)
   - Reads 85-95°F in summer if near brood

2. **Temperature Fluctuations Normal**
   - Winter: 40-70°F (cluster moves)
   - Summer: 85-100°F (varies by proximity to brood)

3. **Trust the Bees**
   - If bees look healthy, temperature OK
   - Don't panic over single sensor reading

### **Weight Readings Fluctuate**

**Symptoms:**
- Weight changes hourly
- Seems to gain/lose weight with temperature

**Explanation:** This is normal! It's thermal expansion of the scale.

**Solution:** Use temperature compensation:
```yaml
# Already included in configuration
sensor.beehive_weight_compensated
```

This corrects for thermal expansion (-0.0558 kg/°C).

---

## 📱 Dashboard Issues

### **Camera Feed Not Showing**

**Symptoms:**
- Black square where camera should be
- "Entity not available"

**Solutions:**

1. **Check Camera Entity**
   ```yaml
   # In dashboard, verify entity ID
   entity: camera.bee_hive_monitor_camera
   ```

2. **Check ESP32 Online**
   - Developer Tools → States
   - Search: `binary_sensor.bee_hive_monitor_status`
   - Should be "on"

3. **Try Different Camera Card**
   ```yaml
   type: picture-entity
   entity: camera.bee_hive_monitor_camera
   camera_view: live  # Or: auto
   ```

### **Cards Showing "Entity Not Found"**

**Symptoms:**
- Red error boxes
- "Entity ... not found"

**Solution:** Update entity IDs in dashboard YAML to match your sensors.

**Find Your Entity IDs:**
1. Developer Tools → States
2. Search for "bee" or "broodminder"
3. Copy exact entity IDs
4. Replace in dashboard YAML

### **Graphs Not Showing Data**

**Symptoms:**
- Blank graphs
- "No data"

**Causes:**

1. **Sensor Doesn't Have state_class**
   - See "Sensors Not Recording Statistics" above

2. **Not Enough Data Yet**
   - Wait 24 hours for meaningful graphs

3. **max_age Too Short**
   ```yaml
   # In statistics sensor
   max_age:
     hours: 24  # Increase if needed
   ```

---

## 🚨 Alert Issues

### **Not Receiving Notifications**

**Symptoms:**
- Automations trigger but no notification
- Silent failures

**Solutions:**

1. **Check Notification Service**
   ```yaml
   # Developer Tools → Services
   # Service: notify.notify
   # Data:
   message: "Test notification"
   ```

2. **Check Home Assistant App Installed**
   - iPhone: Install from App Store
   - Configure in app settings

3. **Check WhatsApp Integration (if using)**
   ```yaml
   # Verify GreenAPI configured
   notify:
     - platform: greenapi
   ```

### **Too Many Notifications**

**Symptoms:**
- Spam of alerts
- Same alert repeating

**Solutions:**

1. **Add Delays to Automations**
   ```yaml
   triggers:
   - trigger: numeric_state
     entity_id: sensor.bee_hive_health_score
     below: 30
     for:
       minutes: 15  # Prevents false alerts
   ```

2. **Set mode: single**
   ```yaml
   - id: bee_hive_critical_health
     alias: Bee Hive - Critical Health Alert
     mode: single  # Won't trigger again until condition clears
   ```

---

## 🌐 Network Issues

### **Devices Keep Going Offline**

**Symptoms:**
- ESP32 or Pi frequently unavailable
- Intermittent connections

**Solutions:**

1. **Use Static IP Addresses**
   ```yaml
   # ESP32
   wifi:
     manual_ip:
       static_ip: 192.168.1.100
       gateway: 192.168.1.1
       subnet: 255.255.255.0
   ```

2. **Check WiFi Signal**
   ```bash
   # On Raspberry Pi
   iwconfig
   # Look for: Link Quality and Signal level
   ```

3. **Use Wired Connection (Pi)**
   - Much more reliable than WiFi
   - Especially for Raspberry Pi

4. **Router DHCP Reservations**
   - Assign static IPs in router settings
   - Prevents IP address changes

---

## 💡 General Tips

### **View Logs**

**Raspberry Pi Script:**
```bash
# Real-time
sudo journalctl -u bee-monitor -f

# Last 50 lines
sudo journalctl -u bee-monitor -n 50

# Or log file
tail -f /home/pi/bee-monitor/bee_monitor.log
```

**Home Assistant:**
```
Settings → System → Logs
```

**ESP32:**
```bash
# ESPHome logs
esphome logs bee-hive-monitor.yaml
```

### **Restart Components**

**Raspberry Pi Script:**
```bash
sudo systemctl restart bee-monitor
```

**ESP32:**
- Button in Home Assistant: `button.bee_hive_monitor_restart`
- Or: Unplug and replug power

**Home Assistant:**
```
Developer Tools → YAML → Restart
```

### **Verify Installation**

```bash
# Checklist
# ✅ ESP32 camera online?
# ✅ Raspberry Pi script running?
# ✅ Broodminder sensors updating?
# ✅ Health score calculated?
# ✅ Notifications working?
# ✅ Dashboard shows data?
```

---

## 📞 Getting Help

### **Before Asking for Help**

1. Check this troubleshooting guide
2. Check Home Assistant logs
3. Check Raspberry Pi logs
4. Test components individually

### **When Asking for Help**

Include:
- What you're trying to do
- What's happening instead
- Error messages (full text)
- Relevant logs
- Configuration files
- Component versions

### **Where to Get Help**

- **GitHub Issues**: [Repository Issues](https://github.com/yourusername/bee-brothel/issues)
- **GitHub Discussions**: [Repository Discussions](https://github.com/yourusername/bee-brothel/discussions)
- **Home Assistant Community**: [community.home-assistant.io](https://community.home-assistant.io)

---

**Still stuck? Open a GitHub issue with details!**
