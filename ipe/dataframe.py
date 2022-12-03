import pandas as pd


class Data:
    def __init__(self, data: pd.core.frame.DataFrame, number_sondas) -> None:
        self.data = data
        self.number_sondas = number_sondas
        self.trata_dados()
        self.graphic_data(2,2)
    
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

    def graphic_data(self, rows, cols):
        self.data['mod_rows'] = [(i+1) % cols for i in range(self.data.shape[0])]
        df = pd.DataFrame()
        aux = []
        grouped_measures = self.data.groupby("mod_rows")
        for element in grouped_measures:
            element[1]['mod_cols'] = [(i+1) % rows for i in range(element[1].shape[0])]
            aux_element = element[1].groupby("mod_cols")
            for item in aux_element:
                df = pd.concat([df, item[1]], ignore_index=True, axis=1)        
        df.to_csv('graphic.csv', index=False)
        pass


a = Data(pd.DataFrame({'medidas':[1,2,3,4,5,6,7,8]}), 4)