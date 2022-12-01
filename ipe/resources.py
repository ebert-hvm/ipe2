import pyvisa as visa
import time as tm
import pandas as pd
from . import constantes as c
from .arduino import Arduino
from .input import Input
import serial
import time


class Resources:
    def __init__(self, input:Input) -> None:
        self.resources = visa.ResourceManager()
        self.multimeter = None 
        self.power_supply = None
        self.arduino = None
        self.values = []
        self.input = input

    def configure(self):
        try:
            self.multimeter = self.resources.open_resource("GPIB0::22::INSTR")
            self.multimeter.query("*IDN?")
        except visa.Error:
            self.multimeter = None
            return False, "Não foi possível conectar ao multímetro"
        try:
            self.power_supply = self.resources.open_resource("USB0::0x0957::0x8B18::MY51144612::0::INSTR")
            self.power_supply.query("*IDN?")
        except visa.Error:
            self.power_supply = None
            return False, "Não foi possível conectar à fonte"
        if self.arduino is None or not self.arduino.is_connected():
            return False, "Não foi possível conectar ao Arduino"
        return True, "Aparelhos conectados"

    def connect_arduino(self, port):
        try:
            self.arduino = Arduino(port)
            return "conectado"
        except serial.SerialException:
            self.arduino = None
            return "não foi possível conectar."

    def start(self) -> None:
        tm.sleep(c.sleep_time_power_supply)
        self.power_supply.write(f"VOLT {5}")
        self.power_supply.write(f"CURR:LIM {0.010}")
        self.power_supply.write(f"VOLT:LIM {6}")
        tm.sleep(c.sleep_time_power_supply)
        self.power_supply.write("OUTP ON")
        tm.sleep(c.sleep_time_power_supply)
        for i in range(5):
            self.run_arduino()
            time.sleep(4)
        self.finish()
        
    def read_value(self) -> None:
        #tm.sleep(c.read_delay)
        self.values.append(self.multimeter.query('READ?'))

    def finish(self) -> None:
        self.power_supply.write("OUTP OFF")
        tm.sleep(c.sleep_time_power_supply)
        self.stop_arduino()
    
    def to_data_frame(self) -> pd.core.frame.DataFrame:
        df = pd.DataFrame(self.values, columns= 'medidas')
        return df

    def run_arduino(self) -> None:
        self.arduino.send_start(int(self.input.get_data('rows'))*int(self.input.get_data('columns')), int(self.input.get_data('delay')))

    def stop_arduino(self) -> None:
        # tm.sleep(c.delay_arduino)
        self.arduino.send_stop()