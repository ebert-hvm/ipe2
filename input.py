import json

class NewInput():
    def __init__(self):
        self.input_data = {}
        self.entries = {}

    def add_input_to_data(self, key, val):
        self.input_data[key] = val

    def add_entry(self, key, val):
        self.entries[key] = val
        self.add_input_to_data(key, val.get())

    def __update_element(self, key):
        self.input_data[key] = self.entries[key].get()

    def update_input_data(self):
        for key in self.entries.keys():
            self.__update_element(key)

    def get_data(self, key):
        self.__update_element(key)
        return self.input_data[key]
    
    def get_entry(self, key):
        return self.entries[key]

    def save_input_data(self):
        with open("input_save.json", "w") as outfile:
            json.dump(self.input_data, outfile)
            
    def load_input_data(self):
        with open('input_save.json', 'r') as openfile:
            self.input_data = json.load(openfile)
            for key in self.input_data.keys():
                self.entries[key].set(self.input_data[key])

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
        self.loops = loops
        self.sondas = sondas
        self.nome_arquivo = nome_arquivo
        self.tipo_arquivo = tipo_arquivo
        self.delay = delay
        self.arduino_port = arduino_port
    def __str__(self):
        str1 = 'voltagem: '+str(self.voltagem)+'\n'
        str2 = 'volt_lim: '+str(self.volt_lim)+'\n'
        str3 = 'amp_lim: '+str(self.amp_lim)+'\n'
        str4 = 'medidas: '+str(self.loops)+'\n'
        str5 = 'sondas: '+str(self.sondas)+'\n'
        str6 = 'nome_arquivo: '+str(self.nome_arquivo)+'\n'
        str7 = 'tipo_arquivo: '+str(self.tipo_arquivo)+'\n'
        str8 = 'tipo_arquivo: '+str(self.tipo_arquivo)+'\n'
        str9 = 'delay: '+str(self.delay)+'\n'
        str10 = 'arduino_port: '+str(self.arduino_port)
        return str1 + str2 + str3 + str4 + str5 + str6 + str7 + str8 + str9 + str10
