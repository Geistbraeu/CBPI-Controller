import time
import logging
import datetime
import os
from CBPIService import CBPIService
from OLEDService import OLEDService

# Setup logging
os.makedirs("logs", exist_ok=True)
log_filename = f"logs/controller_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# Configure logging to both file and console
logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    handlers=[
                        logging.FileHandler(log_filename),
                        logging.StreamHandler()
                    ])

cbpi = CBPIService()
oled = OLEDService()

def main():
    logging.info("Starting controller...")
    error_counter = 0
    
    while True:
        # 1. Refresh data (kettles)
        if not cbpi.refresh():
            logging.error("Failed to refresh kettles")
            error_counter += 1
            time.sleep(1 + error_counter)
            continue
        
        # 2. Check active step
        active_step = cbpi.get_active_step()
        if active_step and active_step.get('type') == 'BoilStep':
            oled.clear_all()
            time.sleep(5) # Wait before next check during boil
            continue

        # 3. Get Data
        mt_kettle = cbpi.get_kettle("MT")
        hlt_kettle = cbpi.get_kettle("HLT")
        
        mt_temp = cbpi.get_sensor_value(mt_kettle.get('sensor')) if mt_kettle else None
        hlt_temp = cbpi.get_sensor_value(hlt_kettle.get('sensor')) if hlt_kettle else None
        
        # 4. Process & Draw
        success = True
        
        # HLT Temp -> OLED 0
        if hlt_temp is not None:
            if not oled.draw_text(0, f"{round(float(hlt_temp),1)}°C"): success = False
        else:
            if not oled.draw_text(0, "Err"): success = False
            
        # HLT Target Temp -> OLED 1
        hlt_target = hlt_kettle.get('target_temp') if hlt_kettle else None
        if hlt_target is not None:
            if not oled.draw_text(1, f"{hlt_target}°C"): success = False
        else:
            if not oled.draw_text(1, "Err"): success = False

        # MT Temp -> OLED 2
        if mt_temp is not None:
            if not oled.draw_text(2, f"{round(float(mt_temp),1)}°C"): success = False
        else:
            if not oled.draw_text(2, "Err"): success = False
        
        # MT Target Temp -> OLED 3
        mt_target = mt_kettle.get('target_temp') if mt_kettle else None
        if mt_target is not None:
            if not oled.draw_text(3, f"{mt_target}°C"): success = False
        else:
            if not oled.draw_text(3, "Err"): success = False

            
        # 4. Sleep Logic
        if success:
            error_counter = 0
            time.sleep(1)
        else:
            error_counter += 1
            time.sleep(1 + error_counter)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Controller stopped by user.")
        oled.clear_all()
