# Hardware Pin Connections

This file contains the pin connections used in the LifeLane AI prototype.

The project uses four ESP32 boards. One ESP32 is used as A1 (master/ambulance controller) and the other three are used for Junction 1, Junction 2 and Junction 3.

## A1 - Master / Ambulance

A1 communicates with the three junction ESP32 boards using ESP-NOW.

The LCDs connected to A1 are used to show the signal status and timing of the junctions.

| LCD | SDA | SCL |

| Junction 1 LCD | GPIO26 | GPIO25 |
| Junction 2 LCD | GPIO27 | GPIO33 |
| Junction 3 LCD | GPIO32 | GPIO13 |

A1 does not have an emergency button. The emergency event is generated from the junction controllers.

## Junction 1

Junction 1 has a traffic signal, two IR sensors, an emergency button and a buzzer.

| Component | GPIO |

| Red LED | GPIO15 |
| Yellow LED | GPIO2 |
| Green LED | GPIO4 |
| Buzzer | GPIO23 |
| Entry IR Sensor | GPIO5 |
| Exit IR Sensor | GPIO18 |
| Emergency Button | GPIO19 |

The entry and exit IR sensors are used to detect the ambulance movement through the junction.

## Junction 2

Junction 2 has a traffic signal, two IR sensors, an emergency button and an accident button.

| Component | GPIO |

| Red LED | GPIO15 |
| Yellow LED | GPIO2 |
| Green LED | GPIO4 |
| Emergency Button | GPIO19 |
| Accident Button | GPIO21 |
| Entry IR Sensor | GPIO5 |
| Exit IR Sensor | GPIO18 |

The accident button is used in the prototype to demonstrate the rerouting process.

## Junction 3

Junction 3 has a traffic signal, two IR sensors, an emergency button and a buzzer.

| Component | GPIO |

| Red LED | GPIO15 |
| Yellow LED | GPIO2 |
| Green LED | GPIO4 |
| Buzzer | GPIO23 |
| Entry IR Sensor | GPIO18 |
| Exit IR Sensor | GPIO19 |
| Emergency Button | GPIO5 |

# Communication

The ESP32 boards communicate with each other using ESP-NOW.

The junction boards send events such as:

- Emergency button pressed
- Accident detected
- Ambulance entry detected
- Ambulance exit detected
- Junction passed

A1 receives these events and sends the required traffic control information to the junctions.

# Note

The pin connections listed here are for the current working prototype. Some components such as GPS and additional displays are planned for the complete version of the system.
