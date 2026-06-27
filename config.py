"""Application global state — single module, no circular imports."""
from __future__ import annotations

# Tkinter / Matplotlib roots
root = None
fig = None
ax = None
canvas = None
toolbar = None

# UI panels
buttons_panel = None
side_panel = None
algorithms_panel = None

# Shape collections
shapes: list = []
null_segments: list = []
label_widgets: list = []
label_widget = None

# Label generation
label_generator = None
deleted_labels: list = []
last_label_before_return: str = "A"
last_turn_before_return: int = 0

# Selected / highlighted
selected_shape = None
last_shape = None
last_widget = None

# Drag state
start_drag_x = None
start_drag_y = None

# Drawing state  (0 = idle, 1 = inserting coords via dialog)
set_shape: int = 0
this_point = None

line_x = line_y = None
segment_x = segment_y = None
circle_x = circle_y = None
circle_cid = None

polygon_vertices: list = []
polygon_x = polygon_y = None
first_point_polygon = None
last_point_polygon = None
curr_polygon = None

# Canvas event connection IDs
cid = None
press_cid = None
release_cid = None
motion_cid = None

# Undo / redo
undo_stack: list = []
redo_stack: list = []
last_command_undo = None
last_command_redo = None

# Algorithms panel
bool_panel_algo: bool = False
algo_var = None
poly_var = None
menu = None
calc: bool = False
conv_vx: str = ""

# Info panel
isopen_info_panel: bool = False
info_window = None
info_panel = None
info_label = None
image_canvas = None
image = None
option_var = None
current_selection: str = ""

# History (position-based snapshot list)
last_shapes_list: list = [[]]
last_pos: list = [0]
index: int = 0

# UI extras
status_bar = None
active_tool: str = ""
