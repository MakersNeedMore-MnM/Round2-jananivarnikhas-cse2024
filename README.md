# Round2-jananivarnikhas-cse2024
Repository for team jananivarnikhas.cse2024 for Round 2

# LifeLane AI
## Predictive Traffic Management for Emergency Vehicles

LifeLane AI is an AI and IoT based emergency traffic management system designed to help ambulances reach hospitals faster by creating an intelligent green corridor.

The system connects multiple traffic junctions using ESP32 controllers and ESP-NOW communication. When an emergency is reported, the system identifies the required route, prepares the traffic signals along that route, monitors ambulance movement using IR sensors, and can change the route when an accident or blockage occurs.

The project is developed as a working prototype using ESP32 hardware, traffic signal LEDs, IR sensors, push buttons, LCD displays, Python backend services and a web-based command center dashboard.

---

# 1. Problem Statement

Ambulances can lose valuable time because of traffic congestion, red signals, accidents and unexpected road conditions.

Traditional traffic signals normally operate using fixed timings or basic traffic-density information. They do not continuously prepare multiple junctions based on the expected movement of an emergency vehicle.

This can result in:

- Ambulances waiting at traffic signals
- Delays at multiple junctions
- Difficulty handling unexpected accidents
- Traffic congestion around emergency routes
- Lack of coordination between different traffic signals
- Limited communication between ambulance and traffic infrastructure

LifeLane AI aims to address these problems by connecting emergency vehicles with intelligent traffic junctions.

---

# 2. Proposed Solution

LifeLane AI creates a coordinated emergency corridor between the ambulance and the required traffic junctions.

The system works using:

1. ESP32 controllers at traffic junctions
2. A1 master/ambulance controller
3. ESP-NOW wireless communication
4. Emergency and accident buttons
5. IR sensors for ambulance detection
6. Traffic signal LEDs
7. LCD displays for junction timing
8. Python backend
9. GPS/location information
10. Web-based monitoring dashboard

When an emergency button is pressed, the corresponding junction sends an emergency event to A1.

A1 processes the event and coordinates the required junctions.

The Python backend receives the system information and updates the dashboard with the emergency route, junction status, ambulance status, traffic information and hospital information.

---

# 3. Main Idea

The main idea of LifeLane AI is:

> "Prepare the road before the ambulance reaches it."

Instead of waiting for the ambulance to arrive at a junction and then changing the signal, the system prepares the required junctions according to the selected emergency route.

The system also monitors the ambulance while it is travelling through the corridor.

If a problem occurs on the selected route, the system can change to an alternate route.

---

# 4. System Architecture

The prototype consists of four ESP32 controllers.

### A1 - Master / Ambulance Controller

A1 acts as the main controller.

It:

- Receives emergency events
- Receives accident events
- Receives IR events from junctions
- Coordinates junction operations
- Communicates with the Python backend
- Controls the emergency route logic
- Displays junction timing information on LCDs

### Junction 1

Junction 1 contains:

- Traffic signal LEDs
- Emergency button
- Entry IR sensor
- Exit IR sensor
- Buzzer

### Junction 2

Junction 2 contains:

- Traffic signal LEDs
- Emergency button
- Accident button
- Entry IR sensor
- Exit IR sensor

### Junction 3

Junction 3 contains:

- Traffic signal LEDs
- Emergency button
- Entry IR sensor
- Exit IR sensor
- Buzzer

### Communication

The ESP32 controllers communicate using ESP-NOW.

The overall communication flow is:

    Junction Sensors / Buttons
              |
              v
       J1 / J2 / J3 ESP32
              |
           ESP-NOW
              |
              v
             A1
              |
         USB Serial
              |
              v
       Python Backend
              |
              v
       Web Dashboard

---

# 5. Emergency Workflow

The prototype uses physical emergency buttons at the junctions.

The dashboard does not contain a manual emergency button. The event comes from the physical IoT hardware.

