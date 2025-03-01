# howdeepisyourlearn

# SmartBin-SG: AI-Driven Food Waste Reduction System  
**2023 Singapore National Sustainability Hackathon Submission**  

## Features  
1. **Real-Time Food Waste Classification**  
   - YOLOv8 model trained on Singaporean cafeteria dataset  
   - U-Net for waste quantity estimation  
2. **IoT-Integrated Order Optimization**  
   - Ridge regression with time-series cross-validation  
   - Integrates weather/holiday data from [Data.gov.sg](https://data.gov.sg)  
3. **NEA Compliance Reporting**  
   - Auto-generates PDF reports matching SS 668 standards  

## Hardware Setup  
1. **Raspberry Pi 4**  
   - Camera Module v2  
   - Ubuntu Server 22.04 LTS  
2. **Arduino Uno**  
   - HX711 Load Cell (Capacity: 5kg)  
   - Calibrate with `arduino/calibrate_hx711.ino`  

## Installation  
```bash
# On Raspberry Pi
git clone https://github.com/yourteam/SmartBin-SG.git
cd SmartBin-SG/raspberry_pi
pip install -r requirements.txt
