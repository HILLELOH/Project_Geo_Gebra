import matplotlib.pyplot as plt
from shapes import *
import tkinter as tk
import numpy as np

class MainWindow:
    def __init__(self):
        #Create the squared XY plane
        fig, ax = plt.subplots()
        
        ax.set_xlim(-10,10)
        ax.set_ylim(-10,10)
        
        #Set the grid lines to be visible
        ax.grid(True)
        
        self.ax = ax
        
        #Empty list of shapes
        self.shapes = []
        
        self.label =tk.Label(text = "", font=("Arial", 14))
        self.label.pack(side="left",padx=10, pady=10)
        
    def run(self):
        plt.show()
        
    def handle_input(self, event):
        if event.button==1:#Left mouse button
            x,y = event.xdata, event.ydata
            self.draw_point(x,y)
        if event.button==2: #Middle Mouse Button
            x1, y1 = event.xdata, event.ydata
            plt.title("Click again to draw a line")
            plt.draw()
            event2 = plt.ginput(1, timeout=-1)[0]
            x2, y2 = event2[0], event2[1]
            self.draw_line(x1, y1,x2, y2)
            self.update_display()
    
    def draw_point(self,x,y):   
        point =Point([(x,y)])
        point.draw(self.ax)
        self.shapes.append(point)
        self.update_display()
        self.update_label()
    
    
    def draw_line(self,x1,y1, x2,y2):
        m = (y2-y1)/(x2-x1)
        b = y1-m*x1
        
        
        x = np.linspace(-10,10,100)
        y = m*x+b
        line = Line(m, b)
        
        line.draw(self.ax)
        
        self.shapes.append(line)
        self.update_display()
        self.update_label()
        
    def update_display(self):
        
        self.ax.cla()
        
        self.ax.set_xlim(-10,10)
        self.ax.set_ylim(-10,10)
        self.ax.grid(True)
        
        for shape in self.shapes:
            shape.draw(self.ax)
             
        plt.draw()
    
    def update_label(self):
        coords = [f"({np.round(p.coords[0],2)}, {np.round(p.coords[1],2)})" for p in self.shapes if isinstance(p, Point)]
        self.label.config(text="\n".join(coords) + "\n" + self.label.cget("text"))
        

window = MainWindow()
cid = window.ax.figure.canvas.mpl_connect('button_press_event', window.handle_input)
window.run()