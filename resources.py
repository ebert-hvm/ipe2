import pyvisa as visa
import time as tm
import pandas as pd


class Resources:
    def __init__(self) -> None:
        self.resources = visa.ResourceManager()
        self.multimeter = self.resources.open_resource("GPIB0::22::INSTR") 
        self.power_supply = self.resources.open_resource("USB0::0x0957::0x8B18::MY51144612::0::INSTR")
        values = []
    
    def start(self, curr_lim: float, volt_lim: float) -> None:
        self.power_supply.write("OUTP ON")
        tm.sleep(5)
        self.power_supply.write(f"CURR:LIM {str(curr_lim)}")
        self.power_supply.write(f"VOLT:LIM {str(volt_lim)}")
        
    def power_supply_setting(self,volt: float, curr: float) -> None:
        self.power_supply.write(f"VOLT {str(volt)}")
        self.power_supply.write(f"CURR {str(curr)}")

    def read_value(self) -> None:
        self.values.append(self.multimeter.query('READ?'))

    def finish(self) -> None:
        tm.sleep(2)
        self.power_supply.write("OUTP OFF")
    
    def to_data_frame(self):
        df = pd.DataFrame(self.values, columns= 'medidas')
        return df