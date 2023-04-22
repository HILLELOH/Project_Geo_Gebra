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

from Shapes.Line import Line2D


class Gui:

    def __init__(self):
        self.window = tk.Tk()
        #self.main_canvas = tk.Canvas(self.window, width=500, height=500, background='white')
        self.main_label = tk.Label(bd = 4, relief ="solid", font ="Times 22 bold", bg ="white", fg ="black")
        self.mouse = Controller()

    # def on_press(self, event):
    #     """Check whether mouse is over us; if so, store some data."""
    #     if event.inaxes != self.rect.axes:
    #         return
    #     contains, attrd = self.rect.contains(event)
    #     if not contains:
    #         return
    #     print('event contains', self.rect.xy)
    #     self.press = self.rect.xy, (event.xdata, event.ydata)
    #
    # def on_motion(self, event):
    #     """Move the rectangle if the mouse is over us."""
    #     if self.press is None or event.inaxes != self.rect.axes:
    #         return
    #     (x0, y0), (xpress, ypress) = self.press
    #     dx = event.xdata - xpress
    #     dy = event.ydata - ypress
    #     # print(f'x0={x0}, xpress={xpress}, event.xdata={event.xdata}, '
    #     #       f'dx={dx}, x0+dx={x0+dx}')
    #     self.rect.set_x(x0+dx)
    #     self.rect.set_y(y0+dy)
    #
    #     self.rect.figure.canvas.draw()
    #
    # def on_release(self, event):
    #     """Clear button press information."""
    #     self.press = None
    #     self.rect.figure.canvas.draw()
    #
    # def disconnect(self):
    #     """Disconnect all callbacks."""
    #     self.rect.figure.canvas.mpl_disconnect(self.cidpress)
    #     self.rect.figure.canvas.mpl_disconnect(self.cidrelease)
    #     self.rect.figure.canvas.mpl_disconnect(self.cidmotion)

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
        self.ax.spines['left'].set_position('center')
        self.ax.spines['right'].set_position('center')
        self.ax.spines['bottom'].set_position('center')
        self.ax.spines['top'].set_position('center')

        # # Eliminate upper and right axes
        # self.ax.spines['right'].set_color('none')
        # self.ax.spines['top'].set_color('none')

        # # Show ticks in the left and lower axes only
        # self.ax.xaxis.set_ticks_position('bottom')
        # self.ax.yaxis.set_ticks_position('left')

        self.ax.grid()

        self.main_canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.main_canvas.get_tk_widget().pack()

        self.toolbar = NavigationToolbar2Tk(self.main_canvas, self.window)
        self.toolbar.update()
        self.main_canvas.get_tk_widget().pack()
        #self.main_canvas.grid()

        # self.main_canvas.draw()
        # self.main_canvas.mpl_connect('button_press_event', self.create_circle)


        self.button(self.window, 3, 10, "Points", 0, 3)

        self.window.mainloop()



    def set_window(self):
        self.window.geometry("2000x1000")
        #self.window.configure(bg='white')
        self.window.attributes('-fullscreen', True)

    # def create_circle(self, pos_x, pos_y, radius, figure):  # center coordinates, radius
    #     self.ax.add_patch(figure.patches.Circle((pos_x, pos_y), radius, fill="black"))

    #function_ that create point in position of click mouse
    # def detect_mouse_pos(self, event):
    #     print("babounigga")
    #     self.main_label['text'] = f'x={event.x} y={event.y}'
    #     print(event.x, event.y)
    #     if event == 'button_press_event':
    #         self.create_circle(event.x, event.y, 4, self.fig)


    #Gui Main Loop
    # def main_loop(self):
    #     # this method is used to draw in position of the mouse after click event
    #     self.main_canvas.bind('<Button-1>', self.detect_mouse_pos)
    #     self.main_canvas.grid(row = 0, column = 0)
    #     self.main_label.grid(row = 1, column = 0)
    #
    #
    #
    #     #main loop of the gui
    #     self.window.mainloop()



if __name__ == '__main__':
    Line2D(1, 2, 4, 5)
    gg = Gui()
    gg.set_window()
    gg.plot()











