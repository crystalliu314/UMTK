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
        self.init_time_params(REFRESH_RATE, TIME_WINDOW)

        # self.set_zero_time()
        self.stop_recording = True # can have it auto record

        self.init_plot(master)
        self.create_interface(master)

    def create_interface(self, master):
        self.graph_title = Label(self, text = "UMTK DEMO: TITLE HERE", font = ('Helvetica', 20, 'normal'))
        
        # ----- TOOLBAR ----
        
        
        self.start = Button(self, text = "START REC", command = self.start_button)
        self.stop = Button(self, text = "STOP REC", command = self.stop_button)
        self.QUIT = Button(self, text = "QUIT", command = self.bye)
        
        self.layout()
        self.init_plot(master)
        
    def layout(self):
        self.graph_title.grid(row = 0, column = 1, pady = 20, sticky = "N")
        
        self.toolbar_width = 15
        
        self.toolbar_col = 0
        self.toolbar_row = 0
        self.display_col = 1
        self.display_row = 0
        
        self.init_button_format(14, 'SteelBlue3', 'linen', 'SteelBlue4', 10, self.toolbar_width)
        QUIT_attribs = (('Helvetica', 14, 'bold'), 'firebrick3', 'linen', 'firebrick4', 3, self.toolbar_width)

        self.format_button(self.start, self.button_attrib_vals)
        self.format_button(self.stop, self.button_attrib_vals)
        self.format_button(self.QUIT, QUIT_attribs)
        
        toolbar_padding = 4
        self.start.grid(row = self.toolbar_row, column = self.toolbar_col, padx = toolbar_padding, pady = toolbar_padding)
        self.stop.grid(row = self.toolbar_row + 1, column = self.toolbar_col, padx = toolbar_padding, pady = toolbar_padding)
        self.QUIT.grid(row = self.toolbar_row + 2, column = self.toolbar_col, padx = toolbar_padding, pady = toolbar_padding)

    def stop_button(self):
        self.stop_recording = True
        print("Recording is currently stopped")

    def start_button(self):
        if self.stop_recording:
            self.set_zero_time()
            self.stop_recording = False

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
                    
    def set_zero_time(self):
        self.zero_time = int(floor(time()))
        self.t_start = self.zero_time
        self.t_end = self.zero_time
        
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
            
    def update_plot(self):
        if not self.stop_recording:
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
            
        self.graph.get_tk_widget().grid(row = self.display_row, column = self.display_col, sticky = "W")
        self.after(int(self.t_refresh * S_TO_MS), self.update_plot)    

    def init_button_format(self, button_text_size, button_bg, button_fg, button_active_bg, button_height, button_width, bd=1):
        button_font = ('Helvetica', button_text_size, 'bold')
        
        self.button_attrib_names = ('font', 'bg', 'fg', 'activebackground', 'height', 'width', 'bd')
        self.button_attrib_vals = (button_font, button_bg, button_fg, button_active_bg, button_height, button_width, bd)

    def format_button(self, button, attribs):
        for i in range(len(attribs)):
            button[self.button_attrib_names[i]] = attribs[i]

    def read_data():
        pass

    
if __name__ == "__main__":
    root = Tk()
    root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='./icon.gif'))
    # root.attributes('-fullscreen', True) # kill me, so scary
    # get window size ?
    display = Display(root)
    display.update_plot()
    display.mainloop()
    root.destroy()

