import pyvisa as visa
from input import Input
import time as tm
import pandas as pd
import constantes as c
import arduino


class Resources:
    def __init__(self, entrada: Input) -> None:
        self.resources = visa.ResourceManager()
        self.multimeter = self.resources.open_resource("GPIB0::22::INSTR") 
        self.power_supply = self.resources.open_resource("USB0::0x0957::0x8B18::MY51144612::0::INSTR")
        self.values = []
        self.input = entrada
        self.configure_arduino()
        
    def start(self) -> None:
        self.power_supply.write(f"VOLT {str(self.input.voltagem)}")
        self.power_supply.write(f"CURR:LIM {str(self.input.amp_lim)}")
        self.power_supply.write(f"VOLT:LIM {str(self.input.volt_lim)}")
        tm.sleep(c.sleep_time_power_supply)
        self.power_supply.write("OUTP ON")
        self.run_arduino()
        
    def read_value(self) -> None:
        #tm.sleep(c.read_delay)
        self.values.append(self.multimeter.query('READ?'))

    def finish(self) -> None:
        self.power_supply.write("OUTP OFF")
        tm.sleep(c.sleep_time_power_supply)
    
    def to_data_frame(self) -> pd.core.frame.DataFrame:
        df = pd.DataFrame(self.values, columns= 'medidas')
        return df

    def configure_arduino(self) -> None:
        self.arduino = arduino.Arduino(port= self.input.arduino_port,
                                        baudrate=c.baudrate,
                                        probes_number= self.input.sondas,
                                        time_delay= self.input.delay)

    def run_arduino(self) -> None:
        self.arduino.send_start()

    def stop_arduino(self) -> None:
        # tm.sleep(c.delay_arduino)
        self.arduino.send_stop()