import json
import logging
import pickle
import tkinter as tk
import config

from logging import debug
from tkinter import ttk, filedialog, messagebox
from Shapes.Circle import *
from Shapes.Point import *
from Shapes.Line import *
from label_conf import generate_alphanumeric_sequence

config.label_generator = generate_alphanumeric_sequence()


class SidePanel(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.text = tk.Text(self, wrap=tk.WORD)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self, command=self.text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=scrollbar.set)


def init_program():
    config.root.geometry("1400x900")
    config.root.resizable(False, False)
    config.root.wm_title("Geogebra")

    config.fig.set_size_inches(8, 8)
    config.ax.set_xlim(-10, 10)
    config.ax.set_ylim(-10, 10)
    config.ax.set_aspect('equal')
    config.ax.grid(True)

    config.ax.set_xticks(np.arange(-20, 21, 5))
    config.ax.set_yticks(np.arange(-20, 21, 5))

    config.ax.axhline(0, color='black', linewidth=0.5)
    config.ax.axvline(0, color='black', linewidth=0.5)
    config.buttons_panel.pack(side=tk.TOP, fill=tk.X)


global button_list, file_button


def create_buttons():
    global button_list, file_button
    point_button = tk.Button(config.buttons_panel, text="Draw Point", command=draw_point)
    line_button = tk.Button(config.buttons_panel, text="Draw Line", command=draw_line)
    circle_button = tk.Button(config.buttons_panel, text="Draw Circle", command=draw_circle)
    # polygon_button = tk.Button(config.buttons_panel, text="polygon", command=draw_polygon)
    reset_button = tk.Button(config.buttons_panel, text="Reset", command=reset)
    save_button = tk.Button(config.buttons_panel, text="Save", command=save)
    load_button = tk.Button(config.buttons_panel, text="Load file", command=load)
    delete_button = tk.Button(config.buttons_panel, text="Delete shape", command=delete_shape)
    undo_button = tk.Button(config.buttons_panel, text="undo", command=undo)
    redo_button = tk.Button(config.buttons_panel, text="redo", command=redo)
    clear_history_button = tk.Button(config.buttons_panel, text="clear history", command=clear_history)

    buttons = [save_button,
               load_button,
               delete_button,
               reset_button,

               point_button,
               line_button,
               circle_button,
               # polygon_button,

               # file_button,
               clear_history_button,
               redo_button,
               undo_button]

    padding = 2
    right = [clear_history_button,
             undo_button,
             redo_button, ]
    for i in range(len(buttons)):
        if buttons[i] in right:
            buttons[i].pack(side=tk.RIGHT, padx=padding)
        # buttons[i].pack(side=tk.RIGHT, padx=padding)
        else:
            buttons[i].pack(side=tk.LEFT, padx=padding)

    # make_file_button_frame(config.file_frame)


def is_start_end(p, line):
    threshold = 0.05

    if abs(p.get_x() - line.get_start_point()[0]) < threshold and abs(
            p.get_y() - line.get_start_point()[1]) < threshold:
        return "start"

    elif abs(p.get_x() - line.get_end_point()[0]) < threshold and abs(
            p.get_y() - line.get_end_point()[1]) < threshold:
        return "end"

    else:
        # return f'{abs(coords[0] - line.get_start_point()[0])}, {abs(coords[1] - line.get_start_point()[1])}\n' \
        #        f'{abs(coords[0] - line.get_end_point()[0])}, {abs(coords[1] - line.get_end_point()[1])}'
        return None


def shape_clicked(x, y):
    threshold = 0.5
    for shape in config.shapes:
        if isinstance(shape, Point):
            try:
                if np.abs(x - shape.get_x()) <= threshold and np.abs(y - shape.get_y()) <= threshold:
                    return shape
            except TypeError:
                print("")

        elif isinstance(shape, Circle):
            circle_x = shape.coords[0][0]
            circle_y = shape.coords[0][0]
            distance = np.sqrt((x - circle_x) ** 2 + (y - circle_y) ** 2)
            if np.abs(distance - shape.radius) <= threshold:
                return shape

        # elif isinstance(shape, Line):
        #     m, b = shape.m_b()
        #     line_y = m * x + b
        #     if np.abs(y - line_y) <= threshold:
        #         return shape
    return None


