# non-native dependencies:
# numpy, matplotlib, serial

from tkinter import *

import numpy as np
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

from time import time
# import serial
from math import floor


APPLICATION_NAME = "Meow :3"
TITLE_STR = "UTMTK MEOW"

S_TO_MS = 1000

REFRESH_RATE = 0.05
SAMPLE_RATE = 100 #Hz
YLABEL = "Stress (MPa)" #config file?
XLABEL = "Strain"


# prompt for recording time - currently infinite
# adjust time window
# fname
global stop_recording
stop_recording = False

class Toolbar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.pack(side = LEFT)
        
        self.create_widgets(master)
        self.layout()

    def create_widgets(self, master):
        self.start = Button(self, text = "START REC", command = self.start_button)
        self.stop = Button(self, text = "STOP REC", command = self.stop_button)
        self.QUIT = Button(self, text = "QUIT", command = self.bye)
        
    def layout(self):
        self.toolbar_width = 15
        self.toolbar_col = 0
        
        self.init_button_format(14, 'SteelBlue3', 'linen', 'SteelBlue4', 10, self.toolbar_width)
        QUIT_attribs = (('Helvetica', 14, 'bold'), 'firebrick3', 'linen', 'firebrick4', 3, self.toolbar_width)

        self.format_button(self.start, self.button_attrib_vals)
        self.format_button(self.stop, self.button_attrib_vals)
        self.format_button(self.QUIT, QUIT_attribs)
        
        self.start.pack(side = TOP)
        self.stop.pack(side = TOP)
        self.QUIT.pack(side = TOP)
        
    def stop_button(self):
        global stop_recording
        stop_recording = True
        print("Recording is currently stopped")

    def start_button(self):
        global stop_recording
        if stop_recording:
            stop_recording = False

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
        
    def init_button_format(self, button_text_size, button_bg, button_fg, button_active_bg, button_height, button_width, bd=1):
        button_font = ('Helvetica', button_text_size, 'bold')
        
        self.button_attrib_names = ('font', 'bg', 'fg', 'activebackground', 'height', 'width', 'bd')
        self.button_attrib_vals = (button_font, button_bg, button_fg, button_active_bg, button_height, button_width, bd)

    def format_button(self, button, attribs):
        for i in range(len(attribs)):
            button[self.button_attrib_names[i]] = attribs[i]

class Display(Frame):
    def __init__(self, master):
        global stop_recording
        
        Frame.__init__(self, master)
        self.master = master
        self.master.title(APPLICATION_NAME)
        self.pack()
        
        self.t_refresh = REFRESH_RATE
        self.set_time()
        stop_recording = False # can have it auto record
        self.init_plot(master)

        self.graph_title = Label(self, text = TITLE_STR, font = ('Helvetica', 20, 'normal'))
        self.graph_title.pack(side = TOP)

    def set_time(self):
        self.zero_time = int(floor(time()))
        self.t_end = self.zero_time
        
    def init_plot(self, master):
        self.fig = Figure(figsize = (7.0, 5.0))
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.plot([],[])
        self.ax.set_xlabel(XLABEL)
        self.ax.set_ylabel(YLABEL)

        self.graph = FigureCanvasTkAgg(self.fig, master=root)
        self.graph.draw()
      
    def update_plot(self):
        global stop_recording
        if not stop_recording:       
            t = np.arange(0, self.t_end - self.zero_time, self.t_refresh)

            self.ax.cla()
            self.ax.plot(t, np.sin(3*t))
            self.ax.set_xlabel(XLABEL)
            self.ax.set_ylabel(YLABEL)
            self.graph.draw()

            self.t_end += self.t_refresh
        else:
            self.set_time()
            
        self.graph.get_tk_widget().pack(side = TOP)
        self.after(int(self.t_refresh * S_TO_MS), self.update_plot)    
        
    def read_data():
        pass

    
if __name__ == "__main__":
    root = Tk()
    root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='./icon.gif'))
    # root.attributes('-fullscreen', True) # kill me, so scary
    # get window size ?
    display = Display(root)
    toolbar = Toolbar(root)
    
    display.update_plot()
    display.mainloop()
    root.destroy()

