# Accident Rerouting

Accident rerouting is one of the main features demonstrated in the LifeLane AI prototype.

## Normal Route

For the main demonstration, the ambulance starts from House 1.

The initial route is:

House 1 → J1 → J2 → Hospital 1

J1 and J2 are prepared for the ambulance.

## Accident Detection

After the ambulance passes J1, an accident can be triggered at J2 using the accident button.

The J2 ESP32 sends the accident information to A1 using ESP-NOW.

## Route Change

After receiving the accident information, A1 changes the emergency route.

The ambulance is redirected through J3 instead of continuing through the blocked junction.

The alternate route used in the demonstration is:

House 1 → J1 → J3 → Hospital 2

## Traffic Signal Changes

The signals on the new route are prepared for the ambulance.

The dashboard also updates the route and junction status.

## Purpose

This feature demonstrates that the emergency corridor does not depend only on a fixed route.

If a junction becomes unavailable, another route can be selected so that the ambulance can continue towards a hospital.
