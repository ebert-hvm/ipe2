import pandas as pd
import numpy as np


number_sondas = 2

data = pd.read_csv('Exports/teste3.csv', sep = ';')
measures = data['Unnamed: 5']
measures.dropna(inplace=True)
measures = measures.to_frame()
measures.index = [i for i in range(measures.shape[0])]
measures.columns = ['medidas']
measures.drop(inplace=True, index=0)

measures['mod'] = [(i+1) % number_sondas for i in range(measures.shape[0])]
df = pd.DataFrame()
grouped_measures = measures.groupby("mod")
for element in grouped_measures:
    element[1].index = [i for i in range(element[1].shape[0])]
    df = pd.concat([df, element[1].medidas], ignore_index=True, axis= 1)

colunas = {}
medida = {}
for i in range(df.shape[0]):
    medida[i] = f'medida {i+1}'
for i in range(df.shape[1]):
    colunas[i] = f'sonda {i+1}'
df.rename(columns=colunas, index=medida, inplace=True)

df.to_csv('saida')
