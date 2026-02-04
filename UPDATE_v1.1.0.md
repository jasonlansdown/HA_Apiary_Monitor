# 🔄 v1.1.0 Update Guide - Calendar-Based Seasonal Switching

**Release Date**: February 4, 2025  
**Breaking Change**: Seasonal mode determination logic updated

---

## 📋 **What Changed**

### **v1.0.0 (Temperature-Based)**
- ❌ Winter mode when external temp ≤ 50°F
- ❌ Summer mode when external temp > 50°F
- **Problem**: Daily flip-flopping in spring/fall, health scores bouncing

### **v1.1.0 (Calendar-Based)**
- ✅ **Winter mode**: November 1 - March 31
- ✅ **Summer mode**: April 1 - October 31
- **Benefits**: 
  - Stable, predictable health scoring
  - Matches bee biological cycles
  - Aligns with beekeeping season management
  - No more daily mode switching
  - **Temperature alerts now seasonal** (40-80°F winter, 85-100°F summer)

---

## 🎯 **Why This Change?**

### **Problems with Temperature-Based:**
1. **Daily Flip-Flopping**: Spring/fall temperatures oscillate around 50°F causing mode switching every day
2. **Doesn't Match Biology**: Bees respond to day length (photoperiod), not just temperature
3. **User Confusion**: "Why did my health score change so much?"

### **Benefits of Calendar-Based:**
1. **Predictable**: Users know exactly when modes switch
2. **Stable Scoring**: No more daily health score variations from mode changes
3. **Biological Accuracy**: Matches seasonal bee behavior patterns
4. **Beekeeping Alignment**: Follows traditional beekeeping seasons
5. **Sensible Alerts**: Temperature alerts match seasonal expectations (no winter "too cold" alerts at 60°F)

---

## 🔧 **How to Update**

### **Option 1: Fresh Install (Recommended)**

If you haven't deployed yet or want a clean slate:

```bash
# 1. Pull latest from GitHub
cd ~/HA_Apiary_Monitor
git pull origin main

# 2. Copy updated configuration
cp config/home-assistant/configuration.yaml /path/to/your/config/

# 3. Update sensor entity IDs (YOUR_SENSOR_IDS)
nano /path/to/your/config/configuration.yaml

# 4. Check configuration in Home Assistant
# Developer Tools → YAML → Check Configuration

# 5. Restart Home Assistant
# Developer Tools → YAML → Restart
```

---

### **Option 2: Manual Update (For Existing Installations)**

If you're already running v1.0.0, follow these steps:

#### **Step 1: Backup Current Config**

```bash
# Backup your configuration
cp /config/configuration.yaml /config/configuration.yaml.v1.0.0.backup
```

#### **Step 2: Update Health Score Sensor**

Open `/config/configuration.yaml` and find the "Bee Hive Health Score" sensor.

**Replace this line:**
```yaml
{% set external_temp = states('sensor.broodminder_w_XXXXX_temperature') | float(0) %}

{# Determine season based on external temperature #}
{% set is_winter = external_temp <= 50 %}
```

**With:**
```yaml
{# Determine season based on calendar month #}
{# Winter: November (11), December (12), January (1), February (2), March (3) #}
{# Summer: April (4) through October (10) #}
{% set month = now().month %}
{% set is_winter = month in [11, 12, 1, 2, 3] %}
```

#### **Step 3: Update Sensor Attributes**

Find the `attributes:` section of the health score sensor and update:

**OLD `season_mode` attribute:**
```yaml
season_mode: >
  {% set external_temp = states('sensor.broodminder_w_XXXXX_temperature') | float(0) %}
  {{ 'Winter' if external_temp <= 50 else 'Summer' }}
```

**NEW `season_mode` attribute:**
```yaml
season_mode: >
  {% set month = now().month %}
  {{ 'Winter' if month in [11, 12, 1, 2, 3] else 'Summer' }}
current_month: >
  {{ now().strftime('%B') }}
```

**Update `scoring_explanation` attribute:**

**OLD:**
```yaml
scoring_explanation: >
  {% set external_temp = states('sensor.broodminder_w_XXXXX_temperature') | float(0) %}
  {{ 'Winter mode active: ...' if external_temp <= 50 else 'Summer mode active: ...' }}
```

**NEW:**
```yaml
scoring_explanation: >
  {% set month = now().month %}
  {% set is_winter = month in [11, 12, 1, 2, 3] %}
  {{ 'Winter mode active (Nov-Mar): ...' if is_winter else 'Summer mode active (Apr-Oct): ...' }}
```

**Update all score breakdowns** (temperature_score, activity_score, weight_score, humidity_score):

