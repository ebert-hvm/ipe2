import tkinter as tk
from input import Input


### BOTÃO DE SAÍDA

def saida():
    volts = float(entry_voltagem.get())
    amp = float(entry_corrente.get())
    # dim_volt = menu_voltagem
    # dim_amp = menu_corrente
    name_arq = entry_arq.get()
    amostra_circular = bool(tipo_amostra_circular.get())
    amostra_2 = bool(tipo_amostra_2.get())
    # entrada = Input(volts,amp,dim_volt,dim_amp,amostra_circular, amostra_2)

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
tipo_amostra_2 = tk.IntVar()

check_amostra_circular = tk.Checkbutton(top, text="amostra circular",
                                        variable=tipo_amostra_circular, 
                                        onvalue=True,
                                        offvalue=False,
                                        height=5,
                                        width=20)


check_amostra_2 = tk.Checkbutton(top, text="amostra 2",
                                        variable=tipo_amostra_2, 
                                        onvalue=True,
                                        offvalue=False,
                                        height=5,
                                        width=20)

check_amostra_circular.grid(row = 2, column= 0)
check_amostra_2.grid(row = 2, column= 1)


### NOME DO ARQUIVO DE SAIDA

label_arq = tk.Label(top,text = 'arquivo de saida')
label_arq.grid(row=4, column=0)
entry_arq = tk.Entry(top, bd=5, width=30)
entry_arq.grid(row=4, column=1)


### TIPO ARQUIVO DE SAIDA


menu_saida = tk.Menubutton(top, text="tipo do arquivo", relief='raised')
menu_saida.grid(row=4, column=2)
menu_saida.menu = tk.Menu(menu_saida, tearoff=0)
menu_saida["menu"] = menu_saida.menu

csv_var = tk.IntVar()
xlsx_var = tk.IntVar()
n_sei_var = tk.IntVar()
menu_saida.menu.add_checkbutton(label="csv", variable=csv_var)
menu_saida.menu.add_checkbutton(label="excel", variable=xlsx_var)
menu_saida.menu.add_checkbutton(label="n sei", variable=n_sei_var)


### BOTÃO DE ENTER

enter_button = tk.Button(top, text="Enter", bg= '#DDDDDD', width= 10, command=saida)
enter_button.grid(row= 12, column= 2)



top.mainloop()
