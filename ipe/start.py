from gui import GUI
from resources import Resources
import time as tm
import serial 
from .dataframe import Data
from . import constantes as c


def start(entry):
    leitura = Resources(entry)
    leitura.start()
    for i in range(leitura.input.sondas*leitura.input.medidas):
        leitura.read_value()

    df = leitura.to_data_frame()
    leitura.finish()
    dados = Data(df)
    dados.trata_dados(leitura.input.sondas)
    dados.exporta_dados(leitura.input.tipo_arquivo, leitura.input.nome_arquivo)