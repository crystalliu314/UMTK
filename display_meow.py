# non-native dependencies:
# numpy, matplotlib, serial

from tkinter import *

import numpy as np
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

from time import time
import serial
from math import floor

S_TO_MS = 1000
REFRESH_RATE = 0.05
TIME_WINDOW = 10
# prompt for recording time - currently infinite
# adjust time window

class QuitDialog(Frame):
    # add option for saving data, is data saved?
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.label = Label(text = "Are you sure you want to exit the application?")

        self.label.grid()
        self.ok_butt = Button(text = "Yes")
        self.ok_butt.grid()
        
        self.not_ok_butt = Button(text = "No")
        self.not_ok_butt.grid()
        
        
class Display(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()

        self.init_vars()
        self.init_plot(master)
        self.create_interface(master)
        self.init_time_params(REFRESH_RATE, TIME_WINDOW)
        
        self.set_zero_time()
        self.t_start = self.zero_time
    
    def init_vars(self):
        self.toolbar_col = 0
        self.toolbar_row = 0
        
        self.display_col = 1
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
        #print(self.t_start)
        #print(self.t_end)
        del_t = self.t_end - self.zero_time
            
        if del_t >= self.t_window:
            self.t_start += self.t_refresh
    
        t = np.arange(self.t_start - self.zero_time, self.t_end - self.zero_time, self.t_refresh)
        #print(np.sin(t))
        self.ax.cla()

        self.ax.plot(t, np.sin(3*t))
        self.graph.draw()
        
        self.t_end += self.t_refresh
        self.after(int(self.t_refresh * S_TO_MS), self.update_plot)
        
    def set_zero_time(self):
        self.zero_time = int(floor(time()))
        self.t_end = self.zero_time
        

if __name__ == "__main__":
    root = Tk()
    display = Display(root)
    display.update_plot()
    display.mainloop()
    root.destroy()

