import pyvisa as visa
import time as tm



class Recourses:
    def __init__(self) -> None:
        self.resources = visa.ResourceManager()
        self.multimeter = self.resources.open_resource("") 
        self.power_supply = self.resources.open_resource("")
    
    def start(self, curr_lim, volt_lim) -> None:
        self.power_supply.write("OUTP ON")
        tm.sleep(5)
        self.power_supply.write(f"CURR:LIM {str(curr_lim)}")
        self.power_supply.write(f"CURR:VOLT {str(volt_lim)}")
        
    def power_supply_setting(self,volt, curr):
        pass

    def finish(self) -> None:
        tm.sleep(2)
        self.power_supply.write("OUTP OFF")