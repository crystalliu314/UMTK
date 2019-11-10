from tkinter import *

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np
import time
import serial
    
class Display(Frame):
    def create_interface(self, master):
        # toolbar
        
        self.QUIT = Button(self, fg = "red", bg = "blue")
        self.QUIT["text"] = "QUIT"
        self.QUIT["command"] =  self.quit
        self.QUIT.pack(side = LEFT)
        
        
        self.butt = Button(self, fg = "blue", bg = "red")
        self.butt["text"] = "Button"
        self.butt.pack(side = LEFT)

        
        self.label = Label(master, text ="ohai")
        self.label.pack(side = BOTTOM)        

    
    def read_data():
        pass

    def init_plot(self, master):
        fig = Figure(figsize=(5, 4), dpi=100)
        t = np.arange(0, 3, .01)
        fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

        self.graph = FigureCanvasTkAgg(fig, master=root)
        self.graph.draw()
        self.graph.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    def update_plot():
        pass
    def __init__(self, master):
        Frame.__init__(self, master)
        self.pack()
        
        self.create_interface(master)
        self.init_plot(master)

if __name__ == "__main__":
    root = Tk()
    display = Display(root)
    display.mainloop()
    root.destroy

