import tkinter as tk
import sys
import glob
import serial
import numpy as np
import serial.tools.list_ports as ports
from .arduino import Arduino
from .input import Input
from .table import Table
from .resources import Resources
from . import constantes as c
import json


class GUI:
    def __init__(self, window) -> None:
        self.top = window
        self.input = Input()
        self.resources = Resources(self.input)
        self.build_interface()
        #self.arduino = None
    
    def import_input(self):
        self.input.load_input_data()

    def save_input(self):
        self.input.save_input_data()
    
    def start(self):
        resources_ok, label = self.resources.configure()
        if not self.check_input_error():
            self.state_indicator.config(text=label)
            if resources_ok:
                self.state_indicator.config(text=label)
                table = Table(self.top, int(self.input.get_data('rows')), int(self.input.get_data('columns')), int(self.input.get_data('measures')))
                self.resources.start()

    def check_input_error(self):
        try:
            arduino_port = self.input.get_data('port')
            volts = float(self.input.get_data('voltage'))
            volt_lim = float(self.input.get_data('voltage limit'))
            cur_lim = float(self.input.get_data('current limit'))
            number_sondas = int(self.input.get_data('rows'))*int(self.input.get_data('columns'))
            measures = int(self.input.get_data('measures'))
            #output_filename = entry_outputfile.get()
            dim_volt = self.lst_voltage_dim.index(self.input.get_data('voltage dimension'))
            dim_volt_lim = self.lst_voltage_dim.index(self.input.get_data('voltage limit dimension'))
            dim_cur_lim = self.lst_current_dim.index(self.input.get_data('current limit dimension'))
            #tipo_arquivo = lst_outputfile_type.index(var_outputfile_type.get())
            
            delay = int(self.input.get_data('delay'))
            delay = max(0, min(delay, 31))
            if delay%2==0:
                delay += 1
            self.input.set_data('delay', delay)

        except ValueError:
            self.state_indicator.config(text="value error")
            return True
        except TypeError:
            self.state_indicator.config(text="type error")
            return True
        except AttributeError:
            self.state_indicator.config(text="attribute error")
            return True
        else:
            if number_sondas > 16:
                self.state_indicator.config(text="O número de sondas máximo é 16")
                return True
            return False
    
    def port_select(self, port):
        self.input.set_data('port', port)
        self.arduino_indicator.config(text="conectando...")
        self.arduino_indicator.config(text=self.resources.connect_arduino(port))


    def refresh_ports(self, init=False):
            available_ports = [port for port,_,_ in sorted(ports.comports())]
            self.menu_ports["menu"].delete(0,"end")
            #print(*available_ports)
            for port in available_ports:
                try:
                    if not init:
                        s = serial.Serial(port, timeout=0.1)
                        s.close()
                    self.menu_ports["menu"].add_command(label=port, command= lambda port= port:self.port_select(port))
                except Exception:
                    pass
                    #print(Exception)
            self.menu_ports["menu"].add_command(label='Refresh', command= self.refresh_ports)

    def build_interface(self):
        ### VOLTAGEM

        self.lst_voltage_dim = ["V",'mV','µV']
        label_voltage = tk.Label(self.top,text = 'DDP da fonte')
        label_voltage.grid(row=0, column=0)
        var_voltage = tk.StringVar(self.top)
        entry_voltage = tk.Entry(self.top, textvariable= var_voltage, bd=5, width=30)
        entry_voltage.grid(row=0, column=1)
        var_voltage_dim = tk.StringVar(self.top)
        var_voltage_dim.set('Dimensão')
        menu_voltage = tk.OptionMenu(self.top,var_voltage_dim, *self.lst_voltage_dim)
        menu_voltage.grid(row=0, column=2)
        self.input.add_var('voltage', var_voltage)
        self.input.add_var('voltage dimension', var_voltage_dim)

        ### LIMITE VOLTAGEM

        label_voltage_lim= tk.Label(self.top,text = 'DDP limite')
        label_voltage_lim.grid(row=1, column=0)
        var_voltage_lim = tk.StringVar(self.top)
        entry_voltage_lim = tk.Entry(self.top, textvariable= var_voltage_lim, bd=5, width=30)
        entry_voltage_lim.grid(row=1, column=1)
        var_voltage_lim_dim = tk.StringVar(self.top)
        var_voltage_lim_dim.set('Dimensão')
        menu_voltage_lim = tk.OptionMenu(self.top,var_voltage_lim_dim, *self.lst_voltage_dim)
        menu_voltage_lim.grid(row=1, column=2)
        self.input.add_var('voltage limit', var_voltage_lim)
        self.input.add_var('voltage limit dimension', var_voltage_lim_dim)

        ### LIMITE CORRENTE

        self.lst_current_dim = ["A",'mA','µA']
        label_current = tk.Label(self.top,text = 'Corrente limite')
        label_current.grid(row=2, column=0)
        var_current_lim = tk.StringVar(self.top)
        entry_current_lim = tk.Entry(self.top, textvariable= var_current_lim, bd=5, width=30)
        entry_current_lim.grid(row=2, column=1)
        var_current_lim_dim = tk.StringVar(self.top)
        var_current_lim_dim.set('Dimensão')
        menu_current = tk.OptionMenu(self.top,var_current_lim_dim, *self.lst_current_dim)
        menu_current.grid(row=2, column=2)
        self.input.add_var('current limit', var_current_lim)
        self.input.add_var('current limit dimension', var_current_lim_dim)

        ### NÚMERO DE SONDAS E MEDIÇÕES
        var_measures = tk.StringVar(self.top)
        var_rows = tk.StringVar(self.top)
        var_columns = tk.StringVar(self.top)

        label_measures = tk.Label(self.top, text='Número de medições')
        label_measures.grid(row=3, column=0)
        entry_measures = tk.Entry(self.top, bd=5, width=30, textvariable= var_measures)
        entry_measures.grid(row=3, column=1)
        
        label_rows = tk.Label(self.top, text='Linhas')
        label_rows.grid(row=4, column=0)
        entry_rows = tk.Entry(self.top, bd=5, width=30, textvariable= var_rows)
        entry_rows.grid(row=4, column=1)

        label_columns = tk.Label(self.top, text='Colunas')
        label_columns.grid(row=5, column=0)
        entry_columns = tk.Entry(self.top, bd=5, width=30, textvariable= var_columns)
        entry_columns.grid(row=5, column=1)
        self.input.add_var('measures', var_measures)
        self.input.add_var('rows', var_rows)
        self.input.add_var('columns', var_columns)

        ### DELAY
        label_delay = tk.Label(self.top,text = 'Delay entre medições (s)')
        label_delay.grid(row=6, column=0)
        #entry_delay = tk.Scale(self.top, from_=1, to=31, orient=tk.HORIZONTAL)
        #entry_delay.set(5)
        var_delay = tk.StringVar(self.top)
        entry_delay = tk.Entry(self.top, bd=5, width=30, textvariable= var_delay)
        entry_delay.grid(row=6, column=1)
        self.input.add_var('delay', var_delay)


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
        self.arduino_indicator = tk.Label(self.top, text= 'Selecione a porta.')
        self.arduino_indicator.grid(row=8, column=0)
        var_port = tk.StringVar(self.top)
        var_port.set('Arduino Port')
        self.menu_ports = tk.OptionMenu(self.top,var_port, 'Refresh', command=self.refresh_ports)
        self.refresh_ports(init=True)
        self.menu_ports.grid(row=8, column=1)
        self.input.add_var('port', var_port)
        #self.menu_ports = tk.OptionMenu(self.top,var_port, available_ports[0], command=check_port)
        #self.menu_ports["menu"].add_command(label='Refresh', command=refresh_ports)
        #refresh_button = tk.Button(self.top, text="Refresh", bg= '#DDDDDD', width= 10, command=serial_ports)
        #refresh_button.grid(row=8, column=2)

        ### ARQUIVO DE ENTRADA

        label_inputfile = tk.Label(self.top,text = 'Importar Entradas')
        label_inputfile.grid(row=10, column=0)

        button_import = tk.Button(self.top,
            text= "Importar",
            bg= '#DDDDDD',
            width=10,
            command= lambda:self.import_input())
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

