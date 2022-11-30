from arduino import Arduino
from time import sleep

ard = Arduino('COM11', 9600, 4, 1)
try:
    while True:
        sleep(7)
        ard.send_start()
except KeyboardInterrupt:
    ard.sen_stop()