import pyvisa as visa
import time as tm
import pandas as pd
from . import constantes as c
from .arduino import Arduino
from .input import Input
import serial
import time as tm
import random


class Resources:
    def __init__(self, input:Input) -> None:
        self.resources = visa.ResourceManager()
        self.multimeter = None 
        self.power_supply = None
        self.arduino = None
        self.configure_data = {}

    def configure(self, configure_data):
        self.configure_data = configure_data
        try:
            self.multimeter = self.resources.open_resource("GPIB0::22::INSTR")
            self.multimeter.query("*IDN?")
        except visa.Error:
            self.multimeter = None
            return False, "Não foi possível conectar ao multímetro"
        try:
            self.power_supply = self.resources.open_resource("USB0::0x0957::0x8B18::MY51144612::0::INSTR")
            self.power_supply.query("*IDN?")
            self.power_supply.write(f"VOLT {configure_data['voltage']}")
            self.power_supply.write(f"CURR:LIM {configure_data['current limit']}")
            self.power_supply.write(f"VOLT:LIM {configure_data['voltage limit']}")
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
        if self.power_supply is not None:
            tm.sleep(c.sleep_time_power_supply)
            
            tm.sleep(c.sleep_time_power_supply)
            self.power_supply.write("OUTP ON")
            tm.sleep(c.sleep_time_power_supply)
        #int(self.input.get_data('rows'))*int(self.input.get_data('columns'))
        #int(self.input.get_data('delay'))
        self.run_arduino()

    def run_arduino(self):
        if self.arduino is not None:
            self.arduino.send_start(self.configure_data['probes number'], self.configure_data['delay'])

    def read_value(self) -> None:
        if self.multimeter is not None:
            tm.sleep(0.9*self.configure_data['delay'])
            read =  self.multimeter.query('READ?')
            #print(read)
            tm.sleep(0.1*self.configure_data['delay'])
            return float(read)
        else:
            #await asyncio.sleep(1)
            return random.randint(1,10)
            
    def finish(self) -> None:
        if self.power_supply is not None:
            self.power_supply.write("OUTP OFF")
            tm.sleep(c.sleep_time_power_supply)
        self.stop_arduino()
    
    def to_data_frame(self) -> pd.core.frame.DataFrame:
        df = pd.DataFrame(self.values, columns= 'medidas')
        return df

    def stop_arduino(self) -> None:
        # tm.sleep(c.delay_arduino)
        if self.arduino is not None:
            self.arduino.send_stop()