**Replace:**
```yaml
{% set external_temp = states('sensor.broodminder_w_XXXXX_temperature') | float(0) %}
{% set is_winter = external_temp <= 50 %}
```

**With:**
```yaml
{% set month = now().month %}
{% set is_winter = month in [11, 12, 1, 2, 3] %}
```

#### **Step 4: Update Queen Health Indicator**

Find the "Bee Hive Queen Health Indicator" sensor and replace:

**OLD:**
```yaml
{% elif temp < 85 and external_temp < 50 %}
  Winter Mode - Normal low activity
```

**NEW:**
```yaml
{% set month = now().month %}
{% set is_winter = month in [11, 12, 1, 2, 3] %}
{% elif temp < 85 and is_winter %}
  Winter Mode - Normal low activity
```

#### **Step 5: Update Temperature Alert Sensor** (NEW in v1.1.0)

Find the "Bee Hive Temperature Alert" binary sensor and replace the entire sensor:

**OLD:**
```yaml
- name: "Bee Hive Temperature Alert"
  unique_id: bee_hive_temp_alert
  device_class: problem
  state: >
    {% set temp = states('sensor.broodminder_t_XXXXX_temperature') | float(0) %}
    {% set high = states('input_number.bee_hive_temp_high_threshold') | float(100) %}
    {% set low = states('input_number.bee_hive_temp_low_threshold') | float(85) %}
    {{ temp > high or (temp < low and temp > 0) }}
```

**NEW:**
```yaml
- name: "Bee Hive Temperature Alert"
  unique_id: bee_hive_temp_alert
  device_class: problem
  state: >
    {% set temp = states('sensor.broodminder_t_XXXXX_temperature') | float(0) %}
    {% set month = now().month %}
    {% set is_winter = month in [11, 12, 1, 2, 3] %}
    
    {# Seasonal thresholds #}
    {% if is_winter %}
      {# Winter: Alert if below 40°F or above 80°F #}
      {% set too_cold = temp < 40 and temp > 0 %}
      {% set too_hot = temp > 80 %}
    {% else %}
      {# Summer: Alert if below 85°F or above 100°F #}
      {% set too_cold = temp < 85 and temp > 0 %}
      {% set too_hot = temp > 100 %}
    {% endif %}
    
    {{ too_cold or too_hot }}
  attributes:
    reason: >
      {% set temp = states('sensor.broodminder_t_XXXXX_temperature') | float(0) %}
      {% set month = now().month %}
      {% set is_winter = month in [11, 12, 1, 2, 3] %}
      
      {% if is_winter %}
        {% if temp > 80 %}
          Winter - Hive too warm ({{ temp | round(1) }}°F)
        {% elif temp < 40 and temp > 0 %}
          Winter - Hive very cold ({{ temp | round(1) }}°F)
        {% else %}
          Normal winter temperature ({{ temp | round(1) }}°F)
        {% endif %}
      {% else %}
        {% if temp > 100 %}
          Summer - Hive too hot ({{ temp | round(1) }}°F)
        {% elif temp < 85 and temp > 0 %}
          Summer - Hive too cold ({{ temp | round(1) }}°F)
        {% else %}
          Normal summer temperature ({{ temp | round(1) }}°F)
        {% endif %}
      {% endif %}
    season_mode: >
      {% set month = now().month %}
      {{ 'Winter' if month in [11, 12, 1, 2, 3] else 'Summer' }}
    winter_low_threshold: "40°F"
    winter_high_threshold: "80°F"
    summer_low_threshold: "85°F"
    summer_high_threshold: "100°F"
```

**Note:** The `input_number` helpers for temperature thresholds (`bee_hive_temp_high_threshold`, `bee_hive_temp_low_threshold`) are now optional and can be removed if desired.

#### **Step 6: Validate & Restart**

```bash
# Check configuration
# Home Assistant → Developer Tools → YAML → Check Configuration

# If no errors, restart
# Developer Tools → YAML → Restart
```

---

## ✅ **Verification**

After updating, verify the changes:

### **1. Check Season Mode**

```yaml
# Developer Tools → States
# Find: sensor.bee_hive_health_score
# Check attributes:
#   - season_mode: Should show "Winter" (Nov-Mar) or "Summer" (Apr-Oct)
#   - current_month: Should show current month name
```

### **2. Verify Health Score Stability**

Monitor health score for 24 hours:
- ✅ Should remain stable (no mode switching)
- ✅ Score changes only reflect actual hive conditions
- ✅ Scoring explanation shows calendar-based dates

### **3. Check Temperature Alerts**

