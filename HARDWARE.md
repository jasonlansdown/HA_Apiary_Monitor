# 🛒 Hardware Shopping List

Complete hardware requirements for The Bee Brothel monitoring system.

---

## 💰 Budget Overview

| Category | Cost Range |
|----------|------------|
| **Core Components** | $200-250 |
| **Optional Upgrades** | $50-100 |
| **Total System** | **$250-350** |

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

**Recommended Models:**
- **Best:** Raspberry Pi 4 (4GB) - $55
- **Good:** Raspberry Pi 3B+ - $35
- **Works:** Raspberry Pi 3B - $35

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
- HiveTool scale ($100+) - DIY, complex setup
- DHT22 sensors ($5) - Much less accurate
- Load cells + HX711 ($15) - DIY scale, calibration needed

---

### **4. Power & Connectivity** - $20-30

**ESP32 Power:**
- USB-C cable (6ft+) - $8
- USB power adapter (5V 2A) - $8
- **Or:** USB battery bank for testing

**Raspberry Pi Power:**
- Official power supply (included if buying new)
- **Or:** Any quality 5V 2.5A+ USB power supply

**Networking:**
- **Best:** Ethernet cable for Pi ($5)
- **Alternative:** WiFi (built into Pi 3B+/4)

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

### **Minimum System - $250**
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

### **Recommended System - $350**
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

---

## ⚡ Optional Upgrades

### **Solar Power (Remote Apiaries)** - $60-100

**For ESP32 Camera:**
- 5W solar panel - $15
- 18650 battery holder + batteries - $25
- Solar charge controller - $10
- Weatherproof battery enclosure - $10
- **Total:** ~$60

