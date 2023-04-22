#imports
import tkinter as tk
from tkinter import BOTTOM, BOTH

from pynput.mouse import Controller
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


import pyautogui

class Gui:

    def __init__(self):
        self.window = tk.Tk()
        #self.main_canvas = tk.Canvas(self.window, width=500, height=500, background='white')
        self.main_label = tk.Label(bd = 4, relief ="solid", font ="Times 22 bold", bg ="white", fg ="black")
        self.mouse = Controller()

    def connect(self):
        """Connect to all the events we need."""
        self.cidpress = self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.fig.canvas.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.fig.canvas.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def button(self, window, height, width, text, pos_x, pos_y):
        b = tk.Button(master=window,
                      height=height,
                      width=width,
                      text=text)
        b.place(x=pos_x, y=pos_y)
        b.pack()

    def plot(self):
        # self.screen_width, self.screen_height = pyautogui.size()
        self.screen_width, self.screen_height = 1000, 1000

        self.fig = Figure(figsize=(12, 8), dpi=100)
        self.ax = self.fig.add_subplot(1, 1, 1)

        # Move left y-axis and bottim x-axis to centre, passing through (0,0)
        #self.ax.spines['left'].set_position('center')
        # self.ax.spines['right'].set_position('center')
        #self.ax.spines['bottom'].set_position('center')
        # self.ax.spines['top'].set_position('center')


        self.ax.grid()

        self.main_canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.main_canvas.get_tk_widget().pack()

        self.toolbar = NavigationToolbar2Tk(self.main_canvas, self.window)
        self.toolbar.update()
        self.main_canvas.get_tk_widget().pack()

        self.window.mainloop()


    def set_window(self):
        self.window.geometry("1000x1000")
        #self.window.configure(bg='white')
        self.window.attributes('-fullscreen', True)



if __name__ == '__main__':
    gg = Gui()
    gg.set_window()
    gg.plot()











