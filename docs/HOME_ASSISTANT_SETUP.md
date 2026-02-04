# 🏠 Home Assistant Configuration

Complete Home Assistant configuration for The Bee Brothel monitoring system.

---

## 📋 File Structure

```
/config/
├── configuration.yaml       # Main configuration
├── automations.yaml        # Alert automations
├── scripts.yaml           # Helper scripts  
└── lovelace/
    └── apiary.yaml        # Dashboard configuration
```

---

## 🔧 configuration.yaml

### **Step 1: Add Customizations**

Add to `homeassistant:` section:

```yaml
homeassistant:
  customize:
    # Fix state_class for Python script sensors
    sensor.bee_hive_monitor_activity_score:
      state_class: measurement
      unit_of_measurement: '%'
      device_class: none
      icon: mdi:bee
    
    sensor.bee_hive_monitor_estimated_bees_per_minute:
      state_class: measurement
      unit_of_measurement: bees/min
      device_class: none
      icon: mdi:bee
```

### **Step 2: Add Input Helpers**

```yaml
input_number:
  # Weight tracking
  bee_hive_weight_snapshot:
    name: "Bee Hive Weight Snapshot"
    min: 0
    max: 200
    step: 0.001
    unit_of_measurement: "kg"
    mode: box

  # Temperature alert thresholds
  bee_hive_temp_high_threshold:
    name: "Bee Hive High Temp Threshold"
    min: 90
    max: 115
    step: 1
    initial: 100
    unit_of_measurement: "°F"
    icon: mdi:thermometer-high

  bee_hive_temp_low_threshold:
    name: "Bee Hive Low Temp Threshold"
    min: 50
    max: 90
    step: 1
    initial: 85
    unit_of_measurement: "°F"
    icon: mdi:thermometer-low
```

### **Step 3: Add Template Sensors**

