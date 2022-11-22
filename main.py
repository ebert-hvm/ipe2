from gui import GUI
from resources import Resources
from dataframe import Data
import time as tm
import serial 


gui = GUI()
entry = gui.entrada
leitura = Resources(entry)
tm.sleep(1)
leitura.start(0.01, 5.0)
leitura.power_supply_setting()
for i in range(leitura.input.sondas*leitura.input.medidas):
    leitura.read_value()



df = leitura.to_data_frame()
dados = Data(df)
dados.trata_dados(leitura.input.sondas)
dados.exporta_dados(leitura.input.tipo_arquivo, leitura.input.nome_arquivo)