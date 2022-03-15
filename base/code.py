# Transmitter Base-Station
# by James Andrews <jandrews7348@floridapoly.edu
import time
import busio
import digitalio
import board
from adafruit_tinylora.adafruit_tinylora import TTN, TinyLoRa
import adafruit_rfm9x

# Pinouts
led = digitalio.DigitalInOut(board.D13)     # LED is wired to PIN 13
ESTOP = digitalio.DigitalInOut(board.D12)   # Connet E-Stop to PIN 12

led.direction = digitalio.Direction.OUTPUT
ESTOP.direction = digitalio.Direction.INPUT
#pinMode(ESTOP, INPUT_PULLUP)

# Create library object using our bus SPI port for radio
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Feather M0 RFM9x Pinouts
cs = digitalio.DigitalInOut(board.RFM9X_CS)
irq = digitalio.DigitalInOut(board.RFM9X_D0)
rst = digitalio.DigitalInOut(board.RFM9X_RST)
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, rst, 915.0)
rfm9x.tx_power = 23

while True:
    # Send Message over LoRa
    led.value = True
    if ESTOP.value is True:
        rfm9x.send('E')
    else:
        rfm9x.send('A')
    led.value = False

    # Receive Message over LoRa
    data = rfm9x.receive(timeout=5)  # Wait 5 seconds
    print(data)
    print(ESTOP.value)