```yaml
# Developer Tools → States
# Find: binary_sensor.bee_hive_temperature_alert
# Check attributes:
#   - season_mode: Should show "Winter" or "Summer"
#   - winter_low_threshold: "40°F"
#   - winter_high_threshold: "80°F"
#   - summer_low_threshold: "85°F"
#   - summer_high_threshold: "100°F"
```

Verify alerts match season:
- ✅ Winter: No alerts for temps 40-80°F
- ✅ Summer: No alerts for temps 85-100°F

### **4. Test Automation Triggers**

Ensure automations still work:
- Critical health alerts
- Robbing detection
- Temperature warnings

---

## 🌍 **Customizing for Your Location**

### **Northern Hemisphere (Default)**
- Winter: November 1 - March 31
- Summer: April 1 - October 31

**Perfect for:** USA, Canada, Europe, Northern Asia

### **Southern Hemisphere**

Change the month logic:

```yaml
{# Winter: May through September #}
{# Summer: October through April #}
{% set month = now().month %}
{% set is_winter = month in [5, 6, 7, 8, 9] %}
```

**Perfect for:** Australia, New Zealand, South America, Southern Africa

### **Adjusting Transition Dates**

If your spring/fall come earlier/later:

**Start winter 2 weeks earlier:**
```yaml
{# Winter: Mid-October through Mid-April #}
{% set month = now().month %}
{% set day = now().day %}
{% set is_winter = (month == 10 and day >= 15) or month in [11, 12, 1, 2, 3] or (month == 4 and day < 15) %}
```

**Start winter 2 weeks later:**
```yaml
{# Winter: Mid-November through Mid-March #}
{% set month = now().month %}
{% set day = now().day %}
{% set is_winter = (month == 11 and day >= 15) or month in [12, 1, 2] or (month == 3 and day < 15) %}
```

---

## 📊 **Expected Health Score Changes**

### **If Currently in Shoulder Season (Spring/Fall)**

**Before (v1.0.0):**
- Mode might switch daily based on temperature
- Health scores vary 10-20 points day-to-day

**After (v1.1.0):**
- Stable mode throughout the month
- Health scores reflect actual hive conditions
- More accurate trending

### **Example: Early April in Colorado**

**v1.0.0 (Temperature-Based):**
- April 1st: 48°F → Winter Mode → Score: 75%
- April 2nd: 55°F → Summer Mode → Score: 55% (drops because activity not summer levels)
- April 3rd: 49°F → Winter Mode → Score: 78%
- **User**: "Why is my score bouncing around?"

**v1.1.0 (Calendar-Based):**
- April 1st-30th: Summer Mode → Score: 60-65% (stable)
- Bees naturally ramping up activity
- Score gradually improves as weather warms
- **User**: "I can see the seasonal progression!"

---

## ⚠️ **Potential Issues & Solutions**

### **Issue 1: Health Score Dropped After Update**

**Cause**: You updated mid-season and calendar mode doesn't match current conditions.

**Example**: Updated in early April (now Summer mode) but bees still in winter behavior.

**Solution**: 
- Monitor for 1-2 weeks as bees transition
- Or temporarily adjust month ranges to delay mode switch
- Remember: Score will stabilize as season progresses

### **Issue 2: Configuration Check Fails**

**Cause**: Syntax error in template

**Solution**:
```bash
# Check Home Assistant logs
# Settings → System → Logs

# Look for template errors
# Fix any typos in the month logic
```

### **Issue 3: Season Mode Shows Wrong**

**Cause**: System time/timezone incorrect

**Solution**:
```bash
# Check system time in Home Assistant
# Settings → System → General → Time Zone
# Ensure it's set correctly for your location
```

---

## 🔄 **Reverting to v1.0.0 (If Needed)**

If you need to roll back:

```bash
# 1. Restore backup
cp /config/configuration.yaml.v1.0.0.backup /config/configuration.yaml

# 2. Restart Home Assistant
# Developer Tools → YAML → Restart

# 3. Report issues on GitHub
```

---

## 📝 **Additional Updates in v1.1.0**

- Updated README.md seasonal descriptions
- Updated INSTALL.md documentation
- Updated QUICKSTART.md guide
- All documentation now reflects calendar-based switching

---

## 💬 **Questions or Issues?**

- **GitHub Issues**: https://github.com/beebrothelman/HA_Apiary_Monitor/issues
- **GitHub Discussions**: https://github.com/beebrothelman/HA_Apiary_Monitor/discussions

---

## ⭐ **What's Next**

Future enhancements being considered:
- **v1.2.0**: Configurable season dates via UI
- **v1.3.0**: Automatic timezone/hemisphere detection
- **v2.0.0**: Multi-hive support with independent season configs

---

**Happy Beekeeping! 🐝**

*Updated: February 4, 2025*
