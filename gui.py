import tkinter as tk
import sys
import glob
import serial
import numpy as np
import serial.tools.list_ports as ports
from .input import Input, NewInput
from .table import Table
import json


class GUI:
    def __init__(self, window) -> None:
        self.entrada=0
        self.top = window
        self.new_input = NewInput()
        self.build_interface()
    def import_input(self):
        self.new_input.load_input_data()
    def save_input(self):
        self.new_input.save_input_data()
    def check_port(self):
        try:
            s = serial.Serial(self.new_input.entries["port"], timeout=0.1)
            s = serial.close()
            print('connection ok')
        except:
            self.new_input.get_data('port').set('Arduino Port')
            print('could not connect')
    
    def start(self):
        if not self.check_input_error():
            table = Table(self.top, int(self.new_input.get_data('rows')), int(self.new_input.get_data('columns')), int(self.new_input.get_data('measures')))
            print('oba')
        else:
            print('erro')
         
    def check_input_error(self):
        try:
            arduino_port = self.new_input.get_data('port')
            volts = float(self.new_input.get_data('voltage'))
            volt_lim = float(self.new_input.get_data('voltage limit'))
            cur_lim = float(self.new_input.get_data('current limit'))
            number_sondas = int(self.new_input.get_data('rows'))*int(self.new_input.get_data('columns'))
            measures = int(self.new_input.get_data('measures'))
            #output_filename = entry_outputfile.get()
            dim_volt = self.lst_voltage_dim.index(self.new_input.get_data('voltage dimension'))
            dim_volt_lim = self.lst_voltage_dim.index(self.new_input.get_data('voltage limit dimension'))
            dim_cur_lim = self.lst_current_dim.index(self.new_input.get_data('current limit dimension'))
            #tipo_arquivo = lst_outputfile_type.index(var_outputfile_type.get())
            
            delay = int(self.new_input.get_data('delay'))
            delay = max(0, min(delay, 31))
            if delay%2==0:
                delay += 1
            entry = self.new_input.get_entry('delay')
            entry.delete(0,tk.END)
            entry.insert(0, str(delay))
            self.state_indicator.config(text="Iniciando...")

        except (AttributeError,ValueError,TypeError):
            #print(e.__annotations__)
            self.state_indicator.config(text="Entrada Inválida")
            return True
        else:
            return False
    def refresh_ports(self):
            available_ports = [port for port,_,_ in sorted(ports.comports())]
            self.menu_ports["menu"].delete(0,"end")
            #print(*available_ports)
            for port in available_ports:
                try:
                    s = serial.Serial(port, timeout=0.1)
                    s.close()
                    self.menu_ports["menu"].add_command(label=port,
                                                        command= lambda var_port= self.new_input.get_data('port'),
                                                        port= port:self.new_input.get_entry('port').set(port))
                except Exception:
                    print(Exception)
            self.menu_ports["menu"].add_command(label='Refresh', command= self.refresh_ports)

    def build_interface(self):
        ### VOLTAGEM

        self.lst_voltage_dim = ["V",'mV','µV']
        label_voltage = tk.Label(self.top,text = 'DDP da fonte')
        label_voltage.grid(row=0, column=0)
        entry_voltage = tk.Entry(self.top, bd=5, width=30)
        entry_voltage.grid(row=0, column=1)
        var_voltage_dim = tk.StringVar(self.top)
        var_voltage_dim.set('Dimensão')
        menu_voltage = tk.OptionMenu(self.top,var_voltage_dim, *self.lst_voltage_dim)
        menu_voltage.grid(row=0, column=2)
        self.new_input.add_entry('voltage', entry_voltage)
        self.new_input.add_entry('voltage dimension', var_voltage_dim)

        ### LIMITE VOLTAGEM

        label_voltage_lim= tk.Label(self.top,text = 'DDP limite')
        label_voltage_lim.grid(row=1, column=0)
        entry_voltage_lim = tk.Entry(self.top, bd=5, width=30)
        entry_voltage_lim.grid(row=1, column=1)
        var_voltage_lim_dim = tk.StringVar(self.top)
        var_voltage_lim_dim.set('Dimensão')
        menu_voltage_lim = tk.OptionMenu(self.top,var_voltage_lim_dim, *self.lst_voltage_dim)
        menu_voltage_lim.grid(row=1, column=2)
        self.new_input.add_entry('voltage limit', entry_voltage_lim)
        self.new_input.add_entry('voltage limit dimension', var_voltage_lim_dim)

        ### LIMITE CORRENTE

        self.lst_current_dim = ["A",'mA','µA']
        label_current = tk.Label(self.top,text = 'Corrente limite')
        label_current.grid(row=2, column=0)
        entry_current_lim = tk.Entry(self.top, bd=5, width=30)
        entry_current_lim.grid(row=2, column=1)
        var_current_lim_dim = tk.StringVar(self.top)
        var_current_lim_dim.set('Dimensão')
        menu_current = tk.OptionMenu(self.top,var_current_lim_dim, *self.lst_current_dim)
        menu_current.grid(row=2, column=2)
        self.new_input.add_entry('current limit', entry_current_lim)
        self.new_input.add_entry('current limit dimension', var_current_lim_dim)

        ### NÚMERO DE SONDAS E MEDIÇÕES

        label_measures = tk.Label(self.top, text='Número de medições')
        label_measures.grid(row=3, column=0)
        entry_measures = tk.Entry(self.top, bd=5, width=30)
        entry_measures.grid(row=3, column=1)
        
        label_rows = tk.Label(self.top, text='Linhas')
        label_rows.grid(row=4, column=0)
        entry_rows = tk.Entry(self.top, bd=5, width=30)
        entry_rows.grid(row=4, column=1)

        label_columns = tk.Label(self.top, text='Colunas')
        label_columns.grid(row=5, column=0)
        entry_columns = tk.Entry(self.top, bd=5, width=30)
        entry_columns.grid(row=5, column=1)
        self.new_input.add_entry('measures', entry_measures)
        self.new_input.add_entry('rows', entry_rows)
        self.new_input.add_entry('columns', entry_columns)

        ### DELAY
        label_delay = tk.Label(self.top,text = 'Delay entre medições (s)')
        label_delay.grid(row=6, column=0)
        #entry_delay = tk.Scale(self.top, from_=1, to=31, orient=tk.HORIZONTAL)
        #entry_delay.set(5)
        entry_delay = tk.Entry(self.top, bd=5, width=30)
        entry_delay.grid(row=6, column=1)
        self.new_input.add_entry('delay', entry_delay)


        ### ARQUIVO DE SAIDA

        #label_outputfile = tk.Label(self.top,text = 'Arquivo de saida')
        #label_outputfile.grid(row=7, column=0)
        #entry_outputfile = tk.Entry(self.top, bd=5, width=30)
        #entry_outputfile.grid(row=7, column=1)

        #lst_outputfile_type = ["csv",'excel']
        #var_outputfile_type = tk.StringVar(self.top)
        #var_outputfile_type.set('Tipo do arquivo')
        #menu_outputfile_type = tk.OptionMenu(self.top,var_outputfile_type, *lst_outputfile_type)
        #menu_outputfile_type.grid(row=7, column=2)
        
        ### PORTA SERIAL DO ARDUINO

        #available_ports = [port for port,_,_ in sorted(ports.comports())]
        var_port = tk.StringVar(self.top)
        var_port.set('Arduino Port')
        self.menu_ports = tk.OptionMenu(self.top,var_port, 'Refresh', command=self.refresh_ports)
        self.refresh_ports()
        self.menu_ports.grid(row=8, column=1)
        self.new_input.add_entry('port', var_port)
        #self.menu_ports = tk.OptionMenu(self.top,var_port, available_ports[0], command=check_port)
        #self.menu_ports["menu"].add_command(label='Refresh', command=refresh_ports)
        #refresh_button = tk.Button(self.top, text="Refresh", bg= '#DDDDDD', width= 10, command=serial_ports)
        #refresh_button.grid(row=8, column=2)

        ### ARQUIVO DE ENTRADA

        label_inputfile = tk.Label(self.top,text = 'Importar Entradas')
        label_inputfile.grid(row=10, column=0)

        button_import = tk.Button(self.top, text= "Importar", bg= '#DDDDDD', width=10, command= self.import_input)
        button_import.grid(row=10, column=1)

        button_save = tk.Button(self.top, text= "Salvar", bg= '#DDDDDD', width=10, command= self.save_input)
        button_save.grid(row=10, column=2)

        ### BOTÃO DE START

        start_button = tk.Button(self.top, text="Iniciar", bg= '#DDDDDD', width= 10, command= self.start)
        start_button.grid(row= 12, column= 2)

        #stop_button = tk.Button(self.top, text="Parar", bg= '#DDDDDD', width= 10)
        #stop_button.grid(row= 12, column= 1)

        self.state_indicator = tk.Label(self.top, bd=5, height= 1, width = 32)
        self.state_indicator.grid(row=12, column=1)
        self.state_indicator.config(text= "Por favor, preencha as entradas.")

