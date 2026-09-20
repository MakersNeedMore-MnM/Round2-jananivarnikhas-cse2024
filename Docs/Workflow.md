# LifeLane AI - Emergency Workflow

The prototype follows the following sequence.

## Step 1 - Emergency

An emergency button is pressed at one of the junctions.

For the prototype:

- J1 emergency → House 1
- J2 emergency → House 2
- J3 emergency → House 3

## Step 2 - Emergency Event

The junction ESP32 detects the button press and sends the emergency event to A1 using ESP-NOW.

## Step 3 - Route Selection

A1 receives the emergency information.

The system selects the junctions that are required for the route to the hospital.

For example:

J1 emergency:

House 1 → J1 → J2 → Hospital 1

## Step 4 - Traffic Signal

The required junction signal is changed to support the ambulance movement.

The LCD connected to A1 can display the junction timing and signal status.

## Step 5 - IR Detection

IR sensors are used to detect the ambulance entering and leaving a junction.

When the ambulance enters, the entry sensor detects it.

When it leaves, the exit sensor detects it.

## Step 6 - Accident

If an accident occurs on the selected route, the accident button at J2 can be pressed in the prototype.

The accident event is sent to A1.

## Step 7 - Rerouting

The system changes the route to avoid the blocked junction.

Example:

House 1 → J1 → J3 → Hospital 2

## Step 8 - Hospital

The ambulance follows the selected route and reaches the hospital.

The dashboard displays the current emergency status and route information.
