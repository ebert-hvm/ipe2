class Input:
    def __init__(self, 
                volts: float,
                volt_lim: float,
                amperes_lim: float,
                dim_volt: int, 
                dim_volt_lim: int,
                dim_amp: int, 
                nome_arquivo: str,
                tipo_arquivo: int,
                delay: int,
                loops: int,
                sondas: int) -> None:
        
        self.voltagem = volts*10**(-3*dim_volt)
        self.volt_lim = volt_lim*10**(-3*dim_volt_lim)
        self.amp_lim = amperes_lim*10**(-3*dim_amp)
        self.medidas = loops*sondas
        self.sondas = sondas
        self.nome_arquivo = nome_arquivo
        self.tipo_arquivo = tipo_arquivo
        self.delay = delay
