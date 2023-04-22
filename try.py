import tkinter as tk
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FigureSaveDialog(tk.Toplevel):
    def __init__(self, parent, fig):
        super().__init__(parent)
        self.fig = fig
        self.filetypes = [('PNG Image', '*.png'), ('JPEG Image', '*.jpg')]
        self.filepath = None
        self.create_widgets()

    def create_widgets(self):
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.save_button = tk.Button(master=self, text='Save', command=self.save_figure)
        self.save_button.pack(side=tk.BOTTOM)


    def save_figure(self):
        self.filepath = filedialog.asksaveasfilename(defaultextension='.png', filetypes=self.filetypes)
        if self.filepath:
            self.fig.savefig(self.filepath)

def on_save_button_press(fig):
    dialog = FigureSaveDialog(window, fig)
    dialog.title('Save Figure')

# create a tkinter window
window = tk.Tk()

# create a matplotlib figure
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
ax.plot([1, 2, 3, 4, 5], [10, 8, 6, 4, 2])

# create a canvas and add the figure to it
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# create a button to save the figure
save_button = tk.Button(master=window, text='Save Figure', command=lambda: on_save_button_press(fig))
save_button.pack(side=tk.BOTTOM)

# run the tkinter event loop
window.mainloop()
