# RoboComm
LoRaWAN Firmware for autonomous ships. This code consists of two major parts, a feather M0, RFM95 LoRaWAN located on a base station, and one located on the ship. The pin definitions of the feather boards are shown below.
<br>

![pinouts](https://cdn-learn.adafruit.com/assets/assets/000/046/255/large1024/feather_Feather_M0_RFM95_v1.2-1.png)
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
Pin D12 is used to check if the E-Stop button has been pressed. If the pin is set low (False) which it is by default, the E-Stop status is interpreted as False. If pin D12 is pulled high (True) the E-Stop condition is set to true, and an E-Stop packet is immediately sent to the boat. It is reccomended to connect D12 to a normally opened button that when closed, connects D12 to the USB pin.

<br>

# Ship
The Feather M0 onboard the ship is flashed with everything in the [boat](https://github.com/Nat-As/RoboComm/tree/main/boat) directory. This directory will eventually have it's own readme consisting of the below sections and their elaborations.

## Wiring
Two control pins controll a red, green, and yellow light to show what mode of operation the ship is in. Digital Pins D11 and D12 are used for this as follows:

<br>

| OPM1 (D11)| OPM2 (D12) | Color |
|------|------|-------|
| 0    | 0    | R     |
| 1    | 0    | Y     |
| 1    | 1    | G     |

<br>

## Reporting
The ship reports back to the base station a byte array across LoRa which can be modeled as a Binary Symmertic Channel (BSC). The byte array can be decoded as a UTF-8 sentence consisting of densely packed data. The data can be interpreted as follows:
<br>

|               | OpMode              | Link         | E-Stop        | GPS         | Jetson Link     | Jetson Data             | /n      |
|---------------|---------------------|--------------|---------------|-------------|-----------------|-------------------------|---------|
| Size (bytes)  | 1                   | 1            | 1             | 20          | 1               | X                       | 1       |
| Byte Location | 0                   | 1            | 2             | 3-24        | 25              | 26-98                   | 99-100  |
| Values        | A,S,M,E             | L,N          | T,F           | 123.45,,... | J,K             | X                       | \n      |
| Purpose       | Main Operation Mode | Link To Base | Manual Button | GPS@10Hz    | TF Link to Jet. | Anything Sent From Jet. | EOL/EOF |

<br>

An example message reads: ```ENF123.45,,12.34,,123.45...JSTANDBY...``` and prints a new line to the terminal. This data is interpreted from left to right meaning: 
<br>

E: E-Stop Mode is active.
<br>

N: The reason for this is there is no link to the base station.
<br>

F: The condition of the manual E-Stop button on board is False.
<br>

123.45,,...: The GPS coordinates updated every 10 seconds.
<br>

J: There is an active link to the Jetson.
<br>

STANDBY: The message 'STANDBY' was recieved from the Jetson.
<br>

/n: Newline. This is the end of the message.