```yaml
template:
  - sensor:
      # =====================================================================
      # DAILY WEIGHT CHANGE WITH COMPENSATION
      # =====================================================================
      - name: "Bee Hive Daily Weight Change"
        unique_id: bee_hive_daily_weight_change
        unit_of_measurement: "kg"
        state_class: measurement
        device_class: weight
        icon: mdi:trending-up
        state: >
          {% set current = states('sensor.beehive_weight_compensated') | float(0) %}
          {% set snapshot = states('input_number.bee_hive_weight_snapshot') | float(current) %}
          {{ (current - snapshot) | round(3) }}
        attributes:
          trend: >
            {% set change = states('sensor.bee_hive_daily_weight_change') | float(0) %}
            {% if change > 0.5 %}Strong Gain (Nectar Flow!)
            {% elif change > 0.1 %}Gaining
            {% elif change > -0.1 %}Stable
            {% elif change > -0.5 %}Losing
            {% else %}Strong Loss (Check for Robbing!){% endif %}

      # =====================================================================
      # TEMPERATURE-COMPENSATED WEIGHT
      # =====================================================================
      - name: "Beehive Weight Compensated"
        unique_id: beehive_weight_compensated
        unit_of_measurement: "kg"
        device_class: weight
        state_class: measurement
        icon: mdi:scale
        state: >
          {% set raw_weight = states('sensor.broodminder_w_57_41_5e_weight_realtime') | float(0) %}
          {% set temperature = states('sensor.broodminder_w_57_41_5e_temperature') | float(30) %}
          
          {# Temperature compensation: -0.0558 kg per °C #}
          {# Reference temperature: 30°C (86°F) #}
          {% set temp_offset = -0.0558 * (temperature - 30) %}
          {% set compensated = raw_weight - temp_offset %}
          
          {{ compensated | round(3) }}
        availability: >
          {{ states('sensor.broodminder_w_57_41_5e_weight_realtime') not in ['unavailable', 'unknown', 'none'] and
             states('sensor.broodminder_w_57_41_5e_temperature') not in ['unavailable', 'unknown', 'none'] }}
        attributes:
          raw_weight: "{{ states('sensor.broodminder_w_57_41_5e_weight_realtime') }}"
          temperature: "{{ states('sensor.broodminder_w_57_41_5e_temperature') }}"
          temperature_offset: >
            {% set temperature = states('sensor.broodminder_w_57_41_5e_temperature') | float(30) %}
            {{ (-0.0558 * (temperature - 30)) | round(3) }}
          compensation_active: true
          calibration_date: "2026-02-02"

      # =====================================================================
      # SEASONAL HEALTH SCORE (COLORADO CLIMATE)
      # =====================================================================
      - name: "Bee Hive Health Score"
        unique_id: bee_hive_health_score
        unit_of_measurement: "%"
        state_class: measurement
        icon: mdi:heart-pulse
        state: >
          {% set activity = states('sensor.bee_hive_monitor_activity_score') | float(0) %}
          {% set temp = states('sensor.broodminder_t_47_50_96_temperature') | float(0) %}
          {% set weight_change = states('sensor.bee_hive_daily_weight_change') | float(0) %}
          {% set humidity = states('sensor.broodminder_w_57_41_5e_humidity') | float(0) %}
          {% set external_temp = states('sensor.broodminder_w_57_41_5e_temperature') | float(0) %}
          
          {# Determine season based on external temperature #}
          {% set is_winter = external_temp <= 50 %}
          
          {# TEMPERATURE SCORE (0-30 points) #}
          {% if is_winter %}
            {% set temp_score = 30 if (temp >= 50 and temp <= 70) else (25 if (temp >= 40 and temp < 50) else (20 if (temp > 70 and temp <= 80) else (15 if (temp >= 30 and temp < 40) else (10 if (temp > 80 and temp <= 90) else 5)))) %}
          {% else %}
            {% set temp_score = 30 if (temp >= 93 and temp <= 95) else (25 if (temp >= 90 and temp <= 97) else (15 if (temp >= 85 and temp <= 100) else (10 if (temp >= 70 and temp < 85) else 5))) %}
          {% endif %}
          
          {# ACTIVITY SCORE (0-25 points) #}
          {% if is_winter %}
            {% set activity_score = 25 if (activity >= 10 and activity <= 30) else (20 if (activity >= 5 and activity < 10) else (20 if (activity > 30 and activity <= 50) else (15 if activity < 5 else (10 if activity > 50 else 5)))) %}
          {% else %}
            {% set activity_score = 25 if activity >= 60 else (20 if activity >= 40 else (15 if activity >= 20 else (10 if activity >= 10 else 5))) %}
          {% endif %}
          
          {# WEIGHT SCORE (0-25 points) #}
          {% if is_winter %}
            {% set weight_score = 25 if (weight_change >= -0.1 and weight_change <= 0.1) else (20 if (weight_change > -0.3 and weight_change < -0.1) else (20 if (weight_change > 0.1 and weight_change <= 0.3) else (15 if (weight_change > -0.5 and weight_change <= -0.3) else (10 if weight_change > 0.3 else 5)))) %}
          {% else %}
            {% set weight_score = 25 if weight_change > 0.5 else (20 if weight_change > 0.1 else (15 if weight_change > -0.1 else (10 if weight_change > -0.5 else 5))) %}
          {% endif %}
          
          {# HUMIDITY SCORE (0-20 points) - COLORADO DRY CLIMATE #}
          {% if is_winter %}
            {% set humidity_score = 20 if (humidity >= 20 and humidity <= 35) else (15 if (humidity >= 15 and humidity <= 45) else (10 if (humidity >= 10 and humidity <= 50) else 5)) %}
          {% else %}
            {% set humidity_score = 20 if (humidity >= 30 and humidity <= 40) else (15 if (humidity >= 20 and humidity <= 50) else (10 if (humidity >= 15 and humidity <= 60) else 5)) %}
          {% endif %}
          
          {{ (temp_score + activity_score + weight_score + humidity_score) | round(0) }}
        attributes:
          season_mode: >
            {% set external_temp = states('sensor.broodminder_w_57_41_5e_temperature') | float(0) %}
            {{ 'Winter' if external_temp <= 50 else 'Summer' }}
          temperature_score: >
            {% set temp = states('sensor.broodminder_t_47_50_96_temperature') | float(0) %}
            {% set external_temp = states('sensor.broodminder_w_57_41_5e_temperature') | float(0) %}
            {% set is_winter = external_temp <= 50 %}
            {% if is_winter %}
              {{ 30 if (temp >= 50 and temp <= 70) else (25 if (temp >= 40 and temp < 50) else (20 if (temp > 70 and temp <= 80) else (15 if (temp >= 30 and temp < 40) else (10 if (temp > 80 and temp <= 90) else 5)))) }}
            {% else %}
              {{ 30 if (temp >= 93 and temp <= 95) else (25 if (temp >= 90 and temp <= 97) else (15 if (temp >= 85 and temp <= 100) else (10 if (temp >= 70 and temp < 85) else 5))) }}
            {% endif %}
          activity_score: >
            {% set activity = states('sensor.bee_hive_monitor_activity_score') | float(0) %}
            {% set external_temp = states('sensor.broodminder_w_57_41_5e_temperature') | float(0) %}
            {% set is_winter = external_temp <= 50 %}
            {% if is_winter %}
              {{ 25 if (activity >= 10 and activity <= 30) else (20 if (activity >= 5 and activity < 10) else (20 if (activity > 30 and activity <= 50) else (15 if activity < 5 else (10 if activity > 50 else 5)))) }}
            {% else %}
              {{ 25 if activity >= 60 else (20 if activity >= 40 else (15 if activity >= 20 else (10 if activity >= 10 else 5))) }}
            {% endif %}
          weight_score: >
            {% set weight_change = states('sensor.bee_hive_daily_weight_change') | float(0) %}
            {% set external_temp = states('sensor.broodminder_w_57_41_5e_temperature') | float(0) %}
            {% set is_winter = external_temp <= 50 %}
            {% if is_winter %}
              {{ 25 if (weight_change >= -0.1 and weight_change <= 0.1) else (20 if (weight_change > -0.3 and weight_change < -0.1) else (20 if (weight_change > 0.1 and weight_change <= 0.3) else (15 if (weight_change > -0.5 and weight_change <= -0.3) else (10 if weight_change > 0.3 else 5)))) }}
            {% else %}
              {{ 25 if weight_change > 0.5 else (20 if weight_change > 0.1 else (15 if weight_change > -0.1 else (10 if weight_change > -0.5 else 5))) }}
            {% endif %}
          humidity_score: >
            {% set humidity = states('sensor.broodminder_w_57_41_5e_humidity') | float(0) %}
            {% set external_temp = states('sensor.broodminder_w_57_41_5e_temperature') | float(0) %}
            {% set is_winter = external_temp <= 50 %}
            {% if is_winter %}
              {{ 20 if (humidity >= 20 and humidity <= 35) else (15 if (humidity >= 15 and humidity <= 45) else (10 if (humidity >= 10 and humidity <= 50) else 5)) }}
            {% else %}
              {{ 20 if (humidity >= 30 and humidity <= 40) else (15 if (humidity >= 20 and humidity <= 50) else (10 if (humidity >= 15 and humidity <= 60) else 5)) }}
            {% endif %}
          health_status: >
            {% set score = states('sensor.bee_hive_health_score') | float(0) %}
            {% if score >= 85 %}Excellent - Hive thriving!
            {% elif score >= 70 %}Good - Normal conditions
            {% elif score >= 50 %}Fair - Monitor closely
            {% elif score >= 30 %}Poor - Intervention may be needed
            {% else %}Critical - Immediate attention required{% endif %}

      # =====================================================================
      # NECTAR FLOW STATUS
      # =====================================================================
      - name: "Bee Hive Nectar Flow Status"
        unique_id: bee_hive_nectar_flow
        icon: mdi:flower-pollen
        state: >
          {% set weight_change = states('sensor.bee_hive_daily_weight_change') | float(0) %}
          {% set activity = states('sensor.bee_hive_monitor_activity_score') | float(0) %}
          {% if weight_change > 0.5 and activity > 60 %}Strong Nectar Flow
          {% elif weight_change > 0.2 and activity > 40 %}Moderate Nectar Flow
          {% elif weight_change > 0 and activity > 20 %}Light Nectar Flow
          {% elif weight_change < -0.2 %}No Flow - Consuming Stores
          {% else %}Stable - No Significant Flow
          {% endif %}
        attributes:
          daily_gain_kg: "{{ states('sensor.bee_hive_daily_weight_change') }}"
          daily_gain_lbs: "{{ (states('sensor.bee_hive_daily_weight_change') | float(0) * 2.20462) | round(2) }}"

      # =====================================================================
      # QUEEN HEALTH INDICATOR
      # =====================================================================
      - name: "Bee Hive Queen Health Indicator"
        unique_id: bee_hive_queen_health
        icon: mdi:crown
        state: >
          {% set temp = states('sensor.broodminder_t_47_50_96_temperature') | float(0) %}
          {% set activity = states('sensor.bee_hive_monitor_activity_score') | float(0) %}
          {% set weight_change = states('sensor.bee_hive_daily_weight_change') | float(0) %}
          {% set external_temp = states('sensor.broodminder_w_57_41_5e_temperature') | float(0) %}
          {% if temp >= 85 and temp <= 95 and activity < 20 and weight_change < 0.1 and external_temp > 60 %}
            Possible Queen Issue - Low activity with good conditions
          {% elif temp >= 90 and activity > 40 and weight_change > 0 %}
            Healthy - Good brood temp, activity, and foraging
          {% elif temp < 85 and external_temp < 50 %}
            Winter Mode - Normal low activity
          {% elif activity > 30 %}
            Normal - Active foraging
          {% else %}
            Monitor - Activity lower than expected
          {% endif %}

  # ===========================================================================
  # BINARY SENSORS
  # ===========================================================================
  - binary_sensor:
      - name: "Bee Hive Temperature Alert"
        unique_id: bee_hive_temp_alert
        device_class: problem
        state: >
          {% set temp = states('sensor.broodminder_t_47_50_96_temperature') | float(0) %}
          {% set high = states('input_number.bee_hive_temp_high_threshold') | float(100) %}
          {% set low = states('input_number.bee_hive_temp_low_threshold') | float(85) %}
          {{ temp > high or (temp < low and temp > 0) }}

      - name: "Bee Hive Nectar Flow Active"
        unique_id: bee_hive_nectar_flow_active
        device_class: running
        icon: mdi:flower-pollen
        state: >
          {% set weight_change = states('sensor.bee_hive_daily_weight_change') | float(0) %}
          {% set activity = states('sensor.bee_hive_monitor_activity_score') | float(0) %}
          {{ weight_change > 0.2 and activity > 40 }}

      - name: "Bee Hive Critical Health Alert"
        unique_id: bee_hive_critical_alert
        device_class: problem
        state: "{{ states('sensor.bee_hive_health_score') | float(100) < 30 }}"

      - name: "Bee Hive Robbing Detected"
        unique_id: bee_hive_robbing_detected
        device_class: problem
        state: >
          {% set weight_change = states('sensor.bee_hive_daily_weight_change') | float(0) %}
          {% set activity = states('sensor.bee_hive_monitor_activity_score') | float(0) %}
          {{ (weight_change < -0.5 and activity > 70) or (weight_change < -0.3 and activity > 50) }}

# =============================================================================
# STATISTICS SENSORS
# =============================================================================
sensor:
  # Activity averages
  - platform: statistics
    name: "Bee Hive Activity (1h avg)"
    entity_id: sensor.bee_hive_monitor_activity_score
    state_characteristic: mean
    max_age:
      hours: 1
    sampling_size: 200

  - platform: statistics
    name: "Bee Hive Activity (24h avg)"
    entity_id: sensor.bee_hive_monitor_activity_score
    state_characteristic: mean
    max_age:
      hours: 24
    sampling_size: 1000

  - platform: statistics
    name: "Bee Hive Peak Activity Today"
    entity_id: sensor.bee_hive_monitor_activity_score
    state_characteristic: value_max
    max_age:
      hours: 24

  # Weight averages
  - platform: statistics
    name: "Bee Hive Weight (24h avg)"
    entity_id: sensor.beehive_weight_compensated
    state_characteristic: mean
    max_age:
      hours: 24
    sampling_size: 1000

  - platform: statistics
    name: "Bee Hive Weight (7d avg)"
    entity_id: sensor.beehive_weight_compensated
    state_characteristic: mean
    max_age:
      days: 7
    sampling_size: 2000

  # Health score average
  - platform: statistics
    name: "Bee Hive Health Score (24h avg)"
    entity_id: sensor.bee_hive_health_score
    state_characteristic: mean
    max_age:
      hours: 24
    sampling_size: 1000
```

