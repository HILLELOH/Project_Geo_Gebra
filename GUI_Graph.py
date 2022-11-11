#imports
import tkinter as tk
from pynput.mouse import Controller
import matplotlib.pyplot as plt
import numpy as np

class Gui:

    def __init__(self):
        self.window = tk.Tk()
        self.main_canvas = tk.Canvas(self.window, width=500, height=500, background='white')
        self.main_label = tk.Label(bd = 4, relief ="solid", font ="Times 22 bold", bg ="white", fg ="black")
        self.mouse = Controller()

    def set_window(self):
        self.window.geometry("500x500")
        self.window.configure(bg='white')

    def create_circle(self, pos_x, pos_y, radius, canvas):  # center coordinates, radius
        x0 = pos_x - radius
        y0 = pos_y - radius
        x1 = pos_x + radius
        y1 = pos_y + radius
        return canvas.create_oval(x0, y0, x1, y1, fill="black")

    #function_ that create point in position of click mouse
    def detect_mouse_pos(self, event):
        self.main_label['text'] = f'x={event.x} y={event.y}'

        self.create_circle(event.x, event.y, 2, self.main_canvas)

    #Gui Main Loop
    def main_loop(self):
        # this method is used to draw in position of the mouse after click event
        self.main_canvas.bind('<Button-1>', self.detect_mouse_pos)
        self.main_canvas.grid(row = 0, column = 0)
        self.main_label.grid(row = 1, column = 0)

        #main loop of the gui
        self.window.mainloop()