**Components:**
- [Voltaic 6W Solar Panel](https://voltaicsystems.com)
- 18650 Li-ion batteries (2x 3.7V)
- TP4056 charge controller
- Battery protection board (BMS)

**Why Solar:**
- ✅ No power outlet needed
- ✅ Remote apiary monitoring
- ✅ Environmentally friendly
- ✅ Continuous operation

**Power Consumption:**
- ESP32-S3: ~500mA active, 10mA idle
- 5W panel sufficient for 24/7 operation
- Battery backup for cloudy days

---

### **Improved WiFi Range** - $30-50

**Options:**
1. **WiFi Extender** - $30
   - Extends range to apiary
   - Place between router and hive

2. **Directional Antenna** - $20
   - For Raspberry Pi
   - Significantly improves range

3. **Long-Range WiFi Bridge** - $60+
   - For very remote locations
   - Point-to-point WiFi link

---

### **Multiple Hives** - $180/hive

**Per Additional Hive:**
- ESP32-S3 camera - $15
- Broodminder-T2 - $45
- Broodminder-W3 - $150
- Weatherproof enclosure - $15
- Misc hardware - $10

**Use Same:**
- Raspberry Pi (handles multiple cameras)
- Home Assistant server
- Power supply (if nearby)

**System Capacity:**
- 1x Raspberry Pi 4: 2-3 hives comfortably
- Network bandwidth is limiting factor

---

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

**When to Upgrade:**
- If doing AI bee counting
- If recording time-lapses
- If camera too far from hive

---

## 🛠️ Tools Needed

**For Assembly:**
- Screwdriver set
- Drill (for mounting camera)
- Utility knife (enclosure modifications)
- Measuring tape
- Level (for camera positioning)

**For Installation:**
- Laptop/computer (initial setup)
- Smartphone (Broodminder sync)
- USB cable (ESP32 programming)

**Optional:**
- Multimeter (troubleshooting)
- WiFi analyzer app
- Soldering iron (modifications)

---

## 📏 Mounting Hardware

**ESP32 Camera:**
- Adjustable camera mount - $10
- Or: DIY mount with PVC pipe
- Stainless steel screws
- Weatherproof tape

**Broodminder Sensors:**
- No mounting needed!
- Place in hive per instructions
- Secure with velcro (optional)

**Raspberry Pi:**
- Place indoors (preferred)
- Or: Weatherproof outdoor enclosure - $30

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

## 🔋 Power Consumption

### **Power Requirements**

| Component | Idle | Active | Daily Average |
|-----------|------|--------|---------------|
| ESP32-S3 | 10mA | 500mA | ~100mAh |
| Raspberry Pi 3B+ | 200mA | 500mA | ~300mAh |
| Raspberry Pi 4 | 300mA | 700mA | ~400mAh |
| Broodminder-T2 | <1mA | - | Lasts 1-2 years |
| Broodminder-W3 | <1mA | - | Lasts 1-2 years |

### **Total System Power**

**Wired Setup:**
- ESP32 + Pi 3B+: ~5W continuous
- Cost: ~$0.10/day @ $0.12/kWh
- ~$3/month electricity

**Solar Setup:**
- 5W panel sufficient
- 2x 18650 batteries (6000mAh) for backup
- 2-3 days backup in bad weather

---

## 🌐 Network Requirements

**Minimum:**
- WiFi 2.4GHz (ESP32 and most Pi)
- Signal: >-75 dBm at camera location
- Bandwidth: 2-5 Mbps (camera stream)

**Recommended:**
- WiFi: >-65 dBm signal strength
- Ethernet for Raspberry Pi
- Static IP addresses for devices
- QoS prioritization (optional)

---

## ✅ Pre-Purchase Checklist

### **Before Ordering:**
- [ ] Measure WiFi signal strength at hive location
- [ ] Verify power outlet available (or plan solar)
- [ ] Check Home Assistant server ready
- [ ] Confirm Broodminder compatible with region
- [ ] Plan camera mounting location
- [ ] Verify Raspberry Pi SD card reader available

### **First-Time Builders:**
Consider buying:
- [ ] Raspberry Pi kit (includes SD card, power, case)
- [ ] USB microSD card reader (programming)
- [ ] Extra USB cables (troubleshooting)
- [ ] Weatherproof test enclosure (before final)

---

## 🏪 Recommended Vendors

### **Electronics:**
- **Adafruit** - Raspberry Pi, accessories
- **Seeed Studio** - ESP32 modules
- **Amazon** - General electronics, cases
- **DigiKey / Mouser** - Components

### **Beekeeping:**
- **Broodminder** - broodminder.com (official)
- **Mann Lake** - Beekeeping supplies
- **Dadant** - Beekeeping supplies

### **Solar:**
- **Voltaic Systems** - Quality solar panels
- **Amazon** - Generic solar kits

---

## 💡 Money-Saving Tips

1. **Start Small:**
   - Begin with 1 temperature sensor
   - Add weight sensor later

2. **Use Existing Hardware:**
   - Old Raspberry Pi 3 works fine
   - Old USB power supplies often work

3. **DIY Weatherproofing:**
   - Tupperware + silicone = cheap enclosure
   - Won't win beauty contests but works

4. **Watch for Sales:**
   - Black Friday / Cyber Monday
   - Raspberry Pi kits often discounted
   - Broodminder occasional sales

5. **Buy Generic:**
   - USB cables don't need to be fancy
   - Any 5V 2A adapter works for ESP32

---

## 📸 Before You Buy

**Recommended Testing Order:**
1. Buy ESP32 + Raspberry Pi first
2. Test basic camera + motion detection
3. If working well, order Broodminder sensors
4. Add weatherproofing last

**Why This Order:**
- Verify WiFi coverage works
- Test system indoors first
- Don't waste money if location doesn't work

---

## 📦 Shipping & Lead Times

**Typical Lead Times:**
- **Amazon/Local:** 2-5 days
- **Adafruit/Seeed:** 5-10 days (US)
- **Broodminder:** 5-7 days (usually in stock)
- **International:** 2-4 weeks

**Plan Ahead:**
- Order 2-3 weeks before spring
- Winter is ideal for indoor testing
- Broodminder occasionally out of stock

---

**Ready to order? See [INSTALL.md](INSTALL.md) for setup instructions!**
