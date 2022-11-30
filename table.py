import tkinter as tk

class Table():
    def __init__(self, root, row, col, tables_number):
        self.root = root
        self.row = row
        self.col = col
        self.tables_number = tables_number
        self.grid = self.make_grid()
        self.cur = 0
    def make_row_label(self):
        for i in range(self.row):
            label = tk.Label(self.root, text=str(i+self.cur*self.row))
            label.grid(row=i+1, column=4)
    def make_grid(self):
        grid = []
        for i in range(self.row):
            lst = []
            label = tk.Label(self.root)
            label.grid(row=i+1, column=4)
            for j in range(self.col):
                e = tk.Entry(self.root, width=10, bd= 5)
                e.grid(row=i+1, column=j+4)
                e.insert(tk.END, '')
                lst.append(e)
            grid.append(lst)
        for i in range(self.col):
            label = tk.Label(self.root, text=str(i))
            label.grid(row=0, column=4+i)
        return grid

    def create_table(self, r, c):
        pass
        #self.tables.append(table)
        
    def add(self, val, i, j):
        #table = self.tables[self.cur]
        self.tables[self.cur][i][j].delete(0, tk.END)
        self.tables[self.cur][i][j].insert(tk.END, val)
    def switch_tables(self):
        pass
