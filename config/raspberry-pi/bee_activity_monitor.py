#!/usr/bin/env python3
"""
Bee Hive Activity Monitor
Real-time motion detection for ESP32-S3 camera
Optimized for Colorado dry climate

Hardware:
- ESP32-S3 camera module (ESPHome)
- Raspberry Pi 3B+ or newer
- Home Assistant server

Author: Jason Lansdown
License: MIT
"""

import cv2
import numpy as np
import requests
import time
import logging
from datetime import datetime
from typing import Optional, Tuple

# =============================================================================
# CONFIGURATION - UPDATE THESE VALUES FOR YOUR SETUP
# =============================================================================

# ESP32 Camera IP address (set in ESPHome config)
ESP32_IP = "192.168.1.100"  # UPDATE THIS

# Home Assistant details
HA_URL = "http://192.168.1.50:8123"  # UPDATE THIS
HA_TOKEN = "YOUR_LONG_LIVED_ACCESS_TOKEN"  # CREATE IN HOME ASSISTANT PROFILE

# Motion detection settings
SENSITIVITY = 25  # Lower = more sensitive (15-30 recommended)
MIN_AREA = 20     # Minimum contour area to consider (15-25 recommended)
UPDATE_INTERVAL = 5  # Seconds between updates

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/pi/bee-monitor/bee_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# =============================================================================
# BEE ACTIVITY DETECTOR CLASS
# =============================================================================

class BeeActivityDetector:
    """
    Detects bee activity using frame differencing algorithm.
    Compares consecutive frames to identify motion.
    """
    
    def __init__(self, sensitivity: int = 25, min_area: int = 20):
        """
        Initialize the detector
        
        Args:
            sensitivity: Threshold for motion detection (0-255)
            min_area: Minimum contour area in pixels
        """
        self.sensitivity = sensitivity
        self.min_area = min_area
        self.previous_frame = None
        
    def preprocess_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Preprocess frame for motion detection
        - Convert to grayscale
        - Apply Gaussian blur to reduce noise
        
        Args:
            frame: Input BGR frame from camera
            
        Returns:
            Processed grayscale frame
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (21, 21), 0)
        return blurred
    
    def detect_motion(self, frame: np.ndarray) -> Tuple[float, int]:
        """
        Detect motion between current and previous frame
        
        Args:
            frame: Current frame from camera
            
        Returns:
            Tuple of (activity_score, motion_pixels)
            - activity_score: 0-100% motion level
            - motion_pixels: Total pixels with motion
        """
        processed = self.preprocess_frame(frame)
        
        # Need previous frame for comparison
        if self.previous_frame is None:
            self.previous_frame = processed
            return 0.0, 0
        
        # Calculate difference between frames
        frame_delta = cv2.absdiff(self.previous_frame, processed)
        
        # Threshold to binary
        thresh = cv2.threshold(
            frame_delta, 
            self.sensitivity, 
            255, 
            cv2.THRESH_BINARY
        )[1]
        
        # Dilate to fill holes
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        # Find contours (areas of motion)
        contours, _ = cv2.findContours(
            thresh.copy(), 
            cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        # Sum up motion pixels from significant contours
        motion_pixels = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > self.min_area:
                motion_pixels += area
        
        # Calculate activity score (0-100%)
        # Scaling factor of 10 accounts for small bee size relative to frame
        frame_area = processed.shape[0] * processed.shape[1]
        activity_score = min(100, (motion_pixels / frame_area) * 100 * 10)
        
        # Store for next comparison
        self.previous_frame = processed
        
        return activity_score, motion_pixels

# =============================================================================
# ESP32 CAMERA INTERFACE CLASS
# =============================================================================

class ESP32Camera:
    """
    Interface to ESP32 camera via Home Assistant API
    """
    
    def __init__(self, ha_url: str, ha_token: str, 
                 camera_entity: str = "camera.bee_hive_monitor_camera"):
        """
        Initialize camera interface
        
        Args:
            ha_url: Home Assistant URL (e.g., http://192.168.1.50:8123)
            ha_token: Long-lived access token
            camera_entity: Camera entity ID in Home Assistant
        """
        self.ha_url = ha_url.rstrip('/')
        self.camera_entity = camera_entity
        self.headers = {'Authorization': f'Bearer {ha_token}'}
        self.snapshot_url = f"{self.ha_url}/api/camera_proxy/{camera_entity}"
        
    def get_frame(self) -> Optional[np.ndarray]:
        """
        Fetch current frame from camera
        
        Returns:
            OpenCV frame (numpy array) or None if failed
        """
        try:
            response = requests.get(
                self.snapshot_url, 
                headers=self.headers, 
                timeout=10
            )
            
            if response.status_code == 200:
                # Decode JPEG to OpenCV frame
                img_array = np.frombuffer(response.content, dtype=np.uint8)
                frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                return frame
            else:
                logger.error(f"Failed to get frame: HTTP {response.status_code}")
                
        except requests.exceptions.Timeout:
            logger.error("Timeout getting frame from camera")
        except Exception as e:
            logger.error(f"Failed to get frame: {e}")
            
        return None

# =============================================================================
# HOME ASSISTANT UPDATER CLASS
# =============================================================================

class HomeAssistantUpdater:
    """
    Updates Home Assistant sensor states via REST API
    """
    
    def __init__(self, url: str, token: str):
        """
        Initialize HA updater
        
        Args:
            url: Home Assistant URL
            token: Long-lived access token
        """
        self.url = url.rstrip('/')
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
    def update_sensor(self, entity_id: str, state, attributes: dict = None):
        """
        Update a sensor state in Home Assistant
        
        Args:
            entity_id: Full entity ID (e.g., sensor.bee_hive_activity)
            state: New state value
            attributes: Optional attributes dictionary
            
        Returns:
            True if successful, False otherwise
        """
        url = f"{self.url}/api/states/{entity_id}"
        
        # Format state value
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
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to update {entity_id}: {e}")
            return False

# =============================================================================
# MAIN MONITORING LOOP
# =============================================================================

def main():
    """
    Main monitoring loop
    - Fetches frames from ESP32 camera
    - Detects motion using frame differencing
    - Updates Home Assistant sensors
    """
    
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
        logger.error("❌ Cannot connect to camera!")
        logger.error("Check:")
        logger.error("  - ESP32 IP address is correct")
        logger.error("  - ESP32 is online (ping it)")
        logger.error("  - Home Assistant token is valid")
        logger.error("  - Camera entity ID is correct")
        return
        
    logger.info(f"✅ Camera connected! Frame size: {test_frame.shape}")
    logger.info("\n🚀 Starting monitoring loop...\n")
    
    # Monitoring loop
    consecutive_failures = 0
    max_failures = 10
    
    try:
        while True:
            # Get current frame
            frame = camera.get_frame()
            
            if frame is not None:
                consecutive_failures = 0
                
                # Detect motion
                activity_score, motion_pixels = detector.detect_motion(frame)
                
                # Estimate bees per minute (rough calculation)
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
                
                # Log activity
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
        logger.error(f"❌ Unexpected error: {e}", exc_info=True)
        
    finally:
        logger.info("🛑 Bee Hive Activity Monitor Stopped")

# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()