## Emergency from Junction 1

When the emergency button at J1 is pressed:

    Emergency Button J1
            ↓
        J1 ESP32
            ↓
         ESP-NOW
            ↓
            A1
            ↓
       Python Backend
            ↓
       Web Dashboard

The emergency is associated with:

    House 1

The main demonstration route is:

    House 1
       ↓
      J1
       ↓
      J2
       ↓
   Hospital 1

J1 and J2 are therefore prepared for the ambulance.

---

## Emergency from Junction 2

When the emergency button at J2 is pressed, the emergency is associated with:

    House 2

The system selects the required route toward the hospital instead of unnecessarily activating unrelated junctions.

Example:

    House 2
       ↓
      J2
       ↓
   Hospital 1

---

## Emergency from Junction 3

When the emergency button at J3 is pressed, the emergency is associated with:

    House 3

The corresponding route is:

    House 3
       ↓
      J3
       ↓
   Hospital 2

---

# 6. Predictive Green Corridor

One of the main features of LifeLane AI is the predictive green corridor.

The system prepares the traffic signals that are present on the selected route.

For example:

    House 1 → J1 → J2 → Hospital 1

When the emergency is received:

- J1 can be prepared for the ambulance
- J2 can be prepared before the ambulance reaches it
- Other unnecessary junctions do not need to be activated
- Signal timing can be adjusted according to the emergency movement

This is different from simply changing one traffic light after the ambulance arrives.

---

# 7. Dynamic Green Wave Synchronization

The system coordinates multiple junctions instead of treating every traffic signal independently.

For an emergency route such as:

    House 1 → J1 → J2 → Hospital 1

the required junctions can be prepared in sequence.

The objective is to allow the ambulance to move through the corridor with minimum signal delay.

The system can use:

- Ambulance position
- Estimated arrival time
- Junction status
- Traffic information
- IR sensor events
- Route information

to determine the required signal timing.

---

# 8. Adaptive Signal Timing

The project includes adaptive signal timing.

Instead of using only one fixed emergency timing, the dashboard and control logic can calculate timing based on the current situation.

The timing can consider:

- Current traffic condition
- Ambulance movement
- IR sensor information
- Junction position on the route
- Estimated arrival time
- Emergency status

For the prototype demonstration, emergency timings can be shortened to demonstrate how the green corridor is created.

Example:

    Normal signal
    Green = 60 seconds

    Emergency corridor
    Green timing can be reduced/adjusted
    according to the emergency movement.

The A1 LCD displays the signal status and timing for the junctions.

---

# 9. IR-Based Ambulance Detection

IR sensors are installed at the junctions.

Each junction has:

- Entry IR sensor
- Exit IR sensor

The sensors are used to identify when the ambulance enters and leaves the junction.

### Entry

When the entry sensor detects the ambulance:

    IR ENTRY DETECTED

The system updates the junction status.

### Exit

When the ambulance reaches the exit sensor:

    IR EXIT DETECTED

The system knows that the ambulance has passed the junction.

This information can be used to update the emergency corridor and prepare the next junction.

The prototype uses edge-based IR detection with a small debounce period to avoid repeated detections.

---

# 10. Accident Detection and Rerouting

Accident rerouting is one of the important features of LifeLane AI.

The main demonstration starts with:

    House 1
       ↓
      J1
       ↓
      J2
       ↓
   Hospital 1

After the ambulance passes J1, an accident can be triggered at J2 using the physical accident button.

The J2 controller sends the accident event to A1.

The system then blocks the affected route and selects an alternate path.

The demonstration can reroute the ambulance through J3:

    House 1
       ↓
      J1
       ↓
      J3
       ↓
   Hospital 2

The dashboard updates the route and displays the changed emergency corridor.

This demonstrates that the emergency route is not fixed and can be changed when the original path becomes unavailable.

---

# 11. Automatic Route Replanning

