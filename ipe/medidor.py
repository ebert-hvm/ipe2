import pyvisa as pv
import pandas as pd
import time as tm
import serial

resources = pv.ResourceManager()
multimeter = resources.open_resource('GPIB0::22::INSTR')
f = resources.open_resource('USB0::0x0957::0x8B18::MY51144612::0::INSTR')
f.write("CURR:LIM .01")
f.write("VOLT:LIM 5")
f.write("VOLT 5.0")



# medidas = []

t0=t1=tm.time()
while True:
    s = input()
    if s == 's':
        break
    if s == 'o':
        f.write("OUTP ON")
    if s == 'f':
        f.write("OUTP OFF")
    t1=tm.time()
    if t1-t0>5:
        print(multimeter.query('READ?'))
        t0=tm.time()


    

# keysight.write("CURR:LIM .5, (@1)")
# keysight.write("VOLT:LIM 30, (@1)")
# keysight.write("VOLT 10, (@1)")
# keysight.write("CURR 1, (@1)")
# keysight.write("OUTP ON,(@1)")


# valores = pd.DataFrame(medidas, columns = 'medidas')


