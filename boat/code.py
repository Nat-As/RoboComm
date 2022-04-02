# Receiver Boat
# by James Andrews <jandrews7348@floridapoly.edu
import time
import busio
import digitalio
import board
from adafruit_tinylora.adafruit_tinylora import TTN, TinyLoRa
from digitalio import DigitalInOut, Direction, Pull
import adafruit_rfm9x

# Custom Libs
import boat

# Pinouts
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

# Create library object using our bus SPI port for radio
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.RFM9X_CS)
irq = digitalio.DigitalInOut(board.RFM9X_D0)
rst = digitalio.DigitalInOut(board.RFM9X_RST)
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, rst, 915.0)

ESTOP = False #ToDo: Controlled by EStop sw
while not ESTOP:
    led.value = True
    # Receive Message over LoRa
    data = rfm9x.receive(timeout=5)
    led.value = False

    report = boat.ProcessCmd(data)
    print(report)
    boat.SetLight(report[0])
    # Send Report back over LoRa
    rfm9x.send(report)
else:
    print("ESTOP ACTIVE!")
    report[0] = "E"
    report[2] = "T"
