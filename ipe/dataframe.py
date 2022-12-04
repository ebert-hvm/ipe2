import pandas as pd
import numpy as np


class Data:
    def __init__(self, data: pd.core.frame.DataFrame, number_sondas,cols) -> None:
        self.data = data
        self.measures= self.data.shape[0] 
        self.number_sondas = number_sondas
        self.trata_dados()
        self.graphic_data(cols)

    def trata_dados(self) -> None:
        self.data['mod'] = [(i+1) % self.number_sondas for i in range(self.data.shape[0])]
        df = pd.DataFrame()
        grouped_measures = self.data.groupby("mod")
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
        df.index.name = 'medidas'
        self.data = df

    def exporta_dados(self, tipo_arquivo: int, nome_arquivo: str) -> None:
        if tipo_arquivo == 0:
            self.data.to_csv(nome_arquivo)
        elif tipo_arquivo == 1:
            self.data.to_excel(nome_arquivo)

    def graphic_data(self, cols):
        print(self.data)
        aux = self.data.to_numpy()
        number = int(np.sqrt(self.number_sondas))
        shape = (cols,cols)
        guard = []
        for element in self.data.columns:
            guard.append(np.zeros((cols,cols)))

        aux_arr = []
        for i in range(len(aux[0])):
            for element in aux:
                aux_arr.append(element[i])
            aux_array = np.array(aux_arr)
            aux_array = aux_array.reshape(shape)
            guard[i] = aux_array
            aux_arr = []
        guard = np.array(guard)
        guard = guard.reshape((number,number,cols,cols))
        print(guard)

        
       

dic = {'medidas': [i for i in range(3**4)]}
df = pd.DataFrame(dic)

obj = Data(df, 3, 3)




