import serial
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()

#for port,_,_ in sorted(ports):
#        print(port)

class Arduino():
    def __init__(self, port, baudrate, probes_number, time_delay):
        self.probes_number = probes_number
        self.time_delay = time_delay
        self.arduino = serial.Serial(port= port, baudrate= baudrate, timeout=.1)
        

    def file_test_start(self):
        with open('input', 'wb') as f:
            val = (self.time_delay>>1) | (self.probes_number << 4)
            f.write(val.to_bytes(1,"big"))
    def file_test_stop(self):
        with open('input', 'wb') as f:
            val = 0
            f.write(val.to_bytes(1,"big"))
    def send_start(self):
        val = (self.time_delay>>1) | (self.probes_number << 4)
        self.arduino.write(val.to_bytes(1,"big"))
    def send_stop(self):
        val = 0
        self.arduino.write(val.to_bytes(1,"big"))
# ar = Arduino(4, 4, 4, 5)
# ar.file_test_stop()