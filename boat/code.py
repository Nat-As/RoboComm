# Transmitter Base-Station
# by James Andrews <jandrews7348@floridapoly.edu
import time
import busio
import digitalio
import board
from adafruit_tinylora.adafruit_tinylora import TTN, TinyLoRa
from digitalio import DigitalInOut, Direction, Pull
import adafruit_rfm9x

# Board Pinouts
OP1 = digitalio.DigitalInOut(board.D11)
OP2 = digitalio.DigitalInOut(board.D12)
led = digitalio.DigitalInOut(board.D13)

OP1.direction = digitalio.Direction.OUTPUT
OP2.direction = digitalio.Direction.OUTPUT
led.direction = digitalio.Direction.OUTPUT

# Create library object using our bus SPI port for radio
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.RFM9X_CS)
irq = digitalio.DigitalInOut(board.RFM9X_D0)
rst = digitalio.DigitalInOut(board.RFM9X_RST)
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, rst, 915.0)

# Light Handler Function
def SetLight(status):
    if status == "No Link":
        OP1.value = False
        OP2.value = False
    elif status == "Autonomous Mode":
        OP1.value = True
        OP2.value = True
    elif status == "Secondary Mode":
        OP1.value = True
        OP2.value = True
    elif status == "Manual Mode":
        OP1.value = True
        OP2.value = False
    elif status == "Emergency Stop":
        OP1.value = False
        OP2.value = False
    else:
        OP1.value = False
        OP2.value = False

while True:
    led.value = True
    # Receive Message over LoRa
    data = rfm9x.receive(timeout=5)
    led.value = False
    if str(data) == 'None':
        status = "No Link"

    elif bytes(data) == b'A':
        status = "Autonomous Mode"

    elif bytes(data) == b'S':
        status = "Secondary Mode"

    elif bytes(data) == b'M':
        status = "Manual Mode"

    elif bytes(data) == b'E':
        status = "Emergency Stop"

    else:
        print(bytes(data))
        status = "Unknown"

    print(status)
    SetLight(status)
    # Send Status over LoRa
    rfm9x.send(status)
