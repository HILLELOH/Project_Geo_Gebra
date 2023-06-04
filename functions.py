import json
import logging
import pickle
import random
import tkinter as tk

import matplotlib.pyplot as plt
import numpy as np

import config

from logging import debug
from tkinter import ttk, filedialog, messagebox
from Shapes.Circle import *
from Shapes.Point import *
from Shapes.Line import *
from Shapes.Polygon import Polygon
from Shapes.Segment import *
from label_generator import generate_alphanumeric_sequence, get_label_parts
import re
from screeninfo import get_monitors
config.label_generator = generate_alphanumeric_sequence()
from scipy.spatial import ConvexHull, Delaunay


class SidePanel(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.text = tk.Text(self, wrap=tk.WORD)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self, command=self.text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=scrollbar.set)


def center_window(window):
    window.update_idletasks()  # Ensure that window dimensions are updated

    # Get screen dimensions
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the position for the window
    x = (screen_width - window.winfo_width()) // 2
    y = (screen_height - window.winfo_height()) // 2

    # Set the window position
    window.geometry(f"+{x}+{y}")

def init_program():
    # config.root.geometry("1400x900")
    # config.root.geometry("1920x1080")
    screen_width = get_monitors()[0].width
    screen_height = get_monitors()[0].height

    # Set the size of the root window to match the screen size
    config.root.geometry(f"{screen_width}x{screen_height}")


    config.root.resizable(False, False)

    config.root.wm_title("PyGeoGebra")


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
    point_button = tk.Button(config.buttons_panel, text="Point", command=draw_point)
    line_button = tk.Button(config.buttons_panel, text="Line", command=draw_line)
    segment_button = tk.Button(config.buttons_panel, text="Segment", command=draw_segment)
    circle_button = tk.Button(config.buttons_panel, text="Circle", command=draw_circle)
    polygon_button = tk.Button(config.buttons_panel, text="Polygon", command=draw_polygon)
    reset_button = tk.Button(config.buttons_panel, text="Reset", command=reset)
    save_button = tk.Button(config.buttons_panel, text="Save", command=save)
    load_button = tk.Button(config.buttons_panel, text="Load file", command=load)
    delete_button = tk.Button(config.buttons_panel, text="Delete shape", command=delete_shape)
    undo_button = tk.Button(config.buttons_panel, text="undo", command=undo)
    redo_button = tk.Button(config.buttons_panel, text="redo", command=redo)
    clear_history_button = tk.Button(config.buttons_panel, text="clear history", command=clear_history)
    tmp = tk.Button(config.buttons_panel, text="Convex Hull", command=convex)
    ix = tk.Button(config.buttons_panel, text="x", command=x)
    tri = tk.Button(config.buttons_panel, text="Triangulation", command=triangulation)

    buttons = [save_button,
               load_button,
               delete_button,
               reset_button,

               point_button,
               line_button,
               segment_button,
               circle_button,
               polygon_button,
               tmp,
               ix,
               tri,

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

def x():
    for shape in config.shapes:
        if isinstance(shape, Segment):
            if shape.get_label() == '':
                config.shapes.remove(shape)
    update_label()
    update_display()


def convex():
    x()
    for shape in config.shapes:
        if isinstance(shape, Polygon):
            points = []
            for segment in shape.get_segment_list():
                start = segment.get_start()
                end = segment.get_end()
                if start not in points:
                    points.append(start)
                if end not in points:
                    points.append(end)
            poly = shape.graham_scan(points)
            for edge_poly in poly:
                draw_shape(edge_poly)
        #         edge_poly.set_color('green')
        #     for seg in shape.get_segment_list():
        #         seg.set_color('blue')
        # plt.draw()

def triangulation():
    for shape in config.shapes:
        if isinstance(shape, Polygon):
            triangles = shape.triangulation()
            for tria in triangles:
                draw_shape(tria)



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
            center = shape.get_center()

            distance = np.sqrt((x - center.get_x()) ** 2 + (y - center.get_y()) ** 2)
            if np.abs(distance - shape.radius) <= threshold:
                return shape

        elif isinstance(shape, Line):
            m, b = shape.m_b()
            line_y = m * x + b
            if np.abs(y - line_y) <= threshold:
                return shape

        elif isinstance(shape, Segment):
            m, b = shape.m_b()
            segment_y = m * x + b
            if np.abs(y - segment_y) <= threshold:
                return shape
    return


def open_insert_window(point):
    # Create a new Tkinter window

    insert_window = tk.Toplevel()
    config.set_shape = 1
    insert_window.geometry("200x120")
    insert_window.resizable(False, False)

    # Create labels and entry fields for x and y coordinates
    x_label = tk.Label(insert_window, text="X Coordinate:")
    x_label.pack()
    x_entry = tk.Entry(insert_window)
    x_entry.pack()

    y_label = tk.Label(insert_window, text="Y Coordinate:")
    y_label.pack()
    y_entry = tk.Entry(insert_window)
    y_entry.pack()

    # Function to handle the submission of x and y coordinates
    def set_point():
        x = x_entry.get()
        y = y_entry.get()
        point.set_p(int(x), int(y))
        config.set_shape = 0
        insert_window.destroy()
        update_label()
        update_display()

        # Bind the window closing event to a function

    def on_closing():
        config.set_shape = 0
        insert_window.destroy()

        # Set the window closing event handler

    insert_window.protocol("WM_DELETE_WINDOW", on_closing)
    submit_button = tk.Button(insert_window, text="Submit", command=set_point)
    submit_button.pack()


def on_press(event):
    if event.button == 1:  # Left mouse button
        config.selected_shape = shape_clicked(event.xdata, event.ydata)
        if config.selected_shape is not None:
            config.start_drag_x, config.start_drag_y = event.xdata, event.ydata

    elif event.button == 3:
        config.selected_shape = shape_clicked(event.xdata, event.ydata)
        if isinstance(config.selected_shape, Point):
            config.start_drag_x, config.start_drag_y = event.xdata, event.ydata
            print(config.set_shape)
            if config.set_shape == 0:
                open_insert_window(config.selected_shape)




def on_release(event):
    if config.selected_shape is not None:
        config.selected_shape = None
        config.start_drag_x, config.start_drag_y = None, None


def on_motion(event):
    if config.selected_shape is not None and event.xdata is not None and event.ydata is not None and event.button == 1:

        x, y = event.xdata, event.ydata
        dx = x - config.start_drag_x
        dy = y - config.start_drag_y
        config.start_drag_x, config.start_drag_y = x, y

        if isinstance(config.selected_shape, Point):
            s = config.selected_shape
            s.set_x(dx)
            s.set_y(dy)

        elif isinstance(config.selected_shape, Circle):
            center = config.selected_shape.get_center()
            center.set_x(dx)
            center.set_y(dy)

        elif isinstance(config.selected_shape, Line):  # Check if the selected_shape is a Line
            s = config.selected_shape
            s.set_start_point(dx, dy)
            s.set_end_point(dx, dy)

        elif isinstance(config.selected_shape, Segment):  # Check if the selected_shape is a Line
            s = config.selected_shape
            s.set_start_point(dx, dy)
            s.set_end_point(dx, dy)

        update_display()
        update_label()
        plt.draw()


def shape_set_coordinate(shape, x_coord, y_coord):
    dx = x_coord
    dy = y_coord
    if isinstance(shape, Point):
        shape.coords[0][0] += dx
        shape.coords[0][1] += dy
        shape.set_x(dx)
        shape.set_y(dy)

    elif isinstance(shape, Circle):
        shape.get_center().coords[0][0] += dx
        shape.get_center().coords[0][1] += dy

        shape.set_center(dx, dy)

    elif isinstance(shape, Line):
        start = shape.get_start()
        end = shape.get_end()

        start.coords[0][0] += dx
        start.coords[0][1] += dy
        shape.set_start_point(dx, dy)

        end.coords[0][0] += dx
        end.coords[0][1] += dy
        shape.set_end_point(dx, dy)

    elif isinstance(shape, Segment):
        start = shape.get_start()
        end = shape.get_end()

        start.coords[0][0] += dx
        start.coords[0][1] += dy
        shape.set_start_point(dx, dy)

        end.coords[0][0] += dx
        end.coords[0][1] += dy
        shape.set_end_point(dx, dy)

    update_display()
    update_label()
    plt.draw()


def on_scroll(event):
    ax = config.ax
    fig = config.fig
    x, y = event.xdata, event.ydata

    if event.button == 'up':  # Zoom in
        factor = 0.95
        if ax.get_xlim()[1] - ax.get_xlim()[0] < 10:  # Check if x range is too small
            return
        if ax.get_ylim()[1] - ax.get_ylim()[0] < 10:  # Check if y range is too small
            return
    elif event.button == 'down':  # Zoom out
        factor = 1.05
        # Check if x range or y range is too large
        x_range = ax.get_xlim()[1] - ax.get_xlim()[0]
        y_range = ax.get_ylim()[1] - ax.get_ylim()[0]
        if x_range > 100 or y_range > 100:
            return
        # Check if x range or y range is too small
        if x_range < 1 or y_range < 1:
            return
    elif event.button == 'pan':  # Drag
        # Calculate the distance moved
        dx = event.x - event.lastx
        dy = event.y - event.lasty
        # Update the plot limits based on the distance moved
        x_lim = ax.get_xlim()
        y_lim = ax.get_ylim()
        ax.set_xlim(x_lim[0] - dx, x_lim[1] - dx)
        ax.set_ylim(y_lim[0] - dy, y_lim[1] - dy)
        # Redraw the plot
        fig.canvas.draw_idle()
        return

    x_lim = ax.get_xlim()
    y_lim = ax.get_ylim()
    ax.set_xlim(x - factor * (x - x_lim[0]), x + factor * (x_lim[1] - x))
    ax.set_ylim(y - factor * (y - y_lim[0]), y + factor * (y_lim[1] - y))

    x_ticks_major = range(int(ax.get_xlim()[0]), int(ax.get_xlim()[1]) + 1, 1)
    y_ticks_major = range(int(ax.get_ylim()[0]), int(ax.get_ylim()[1]) + 1, 1)
    ax.xaxis.set_ticks(x_ticks_major, minor=False)
    ax.yaxis.set_ticks(y_ticks_major, minor=False)
    # Set grid lines
    ax.grid(True, which='major', linewidth=1)
    ax.grid(True, which='minor', linewidth=0.5)

    fig.canvas.draw_idle()


def hide(event):
    clicked_label = event.widget
    equality = clicked_label.cget("text")
    label = re.match("\((\\w+)\)", equality).groups()[0]
    shape = get_shape_by_label(label)
    print(label)

    if isinstance(shape, Point):
        circle = shape.is_circle_part()
        line = shape.is_line_part()
        segment = shape.is_segment_part()
        if circle:
            if shape.is_hidden():
                circle.set_hidden(False)
                shape.set_hidden(False)

            else:
                circle.set_hidden(True)
                shape.set_hidden(True)

        if line:
            if shape.is_hidden():
                line.get_start().set_hidden(False)
                line.get_end().set_hidden(False)
                line.set_hidden(False)

            else:
                line.get_start().set_hidden(True)
                line.get_end().set_hidden(True)
                line.set_hidden(True)

        if segment:
            if shape.is_hidden():
                segment.get_start().set_hidden(False)
                segment.get_end().set_hidden(False)
                segment.set_hidden(False)

            else:
                segment.get_start().set_hidden(True)
                segment.get_end().set_hidden(True)
                segment.set_hidden(True)

        elif not line and not circle and not segment:
            if shape.is_hidden():
                shape.set_hidden(False)
            else:
                shape.set_hidden(True)

    if isinstance(shape, Line):
        if shape.is_hidden():
            shape.get_start().set_hidden(False)
            shape.get_end().set_hidden(False)
            shape.set_hidden(False)

        else:
            shape.get_start().set_hidden(True)
            shape.get_end().set_hidden(True)
            shape.set_hidden(True)

    if isinstance(shape, Segment):
        if shape.is_hidden():
            shape.get_start().set_hidden(False)
            shape.get_end().set_hidden(False)
            shape.set_hidden(False)

        else:
            shape.get_start().set_hidden(True)
            shape.get_end().set_hidden(True)
            shape.set_hidden(True)

    if isinstance(shape, Circle):
        if shape.is_hidden():
            shape.get_center().set_hidden(False)
            shape.set_hidden(False)

        else:
            shape.get_center().set_hidden(True)
            shape.set_hidden(True)

    update_display()
    update_label()


def reset_cids():
    if not config.cid:
        config.ax.figure.canvas.mpl_disconnect(config.cid)

    if not config.circle_cid:
        config.ax.figure.canvas.mpl_disconnect(config.circle_cid)


def delete_shape():
    reset_cids()
    config.cid = config.ax.figure.canvas.mpl_connect('button_press_event', handle_delete_shape)
    plt.title("Click shape to delete")
    plt.draw()


def draw_point():
    reset_cids()
    config.cid = config.ax.figure.canvas.mpl_connect('button_press_event', handle_input_point)
    plt.title("Click left mouse button to create point")
    plt.draw()


def draw_line():
    reset_cids()
    config.cid = config.ax.figure.canvas.mpl_connect('button_press_event', handle_input_line)
    plt.title("Click left mouse button to start line")
    plt.draw()


def draw_segment():
    reset_cids()
    config.cid = config.ax.figure.canvas.mpl_connect('button_press_event', handle_input_segment)
    plt.title("Click left mouse button to start segment")
    plt.draw()


def draw_polygon():
    reset_cids()
    config.cid = config.ax.figure.canvas.mpl_connect('button_press_event', handle_input_polygon)
    plt.title("Click left mouse button to start polygon")

    plt.draw()


def draw_circle():
    reset_cids()
    config.circle_cid = config.ax.figure.canvas.mpl_connect('button_press_event', handle_input_circle)
    plt.title("Click left mouse button to set center")
    plt.draw()


def handle_input_point(event):
    config.line_x, config.line_y = [None] * 2
    if event.button == 1:  # Left mouse button
        x, y = event.xdata, event.ydata
        if x is None and y is None:
            return
        point = Point(x, y, next(config.label_generator))
        draw_shape(point)

        # Disconnect the event listener so points can't be drawn anymore
        config.ax.figure.canvas.mpl_disconnect(config.cid)


def handle_input_line(event):
    if event.button == 1:  # Left mouse button
        if event.xdata is None and event.ydata is None:
            return
        if not config.line_x and not config.line_y:
            # First click sets the start point
            config.line_x, config.line_y = event.xdata, event.ydata
            shape = shape_clicked(event.xdata, event.ydata)
            if isinstance(shape, Point):
                config.this_point = shape
            plt.title("Click left click to draw the end point")
            plt.draw()

        else:
            # Second click sets the end point
            if not config.this_point:
                p1 = Point(config.line_x, config.line_y, next(config.label_generator))
                draw_shape(p1)
                config.undo_stack.pop()

            else:
                p1 = config.this_point

            p2 = Point(event.xdata, event.ydata, next(config.label_generator))
            line = Line(p1, p2, next(config.label_generator))

            draw_shape(p2)
            config.undo_stack.pop()
            draw_shape(line)

            config.ax.figure.canvas.mpl_disconnect(config.cid)
            # Remove start_point attribute so user can draw another line
            config.line_x, config.line_y = [None] * 2
            config.this_point = None
            plt.title("")
            plt.draw()


def handle_input_segment(event):
    if event.button == 1:  # Left mouse button
        if event.xdata is None and event.ydata is None:
            return
        if not config.segment_x and not config.segment_y:
            # First click sets the start point
            config.segment_x, config.segment_y = event.xdata, event.ydata
            shape = shape_clicked(event.xdata, event.ydata)
            if isinstance(shape, Point):
                config.this_point = shape
            plt.title("Click left click to draw the end segment point")
            plt.draw()

        else:
            # Second click sets the end point
            if not config.this_point:
                p1 = Point(config.segment_x, config.segment_y, next(config.label_generator))
                draw_shape(p1)
                config.undo_stack.pop()

            else:
                p1 = config.this_point

            p2 = Point(event.xdata, event.ydata, next(config.label_generator))
            segment = Segment(p1, p2, next(config.label_generator))

            draw_shape(p2)
            config.undo_stack.pop()
            draw_shape(segment)
            config.ax.figure.canvas.mpl_disconnect(config.cid)
            # Remove start_point attribute so user can draw another line
            config.segment_x, config.segment_y = [None] * 2
            config.this_point = None
            plt.title("")
            plt.draw()


def handle_input_circle(event):
    if event.button == 1:  # Left mouse button
        if event.xdata is None and event.ydata is None:
            return
        if not config.circle_x and not config.circle_x:  # first click
            config.circle_x, config.circle_y = event.xdata, event.ydata
            shape = shape_clicked(event.xdata, event.ydata)
            if isinstance(shape, Point):
                config.this_point = shape

            config.ax.set_title("Click left click again to set the radius")
            config.ax.figure.canvas.draw()

        else:  # second click
            x, y = event.xdata, event.ydata
            if not config.this_point:
                radius = np.sqrt((x - config.circle_x) ** 2 + (y - config.circle_y) ** 2)
                center = Point(config.circle_x, config.circle_y, next(config.label_generator))
                draw_shape(center)
                config.undo_stack.pop()

            else:
                last_x, last_y = config.this_point.get_x(), config.this_point.get_y()
                radius = np.sqrt((x - last_x) ** 2 + (y - last_y) ** 2)
                center = config.this_point

            circle = Circle(center, radius, next(config.label_generator))
            draw_shape(circle)

            # Disconnect the circle event listener so it doesn't interfere with other shapes
            config.ax.figure.canvas.mpl_disconnect(config.circle_cid)
            config.circle_cid, config.circle_x, config.circle_y = [None] * 3


def handle_input_polygon(event):
    if event.button == 1:  # Left mouse button
        if event.xdata is None and event.ydata is None:
            return
        if not config.curr_polygon:
            # First click sets the start point

            config.curr_polygon = Polygon([], next(config.label_generator))
            config.polygon_x, config.polygon_y = event.xdata, event.ydata
            config.first_point_polygon = Point(event.xdata, event.ydata, next(config.label_generator))
            config.last_point_polygon = config.first_point_polygon
            plt.title("Click left click to draw the end segment point")
            plt.draw()

        elif shape_clicked(event.xdata, event.ydata) == config.first_point_polygon:
            print(shape_clicked(event.xdata, event.ydata))
            print(config.first_point_polygon)
            p1 = config.last_point_polygon
            p2 = config.first_point_polygon

            segment = Segment(p1, p2, next(config.label_generator))
            config.curr_polygon.add_segment(segment)
            draw_shape(p1)
            draw_shape(p2)
            config.shapes.pop()
            config.shapes.pop()
            draw_shape(segment)
            config.undo_stack.pop()
            config.undo_stack.pop()
            config.undo_stack.pop()
            config.shapes.append(config.curr_polygon)
            print(config.shapes)

            command = {"type": 'draw', "shape": config.curr_polygon}
            config.undo_stack.insert(len(config.undo_stack), command)

            config.ax.figure.canvas.mpl_disconnect(config.cid)
            config.first_point_polygon = None
            config.last_point_polygon = None
            config.curr_polygon = None
            config.polygon_x, config.polygon_y = [None] * 2
            plt.title("")
            plt.draw()

        else:
            # Second click sets the end point
            p1 = config.last_point_polygon
            p2 = Point(event.xdata, event.ydata, next(config.label_generator))
            segment = Segment(p1, p2, next(config.label_generator))

            config.curr_polygon.add_segment(segment)
            draw_shape(p1)
            if config.first_point_polygon != config.last_point_polygon:
                config.shapes.pop()

            draw_shape(p2)
            draw_shape(segment)

            config.undo_stack.pop()
            config.undo_stack.pop()
            config.undo_stack.pop()
            # draw_shape(config.curr_polygon)
            config.last_point_polygon = p2
            plt.title("Click left click to draw segment or finish the poly")
            plt.draw()


def get_shape_by_label(label):
    for shape in config.shapes:
        if shape.get_label() == label:
            return shape

    return None


def delete_by_label(label):
    shape = get_shape_by_label(label)
    if shape is not None:
        if isinstance(shape, Point):
            line = shape.is_line_part()
            circle = shape.is_circle_part()
            segment = shape.is_segment_part()
            if line is not False:
                debug("line_part")

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


            elif segment is not False:
                debug("segment_part")

                start = segment.get_start()
                end = segment.get_end()

                config.shapes.remove(start)
                config.shapes.remove(end)
                config.shapes.remove(segment)

                config.deleted_labels.append(start.get_label())
                config.deleted_labels.append(end.get_label())
                config.deleted_labels.append(segment.get_label())

                command = {"type": 'delete', "shape": segment}
                config.undo_stack.insert(len(config.undo_stack), command)

            elif circle is not False:
                debug("circle_part")
                center = circle.get_center()
                config.shapes.remove(center)
                config.shapes.remove(circle)
                config.deleted_labels.append(circle.get_label())
                config.deleted_labels.append(center.get_label())

                command = {"type": 'delete', "shape": circle}
                config.undo_stack.insert(len(config.undo_stack), command)

            elif not line and not segment and not circle:
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

        elif isinstance(shape, Segment):
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
            center = shape.get_center()
            label = shape.get_label()

            config.shapes.remove(center)
            config.deleted_labels.append(center.get_label())

            config.shapes.remove(shape)
            config.deleted_labels.append(label)

            command = {"type": 'delete', "shape": shape}
            config.undo_stack.insert(len(config.undo_stack), command)

        update_display()
        update_label()


def handle_delete_shape(event):
    if event.button == 1:
        shape = shape_clicked(event.xdata, event.ydata)
        if shape is not None:
            delete_by_label(shape.get_label())
    config.ax.figure.canvas.mpl_disconnect(config.cid)


def draw_shape(shape):
    label = shape.get_label()
    chars, numbers = get_label_parts(label)
    config.last_label_before_return = chars
    config.last_turn_before_return = numbers

    shape.draw(config.ax)
    config.shapes.append(shape)

    command = {"type": 'draw', "shape": shape}
    config.undo_stack.insert(len(config.undo_stack), command)

    update_display()
    update_label()


def run():
    config.root.mainloop()


def on_closing():
    if messagebox.askyesno("Quit", "Do you want to Save?"):
        save()
    config.root.quit()
    config.root.destroy()


def update_display():
    prev_xlim = config.ax.get_xlim()
    prev_ylim = config.ax.get_ylim()
    prev_aspect = config.ax.get_aspect()
    prev_xticks = config.ax.get_xticks()
    prev_yticks = config.ax.get_yticks()

    config.ax.cla()
    config.ax.set_xlim(prev_xlim)
    config.ax.set_ylim(prev_ylim)

    config.ax.set_xticks(prev_xticks)
    config.ax.set_yticks(prev_yticks)
    config.ax.set_aspect(prev_aspect)  # Set the aspect ratio to 'equal'
    config.ax.grid(True)


    for shape in config.shapes:
        if not shape.is_hidden():
            shape.draw(config.ax)
    plt.draw()


def update_label():
    global label_text, coords
    for widget in config.label_widgets:
        widget.destroy()
    config.label_widgets = []

    # unique = np.array(config.shapes)
    # uni = np.unique(unique)
    # config.shapes = uni.tolist()
    # res = [i for n, i in enumerate(test_list) if i not in test_list[:n]]

    # config.shapes = [i for n, i in enu]

    # print(f"Before:  {config.shapes}")
    # uni = []
    # for shape in config.shapes:
    #     if shape not in uni:
    #         uni.append(shape)
    # config.shapes = uni
    # print(f"After:  {uni}")

    # config.shapes = list(set(config.shapes))

    l = []
    for shape in config.shapes:
        if shape.get_label() in l:
            continue
        l.append(shape.get_label())
        if shape.get_label() == '':
            continue
        hidden_str = ''
        if shape.is_hidden():
            hidden_str = '[hidden]'
        if isinstance(shape, Line):
            m, b = shape.m_b()
            label_text = f'({shape.get_label()}) Line: y = {m:.3f}x + {b:.3f} {hidden_str} '

        elif isinstance(shape, Segment):
            m, b = shape.m_b()
            label_text = f'({shape.get_label()}) Line: y = {m:.3f}x + {b:.3f} {hidden_str} '

        elif isinstance(shape, Point):
            try:
                label_text = f'({shape.get_label()}) Point: ({shape.get_x():.3f}, {shape.get_y():.3f}) {hidden_str} '

            except TypeError:
                print(f'coords:')

        elif isinstance(shape, Circle):
            x = shape.get_center().get_x()
            y = shape.get_center().get_y()
            r = shape.get_radius()

            label_text = f'({shape.get_label()}) Circle: (x-{x:.3f})^2 + (y-{y:.3f})^2 = {r ** 2:.3f} {hidden_str} '

        config.label_widget = tk.Label(config.side_panel.text, text=label_text, bg='white')
        config.label_widget.pack(anchor='w')
        config.label_widgets.append(config.label_widget)
        config.label_widget.bind("<Button-1>", hide)



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

        elif isinstance(shape, Segment):
            draw_shape(shape.get_start())
            draw_shape(shape.get_end())
            draw_shape(shape)

            config.undo_stack.pop()
            config.undo_stack.pop()
            config.undo_stack.pop()

        elif isinstance(shape, Circle):
            center = shape.get_center()
            draw_shape(center)
            draw_shape(shape)

            config.undo_stack.pop()
            config.undo_stack.pop()

        elif isinstance(shape, Point):
            l = [x["shape"] for x in shapes_data]
            if not shape.is_line_part(l) and not shape.is_circle_part(l) and not shape.is_segment_part(l):
                draw_shape(shape)
                config.undo_stack.pop()

    debug(config.shapes)


def do_same_command(command):
    global curr_x, curr_y
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

        if isinstance(shape, Segment):
            start = shape.get_start()
            end = shape.get_end()

            config.shapes.remove(start)
            config.shapes.remove(end)
            config.shapes.remove(shape)

        if isinstance(shape, Circle):
            center = shape.get_center()

            config.shapes.remove(center)
            config.shapes.remove(shape)

    elif command["type"] == 'draw':
        shape = command["shape"]

        if isinstance(shape, Point):
            if not shape.is_line_part() and not shape.is_circle_part() and not shape.is_segment_part():
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

        if isinstance(shape, Segment):
            start = shape.get_start()
            end = shape.get_end()

            draw_shape(start)
            draw_shape(end)
            draw_shape(shape)

            config.undo_stack.pop()
            config.undo_stack.pop()
            config.undo_stack.pop()

        if isinstance(shape, Circle):
            center = shape.get_center()

            draw_shape(center)
            draw_shape(shape)

            config.undo_stack.pop()
            config.undo_stack.pop()

        if isinstance(shape, Polygon):
            for segment in shape.get_segment_list():
                draw_shape(segment)
                config.undo_stack.pop()

                draw_shape(segment.get_start())
                config.undo_stack.pop()


    elif command["type"] == 'move':
        shape = command["shape"]
        x = command["last_x"]
        y = command["last_y"]

        if isinstance(shape, Point):
            curr_x = -1 * shape.get_x() + x
            curr_y = -1 * shape.get_y() + y

        if isinstance(shape, Line):
            pass

        if isinstance(shape, Segment):
            pass

        if isinstance(shape, Circle):
            center = shape.get_center()
            curr_x = -1 * center.get_x() + x
            curr_y = -1 * center.get_y() + y

        dx = curr_x
        dy = curr_y

        shape_set_coordinate(shape, dx, dy)



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

        if isinstance(shape, Segment):
            start = shape.get_start()
            end = shape.get_end()

            config.shapes.remove(start)
            config.shapes.remove(end)
            config.shapes.remove(shape)

        if isinstance(shape, Circle):
            center = shape.get_center()

            config.shapes.remove(center)
            config.shapes.remove(shape)

        if isinstance(shape, Polygon):
            for segment in shape.get_segment_list():
                config.shapes.remove(segment)
                config.shapes.remove(segment.get_start())



    elif command["type"] == 'delete':
        shape = command["shape"]
        if isinstance(shape, Point):
            if not shape.is_line_part() and not shape.is_circle_part() and not shape.is_segment_part():
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

        if isinstance(shape, Segment):
            start = shape.get_start()
            end = shape.get_end()

            draw_shape(start)
            draw_shape(end)
            draw_shape(shape)

            config.undo_stack.pop()
            config.undo_stack.pop()
            config.undo_stack.pop()

        if isinstance(shape, Circle):
            center = shape.get_center()

            draw_shape(center)
            draw_shape(shape)

            config.undo_stack.pop()
            config.undo_stack.pop()

    elif command["type"] == 'move':
        shape = command["shape"]
        x = command["last_x"]
        y = command["last_y"]
        curr_x = -999999
        curr_y = -999999
        if isinstance(shape, Point):
            curr_x = shape.get_x()
            curr_y = shape.get_y()

        if isinstance(shape, Line):
            pass

        if isinstance(shape, Circle):
            center = shape.get_center()
            curr_x = center.get_x()
            curr_y = center.get_y()

        dx = x - curr_x
        dy = y - curr_y
        shape_set_coordinate(shape, dx, dy)


    elif command["type"] == 'reset':
        config.shapes = command["list"]

    update_display()
    update_label()


def redo():
    if len(config.redo_stack) == 0:
        "nothing to redo"

    elif len(config.redo_stack) > 0:

        command = config.redo_stack.pop()
        config.last_command_redo = command
        do_same_command(command)
        config.undo_stack.append(command)


def undo():
    if len(config.undo_stack) == 0:
        "nothing to undo"
    elif len(config.undo_stack) > 0:

        command = config.undo_stack.pop()
        config.last_command_undo = command
        do_opposite_command(command)
        config.redo_stack.append(command)


def clear_history():
    config.undo_stack = []
    config.redo_stack = []
