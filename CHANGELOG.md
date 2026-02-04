# Changelog

All notable changes to the HA Apiary Monitor project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2025-02-04

### 🔄 Changed

**BREAKING CHANGE: Seasonal switching now calendar-based instead of temperature-based**

#### **Seasonal Mode Logic**
- **Changed from**: External temperature ≤50°F = Winter, >50°F = Summer
- **Changed to**: Calendar dates determine season
  - **Winter Mode**: November 1 - March 31
  - **Summer Mode**: April 1 - October 31

**Why this change?**
- ✅ Eliminates daily mode flip-flopping in spring/fall
- ✅ Provides stable, predictable health scoring
- ✅ Matches bee biological cycles (photoperiod-based)
- ✅ Aligns with traditional beekeeping season management

#### **Updated Files**
- `config/home-assistant/configuration.yaml` - Health score sensor logic
- `README.md` - Seasonal intelligence descriptions
- `INSTALL.md` - Documentation references
- Added `UPDATE_v1.1.0.md` - Comprehensive migration guide

#### **Health Score Sensor Changes**
- Removed `external_temp` variable dependency
- Added calendar month check: `{% set month = now().month %}`
- Updated winter detection: `{% set is_winter = month in [11, 12, 1, 2, 3] %}`
- Added `current_month` attribute to show month name
- Updated `season_mode` attribute to use calendar
- Updated `scoring_explanation` to show calendar dates (Nov-Mar / Apr-Oct)
- Updated Queen Health Indicator to use calendar logic

#### **Temperature Alert Sensor Changes** (NEW)
- Replaced manual threshold input_numbers with seasonal logic
- **Winter thresholds**: Alert if <40°F or >80°F
- **Summer thresholds**: Alert if <85°F or >100°F
- Added `season_mode` attribute showing current season
- Added threshold attributes for transparency
- Temperature alerts now match seasonal health scoring expectations

### 📝 Documentation
- Added comprehensive migration guide (`UPDATE_v1.1.0.md`)
- Updated all seasonal descriptions across documentation
- Added Southern Hemisphere customization examples
- Added troubleshooting for mid-season updates

### ⚙️ Migration Required
Users running v1.0.0 must update their `configuration.yaml` to use the new calendar-based logic. See `UPDATE_v1.1.0.md` for detailed instructions.

---

## [1.0.0] - 2025-02-04

### 🎉 Initial Release

**The Bee Brothel - Complete Smart Hive Monitoring System**

A comprehensive, production-ready bee hive monitoring system using computer vision, environmental sensors, and Home Assistant automation.

### ✨ Features

#### **Real-Time Monitoring**
- Live ESP32-S3 camera feed (1600x1200 @ 5fps)
- Computer vision motion detection with bee counting
- Activity scoring (0-100%) with automatic classification
- Temperature-compensated weight tracking (-0.0558 kg/°C)
- Dual temperature probes (internal hive monitoring)
- Humidity monitoring (Colorado dry climate optimized)

#### **Intelligent Health Scoring** (100-point system)
- **Seasonal modes**: Automatic winter/summer adjustment (temperature-based in v1.0.0)
- **Temperature component** (30 points): Optimal ranges for brood/clustering
- **Activity component** (25 points): Motion detection analysis
- **Weight component** (25 points): Daily weight change tracking
- **Humidity component** (20 points): Dry climate calibration (20-40% optimal)
- **Health ratings**: Excellent (85-100%), Good (70-84%), Fair (50-69%), Poor (30-49%), Critical (0-29%)

#### **Temperature-Compensated Weight**
- Raw scale readings corrected for thermal expansion
- Coefficient: -0.0558 kg/°C (calibrated 2026-02-02)
- Reference temperature: 30°C (86°F)
- Accurate daily weight change calculations
- Nectar flow vs consumption tracking

#### **Smart Alerts** (11 automations)
- Critical health (<30% for 15 min)
- Robbing detection (high activity + weight loss)
- Temperature alerts (too hot/cold for 30 min)
- Nectar flow detection (weight gain + high activity for 2 hrs)
- Daily summary report (8 PM)
- Low activity warnings (4 hrs during warm weather)
- Daily weight snapshot (midnight)
- Battery low alerts (<20%)
- Camera offline detection (10 min)
- Excellent health celebration (>85% for 6 hrs)
- Significant weight loss (>0.5 kg/day)

#### **Dashboard Features**
- Multi-column responsive layout (optimized for desktop/mobile)
- Live camera feed with 16:9 aspect ratio
- Health score breakdown with color-coded status
- Activity, temperature, weight, humidity cards
- 24-hour trend graphs (activity, temperature, weight)
- Long-term statistics (1h, 24h, 7d averages)
- System health monitoring (WiFi signal, battery levels, uptime)
- Queen health indicator
- Nectar flow status
- Manual controls (restart camera, capture snapshot)

#### **Hardware Support**
- **Camera**: Seeed XIAO ESP32-S3 Sense (OV2640 2MP)
- **Computer Vision**: Raspberry Pi 3B+ or 4
- **Sensors**: Broodminder-T2 (temperature) + W3 (scale/humidity/temp)
- **Total Cost**: ~$250-350

