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
                sondas: int,
                arduino_port: str) -> None:
        
        self.voltagem = volts*10**(-3*dim_volt)
        self.volt_lim = volt_lim*10**(-3*dim_volt_lim)
        self.amp_lim = amperes_lim*10**(-3*dim_amp)
        self.medidas = loops*sondas
        self.sondas = sondas
        self.nome_arquivo = nome_arquivo
        self.tipo_arquivo = tipo_arquivo
        self.delay = delay
        self.arduino_port = arduino_port
    def __str__(self):
        return 'voltagem: '+str(self.voltagem)+'\n'+'volt_lim: '+str(self.volt_lim)+'\n'+'amp_lim: '+str(self.amp_lim)+'\n'+'medidas: '+str(self.medidas)+'\n'+'sondas: '+str(self.sondas)+'\n'+'nome_arquivo: '+str(self.nome_arquivo)+'\n'+'tipo_arquivo: '+str(self.tipo_arquivo)+'\n'+'delay: '+str(self.delay)+'\n'+'arduino_port: '+str(self.arduino_port)
