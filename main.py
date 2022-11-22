from gui import GUI
from resources import Resources
from dataframe import Data
import time as tm
import constantes as c
import serial 


gui = GUI()
entry = gui.entrada
leitura = Resources(entry)
tm.sleep(1)
leitura.start(curr_lim= c.limit_current, volt_lim= c.limit_volt)
leitura.power_supply_setting()
for i in range(leitura.input.sondas*leitura.input.medidas):
    leitura.read_value()



df = leitura.to_data_frame()
leitura.finish()
dados = Data(df)
dados.trata_dados(leitura.input.sondas)
dados.exporta_dados(leitura.input.tipo_arquivo, leitura.input.nome_arquivo)