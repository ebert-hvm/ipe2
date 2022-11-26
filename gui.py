from input import Input
import tkinter as tk
import serial.tools.list_ports as ports
import sys
import glob
import serial


class GUI:
    def __init__(self, window) -> None:
        self.entrada=0
        self.top = window
        self.interface()


    def interface(self):
        
        ### PORTS COMMANDS
        def refresh_ports():
            available_ports = [port for port,_,_ in sorted(ports.comports())]
            menu_ports["menu"].delete(0,"end")
            #print(*available_ports)
            for port in available_ports:
                try:
                    s = serial.Serial(port, timeout=0.1)
                    s.close()
                    menu_ports["menu"].add_command(label=port, command= lambda label= label_ports, port= port:label.set(port))
                except Exception:
                    print(Exception)
                    pass
            menu_ports["menu"].add_command(label='Refresh', command= refresh_ports)

        ### BOTÃO DE SAÍDA
        def start():
            try:
                arduino_port = label_ports.get()
                volts = float(entry_voltagem.get())
                volt_lim = float(entry_volt_lim.get())
                amp_lim = float(entry_corrente.get())
                dim_volt = labels_voltagem.index(label_volt.get())
                dim_volt_lim = labels_volt_lim.index(label_volt_lim.get())
                dim_amp = labels_corrente.index(label_amp.get())
                number_sondas = int(entry_sondas.get())
                medidas_por_sonda = int(entry_medida.get())
                delay = int(entry_delay.get())
                delay = max(0, min(delay, 31))
                if delay%2==0:
                    delay += 1
                entry_delay.delete(0,tk.END)
                entry_delay.insert(0, str(delay))
                name_arq = entry_arq.get()
                tipo_arquivo = labels_arquivo.index(label_arquivo.get())

                self.entrada = Input(volts,
                                    volt_lim,
                                    amp_lim,
                                    dim_volt,
                                    dim_volt_lim,
                                    dim_amp,
                                    name_arq,
                                    tipo_arquivo,
                                    delay,
                                    loops=medidas_por_sonda,
                                    sondas=number_sondas,
                                    arduino_port=arduino_port)
                msg.config(text="Iniciando...")
                print(self.entrada)
            except Exception as e:
                print(e)
                msg.config(text="Entrada Inválida")
                pass
            #self.top.destroy()

        ### PORTA SERIAL DO ARDUINO
        available_ports = [port for port,_,_ in sorted(ports.comports())]
        label_ports = tk.StringVar(self.top)
        label_ports.set('Arduino Port')
        menu_ports = tk.OptionMenu(self.top,label_ports, *available_ports)
        menu_ports["menu"].add_command(label='Refresh', command=refresh_ports)
        menu_ports.grid(row=8, column=1)
        #refresh_button = tk.Button(self.top, text="Refresh", bg= '#DDDDDD', width= 10, command=serial_ports)
        #refresh_button.grid(row=8, column=2)

        ### VOLTAGEM

        label_voltagem = tk.Label(self.top,text = 'DDP da fonte')
        label_voltagem.grid(row=0, column=0)
        entry_voltagem = tk.Entry(self.top, bd=5, width=30)
        entry_voltagem.grid(row=0, column=1)
        labels_voltagem = ["V",'mV','µV']
        label_volt = tk.StringVar(self.top)
        label_volt.set('Dimensão')
        menu_volt = tk.OptionMenu(self.top,label_volt, *labels_voltagem)
        menu_volt.grid(row=0, column=2)


        ### LIMITE VOLTAGEM

        label_volt_lim= tk.Label(self.top,text = 'DDP limite')
        label_volt_lim.grid(row=1, column=0)
        entry_volt_lim = tk.Entry(self.top, bd=5, width=30)
        entry_volt_lim.grid(row=1, column=1)
        labels_volt_lim = ["V",'mV','µV']
        label_volt_lim = tk.StringVar(self.top)
        label_volt_lim.set('Dimensão')
        menu_volt_lim = tk.OptionMenu(self.top,label_volt_lim, *labels_voltagem)
        menu_volt_lim.grid(row=1, column=2)


        ### LIMITE CORRENTE

        label_corrente = tk.Label(self.top,text = 'Corrente limite')
        label_corrente.grid(row=2, column=0)
        entry_corrente = tk.Entry(self.top, bd=5, width=30)
        entry_corrente.grid(row=2, column=1)
        labels_corrente = ["A",'mA','µA']
        label_amp = tk.StringVar(self.top)
        label_amp.set('Dimensão')
        menu_corrente = tk.OptionMenu(self.top,label_amp, *labels_corrente)
        menu_corrente.grid(row=2, column=2)


        ### NÚMERO DE SONDAS E MEDIÇÕES

        label_medidas = tk.Label(self.top, text='Número de medidas')
        label_medidas.grid(row=4, column=0)
        entry_medida = tk.Entry(self.top, bd=5, width=30)
        entry_medida.grid(row=4, column=1)
        
        label_sondas = tk.Label(self.top, text='Número de sondas')
        label_sondas.grid(row=5, column=0)
        entry_sondas = tk.Entry(self.top, bd=5, width=30)
        entry_sondas.grid(row=5, column=1)


        ### DELAY
        label_delay = tk.Label(self.top,text = 'Delay entre medidas (s)')
        label_delay.grid(row=6, column=0)
        #entry_delay = tk.Scale(self.top, from_=1, to=31, orient=tk.HORIZONTAL)
        #entry_delay.set(5)
        entry_delay = tk.Entry(self.top, bd=5, width=30)
        entry_delay.grid(row=6, column=1)


        ### ARQUIVO DE SAIDA

        label_arq = tk.Label(self.top,text = 'Arquivo de saida')
        label_arq.grid(row=7, column=0)
        entry_arq = tk.Entry(self.top, bd=5, width=30)
        entry_arq.grid(row=7, column=1)

        labels_arquivo = ["csv",'excel']
        label_arquivo = tk.StringVar(self.top)
        label_arquivo.set('Tipo do arquivo')
        menu_arquivo = tk.OptionMenu(self.top,label_arquivo, *labels_arquivo)
        menu_arquivo.grid(row=7, column=2)


        ### BOTÃO DE START

        start_button = tk.Button(self.top, text="Iniciar", bg= '#DDDDDD', width= 10, command=start)
        start_button.grid(row= 12, column= 2)
        msg = tk.Label(self.top, bd=5, height= 1, width = 32)
        msg.grid(row=12, column=1)
        msg.config(text= "Por favor, preencha as entradas.")


