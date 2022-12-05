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
from .graphic import Graphic
from . import constantes as c
import json
import asyncio


class GUI:
    def __init__(self, loop) -> None:
        self.loop = loop
        self.root = tk.Tk()
        self.input = Input()
        self.table = None
        self.graph = None
        self.resources = Resources(self.input)
        self.configure_data = {}
        self.close_windows = 0
        self.start_trigger = 0
        self.build_interface()
        #self.arduino = None
    
    def import_input(self):
        self.input.load_input_data()

    def save_input(self):
        self.input.save_input_data()
    

    def check_input_error(self):
        try:
            delay = int(self.input.get_data('delay'))
            delay = max(0, min(delay, 31))
            if delay%2==0:
                delay += 1
            self.input.set_data('delay', delay)
            
            self.configure_data['delay'] = int(self.input.get_data('delay'))
            self.configure_data['voltage'] = float(self.input.get_data('voltage'))*10**(-3*self.lst_voltage_dim.index(self.input.get_data('voltage dimension')))
            self.configure_data['voltage limit'] = float(self.input.get_data('voltage limit'))*10**(-3*self.lst_voltage_dim.index(self.input.get_data('voltage limit dimension')))
            self.configure_data['current limit'] = float(self.input.get_data('current limit'))*10**(-3*self.lst_current_dim.index(self.input.get_data('current limit dimension')))
            self.configure_data['rows'] = int(self.input.get_data('rows'))
            self.configure_data['columns'] = int(self.input.get_data('columns'))
            self.configure_data['probes number'] = int(self.input.get_data('rows'))*int(self.input.get_data('columns'))
            self.configure_data['measures'] = int(self.input.get_data('measures'))
            self.configure_data['probes distance'] = int(self.input.get_data('probes distance'))
            self.configure_data['probes end distance'] = int(self.input.get_data('probes end distance'))
            #output_filename = entry_outputfile.get()
            #tipo_arquivo = lst_outputfile_type.index(var_outputfile_type.get())
                
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
            if self.configure_data['probes number'] > 16:
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

    async def start(self):
        if not self.start_trigger:
            self.start_trigger = 1
            if not self.check_input_error():
                resources_ok, label = self.resources.configure(self.configure_data)
                self.state_indicator.config(text=label)
                if resources_ok or 1==1:
                    #self.async_tasks(label)
                    self.state_indicator.config(text=label)
                    if self.table is not None:
                        self.table.remove_from_grid()
                    self.table = Table(self.root, self.configure_data)
                    #table.write_cell(2, 0, 0, 0)
                    await asyncio.sleep(0.5)
                    self.resources.start()
                    for m in range(self.configure_data['measures']):
                        for i in range(self.configure_data['rows']):
                            for j in range(self.configure_data['columns']):
                                await asyncio.sleep(0.9*self.configure_data['delay'])
                                self.state_indicator.config(text=f"Medida : {m}\nSonda: {i*self.configure_data['columns']+j}")
                                self.table.write_cell(self.resources.read_value(), m, i, j)
                                await asyncio.sleep(0.1*self.configure_data['delay'])
                    self.resources.finish()
                    self.graph = Graphic(self.table.tables, self.configure_data)
                    self.graph.set_axis()
                    self.state_indicator.config(text= 'Completo')
            self.start_trigger = 0

    def on_closing(self):
       # if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
        self.close_windows = 1
        self.root.destroy()

    async def show(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        while not self.close_windows:
            #self.label["text"] = self.animation
            #self.animation = self.animation[1:] + self.animation[0]
            self.root.update()
            await asyncio.sleep(.1)

    # async def async_tasks(self,label):
    #     #async with asyncio.TaskGroup() as tg:
    #     task1 = asyncio.create_task(self.print_table(label))
    #     task2 = asyncio.create_task(self.run_resources())
    #     await asyncio.gather(task1, task2)

    # async def print_table(self,label):
    #     self.state_indicator.config(text=label)
    #     self.table = Table(self.root, self.configure_data)    


    # async def run_resources(self):
    #     self.resources.start()
    #     for m in range(self.configure_data['measures']):
    #         self.resources.run_arduino()
    #         for i in range(self.configure_data['rows']):
    #             for j in range(self.configure_data['columns']):
    #                 self.state_indicator.config(text=f"Medida : {m}\nSonda: {i*self.configure_data['columns']+j}")
    #                 self.table.write_cell(self.resources.read_value(), m, i, j)
    #     self.resources.finish()
    #     self.state_indicator.config(text= 'Completo')

                    
    def build_interface(self):
        ### VOLTAGEM

        self.lst_voltage_dim = ["V",'mV','µV']
        label_voltage = tk.Label(self.root,text = 'DDP da fonte')
        label_voltage.grid(row=0, column=0)
        var_voltage = tk.StringVar(self.root)
        entry_voltage = tk.Entry(self.root, textvariable= var_voltage, bd=5, width=30)
        entry_voltage.grid(row=0, column=1)
        var_voltage_dim = tk.StringVar(self.root)
        var_voltage_dim.set('Dimensão')
        menu_voltage = tk.OptionMenu(self.root,var_voltage_dim, *self.lst_voltage_dim)
        menu_voltage.grid(row=0, column=2)
        self.input.add_var('voltage', var_voltage)
        self.input.add_var('voltage dimension', var_voltage_dim)

        ### LIMITE VOLTAGEM

        label_voltage_lim= tk.Label(self.root,text = 'DDP limite')
        label_voltage_lim.grid(row=1, column=0)
        var_voltage_lim = tk.StringVar(self.root)
        entry_voltage_lim = tk.Entry(self.root, textvariable= var_voltage_lim, bd=5, width=30)
        entry_voltage_lim.grid(row=1, column=1)
        var_voltage_lim_dim = tk.StringVar(self.root)
        var_voltage_lim_dim.set('Dimensão')
        menu_voltage_lim = tk.OptionMenu(self.root,var_voltage_lim_dim, *self.lst_voltage_dim)
        menu_voltage_lim.grid(row=1, column=2)
        self.input.add_var('voltage limit', var_voltage_lim)
        self.input.add_var('voltage limit dimension', var_voltage_lim_dim)

        ### LIMITE CORRENTE

        self.lst_current_dim = ["A",'mA','µA']
        label_current = tk.Label(self.root,text = 'Corrente limite')
        label_current.grid(row=2, column=0)
        var_current_lim = tk.StringVar(self.root)
        entry_current_lim = tk.Entry(self.root, textvariable= var_current_lim, bd=5, width=30)
        entry_current_lim.grid(row=2, column=1)
        var_current_lim_dim = tk.StringVar(self.root)
        var_current_lim_dim.set('Dimensão')
        menu_current = tk.OptionMenu(self.root,var_current_lim_dim, *self.lst_current_dim)
        menu_current.grid(row=2, column=2)
        self.input.add_var('current limit', var_current_lim)
        self.input.add_var('current limit dimension', var_current_lim_dim)

        ### NÚMERO DE SONDAS E MEDIÇÕES
        var_measures = tk.StringVar(self.root)
        var_rows = tk.StringVar(self.root)
        var_columns = tk.StringVar(self.root)

        label_measures = tk.Label(self.root, text='Número de medições')
        label_measures.grid(row=3, column=0)
        entry_measures = tk.Entry(self.root, bd=5, width=30, textvariable= var_measures)
        entry_measures.grid(row=3, column=1)
        
        label_rows = tk.Label(self.root, text='Linhas')
        label_rows.grid(row=4, column=0)
        entry_rows = tk.Entry(self.root, bd=5, width=30, textvariable= var_rows)
        entry_rows.grid(row=4, column=1)

        label_columns = tk.Label(self.root, text='Colunas')
        label_columns.grid(row=5, column=0)
        entry_columns = tk.Entry(self.root, bd=5, width=30, textvariable= var_columns)
        entry_columns.grid(row=5, column=1)
        self.input.add_var('measures', var_measures)
        self.input.add_var('rows', var_rows)
        self.input.add_var('columns', var_columns)

        ### DELAY
        label_delay = tk.Label(self.root,text = 'Delay entre medições (s)')
        label_delay.grid(row=6, column=0)
        #entry_delay = tk.Scale(self.root, from_=1, to=31, orient=tk.HORIZONTAL)
        #entry_delay.set(5)
        var_delay = tk.StringVar(self.root)
        entry_delay = tk.Entry(self.root, bd=5, width=30, textvariable= var_delay)
        entry_delay.grid(row=6, column=1)
        self.input.add_var('delay', var_delay)

        var_probes_dist = tk.StringVar(self.root)
        label_probes_dist = tk.Label(self.root, text='Distância entre as sondas (mm)')
        label_probes_dist.grid(row=7, column=0)
        entry_probes_dist = tk.Entry(self.root, bd=5, width=30, textvariable= var_probes_dist)
        entry_probes_dist.grid(row=7, column=1)
        self.input.add_var('probes distance', var_probes_dist)

        var_probes_end_dist = tk.StringVar(self.root)
        label_probes_end_dist = tk.Label(self.root, text='Distância entre as pontas da sonda (mm)')
        label_probes_end_dist.grid(row=8, column=0)
        entry_probes_end_dist = tk.Entry(self.root, bd=5, width=30, textvariable= var_probes_end_dist)
        entry_probes_end_dist.grid(row=8, column=1)
        self.input.add_var('probes end distance', var_probes_end_dist)
        ### ARQUIVO DE SAIDA

        #label_outputfile = tk.Label(self.root,text = 'Arquivo de saida')
        #label_outputfile.grid(row=7, column=0)
        #entry_outputfile = tk.Entry(self.root, bd=5, width=30)
        #entry_outputfile.grid(row=7, column=1)

        #lst_outputfile_type = ["csv",'excel']
        #var_outputfile_type = tk.StringVar(self.root)
        #var_outputfile_type.set('Tipo do arquivo')
        #menu_outputfile_type = tk.OptionMenu(self.root,var_outputfile_type, *lst_outputfile_type)
        #menu_outputfile_type.grid(row=7, column=2)
                
        ### PORTA SERIAL DO ARDUINO

        #available_ports = [port for port,_,_ in sorted(ports.comports())]
        self.arduino_indicator = tk.Label(self.root, text= 'Selecione a porta.')
        self.arduino_indicator.grid(row=9, column=0)
        var_port = tk.StringVar(self.root)
        var_port.set('Arduino Port')
        self.menu_ports = tk.OptionMenu(self.root,var_port, 'Refresh', command=self.refresh_ports)
        self.refresh_ports(init=True)
        self.menu_ports.grid(row=9, column=1)
        self.input.add_var('port', var_port)
        #self.menu_ports = tk.OptionMenu(self.root,var_port, available_ports[0], command=check_port)
        #self.menu_ports["menu"].add_command(label='Refresh', command=refresh_ports)
        #refresh_button = tk.Button(self.root, text="Refresh", bg= '#DDDDDD', width= 10, command=serial_ports)
        #refresh_button.grid(row=8, column=2)

        ### ARQUIVO DE ENTRADA

        label_inputfile = tk.Label(self.root,text = 'Importar Entradas')
        label_inputfile.grid(row=10, column=0)

        button_import = tk.Button(self.root,
            text= "Importar",
            bg= '#DDDDDD',
            width=10,
            command= lambda:self.import_input())
        button_import.grid(row=10, column=1)

        button_save = tk.Button(self.root, text= "Salvar", bg= '#DDDDDD', width=10, command= self.save_input)
        button_save.grid(row=10, column=2)

        ### BOTÃO DE START

        start_button = tk.Button(self.root, text="Iniciar", bg= '#DDDDDD', width= 10, command= lambda: self.loop.create_task(self.start()))
        start_button.grid(row= 12, column= 2)

        #stop_button = tk.Button(self.root, text="Parar", bg= '#DDDDDD', width= 10)
        #stop_button.grid(row= 12, column= 1)

        self.state_indicator = tk.Label(self.root, bd=5, height= 1, width = 32)
        self.state_indicator.grid(row=12, column=1)
        self.state_indicator.config(text= "Por favor, preencha as entradas.")

