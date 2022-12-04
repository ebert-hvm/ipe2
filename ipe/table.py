import tkinter as tk
import numpy as np

class Table():
    def __init__(self, root, configure_data):
        self.root = root
        self.label = tk.StringVar(self.root) 
        self.row = configure_data['rows']
        self.col = configure_data['columns']
        self.tables_number = configure_data['measures']
        self.cur = 0
        #self.tables = np.array()
        self.tables = [[['' for k in range(self.col)] for j in range(self.row)] for i in range(self.tables_number)]
        #self.tables = [[['']*self.col]*self.row]*self.tables_number
        self.elements = []
        self.grid = self.make_grid()
        self.switch_table = self.configure_table()
    
    def remove_from_grid(self):
        for el in self.elements:
            el.grid_remove()
  
    def make_grid(self):
        grid = []
        for i in range(self.row):
            labelc = tk.Label(self.root, text=str(i+1))
            labelc.grid(row=i+2, column=4)
            lst = []
            for j in range(self.col):
                s = tk.StringVar(self.root)
                s.set('')
                e = tk.Entry(self.root, width=10, bd= 5, textvariable=s)
                e.grid(row=i+2, column=j+5)
                self.elements.append(e)
                lst.append(s)
            grid.append(lst)
        for i in range(self.col):
            label = tk.Label(self.root, text=str(i+1))
            label.grid(row=1, column=5+i)
            self.elements.append(label)
  
        return grid
    
    def switch(self, val, i, j):
        self.grid[i][j].set(str(val))
        #table = self.tables[self.cur]
        # self.tables[self.cur][i][j].delete(0, tk.END)
        # self.tables[self.cur][i][j].insert(tk.END, val)

    def configure_table(self):
        previous_button = tk.Button(self.root, text= 'Anterior', bg='#DDDDDD', width=10, command= lambda switch =-1 :self.switch_tables(switch))
        next_button = tk.Button(self.root, text= 'Próximo', bg='#DDDDDD', width=10, command= lambda switch = 1 :self.switch_tables(switch))
        self.label.set(f'Medição {self.cur+1}')
        label = tk.Label(self.root, textvariable=self.label)
        label.grid(row=0, column=5)
        self.elements.append(label)
        previous_button.grid(row=self.row+2, column=5)
        self.elements.append(previous_button)
        if self.col == 1:
            next_button.grid(row=self.row+2, column=5+self.col)
        else:   
            next_button.grid(row=self.row+2, column=4+self.col)
        self.elements.append(next_button)

    def switch_tables(self, switch):
        if self.tables_number > self.cur+switch and self.cur+switch >-1:
            self.cur += switch
            self.label.set(f'Medição {self.cur+1}')
            #print(self.cur)
        else:
            return
        for i in range(self.row):
            for j in range(self.col):
                #print(self.tables[self.cur][i][j])
                #print(self.cur)
                self.grid[i][j].set(self.tables[self.cur][i][j])
        #print(self.tables)
    def write_cell(self, val, cur, i, j):
        if cur == self.cur:
            self.grid[i][j].set(str(val))
        self.tables[cur][i][j] = str(val)
        #self.tables[cur][i][j] = 4

        #print(self.tables)
        #print(self.tables.__type__)
        