#### **Software Stack**
- **ESPHome**: ESP32 firmware framework
- **Home Assistant**: Automation platform (2024.1+)
- **Python**: Motion detection script (OpenCV, NumPy)
- **Systemd**: Auto-start service for Raspberry Pi script

### 📦 Repository Structure

**Documentation** (7 files)
- `README.md` - Project overview
- `INSTALL.md` - Step-by-step installation guide
- `QUICKSTART.md` - Fast 4-step setup
- `HARDWARE.md` - Complete shopping list with specs
- `TROUBLESHOOTING.md` - Common issues & solutions
- `GITHUB_SETUP.md` - Repository organization guide
- `LICENSE` - MIT License

**Configuration Files** (10 files)
- Complete ESPHome configuration for ESP32-S3
- Complete Home Assistant configuration (sensors, automations, dashboard)
- Complete Python motion detection script
- Systemd service for auto-start
- Python requirements file
- Secrets template
- `.gitignore` for sensitive data

**Additional Documentation**
- `docs/HOME_ASSISTANT_SETUP.md` - Detailed HA configuration guide
- `docs/images/` - Directory for screenshots

### 🎯 Design Principles

#### **Self-Hosted & Privacy-First**
- 100% local processing (computer vision runs on Raspberry Pi)
- No cloud dependencies except optional Broodminder sensors
- Secure communications (Home Assistant encrypted API)

#### **Production-Ready**
- All configuration files included
- Comprehensive documentation
- Error handling and automated recovery
- Tested on Colorado dry climate (20-40% humidity)

#### **Climate-Adaptable**
- Default: Colorado dry climate (20-40% humidity)
- Documented adjustments for:
  - Humid climates (Eastern US, Europe): 40-70% humidity
  - Very dry climates (Southwest): 15-30% humidity
- Configurable temperature thresholds

#### **Beekeeping-Focused**
- Health scoring matches seasonal bee behavior
- Alerts designed for actual management decisions
- Terminology aligned with beekeeping practices
- Robbing detection algorithm
- Nectar flow tracking
- Queen health indicators

### 🔧 Technical Highlights

#### **Motion Detection Algorithm**
- Frame differencing with OpenCV
- Gaussian blur for noise reduction
- Configurable sensitivity (15-30 recommended)
- Minimum contour area filtering (15-25 pixels)
- Activity score: 0-100% (scaled for bee size)
- Bees per minute estimation (motion_pixels / 75)

#### **Health Scoring Logic**
- **Temperature scoring**: 
  - Winter: 50-70°F optimal (cluster temps)
  - Summer: 93-95°F optimal (brood rearing)
- **Activity scoring**:
  - Winter: 10-30% optimal (low activity normal)
  - Summer: 60%+ optimal (high foraging)
- **Weight scoring**:
  - Winter: ±0.1 kg/day (stable)
  - Summer: +0.5 kg/day (nectar flow)
- **Humidity scoring**:
  - Winter: 20-35% optimal (Colorado)
  - Summer: 30-40% optimal (Colorado)

#### **Update Intervals**
- Python motion detection: 5-second loop
- ESP32 camera: 5fps active, 0.2fps idle
- WiFi signal: 60s updates
- Broodminder sensors: Bluetooth sync via cloud
- Home Assistant recording: Continuous

### 🌍 Supported Regions
- **Primary**: Colorado / Rocky Mountain region (dry climate)
- **Adaptable**: Any climate with humidity range adjustments
- **Hemisphere**: Northern (default), Southern (configurable)

### 🔒 Security Features
- Secrets.yaml for sensitive data
- .gitignore prevents credential commits
- API token authentication
- Local-only camera stream (optional)
- No external cloud dependencies

### 📊 Data Storage
- Home Assistant recorder integration
- Statistics sensors for long-term trends
- Configurable retention period
- Long-term database format
- Exportable via HA backup system

### 🚀 Installation Time
- **Hardware setup**: 1-2 hours
- **ESP32 flash**: 15 minutes
- **Raspberry Pi setup**: 30 minutes
- **Home Assistant config**: 30-60 minutes
- **Testing & calibration**: 1-2 days
- **Total to production**: ~1 week including monitoring

### 🐛 Known Limitations (v1.0.0)
- Temperature-based seasonal switching can flip-flop in spring/fall *(Fixed in v1.1.0)*
- Single hive support only (multi-hive planned for v2.0.0)
- Manual sensor entity ID updates required
- No automatic timezone/hemisphere detection
- English language only in documentation

### 📝 License
MIT License - Free for personal and commercial use

### 🙏 Credits
- **Broodminder**: Professional hive sensors
- **ESPHome**: ESP32 firmware framework
- **Home Assistant**: Home automation platform
- **OpenCV**: Computer vision library
- **Colorado beekeeping community**: Testing and feedback

---

## Release Links

- **[v1.1.0]** - https://github.com/beebrothelman/HA_Apiary_Monitor/releases/tag/v1.1.0
- **[v1.0.0]** - https://github.com/beebrothelman/HA_Apiary_Monitor/releases/tag/v1.0.0
