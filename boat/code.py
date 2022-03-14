# Transmitter Base-Station
# by James Andrews <jandrews7348@floridapoly.edu
import time
import busio
import digitalio
import board
from adafruit_tinylora.adafruit_tinylora import TTN, TinyLoRa
from digitalio import DigitalInOut, Direction, Pull
import adafruit_rfm9x
# Board LED
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

# Create library object using our bus SPI port for radio
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Feather M0 RFM9x Pinouts
led_red = digitalio.DigitalInOut(board.D12)
led_yellow = digitalio.DigitalInOut(board.D11)
led_green = digitalio.DigitalInOut(board.D10)
led_red.direction = Direction.OUTPUT
led_yellow.direction = Direction.OUTPUT
led_green.direction = Direction.OUTPUT

cs = digitalio.DigitalInOut(board.RFM9X_CS)
irq = digitalio.DigitalInOut(board.RFM9X_D0)
rst = digitalio.DigitalInOut(board.RFM9X_RST)
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, rst, 915.0)

while True:
    led.value = True
    # Receive Message over LoRa
    data = rfm9x.receive(timeout=5)
    led.value = False
    time.sleep(0.5)
    if str(data) == 'None':
        print("No Link")
        status = "No Link"
        led_red.value = False
        led_green.value = False
        led_yellow.value = False

    elif bytes(data) == b'A':
        print("Autonomous Mode Active")
        led_green.value = True
        led_red.value = False
        led_yellow.value = False
        status = "Autonomous Mode"

    elif bytes(data) == b'S':
        print("Secondary Mode Active")

    elif bytes(data) == b'M':
        print("Manual Mode Active")
        led_yellow.value = True
        led_red.value = False
        led_green.value = False
        status = "Manual Mode"

    elif bytes(data) == b'E':
        print("Emergency Stop!")
        led_red.value = True
        led_yellow.value = False
        led_green.value = False
        status = "Emergency Stop"

    else:
        print(bytes(data))
        led_red.value = False
        led_yellow.value = False
        led_green.value = False
        status = "Unknown"

    # Send Status over LoRa
    rfm9x.send(status)
    #rfm9x.send('RSSI: {0} dB'.format(rfm9x.rssi))
