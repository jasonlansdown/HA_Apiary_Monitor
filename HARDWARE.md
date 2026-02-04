# 🛒 Hardware Shopping List

Complete hardware requirements for The Bee Brothel monitoring system.


---

## 📦 Core Components (Required)

### **1. ESP32 Camera Module** - $15
**SEEED XIAO ESP32-S3 Sense**

**Buy:** 
- [Seeed Studio](https://www.seeedstudio.com/XIAO-ESP32S3-Sense-p-5639.html)
- [Amazon](https://amazon.com) (search: "XIAO ESP32-S3 Sense")

**Specifications:**
- ESP32-S3 chip (dual-core, 240MHz)
- 8MB PSRAM
- OV2640 camera (2MP)
- Built-in WiFi & Bluetooth
- USB-C connector

**Why This Model:**
- ✅ Integrated camera (no wiring)
- ✅ Small form factor (weatherproof friendly)
- ✅ Good image quality for motion detection
- ✅ Low power consumption (solar capable)
- ✅ ESPHome support

**Alternatives:**
- ESP32-CAM ($8) - Budget option, requires FTDI programmer
- M5Stack Camera Unit ($30) - Easier but more expensive

---

### **2. Raspberry Pi** - $35-75

**Buy:**
- [Official Distributors](https://www.raspberrypi.com/products/)
- [Amazon](https://amazon.com)
- [Adafruit](https://www.adafruit.com)

**Why Raspberry Pi:**
- ✅ Runs OpenCV efficiently
- ✅ Can run 24/7
- ✅ Network connectivity (Ethernet preferred)
- ✅ Easy Python development

**Don't Forget:**
- microSD card (32GB+, Class 10) - $10
- Official power supply (5V 2.5A) - $8
- Case (optional but recommended) - $5

**Total Pi Cost:** ~$50-75

---

### **3. Broodminder Sensors** - $150-200

**Required Sensors:**

**A. Broodminder-T2** (Temperature)
- **Cost:** $40-50 each
- **Quantity:** 1-2 (recommend 2 for better monitoring)
- **Measures:** Internal hive temperature
- **Battery Life:** 1-2 years (CR2032)
- **Buy:** [broodminder.com](https://broodminder.com)

**B. Broodminder-W3** (Scale)
- **Cost:** $150-170
- **Quantity:** 1
- **Measures:** 
  - Hive weight
  - External temperature
  - Humidity
- **Battery Life:** 1-2 years (2x AA)
- **Buy:** [broodminder.com](https://broodminder.com)

**Broodminder Total:** $190-220

**Why Broodminder:**
- ✅ Professional beekeeping sensors
- ✅ Weather-resistant
- ✅ Bluetooth + Cloud sync
- ✅ Proven reliability
- ✅ Home Assistant integration

**Alternatives:**
- I tried to make this simpler, and less DIY, if anyone is interested in the homemade scale and temperature probes please let me know. This requires other know-how whereas I was aiming to make this instructional more off-the-shelf.

---

### **5. Weatherproofing** - $20-30

**For ESP32 Camera:**
- IP65+ enclosure (clear front) - $15
- Examples:
  - [Hammond 1554 Series](https://www.hammfg.com)
  - [Amazon generic waterproof boxes](https://amazon.com)
- Cable glands / rubber grommets - $5
- Silicone sealant - $5

**For Broodminder Sensors:**
- Already weatherproof! ✅

---

## 🔌 Complete Shopping List

### **Minimum System**
```
☐ SEEED XIAO ESP32-S3 Sense      $15
☐ Raspberry Pi 3B+                $35
☐ microSD card (32GB)             $10
☐ Pi power supply                 $8
☐ Broodminder-T2 (x1)            $45
☐ Broodminder-W3                 $150
☐ USB-C cable                    $8
☐ USB power adapter              $8
☐ Weatherproof enclosure         $15
☐ Misc (sealant, glands, etc.)  $10
                        Total: ~$304
```

### **Recommended System**
```
☐ SEEED XIAO ESP32-S3 Sense      $15
☐ Raspberry Pi 4 (4GB)           $55
☐ microSD card (64GB)            $15
☐ Pi case                        $5
☐ Broodminder-T2 (x2)            $90
☐ Broodminder-W3                 $150
☐ USB-C cable                    $8
☐ USB power adapter              $8
☐ Weatherproof enclosure         $20
☐ Ethernet cable                 $5
☐ Misc (sealant, glands, etc.)  $15
                        Total: ~$386
```

### **Better Camera Quality** - $30-50

**Upgrade Options:**

1. **AI Thinker ESP32-CAM with OV5640** - $35
   - 5MP resolution
   - Better low-light performance
   - Requires programming adapter

2. **M5Stack Timer Camera** - $50
   - Built-in battery
   - Time-lapse features
   - Easier setup

---

## 🌡️ Environmental Considerations

### **Temperature Range**

**ESP32-S3:**
- Operating: -40°C to +85°C (-40°F to +185°F)
- Storage: -40°C to +125°C (-40°F to +257°F)
- ✅ Handles all weather conditions

**Raspberry Pi:**
- Operating: 0°C to 50°C (32°F to 122°F)
- 💡 Keep indoors in extreme climates

**Broodminder Sensors:**
- Designed for outdoor beehive use
- ✅ Weather-resistant by design

---


**Ready to order? See [INSTALL.md](INSTALL.md) for setup instructions!**
