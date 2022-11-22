from input import Input
import tkinter as tk


class GUI:
    def __init__(self) -> None:
        self.entrada=0
        self.interface()


    def interface(self):
        
        ### BOTÃO DE SAÍDA

        def saida():
            volts = float(entry_voltagem.get())
            amp = float(entry_corrente.get())
            dim_volt, dim_amp,tipo_arquivo = 0,0,0
            # dim_volt = menu_voltagem (0 = V, 1=mV, 2=µV)
            # dim_amp = menu_corrente
            number_sondas = entry_sondas.get()
            medidas_por_sonda = entry_medida.get()
            name_arq = entry_arq.get()
            # tipo_arquivo = menu_saida (0 = csv, 1 = excel)
            amostra_circular = bool(tipo_amostra_circular.get())
            amostra_condutor = bool(tipo_amostra_condutor.get())

            if number_sondas != '':
                number_sondas = int(number_sondas)
            else:
                number_sondas = 1
            if medidas_por_sonda != '':
                medidas_por_sonda = int(medidas_por_sonda)
            else:
                medidas_por_sonda = 10

            self.entrada = Input(volts,
                                 amp,
                                 dim_volt,
                                 dim_amp,
                                 amostra_circular,
                                 amostra_condutor,
                                 name_arq,
                                 tipo_arquivo,
                                 loops=medidas_por_sonda,
                                 sondas=number_sondas)

            top.destroy()


        ### GERAÇÃO DA INTERFACE

        top = tk.Tk()

        ### VOLTAGEM E AMPERAGEM

        label_voltagem = tk.Label(top,text = 'ddp da fonte')
        label_voltagem.grid(row=0, column=0)
        entry_voltagem = tk.Entry(top, bd=5, width=30)
        entry_voltagem.grid(row=0, column=1)

        menu_voltagem = tk.Menubutton(top, text="dimensão", relief='raised')
        menu_voltagem.grid(row=0, column=2)
        menu_voltagem.menu = tk.Menu(menu_voltagem, tearoff=0)
        menu_voltagem["menu"] = menu_voltagem.menu

        volt_var = tk.IntVar()
        mili_volt_var = tk.IntVar()
        micro_volt_var = tk.IntVar()
        menu_voltagem.menu.add_checkbutton(label="V", variable=volt_var)
        menu_voltagem.menu.add_checkbutton(label="mV", variable=mili_volt_var)
        menu_voltagem.menu.add_checkbutton(label="µV", variable=micro_volt_var)


        label_corrente = tk.Label(top,text = 'corrente da fonte')
        label_corrente.grid(row=1, column=0)
        entry_corrente = tk.Entry(top, bd=5, width=30)
        entry_corrente.grid(row=1, column=1)
        menu_corrente = tk.Menubutton(top, text="dimensão", relief='raised')
        menu_corrente.grid(row=1, column=2)
        menu_corrente.menu = tk.Menu(menu_corrente, tearoff=0)
        menu_corrente["menu"] = menu_corrente.menu

        ampere_var = tk.IntVar()
        mili_ampere_var = tk.IntVar()
        micro_ampere_var = tk.IntVar()
        menu_corrente.menu.add_checkbutton(label="A", variable=ampere_var)
        menu_corrente.menu.add_checkbutton(label="mA", variable=mili_ampere_var)
        menu_corrente.menu.add_checkbutton(label="µA", variable=micro_ampere_var)


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

        check_amostra_circular.grid(row = 2, column= 0)
        check_amostra_condutor.grid(row = 2, column= 1)


        ### NÚMERO DE SONDAS E MEDIÇÕES

        label_medidas = tk.Label(top, text='medidas')
        label_medidas.grid(row=4, column=0)
        entry_medida = tk.Entry(top, bd=5, width=30)
        entry_medida.grid(row=4, column=1)
        
        label_sondas = tk.Label(top, text='sondas')
        label_sondas.grid(row=5, column=0)
        entry_sondas = tk.Entry(top, bd=5, width=30)
        entry_sondas.grid(row=5, column=1)

        ### ARQUIVO DE SAIDA

        label_arq = tk.Label(top,text = 'arquivo de saida')
        label_arq.grid(row=7, column=0)
        entry_arq = tk.Entry(top, bd=5, width=30)
        entry_arq.grid(row=7, column=1)

        menu_saida = tk.Menubutton(top, text="tipo do arquivo", relief='raised')
        menu_saida.grid(row=7, column=2)
        menu_saida.menu = tk.Menu(menu_saida, tearoff=0)
        menu_saida["menu"] = menu_saida.menu

        csv_var = tk.IntVar()
        xlsx_var = tk.IntVar()
        
        menu_saida.menu.add_checkbutton(label="csv", variable=csv_var)
        menu_saida.menu.add_checkbutton(label="excel", variable=xlsx_var)


        ### BOTÃO DE ENTER

        enter_button = tk.Button(top, text="Enter", bg= '#DDDDDD', width= 10, command=saida)
        enter_button.grid(row= 12, column= 2)



        top.mainloop()
