from tkinter import *

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


import numpy as np
from time import time
import serial

from math import floor

S_TO_MS = 1000
    
class Display(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()

        self.init_vars()
        self.init_plot(master)
        self.create_interface(master)
        self.init_time_params(0.1, 60, 70)
        
        self.set_zero_time()
        self.t_start = self.zero_time
        
    def init_vars(self):
        self.toolbar_col = 0
        self.toolbar_row = 0
        
        self.display_col = 1 # graph
        self.display_row = 0

        self.button_fg = 'blue'
        self.button_bg = 'grey'
        
    def create_interface(self, master):
        self.init_plot(master)
        
        self.QUIT = Button(self, bg = "red")
        self.QUIT["text"] = "QUIT"
        self.QUIT["command"] =  self.quit
        self.QUIT.grid(row = self.toolbar_row, column = self.toolbar_col, sticky = N)
        
        self.start = Button(self, fg = self.button_fg, bg = self.button_bg)
        self.start["text"] = "START REC"
        self.start.grid(row = self.toolbar_row + 1, column = self.toolbar_col, sticky = N)

        self.stop = Button(self, fg = self.button_fg, bg = self.button_bg)
        self.stop["text"] = "STOP REC"
        self.stop.grid(row = self.toolbar_row + 2, column = self.toolbar_col, sticky = N)
        
    def read_data():
        pass
    
    def init_time_params(self, t_refresh, t_window, duration=-1):
        self.t_refresh = t_refresh
        self.t_window = t_window
        self.duration = duration

    def init_plot(self, master):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.plot([],[])

        self.graph = FigureCanvasTkAgg(self.fig, master=root)
        self.graph.draw()
        
        self.graph.get_tk_widget().grid(row = self.display_row, column = self.display_col)
           
    def update_plot(self):
        print(self.t_start)
        print(self.t_end)
        del_t = self.t_end - self.zero_time
            
        if del_t >= self.t_window:
            self.t_start += self.t_refresh
            
        
        t = np.arange(self.t_start, self.t_end, self.t_refresh)
        print(np.sin(t))
        # self.line.set_data(t, np.sin(t))
        #self.ax = self.fig.add_subplot(1, 1, 1)

        self.ax.plot(t, np.sin(t))
        self.graph.draw()
        
        self.t_end += self.t_refresh
        
        self.after(int(self.t_refresh * S_TO_MS), self.update_plot)
        
    def set_zero_time(self):
        self.zero_time = int(floor(time()))
        self.t_end = self.zero_time
        


        

if __name__ == "__main__":
    root = Tk()
    display = Display(root)
    #animation = FuncAnimation(display.fig, display.update_plot, interval=100, blit=False)
    display.update_plot()
    display.mainloop()
    root.destroy()

