import tkinter as tk
import numpy as np

class Table():
    def __init__(self, root, row, col, tables_number):
        self.root = root
        self.row = row
        self.col = col      
        self.tables_number = tables_number
        self.cur = 0
        self.tables = np.zeros((self.tables_number,self.row,self.col)).tolist()
        self.grid = self.make_grid()
  
        self.switch_table = self.modify_table()

    def make_grid(self):
        grid = []
        for i in range(self.row):
            labelc = tk.Label(self.root, text=str(i+1))
            labelc.grid(row=i+1, column=4)
            lst = []
            for j in range(self.col):
                s = tk.StringVar(self.root)
                s.set('')
                e = tk.Entry(self.root, width=10, bd= 5, textvariable=s)
                e.grid(row=i+1, column=j+5)
                lst.append(s)
            grid.append(lst)
        for i in range(self.col):
            label = tk.Label(self.root, text=str(i+1))
            label.grid(row=0, column=5+i)
  
        return grid
    
    def switch(self, val, i, j):
        self.grid[i][j].set(str(val))
        #table = self.tables[self.cur]
        # self.tables[self.cur][i][j].delete(0, tk.END)
        # self.tables[self.cur][i][j].insert(tk.END, val)
        pass

    def modify_table(self):
        previous_button = tk.Button(self.root, text= 'Anterior', bg='#DDDDDD', width=10, command= lambda switch =-1 :self.switch_tables(switch))
        next_button = tk.Button(self.root, text= 'Próximo', bg='#DDDDDD', width=10, command= lambda switch = 1 :self.switch_tables(switch))
        previous_button.grid(row=self.row+1, column=5)
        if self.col == 1:
            next_button.grid(row=self.row+1, column=5+self.col)
        else:   
            next_button.grid(row=self.row+1, column=4+self.col)

    def switch_tables(self, switch):
        if self.tables_number > self.cur+switch and self.cur+switch >-1:
            self.cur += switch
            print(self.cur)
        else:
            return 0
        for i in range(self.row):
            for j in range(self.col):
                self.switch(self.tables[self.cur][i][j],i,j)
        