The system is designed to support route replanning when an unexpected situation occurs.

Possible reasons for replanning include:

- Accident
- Road blockage
- Heavy traffic
- Junction unavailable
- Change in hospital destination

Instead of continuing to use a blocked route, the system can select an alternate route.

The current prototype demonstrates this concept using the accident button at J2.

---

# 12. GPS and Location Tracking

GPS is planned as part of the complete LifeLane AI system.

The intended system can use GPS information to determine:

- Ambulance location
- Distance to junction
- Distance to hospital
- Ambulance speed
- Estimated arrival time
- Nearest ambulance

A Neo-6M GPS module was considered for the hardware implementation.

During prototype testing, phone GPS is used for the GPS-related demonstration because the hardware GPS module did not provide a reliable location fix indoors.

The complete system can use real GPS coordinates from ambulances.

---

# 13. Nearest Ambulance Selection

In the complete LifeLane AI system, multiple ambulances can be connected to the platform.

When an emergency is received, the system can compare the location of available ambulances and select the nearest suitable ambulance.

The selection can consider:

- Ambulance GPS location
- Distance to emergency location
- Ambulance availability
- Current route
- Estimated travel time

The current physical prototype uses A1 as the available ambulance/master controller.

Multi-ambulance selection is planned as a future enhancement.

---

# 14. Hospital Selection

The system also considers the hospital destination.

The complete system can select or recommend a hospital based on factors such as:

- Distance
- Route availability
- Current road condition
- Emergency situation
- Hospital availability
- Estimated arrival time

The prototype demonstrates Hospital 1 and Hospital 2 as destination points.

---

# 15. Hospital Pre-Notification

A future version of LifeLane AI can provide information to the hospital before the ambulance arrives.

The hospital could receive:

- Ambulance ID
- Patient emergency information
- Estimated arrival time
- Ambulance location
- Selected route
- Hospital destination

This can allow the hospital team to prepare before the ambulance reaches the hospital.

---

# 16. Web Command Center

LifeLane AI includes a web-based dashboard for monitoring the system.

The dashboard provides information about:

- Active emergency
- Ambulance
- Emergency location
- Selected hospital
- Selected route
- Junction status
- Traffic information
- IR sensor events
- Signal timing
- Accident status
- Route changes
- System events

The dashboard contains a real-world map using Leaflet and map data.

The map can display:

- Project junctions
- Ambulance
- Emergency houses
- Hospitals
- Traffic signal locations
- Hospital locations
- Selected emergency route
- Blocked areas
- Alternate routes

---

# 17. Real-Time IoT Integration

The dashboard is connected to the actual prototype through the Python backend.

The data flow is:

    Physical Button
          ↓
       ESP32
          ↓
       ESP-NOW
          ↓
          A1
          ↓
      USB Serial
          ↓
     Python Server
          ↓
         API
          ↓
      Web Dashboard

Therefore, an emergency event shown on the dashboard can originate from the physical hardware.

The dashboard is not intended to replace the physical IoT buttons.

---

# 18. AI and Decision Engine

The project uses a Python-based decision and processing layer.

The complete LifeLane AI concept can use:

- Route optimization
- ETA prediction
- Traffic analysis
- Ambulance location
- Junction conditions
- Accident information
- Hospital information

The purpose of the decision engine is to determine how the emergency corridor should be organized.

The prototype demonstrates the decision flow using predefined project routes and real hardware events.

More advanced machine learning models can be added as more traffic and ambulance data becomes available.

---

# 19. Project Novelty

The main novelty of LifeLane AI is the combination of emergency vehicle tracking, predictive traffic control, IoT junction communication and route replanning.

Important features include:

### 1. Predictive Green Corridor

Traffic signals are prepared before the ambulance reaches the junction.

### 2. Dynamic Green Wave

Multiple junctions can be coordinated as one emergency corridor.

### 3. Adaptive Signal Timing

