import json
import tkinter as tk

class Input():
    def __init__(self):
        self.input_data = {}
        self.input_var = {}

    def __add_input_to_data(self, key, val):
        self.input_data[key] = val

    def add_var(self, key, val):
        self.input_var[key] = val
        self.__add_input_to_data(key, val.get())

    def __update_element(self, key):
        self.input_data[key] = self.input_var[key].get()

    def update_input_data(self):
        for key in self.input_var.keys():
            self.__update_element(key)

    def get_data(self, key):
        self.__update_element(key)
        return self.input_data[key]

    def set_data(self, key, val):
        self.input_var[key].set(val)
        self.__update_element(key)
        
    def get_var(self, key):
        return self.input_var[key]

    def save_input_data(self):
        with open("ipe/input_save.json", "w", encoding='utf8') as outfile:
            self.update_input_data()
            print(self.input_data)
            json.dump(self.input_data, outfile, indent=4, ensure_ascii=False)
            
    def load_input_data(self):
        with open('ipe/input_save.json', 'r', encoding='utf8') as openfile:
            self.input_data = json.load(openfile)
            for key in self.input_data.keys():
                self.input_var[key].set(self.input_data[key])