def on_press(event):
    if event.button == 1:  # Left mouse button
        config.selected_shape = shape_clicked(event.xdata, event.ydata)
        if config.selected_shape is not None:
            config.start_drag_x, config.start_drag_y = event.xdata, event.ydata


def on_release(event):
    if config.selected_shape is not None:
        config.selected_shape = None
        config.start_drag_x, config.start_drag_y = None, None


def on_motion(event):
    if config.selected_shape is not None and event.xdata is not None and event.ydata is not None:
        x, y = event.xdata, event.ydata
        dx = x - config.start_drag_x
        dy = y - config.start_drag_y
        config.start_drag_x, config.start_drag_y = x, y

        # if isinstance(config.selected_shape, Line):  # Check if the selected_shape is a Line
        #     m, b = config.selected_shape.m_b()
        #     b += dy  # Update the y-intercept of the line
        #     xdata, ydata = config.selected_shape.line_obj.get_data()
        #     ydata = m * xdata + b
        #     config.selected_shape.line_obj.set_data(xdata, ydata)
        #
        #     config.selected_shape.set_start_point(dx, dy)
        #     config.selected_shape.set_end_point(dx, dy)

        if isinstance(config.selected_shape, Point):
            flag = False
            for shape in config.shapes:
                if isinstance(shape, Line):
                    if shape.is_line_edge(config.selected_shape)[1] == "start":
                        config.selected_shape.coords[0][0] += dx
                        config.selected_shape.coords[0][1] += dy

                        shape.set_start_point(dx, dy)
                        flag = True
                        break

                    elif shape.is_line_edge(config.selected_shape)[1] == "end":
                        config.selected_shape.coords[0][0] += dx
                        config.selected_shape.coords[0][1] += dy
                        shape.set_end_point(dx, dy)
                        flag = True
                        break

            if not flag:
                config.selected_shape.coords[0][0] += dx
                config.selected_shape.coords[0][1] += dy
                config.selected_shape.set_x(dx)
                config.selected_shape.set_y(dy)

        elif isinstance(config.selected_shape, Circle):
            config.selected_shape.coords[0][0] += dx
            config.selected_shape.coords[0][1] += dy

        update_display()
        update_label()
        plt.draw()


def on_scroll(event):
    ax = config.ax
    fig = config.fig
    x, y = event.xdata, event.ydata

    factor = 1.1 if event.step > 0 else 0.9
    x_lim = ax.get_xlim()
    y_lim = ax.get_ylim()
    ax.set_xlim(x - factor * (x - x_lim[0]), x + factor * (x_lim[1] - x))
    ax.set_ylim(y - factor * (y - y_lim[0]), y + factor * (y_lim[1] - y))
    ax.xaxis.set_ticks(range(int(ax.get_xlim()[0]), int(ax.get_xlim()[1]) + 1))
    ax.yaxis.set_ticks(range(int(ax.get_ylim()[0]), int(ax.get_ylim()[1]) + 1))
    ax.grid(True)
    fig.canvas.draw_idle()


def delete_shape():
    if not config.cid:
        config.ax.figure.canvas.mpl_disconnect(config.cid)

    if not config.circle_cid:
        config.ax.figure.canvas.mpl_disconnect(config.circle_cid)

    config.cid = config.ax.figure.canvas.mpl_connect('button_press_event', handle_delete_shape)
    plt.title("Click shape to delete")
    plt.draw()


def draw_point():
    if not config.cid:
        config.ax.figure.canvas.mpl_disconnect(config.cid)

    if not config.circle_cid:
        config.ax.figure.canvas.mpl_disconnect(config.circle_cid)

    config.cid = config.ax.figure.canvas.mpl_connect('button_press_event', handle_input_point)
    plt.title("Click left mouse button to create point")
    plt.draw()


def draw_line():
    if config.cid is not None:
        config.ax.figure.canvas.mpl_disconnect(config.cid)

    if config.circle_cid is not None:
        config.ax.figure.canvas.mpl_disconnect(config.circle_cid)

    config.cid = config.ax.figure.canvas.mpl_connect('button_press_event', handle_input_line)
    plt.title("Click left mouse button to start line")
    plt.draw()


def draw_circle():
    if config.cid is not None:
        config.ax.figure.canvas.mpl_disconnect(config.cid)

    if config.circle_cid is not None:
        config.ax.figure.canvas.mpl_disconnect(config.circle_cid)

    config.circle_cid = config.ax.figure.canvas.mpl_connect('button_press_event', handle_input_circle)
    plt.title("Click left mouse button to set center")
    plt.draw()


