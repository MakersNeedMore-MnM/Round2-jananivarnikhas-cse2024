# Components Used

These are the main components used for building the LifeLane AI prototype.

# ESP32 Boards

4 ESP32 development boards are used in the prototype.

- 1 ESP32 for A1 (Master/Ambulance)
- 1 ESP32 for Junction 1
- 1 ESP32 for Junction 2
- 1 ESP32 for Junction 3

The ESP32 boards handle the junction signals, sensors, buttons and wireless communication.

# Traffic Signal LEDs

Traffic LED modules are used at each junction.

Each junction has:

- Red signal
- Yellow signal
- Green signal

The signals are controlled by the ESP32 depending on the normal traffic condition or emergency route.

# IR Sensors

IR proximity sensors are used to detect vehicles/ambulance movement at the junctions.

Two sensors are used at each junction:

- Entry sensor
- Exit sensor

The entry sensor detects when the ambulance enters the junction area and the exit sensor detects when it leaves.

# Push Buttons

Different buttons are used for the prototype demonstration.

# Emergency Button

The emergency button is placed at the junction and represents an emergency call.

When it is pressed, the event is sent to A1 through ESP-NOW.

# Accident Button

The accident button is available at Junction 2.

It is used to demonstrate an accident occurring on the selected route. When the button is pressed, the system can change the route and use Junction 3 as an alternate path.

# Buzzer

Buzzers are used at Junction 1 and Junction 3.

The buzzer provides an indication during the emergency vehicle movement.

# LCD Displays

LCD displays are connected to A1 for showing the status of the junctions.

The displays can show information such as:

- Junction name
- Red signal time
- Green signal time
- Emergency corridor status

Three LCD displays are planned for J1, J2 and J3.

# GPS

GPS is part of the planned complete system for tracking ambulance location.

A Neo-6M GPS module was considered for the prototype. For the current demonstration, phone GPS is used for the GPS-related part because the hardware GPS module was not giving a proper location fix during testing.

# Breadboards and Wires

Breadboards and jumper wires are used to connect the ESP32 boards, LEDs, buttons and sensors during prototype testing.

# Other Prototype Materials

The physical demonstration also uses:

- Toy ambulance
- Toy cars
- Hospital model
- Breadboards
- USB cables
- Wi-Fi router/mobile hotspot

# Main Software Used

The hardware works together with the following software:

- Arduino IDE
- ESP32 Arduino Core
- ESP-NOW
- Python
- Flask
- GPS/NMEA processing
- Web dashboard

The hardware and software together demonstrate the emergency corridor, traffic signal control, IR-based ambulance detection and accident rerouting.
