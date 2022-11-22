from gui import GUI
from input import Input
from resources import Resources
from dataframe import Data
import pandas as pd
import tkinter as tk
import time as tm


gui = GUI()
entry = gui.entrada
leitura = Resources(entry)
tm.sleep(1)
leitura.start(0.01, 5.0)
leitura.power_supply_setting()



# df = 
# dados = Data(df)