---

## 🚨 automations.yaml

```yaml
# =============================================================================
# BEE HIVE AUTOMATIONS
# =============================================================================

- id: bee_hive_critical_health
  alias: Bee Hive - Critical Health Alert
  mode: single
  triggers:
  - trigger: numeric_state
    entity_id: sensor.bee_hive_health_score
    below: 30
    for:
      minutes: 15
  actions:
  - action: notify.notify
    data:
      title: "🚨 HIVE HEALTH CRITICAL"
      message: "Bee Brothel health score is {{ states('sensor.bee_hive_health_score') }}%"

- id: bee_hive_robbing_detected
  alias: Bee Hive - Robbing Detection
  mode: single
  triggers:
  - trigger: state
    entity_id: binary_sensor.bee_hive_robbing_detected
    to: 'on'
    for:
      minutes: 5
  actions:
  - action: notify.notify
    data:
      title: "🚨 ROBBING DETECTED"
      message: "Possible robbing! Activity: {{ states('sensor.bee_hive_monitor_activity_score') }}%"

- id: bee_hive_temperature_alert
  alias: Bee Hive - Temperature Alert
  mode: single
  triggers:
  - trigger: state
    entity_id: binary_sensor.bee_hive_temperature_alert
    to: 'on'
    for:
      minutes: 30
  actions:
  - action: notify.notify
    data:
      title: "🌡️ Hive Temperature Alert"
      message: "{{ state_attr('binary_sensor.bee_hive_temperature_alert', 'reason') }}"

- id: bee_hive_nectar_flow_started
  alias: Bee Hive - Nectar Flow Started
  mode: single
  triggers:
  - trigger: state
    entity_id: binary_sensor.bee_hive_nectar_flow_active
    to: 'on'
    for:
      hours: 2
  actions:
  - action: notify.notify
    data:
      title: "🌸 Nectar Flow Started!"
      message: "Bee Brothel is bringing in nectar!"

- id: bee_hive_daily_report
  alias: Bee Hive - Daily Summary Report
  mode: single
  triggers:
  - trigger: time
    at: '20:00:00'
  actions:
  - action: notify.notify
    data:
      title: "📊 Bee Brothel Daily Report"
      message: |
        Health: {{ states('sensor.bee_hive_health_score') }}%
        Activity: {{ states('sensor.bee_hive_monitor_activity_score') }}%
        Weight Change: {{ states('sensor.bee_hive_daily_weight_change') }} kg

- id: bee_hive_low_activity_warning
  alias: Bee Hive - Low Activity Warning
  mode: single
  triggers:
  - trigger: numeric_state
    entity_id: sensor.bee_hive_monitor_activity_score
    below: 15
    for:
      hours: 4
  conditions:
  - condition: numeric_state
    entity_id: sensor.broodminder_w_57_41_5e_temperature
    above: 65
  - condition: time
    after: '09:00:00'
    before: '18:00:00'
  actions:
  - action: notify.notify
    data:
      title: "⚠️ Low Hive Activity"
      message: "Low activity during warm weather"

- id: bee_hive_weight_snapshot
  alias: Bee Hive - Daily Weight Snapshot
  triggers:
  - trigger: time
    at: '00:00:00'
  actions:
  - action: input_number.set_value
    target:
      entity_id: input_number.bee_hive_weight_snapshot
    data:
      value: '{{ states(''sensor.beehive_weight_compensated'') | float(0) }}'

- id: bee_hive_battery_low
  alias: Bee Hive - Sensor Battery Low
  mode: parallel
  triggers:
  - trigger: numeric_state
    entity_id:
    - sensor.broodminder_t_47_50_96_battery
    - sensor.broodminder_w_57_41_5e_battery
    below: 20
  actions:
  - action: notify.notify
    data:
      title: "🔋 Bee Sensor Battery Low"
      message: "{{ trigger.to_state.attributes.friendly_name }} is at {{ trigger.to_state.state }}%"

- id: bee_hive_camera_offline
  alias: Bee Hive - Camera Offline
  mode: single
  triggers:
  - trigger: state
    entity_id: binary_sensor.bee_hive_monitor_status
    to: 'off'
    for:
      minutes: 10
  actions:
  - action: notify.notify
    data:
      title: "📷 Bee Camera Offline"
      message: "Bee hive camera has been offline for 10 minutes"
```