# def draw_polygon():
#     if config.cid is not None:
#         config.ax.figure.canvas.mpl_disconnect(config.cid)
#
#     if config.circle_cid is not None:
#         config.ax.figure.canvas.mpl_disconnect(config.circle_cid)
#
#     config.circle_cid = config.ax.figure.canvas.mpl_connect('button_press_event', handle_input_polygon)
#     plt.title("Click left mouse button to set points")
#     plt.draw()

def handle_input_point(event):
    config.line_x, config.line_y = [None] * 2
    if event.button == 1:  # Left mouse button
        x, y = event.xdata, event.ydata
        point = Point((x, y), next(config.label_generator))
        draw_shape(point)

        # Disconnect the event listener so points can't be drawn anymore
        config.ax.figure.canvas.mpl_disconnect(config.cid)


def handle_input_line(event):
    if event.button == 1:  # Left mouse button
        if not config.line_x and not config.line_y:
            # First click sets the start point
            config.line_x, config.line_y = event.xdata, event.ydata
            plt.title("Click left click to draw the end point")
            plt.draw()

        else:
            # Second click sets the end point
            p1 = Point((config.line_x, config.line_y), next(config.label_generator))
            p2 = Point((event.xdata, event.ydata), next(config.label_generator))
            line = Line(p1, p2, next(config.label_generator))

            draw_shape(p1)
            draw_shape(p2)
            config.undo_stack.pop()
            config.undo_stack.pop()

            draw_shape(line)
            config.ax.figure.canvas.mpl_disconnect(config.cid)
            # Remove start_point attribute so user can draw another line
            config.line_x, config.line_y = [None] * 2
            plt.title("")
            plt.draw()


def handle_input_circle(event):
    if event.button == 1:  # Left mouse button
        if not config.circle_x and not config.circle_x:  # first click
            config.circle_x, config.circle_y = event.xdata, event.ydata
            config.ax.set_title("Click left click again to set the radius")
            config.ax.figure.canvas.draw()

        else:  # second click
            x, y = event.xdata, event.ydata
            radius = np.sqrt((x - config.circle_x) ** 2 + (y - config.circle_y) ** 2)
            circle = Circle((config.circle_x, config.circle_y), radius, next(config.label_generator))
            draw_shape(circle)

            # Disconnect the circle event listener so it doesn't interfere with other shapes
            config.ax.figure.canvas.mpl_disconnect(config.circle_cid)
            config.circle_cid, config.circle_x, config.circle_y = [None] * 3


#
# def handle_input_polygon(event):
#     if event.button == 1:  # Left mouse button
#         if len(config.polygon_vertices) == 0:
#             draw_point_shape(event.xdata, event.ydata)
#             config.polygon_vertices.append((event.xdata, event.ydata))
#         else:
#             if (event.xdata, event.ydata) == (config.polygon_vertices[0]):
#                 draw_point_shape(event.xdata, event.ydata)
#                 last_point = config.polygon_vertices[-1]
#                 line = Line((event.xdata, event.ydata), (last_point[0], last_point[1]))
#                 draw_line_shape(line)
#                 config.polygon_vertices.append((event.xdata, event.ydata))
#
#                 config.ax.figure.canvas.mpl_disconnect(config.cid)
#                 # Remove start_point attribute so user can draw another line
#                 config.polygon_vertices = []
#                 plt.title("")
#                 plt.draw()
#
#             else:
#                 draw_point_shape(event.xdata, event.ydata)
#                 last_point = config.polygon_vertices[-1]
#                 p1 = Point((event.xdata, event.ydata))
#                 p2 = Point((last_point[0], last_point[1]))
#                 line = Line(p1, p2)
#                 draw_line_shape(line)
#                 config.polygon_vertices.append((event.xdata, event.ydata))
#
#                 config.circle_cid = config.ax.figure.canvas.mpl_connect('button_press_event', handle_input_polygon)

