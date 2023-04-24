from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.cm as cm
from config import *

# refactor
from functions import *

config.root = tk.Tk()
config.fig, config.ax = plt.subplots()
config.buttons_panel = tk.Frame(root)
init_program()

config.canvas = FigureCanvasTkAgg(config.fig, master=root)
config.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

config.toolbar = NavigationToolbar2Tk(config.canvas, config.root)
config.toolbar.update()

config.shapes = []
config.label_widgets = []
create_buttons()

config.side_panel = SidePanel(config.root)
config.side_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

config.press_cid = config.ax.figure.canvas.mpl_connect('button_press_event', on_press)
config.release_cid = config.ax.figure.canvas.mpl_connect('button_release_event', on_release)
config.motion_cid = config.ax.figure.canvas.mpl_connect('motion_notify_event', on_motion)

update_display()
run()