Signal timing can be adjusted according to ambulance movement and traffic conditions.

### 4. Automatic Route Replanning

The route can be changed when an accident or blockage occurs.

### 5. IoT Junction Communication

ESP32 junction controllers communicate wirelessly using ESP-NOW.

### 6. Physical Emergency Trigger

Emergency events originate from physical IoT buttons instead of only being simulated from software.

### 7. IR-Based Vehicle Movement Detection

Entry and exit sensors provide information about ambulance movement through each junction.

### 8. Hospital Integration

The system is designed to provide ambulance information and ETA to hospitals.

### 9. Emergency Vehicle Authentication

A future version can authenticate registered emergency vehicles before giving them priority.

### 10. Multiple Ambulance Priority

The complete system can support multiple ambulances and determine which available ambulance should respond to an emergency.

---

# 20. Hardware Used

The prototype uses:

- ESP32 development boards × 4
- Traffic LED modules
- IR proximity sensors
- Push buttons
- Buzzer
- LCD displays
- Breadboards
- Jumper wires
- USB cables
- Toy ambulance
- Toy vehicles
- Hospital model
- Wi-Fi network

---

# 21. Software and Technologies

### Hardware

- ESP32
- IR Sensors
- Traffic LEDs
- LCD
- GPS / Phone GPS

### Communication

- ESP-NOW
- Serial communication

### Backend

- Python
- Flask
- PySerial
- pynmea2

### Frontend

- HTML
- CSS
- JavaScript
- Leaflet.js

### Map

- Leaflet
- OpenStreetMap / map services
- Route service integration

### Development

- Arduino IDE
- ESP32 Arduino Core
- Python

---

# 22. ESP-NOW Communication

ESP-NOW is used for communication between the ESP32 controllers.

The junction boards can send events such as:

    EMERGENCY_J1
    EMERGENCY_J2
    EMERGENCY_J3

    ACCIDENT_J2

    J1_TRAFFIC_ENTRY
    J1_TRAFFIC_EXIT

    J2_TRAFFIC_ENTRY
    J2_TRAFFIC_EXIT

    J3_TRAFFIC_ENTRY
    J3_TRAFFIC_EXIT

A1 receives these events and processes the emergency corridor.

This allows the junction controllers to communicate without requiring every control message to pass through the web server.

---

# 23. Current Prototype Demonstration

The main demonstration follows this sequence.

### Step 1

An emergency is triggered at Junction 1 using the physical emergency button.

### Step 2

The system identifies the emergency location as House 1.

### Step 3

The route is selected:

    House 1 → J1 → J2 → Hospital 1

### Step 4

The required junction signals are prepared.

### Step 5

The ambulance moves toward J1.

### Step 6

J1 entry and exit IR sensors detect the ambulance.

### Step 7

After J1 is passed, J2 becomes the next required junction.

### Step 8

An accident is triggered at J2 using the physical accident button.

### Step 9

The system receives the accident event.

### Step 10

The route is changed to an alternate path through J3.

### Step 11

The dashboard updates the route, junctions and hospital.

### Step 12

The ambulance continues toward the alternate hospital.

This demonstrates emergency detection, predictive signal coordination, IR-based movement detection and accident rerouting.

---

# 24. Project Structure

```text
LifeLane-AI/
│
├── firmware/
│   ├── A1/
│   │   └── A1.ino
│   ├── J1/
│   │   └── J1.ino
│   ├── J2/
│   │   └── J2.ino
│   └── J3/
│       └── J3.ino
│
├── backend/
│   └── server.py
│
├── frontend/
│   └── index.html
│
├── hardware/
│   ├── pin_connections.md
│   └── components.md
│
├── docs/
│   ├── architecture.md
│   ├── workflow.md
│   └── accident_rerouting.md
│
├── demo/
│   ├── screenshots/
│   └── demo_video_link.txt
│
├── requirements.txt
├── .gitignore
└── README.md
