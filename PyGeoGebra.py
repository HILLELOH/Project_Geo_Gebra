from tkinter import Toplevel

import matplotlib
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import config
from config import *

# refactor
from functions import *

config.root = tk.Tk()
# create a new figure and axis
config.fig, config.ax = plt.subplots()
# plt.gcf().set_visible(False)
# config.fig.withdraw()

config.buttons_panel = tk.Frame(root)

# config.algorithms_panel = tk.Frame(root)
init_program()

config.canvas = FigureCanvasTkAgg(config.fig, master=root)

config.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

config.toolbar = NavigationToolbar2Tk(config.canvas, config.root)
config.toolbar.update()

config.shapes = []
config.label_widgets = []
create_buttons()

config.side_panel = SidePanel(config.root, True, tk.LEFT, True)
config.side_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
config.label_widget = tk.Label(config.side_panel.text, text="Algebra ", bg="white", font='Helvetica 18 bold underline')
config.label_widget.pack(anchor='w')

config.press_cid = config.ax.figure.canvas.mpl_connect('button_press_event', on_press)

config.release_cid = config.ax.figure.canvas.mpl_connect('button_release_event', on_release)
config.motion_cid = config.ax.figure.canvas.mpl_connect('motion_notify_event', on_motion)
config.ax.figure.canvas.mpl_connect('scroll_event', on_scroll)
config.ax.figure.canvas.mpl_connect('key_press_event', on_key)
config.root.protocol("WM_DELETE_WINDOW", on_closing)


update_display()
run()
