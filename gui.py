from input import Input
import tkinter as tk


class GUI:
    def __init__(self) -> None:
        self.entrada=0
        self.interface()


    def interface(self):
        
        ### BOTÃO DE SAÍDA

        def saida():
            volts = entry_voltagem.get()
            if volts != '':
                volts = float(volts)
            else:
                volts = 0.0

            volt_lim = entry_volt_lim.get()
            if volts != '':
                volt_lim = float(volt_lim)
            else:
                volt_lim = 5.0

            amp_lim = entry_corrente.get()
            if amp_lim != '':
                amp_lim = float(amp_lim)
            else:
                amp_lim = 0.01

            dim_volt = labels_voltagem.index(label_volt.get())
            dim_volt_lim = labels_volt_lim.index(label_volt_lim.get())
            dim_amp = labels_corrente.index(label_amp.get())
            
            number_sondas = entry_sondas.get()
            if number_sondas != '':
                number_sondas = int(number_sondas)
            else:
                number_sondas = 1

            medidas_por_sonda = entry_medida.get()
            if medidas_por_sonda != '':
                medidas_por_sonda = int(medidas_por_sonda)
            else:
                medidas_por_sonda = 10

            amostra_circular = bool(tipo_amostra_circular.get())
            amostra_condutor = bool(tipo_amostra_condutor.get())

            delay = entry_delay.get()
            if delay != '':
                delay = int(delay)
            else:
                volt_lim = 5

            name_arq = entry_arq.get()
            if name_arq == '':
                name_arq = 'out'

            tipo_arquivo = labels_arquivo.index(label_arquivo.get())


            self.entrada = Input(volts,
                                 volt_lim,
                                 amp_lim,
                                 dim_volt,
                                 dim_volt_lim,
                                 dim_amp,
                                 amostra_circular,
                                 amostra_condutor,
                                 name_arq,
                                 tipo_arquivo,
                                 delay,
                                 loops=medidas_por_sonda,
                                 sondas=number_sondas)

            top.destroy()


        ### GERAÇÃO DA INTERFACE

        top = tk.Tk()


        ### VOLTAGEM

        label_voltagem = tk.Label(top,text = 'ddp da fonte')
        label_voltagem.grid(row=0, column=0)
        entry_voltagem = tk.Entry(top, bd=5, width=30)
        entry_voltagem.grid(row=0, column=1)
        labels_voltagem = ["V",'mV','µV']
        label_volt = tk.StringVar(top)
        label_volt.set('dimensão')
        menu_volt = tk.OptionMenu(top,label_volt, *labels_voltagem)
        menu_volt.grid(row=0, column=2)


        ### LIMITE VOLTAGEM

        label_volt_lim= tk.Label(top,text = 'ddp limite')
        label_volt_lim.grid(row=1, column=0)
        entry_volt_lim = tk.Entry(top, bd=5, width=30)
        entry_volt_lim.grid(row=1, column=1)
        labels_volt_lim = ["V",'mV','µV']
        label_volt_lim = tk.StringVar(top)
        label_volt_lim.set('dimensão')
        menu_volt_lim = tk.OptionMenu(top,label_volt_lim, *labels_voltagem)
        menu_volt_lim.grid(row=1, column=2)


        ### LIMITE CORRENTE

        label_corrente = tk.Label(top,text = 'corrente limite')
        label_corrente.grid(row=2, column=0)
        entry_corrente = tk.Entry(top, bd=5, width=30)
        entry_corrente.grid(row=2, column=1)
        labels_corrente = ["A",'mA','µA']
        label_amp = tk.StringVar(top)
        label_amp.set('dimensão')
        menu_corrente = tk.OptionMenu(top,label_amp, *labels_corrente)
        menu_corrente.grid(row=2, column=2)


        ### TIPOS DE AMOSTRA

        tipo_amostra_circular = tk.IntVar()
        tipo_amostra_condutor = tk.IntVar()

        check_amostra_circular = tk.Checkbutton(top, text="amostra circular",
                                                variable=tipo_amostra_circular, 
                                                onvalue=True,
                                                offvalue=False,
                                                height=5,
                                                width=20)


        check_amostra_condutor = tk.Checkbutton(top, text="amostra condutora",
                                                variable=tipo_amostra_condutor, 
                                                onvalue=True,
                                                offvalue=False,
                                                height=5,
                                                width=20)

        check_amostra_circular.grid(row = 3, column= 0)
        check_amostra_condutor.grid(row = 3, column= 1)


        ### NÚMERO DE SONDAS E MEDIÇÕES

        label_medidas = tk.Label(top, text='medidas')
        label_medidas.grid(row=4, column=0)
        entry_medida = tk.Entry(top, bd=5, width=30)
        entry_medida.grid(row=4, column=1)
        
        label_sondas = tk.Label(top, text='sondas')
        label_sondas.grid(row=5, column=0)
        entry_sondas = tk.Entry(top, bd=5, width=30)
        entry_sondas.grid(row=5, column=1)


        ### DELAY
        label_delay = tk.Label(top,text = 'delay')
        label_delay.grid(row=6, column=0)
        entry_delay = tk.Entry(top, bd=5, width=30)
        entry_delay.grid(row=6, column=1)


        ### ARQUIVO DE SAIDA

        label_arq = tk.Label(top,text = 'arquivo de saida')
        label_arq.grid(row=7, column=0)
        entry_arq = tk.Entry(top, bd=5, width=30)
        entry_arq.grid(row=7, column=1)

        labels_arquivo = ["csv",'excel']
        label_arquivo = tk.StringVar(top)
        label_arquivo.set('tipo do arquivo')
        menu_arquivo = tk.OptionMenu(top,label_arquivo, *labels_arquivo)
        menu_arquivo.grid(row=7, column=2)


        ### BOTÃO DE ENTER

        enter_button = tk.Button(top, text="Enter", bg= '#DDDDDD', width= 10, command=saida)
        enter_button.grid(row= 12, column= 2)



        top.mainloop()

obj = GUI()