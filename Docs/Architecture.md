# LifeLane AI - System Architecture

LifeLane AI consists of ESP32 junction controllers, an ambulance/master controller, a Python backend and a web dashboard.

## Main Parts

1. A1 - Master/Ambulance Controller
2. Junction 1 (J1)
3. Junction 2 (J2)
4. Junction 3 (J3)
5. Python Backend
6. Web Dashboard
7. GPS system

## Working

The junction ESP32 boards collect information from the emergency buttons, accident button and IR sensors.

The junction controllers communicate with A1 using ESP-NOW.

A1 receives the information and decides the required emergency traffic control. The information is also sent to the Python backend through the serial connection.

The Python backend processes the received events and provides the data to the web dashboard.

The dashboard displays the emergency route, junction status, traffic information, ambulance status and hospital information.

## Basic Flow

Junction Sensors/Buttons
        ↓
J1 / J2 / J3 ESP32
        ↓
     ESP-NOW
        ↓
        A1
        ↓
   USB Serial
        ↓
 Python Backend
        ↓
   Web Dashboard

GPS information can also be used by the backend for ambulance location and route-related information.
