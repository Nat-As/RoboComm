# Libraries and Funtions for the Boat
import board
import digitalio

#Pinouts
OP1 = digitalio.DigitalInOut(board.D11)
OP2 = digitalio.DigitalInOut(board.D12)

OP1.direction = digitalio.Direction.OUTPUT
OP2.direction = digitalio.Direction.OUTPUT

# Processes Received data to set flags
def ProcessCmd(data):
    if str(data) == 'None':
        link = "N"
        status = "E"

    elif bytes(data) == b'A':
        link = "L"
        status = "A"

    elif bytes(data) == b'S':
        link = "L"
        status = "S"

    elif bytes(data) == b'M':
        link = "L"
        status = "M"

    elif bytes(data) == b'E':
        link = "L"
        status = "E"

    else:
        print(bytes(data))
        link = "N"
        status = "X"

    return status+link+"F"

# Takes the Status Charachter and Sets traffic light accordingly
def SetLight(status):
    if status == "No Link":
        OP1.value = False
        OP2.value = False
    elif status == "A":
        OP1.value = True
        OP2.value = True
    elif status == "S":
        OP1.value = True
        OP2.value = True
    elif status == "M":
        OP1.value = True
        OP2.value = False
    elif status == "E":
        OP1.value = False
        OP2.value = False
    else:
        OP1.value = False
        OP2.value = False