def delete_by_label(label):
    for shape in config.shapes:
        if shape.get_label() == label:
            if isinstance(shape, Point):
                line = shape.is_line_part()
                if line is not False:
                    start = line.get_start()
                    end = line.get_end()

                    config.shapes.remove(start)
                    config.shapes.remove(end)
                    config.shapes.remove(line)

                    config.deleted_labels.append(start.get_label())
                    config.deleted_labels.append(end.get_label())
                    config.deleted_labels.append(line.get_label())

                    command = {"type": 'delete', "shape": line}
                    config.undo_stack.insert(len(config.undo_stack), command)

                else:
                    config.shapes.remove(shape)
                    config.deleted_labels.append(shape.get_label())

                    command = {"type": 'delete', "shape": shape}
                    config.undo_stack.insert(len(config.undo_stack), command)

            elif isinstance(shape, Line):
                start = shape.get_start()
                end = shape.get_end()

                config.shapes.remove(start)
                config.shapes.remove(end)
                config.shapes.remove(shape)

                config.deleted_labels.append(start.get_label())
                config.deleted_labels.append(end.get_label())
                config.deleted_labels.append(shape.get_label())

                command = {"type": 'delete', "shape": shape}
                config.undo_stack.insert(len(config.undo_stack), command)

            elif isinstance(shape, Circle):
                config.shapes.remove(shape)
                config.deleted_labels.append(shape.get_label())

                command = {"type": 'delete', "shape": shape}
                config.undo_stack.insert(len(config.undo_stack), command)

    update_display()
    update_label()


def handle_delete_shape(event):
    if event.button == 1:
        shape = shape_clicked(event.xdata, event.ydata)
        if shape is not None:
            delete_by_label(shape.get_label())


def draw_shape(shape):
    shape.draw(config.ax)
    config.shapes.append(shape)

    command = {"type": 'draw', "shape": shape}
    config.undo_stack.insert(len(config.undo_stack), command)

    update_display()
    update_label()


def run():
    config.root.mainloop()


def on_closing():
    # if messagebox.askokcancel("Quit", "Do you want to quit?"):
    config.root.quit()
    config.root.destroy()


def update_display():
    config.ax.cla()
    config.ax.set_xlim(-10, 10)
    config.ax.set_ylim(-10, 10)
    config.ax.set_aspect('equal')  # Set the aspect ratio to 'equal'
    config.ax.grid(True)
    config.ax.set_xticks(np.arange(-20, 21, 5))
    config.ax.set_yticks(np.arange(-20, 21, 5))
    # config.canvas.update_idletasks()
    for shape in config.shapes:
        if isinstance(shape, Point):
            flag = False
            for s in config.shapes:
                if isinstance(s, Line):
                    if s.is_line_edge(shape)[0]:
                        flag = True

            if not flag:
                shape.draw(config.ax)

            else:
                pass

        elif isinstance(shape, Circle):
            shape.draw(config.ax)

        elif isinstance(shape, Line):
            shape.get_start().draw(config.ax)
            shape.get_end().draw(config.ax)
            shape.draw(config.ax)

    plt.draw()


def update_label():
    global label_text, coords
    for widget in config.label_widgets:
        widget.destroy()
    config.label_widgets = []

    for shape in config.shapes:
        if isinstance(shape, Line):
            m, b = shape.m_b()
            label_text = f'({shape.get_label()}) Line: y = {m:.3f}x + {b:.3f}'

        elif isinstance(shape, Point):
            try:
                label_text = f'({shape.get_label()}) Point: ({shape.get_x():.3f}, {shape.get_y():.3f})'

            except TypeError:
                print(f'coords:')

        elif isinstance(shape, Circle):
            x, y = shape.coords[0]
            r = shape.radius
            label_text = f'({shape.get_label()}) Circle: (x-{x:.3f})^2 + (y-{y:.3f})^2 = {r ** 2:.3f}'

        label_widget = tk.Label(config.side_panel.text, text=label_text, bg='white')
        label_widget.pack(anchor='w')
        config.label_widgets.append(label_widget)


def reset():
    command = {"type": 'reset', "list": config.shapes}
    config.undo_stack.insert(len(config.undo_stack), command)

    config.ax.clear()
    config.shapes = []
    config.deleted_labels = []
    for widget in config.label_widgets:
        widget.destroy()
    config.label_widgets = []
    config.label_generator = generate_alphanumeric_sequence()
    # Reset the axes and grid
    config.ax.set_xlim(-10, 10)
    config.ax.set_ylim(-10, 10)
    config.ax.set_aspect('equal')
    config.ax.grid(True)
    config.ax.set_xticks(np.arange(-20, 21, 5))
    config.ax.set_yticks(np.arange(-20, 21, 5))

    plt.draw()