---

## 🎨 Dashboard

See [`dashboard.yaml`](dashboard.yaml) in repository for complete configuration.

**Quick Install:**
1. Settings → Dashboards → + Add Dashboard
2. Name: "Apiary"
3. ⋮ → Raw Configuration Editor
4. Paste contents from `dashboard.yaml`
5. Save

---

## ✅ Verification

### **Check All Sensors**

**Developer Tools → States**, verify these exist:
- `sensor.bee_hive_monitor_activity_score`
- `sensor.bee_hive_monitor_estimated_bees_per_minute`
- `sensor.bee_hive_health_score`
- `sensor.beehive_weight_compensated`
- `sensor.bee_hive_daily_weight_change`
- `binary_sensor.bee_hive_critical_health_alert`
- `binary_sensor.bee_hive_robbing_detected`

### **Test Template Syntax**

**Developer Tools → Template**:
```jinja2
{{ states('sensor.bee_hive_health_score') }}
{{ state_attr('sensor.bee_hive_health_score', 'season_mode') }}
{{ state_attr('sensor.bee_hive_health_score', 'temperature_score') }}
```

Should return numbers, not "unknown".

---

## 🔧 Customization

### **Change Seasonal Threshold**

Default: 50°F switches between winter/summer

```yaml
# In template sensors, change this line:
{% set is_winter = external_temp <= 50 %}

# To (example for warmer climate):
{% set is_winter = external_temp <= 40 %}
```

