# RoboComm
LoRaWAN Firmware for autonomous ships. This code consists of two major parts, a feather M0, RFM95 LoRaWAN located on a base station, and one located on the ship.
# Base Station
The Base Station sends a packet over LoRaWAN that currently only contains one letter corresponding to an operation Mode. The letters are interpreted by the boat as follows:
<br>
| Letter | Mode           | Color |
|--------|----------------|-------|
| A      | Autonomous     | G     |
| S      | Secondary      | G     |
| M      | Manual         | Y     |
| E      | Emergency Stop | R     |
<br>

# Ship
Two control pins controll a red, green, and yellow light to show what mode of operation the ship is in. Digital Pins D11 and D12 are used for this as follows:

<br>

| OPM1 (D11)| OPM2 (D12) | Color |
|------|------|-------|
| 0    | 0    | R     |
| 1    | 0    | Y     |
| 1    | 1    | G     |

<br>