def save():
    global shape_data
    filepath = filedialog.asksaveasfilename(defaultextension=".p", filetypes=[("PICKLE Files", "*.p")])
    if not filepath:
        return
    shapes_data = []
    for shape in config.shapes:
        shape_data = {"shape": shape}
        shapes_data.append(shape_data)

    with open(filepath, 'wb') as f:
        pickle.dump(shapes_data, f)


def load():
    global config
    filepath = filedialog.askopenfilename(filetypes=[("PICKLE Files", "*.p")])
    if not filepath:
        return

    reset()
    with open(filepath, 'rb') as f:
        shapes_data = pickle.load(f)

    for shape_data in shapes_data:
        shape = shape_data["shape"]

        if isinstance(shape, Line):
            draw_shape(shape.get_start())
            draw_shape(shape.get_end())
            draw_shape(shape)

            config.undo_stack.pop()
            config.undo_stack.pop()
            config.undo_stack.pop()


        elif isinstance(shape, Circle):
            draw_shape(shape)
            config.undo_stack.pop()

        elif isinstance(shape, Point):
            if not shape.is_line_part([x["shape"] for x in shapes_data]):
                print("true")
                draw_shape(shape)
                config.undo_stack.pop()

    debug(config.shapes)


def do_same_command(command):
    if command["type"] == 'delete':
        shape = command["shape"]
        if isinstance(shape, Point):
            config.shapes.remove(shape)

        if isinstance(shape, Line):
            start = shape.get_start()
            end = shape.get_end()

            config.shapes.remove(start)
            config.shapes.remove(end)
            config.shapes.remove(shape)

        if isinstance(shape, Circle):
            config.shapes.remove(shape)

    elif command["type"] == 'draw':
        shape = command["shape"]

        if isinstance(shape, Point):
            if not shape.is_line_part():
                draw_shape(shape)
                config.undo_stack.pop()

        if isinstance(shape, Line):
            start = shape.get_start()
            end = shape.get_end()

            draw_shape(start)
            draw_shape(end)
            draw_shape(shape)
            config.undo_stack.pop()
            config.undo_stack.pop()
            config.undo_stack.pop()

        if isinstance(shape, Circle):
            draw_shape(shape)
            config.undo_stack.pop()

    elif command["type"] == 'reset':
        reset()
    # elif command["type"] is 'move':

    update_display()
    update_label()


def do_opposite_command(command):
    if command["type"] == 'draw':
        shape = command["shape"]
        if isinstance(shape, Point):
            config.shapes.remove(shape)

        if isinstance(shape, Line):
            start = shape.get_start()
            end = shape.get_end()

            config.shapes.remove(start)
            config.shapes.remove(end)
            config.shapes.remove(shape)

        if isinstance(shape, Circle):
            config.shapes.remove(shape)

    elif command["type"] == 'delete':
        shape = command["shape"]
        if isinstance(shape, Point):
            if not shape.is_line_part():
                draw_shape(shape)
                config.undo_stack.pop()

        if isinstance(shape, Line):
            start = shape.get_start()
            end = shape.get_end()

            draw_shape(start)
            draw_shape(end)
            config.undo_stack.pop()
            config.undo_stack.pop()
            draw_shape(shape)

        if isinstance(shape, Circle):
            draw_shape(shape)

    elif command["type"] == 'reset':
        config.shapes = command["list"]



    update_display()
    update_label()


r = logging.getLogger()
r.setLevel(logging.DEBUG)


def redo():
    if len(config.redo_stack) == 0:
        "nothing to redo"

    elif len(config.redo_stack) > 0:

        command = config.redo_stack.pop()
        config.last_command_redo = command
        do_same_command(command)
        config.undo_stack.append(command)

    debug(f'redo: {config.redo_stack}')
    debug(f'undo: {config.undo_stack}')


def undo():
    if len(config.undo_stack) == 0:
        "nothing to undo"
    elif len(config.undo_stack) > 0:

        command = config.undo_stack.pop()
        config.last_command_undo = command
        do_opposite_command(command)
        config.redo_stack.append(command)

    debug(f'redo: {config.redo_stack}')
    debug(f'undo: {config.undo_stack}')


def clear_history():
    config.undo_stack = []
    config.redo_stack = []
