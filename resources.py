import pyvisa as visa
from input import Input
import time as tm
import pandas as pd


class Resources:
    def __init__(self, entrada: Input) -> None:
        self.resources = visa.ResourceManager()
        self.multimeter = self.resources.open_resource("GPIB0::22::INSTR") 
        self.power_supply = self.resources.open_resource("USB0::0x0957::0x8B18::MY51144612::0::INSTR")
        self.values = []
        self.input = entrada
    
    def start(self, curr_lim: float, volt_lim: float) -> None:
        self.power_supply.write("OUTP ON")
        tm.sleep(2)
        self.power_supply.write(f"CURR:LIM {str(curr_lim)}")
        self.power_supply.write(f"VOLT:LIM {str(volt_lim)}")
        
    def power_supply_setting(self) -> None:
        self.power_supply.write(f"VOLT {str(self.input.volts)}")
        self.power_supply.write(f"CURR {str(self.input.amperes)}")

    def read_value(self) -> None:
        self.values.append(self.multimeter.query('READ?'))

    def finish(self) -> None:
        tm.sleep(2)
        self.power_supply.write("OUTP OFF")
    
    def to_data_frame(self) -> pd.core.frame.DataFrame:
        df = pd.DataFrame(self.values, columns= 'medidas')
        return df