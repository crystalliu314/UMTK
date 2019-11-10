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

APPLICATION_NAME = "Meow :3"

S_TO_MS = 1000
REFRESH_RATE = 0.05
TIME_WINDOW = 10
YLABEL = "Force (N)" #config file?
XLABEL = "Time (s)"
# prompt for recording time - currently infinite
# adjust time window
# fname
        
class Display(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title(APPLICATION_NAME)
        self.grid()

        self.init_vars()
        self.init_time_params(REFRESH_RATE, TIME_WINDOW)

        self.set_zero_time()
        self.t_start = self.zero_time
        
        self.init_plot(master)
        self.create_interface(master)
        
    def init_vars(self):
        self.cols = 0
        
        self.user_in_col = 0
        self.user_in_row = 0
        self.cols += 1
        
        self.toolbar_col = 1
        self.toolbar_row = 1
        self.cols += 1
        
        self.display_col = 2
        self.display_row = 1
        self.cols += 1

        self.button_fg = 'blue'
        self.button_bg = 'grey'

    def create_interface(self, master):
        self.init_plot(master)

        # ---- USER INPUT ----
        #self.fname_label = Label(text = "Save data in: ")
        #self.fname_label.grid(row = self.user_in_row, column = self.user_in_col + 1)
        
        #self.save_data = Entry()
        #self.save_data.grid(row = self.user_in_row)
                
        # ----- TOOLBAR ----
        self.QUIT = Button(self, bg = "red")
        self.QUIT["text"] = "QUIT"
        self.QUIT["command"] = self.bye
        self.QUIT.grid(row = self.toolbar_row + 1, column = self.toolbar_col)
        
        self.start = Button(self, fg = self.button_fg, bg = self.button_bg)
        self.start["text"] = "START REC"
        self.start["command"] = self.update_plot
        self.start.grid(row = self.toolbar_row + 2, column = self.toolbar_col)

        self.stop = Button(self, fg = self.button_fg, bg = self.button_bg)
        self.stop["text"] = "STOP REC"
        self.stop.grid(row = self.toolbar_row + 3, column = self.toolbar_col)


    def bye(self):
        self.bye_bye = Toplevel(self)
        self.bye_bye.label = Label(self.bye_bye, text = "Are you sure you want to exit the application?")
        self.bye_bye.label.grid()
        
        self.bye_bye.ok_butt = Button(self.bye_bye, text = "Yes")
        self.bye_bye.not_ok_butt = Button(self.bye_bye, text = "No")
        self.bye_bye.ok_butt["command"] = self.ok
        self.bye_bye.not_ok_butt["command"] = self.not_ok
        self.bye_bye.ok_butt.grid()
        self.bye_bye.not_ok_butt.grid()
        
    def ok(self):
        self.quit()
    def not_ok(self):
        self.bye_bye.destroy()
                    
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
        self.ax.set_xlabel(XLABEL)
        self.ax.set_ylabel(YLABEL)

        self.graph = FigureCanvasTkAgg(self.fig, master=root)
        self.graph.draw()
        
        self.graph.get_tk_widget().grid(row = self.display_row, column = self.display_col)
           
    def update_plot(self):
        del_t = self.t_end - self.zero_time
            
        if del_t >= self.t_window:
            self.t_start += self.t_refresh
    
        t = np.arange(self.t_start - self.zero_time, self.t_end - self.zero_time, self.t_refresh)

        self.ax.cla()
        self.ax.plot(t, np.sin(3*t))
        self.ax.set_xlabel(XLABEL)
        self.ax.set_ylabel(YLABEL)
        self.graph.draw()

        self.t_end += self.t_refresh
        self.after(int(self.t_refresh * S_TO_MS), self.update_plot)
        
    def set_zero_time(self):
        self.zero_time = int(floor(time()))
        self.t_end = self.zero_time
        

if __name__ == "__main__":
    root = Tk()
    # root.attributes('-fullscreen', True) # kill me, so scary
    # get window size
    display = Display(root)
    display.mainloop()
    root.destroy()

