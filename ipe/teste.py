from arduino import Arduino
from time import sleep

ard = Arduino('COM4', 9600, 3, 1)
sleep(2)
try:
    while True:
        ard.send_start()
        sleep(1)
except KeyboardInterrupt:
    ard.send_stop()