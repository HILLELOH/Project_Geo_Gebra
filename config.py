

root, fig, ax, canvas, toolbar, shapes, side_panel, cid, circle_cid, selected_shape, start_drag_x,\
    start_drag_y, press_cid, release_cid, motion_cid, buttons_panel = [None] * 16

label_widgets = None
label_widget = None

x1, y1 = [None]*2

circle_x, circle_y = [None]*2
line_x, line_y = [None]*2
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

last_reset = []

