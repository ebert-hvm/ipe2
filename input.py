class Input:
    def __init__(self, 
                volts: float,
                amperes: float,
                dim_volt: int, 
                dim_amp: int, 
                amostra_circular: bool, 
                amostra_condutor: bool,
                nome_arquivo: str,
                tipo_arquivo: int,
                loops: int,
                sondas: int) -> None:
        
        self.voltagem = volts
        self.corrente = amperes
        self.unidade_volt = dim_volt
        self.unidade_corrente = dim_amp
        self.tipo_da_amostra = self.tipo_amostra(amostra_circular, amostra_condutor)
        self.medidas = loops*sondas
        self.sondas = sondas
        self.nome_arquivo = nome_arquivo
        self.tipo_arquivo = tipo_arquivo

    def tipo_amostra(self, tipo_amostra_1: bool, tipo_amostra_condutor: bool) -> int:
        tipo = 0
        if tipo_amostra_1:
            tipo += 1
        if tipo_amostra_condutor:
            tipo += 2
        return tipo