### **Adjust Humidity Ranges**

For **humid climates** (Eastern US, Europe):

```yaml
# Winter mode
{% set humidity_score = 20 if (humidity >= 40 and humidity <= 60) else ... %}

# Summer mode
{% set humidity_score = 20 if (humidity >= 50 and humidity <= 70) else ... %}
```

### **Notification Timing**

Change daily report time:

```yaml
# In bee_hive_daily_report automation
triggers:
- trigger: time
  at: '20:00:00'  # Change to desired time
```

---

## 📱 WhatsApp Notifications (Optional)

### **Install GreenAPI Integration**

```yaml
# configuration.yaml
notify:
  - platform: greenapi
    name: greenapi
    instance_id: !secret greenapi_instance_id
    token: !secret greenapi_token

# secrets.yaml
greenapi_instance_id: "YOUR_INSTANCE_ID"
greenapi_token: "YOUR_TOKEN"
```

### **Update Automations**

Replace:
```yaml
action: notify.notify
```

With:
```yaml
action: notify.greenapi
data:
  target: "120363389941644540@g.us"  # Your WhatsApp group ID
  message: "{{ title }}: {{ message }}"
```

---

## 🐛 Troubleshooting

### **Health Score Shows "Unknown"**

**Cause**: Missing dependencies

**Fix**:
1. Check all Broodminder sensors are available
2. Verify `sensor.bee_hive_monitor_activity_score` exists
3. Check `sensor.bee_hive_daily_weight_change` is not "unknown"

### **Weight Compensation Not Working**

**Cause**: Sensor names don't match

**Fix**: Update sensor entity IDs in template to match your Broodminder sensors:
```yaml
# Find your actual entity IDs in Developer Tools → States
# Replace everywhere:
sensor.broodminder_w_57_41_5e_weight_realtime
sensor.broodminder_w_57_41_5e_temperature
```

### **Automations Not Triggering**

**Check**:
1. Automations enabled? (Settings → Automations)
2. Correct entity IDs?
3. Check traces (Settings → Automations → Select automation → Traces)

---

**Next**: [Dashboard Setup](DASHBOARD.md)
