import pandas as pd


class Data:
    def __init__(self, data: pd.core.frame.DataFrame) -> None:
        self.data = data
    
    def trata_dados(self, number_sondas: int) -> None:
        self.data = pd.read_csv('Exports/teste3.csv', sep = ';')
        self.data.columns = ['medidas']

        self.data['mod'] = [(i+1) % number_sondas for i in range(self.data.shape[0])]
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

    def exporta_dados(self, tipo_arquivo: str, nome_arquivo: str) -> None:
        if tipo_arquivo == 'csv':
            self.data.to_csv(nome_arquivo)
        elif tipo_arquivo == 'excel':
            self.data.to_excel(nome_arquivo)