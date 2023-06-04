

root, fig, ax, canvas, toolbar, shapes, side_panel, cid, circle_cid, selected_shape, start_drag_x,\
    start_drag_y, press_cid, release_cid, motion_cid, buttons_panel = [None] * 16

label_widgets = None
label_widget = None

x1, y1 = [None]*2

circle_x, circle_y = [None]*2
line_x, line_y = [None]*2
segment_x, segment_y = [None]*2
edit_frame, file_frame = [None]*2

over_cid, leave_cid = [None]*2

undo_stack = []
redo_stack = []

polygon_vertices = []

last_command_undo = None
last_command_redo = None

label_generator = None
label_objects = None
deleted_labels = []
last_label_before_return = None
last_turn_before_return = None
last_reset = []

polygon_x = None
polygon_y = None
first_point_polygon = None
last_point_polygon = None
curr_polygon = None

this_point = None

set_shape = 0
bool_conv = False
bool_tria = False
bool_panel_algo = False
algorithms_panel = None
algo_var, poly_var = [None]*2
info = None
calc = False
conv_vx = ""


