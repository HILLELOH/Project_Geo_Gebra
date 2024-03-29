import json
import logging
import os
import pickle
import random
import tkinter as tk
from colorama import init as coloramainit

coloramainit()

from tkinter import ttk, filedialog, messagebox
from Shapes.Circle import *
from Shapes.Point import *
from Shapes.Line import *
from Shapes.Polygon import Polygon
from Shapes.Segment import *
from label_generator import generate_alphanumeric_sequence, get_label_parts
import re
import config
config.label_generator = generate_alphanumeric_sequence()
from scipy.spatial import ConvexHull, Delaunay


class SidePanel(tk.Frame):
    def __init__(self, parent, bool, side, pack_bool):
        tk.Frame.__init__(self, parent)
        self.text = tk.Text(self, wrap=tk.WORD)
        self.text.configure(state="disabled")

        if pack_bool:
            self.text.pack(side=side, fill=tk.BOTH, expand=True)

        if bool:
            scrollbar = ttk.Scrollbar(self, command=self.text.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.text.config(yscrollcommand=scrollbar.set)

    def insert_text(self, text):
        self.text.configure(state="normal")  # Enable editing
        self.text.insert(tk.END, text)  # Insert the text at the end
        self.text.configure(state="disabled")  # Disable editing

    def insert_block(self, texts):
        for text in texts:
            self.insert_text(text)

    def clear_text(self):
        self.text.configure(state="normal")  # Enable editing
        self.text.delete(1.0, tk.END)  # Delete all text from the start to the end
        self.text.configure(state="disabled")  # Disable editing


def init_program():
    width = config.root.winfo_screenwidth()
    height = config.root.winfo_screenheight()
    # setting tkinter window size
    config.root.geometry("%dx%d" % (width, height))

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

    algors = tk.Button(config.buttons_panel, text="Algorithms", command=algos)
    undo_button = tk.Button(config.buttons_panel, text="undo", command=undo)
    redo_button = tk.Button(config.buttons_panel, text="redo", command=redo)
    clear_history_button = tk.Button(config.buttons_panel, text="clear history", command=clear_history)
    info_button = tk.Button(config.buttons_panel, text="Info", command=information)

    buttons = [save_button,
               load_button,
               delete_button,
               reset_button,

               point_button,
               line_button,
               segment_button,
               circle_button,
               polygon_button,
               algors,
               # tmp,
               # ix,

               # file_button,
               info_button,
               clear_history_button,
               redo_button,
               undo_button]

    padding = 2
    right = [info_button,
            clear_history_button,
             undo_button,
             redo_button, ]
    for i in range(len(buttons)):
        if buttons[i] in right:
            buttons[i].pack(side=tk.RIGHT, padx=padding)
        else:
            buttons[i].pack(side=tk.LEFT, padx=padding)


# def show_algorithms():
#     # Function to display the choices for Algorithms
#     config.info_panel.config(text="Choose an algorithm:")
#     choices = ["Yes", "No", "Maybe"]
#     config.option_var.set(choices[0])  # Set the default choice
#     config.option_menu = tk.OptionMenu(config.info_window, config.option_var, *choices)
#     config.option_menu.pack(padx=10, pady=10)
#     config.current_selection = "Algorithms"
#
# def show_shapes():
#     # Function to display the choices for Shapes
#     config.info_panel.config(text="Choose a shape:")
#     choices = ["Line", "Segment", "Triangle", "Circle", "Polygon"]
#     config.option_var.set(choices[0])  # Set the default choice
#     config.option_menu = tk.OptionMenu(config.info_window, config.option_var, *choices)
#     config.option_menu.pack(padx=10, pady=10)
#     config.current_selection = "Shapes"
#
#
# def information():
#     if not config.isopen_info_panel:  # Check if info panel is not already open
#         # Create a new window (panel) to display the message
#         config.info_window = tk.Toplevel(config.root)  # 'root' is the main Tkinter window
#
#         # Set the window title
#         config.info_window.title("Information Panel")
#
#         # Create a label with the message
#         config.info_panel = tk.Label(config.info_window, text="Hello")
#         config.info_panel.pack(padx=10, pady=10)
#
#         # Add a variable to store the selected choice
#         config.option_var = tk.StringVar()
#
#         # Add a variable to store the current selection
#         config.current_selection = ""
#
#         # Set config.isopen_info_panel to True to indicate that the panel is now open
#         config.isopen_info_panel = True
#
#         # Create a menu for selecting Algorithms or Shapes
#         menu_choices = ["Algorithms", "Shapes"]
#         config.menu_var = tk.StringVar(config.info_window)
#         config.menu_var.set(menu_choices[0])  # Set the default choice
#         config.menu = tk.OptionMenu(config.info_window, config.menu_var, *menu_choices, command=menu_callback)
#         config.menu.pack(padx=10, pady=10)
#
#
# def menu_callback(selection):
#     # Function to handle the selection from the Algorithms/Shapes menu
#     if config.current_selection == selection:
#         # If the same selection is chosen, do nothing
#         return
#
#     # Remove the existing option menu if it exists
#     if hasattr(config, "option_menu"):
#         config.option_menu.pack_forget()
#
#     if selection == "Algorithms":
#         show_algorithms()
#     elif selection == "Shapes":
#         show_shapes()


# def show_information():
#     # Function to display the information about the chosen shape
#     config.info_label = tk.Label(config.info_window, text="", font=("Arial", 12), anchor="center")
#     config.info_label.pack(padx=10, pady=5)
#     chosen_shape = config.option_var.get()
#     info_text = f"{chosen_shape}"
#     config.info_label.config(text=info_text, font=("Arial", 18, "bold"), fg="blue")
#
#     # config.canvas.delete("all")
#
#     # Display the corresponding image based on the selected shape
#     chosen_shape = config.option_var.get()
#     image = None
#     if chosen_shape != "Choose":
#         l = os.listdir("./Images")
#         print(l)
#         image = tk.PhotoImage(file=f"./Images/{chosen_shape}.png")
#         config.info_window.create_image(150, 50, image=image)
#
#
# def show_shapes():
#     # Function to display the choices for Shapes
#     config.info_panel.config(text="Choose a shape:")
#     choices = ["Choose", "Point", "Segment", "Line", "Circle", "Polygon"]
#     config.option_var.set(choices[0])  # Set the default choice
#     config.option_menu = tk.OptionMenu(config.info_window, config.option_var, *choices)
#     config.option_menu.pack(padx=10, pady=10)
#     config.current_selection = "Shapes"
#
# def on_panel_close():
#     # Function to handle the event when the information panel is closed
#     config.isopen_info_panel = False
#     config.info_window.destroy()
#     config.info_panel = None
#     config.info_label = None
#     config.current_selection = ""
#
#
# def information():
#     if not config.isopen_info_panel:
#         # Create a new window (panel) to display the message
#         config.info_window = tk.Toplevel(config.root)
#
#         # Set the window title
#         config.info_window.title("Information Panel")
#         config.info_window.geometry("400x700")
#
#         # Bind the event of closing the panel window to on_panel_close function
#         config.info_window.protocol("WM_DELETE_WINDOW", on_panel_close)
#
#         # Create a label with the message
#         config.info_panel = tk.Label(config.info_window, text="Choose a shape:")
#         config.info_panel.pack(padx=10, pady=10)
#
#         # Add a variable to store the selected choice
#         config.option_var = tk.StringVar()
#
#         # Add a variable to store the current selection
#         config.current_selection = ""
#
#         # Create a menu for selecting Shapes
#         choices = ["Choose", "Point", "Segment", "Line", "Circle", "Polygon"]
#         config.option_var.set(choices[0])  # Set the default choice
#         config.option_menu = tk.OptionMenu(config.info_window, config.option_var, *choices)
#         config.option_menu.pack(padx=10, pady=10)
#
#
#
#         # Set config.isopen_info_panel to True to indicate that the panel is now open
#         config.isopen_info_panel = True
#
#         # Create a "Show Information" button
#         show_info_btn = tk.Button(config.info_window, text="Load Info", command=show_information)
#         show_info_btn.pack(pady=5)
from PIL import Image, ImageTk


def display_shape_information(chosen_shape):
    info_file_path = f"./Info/{chosen_shape}_info.txt"

    if os.path.exists(info_file_path):
        with open(info_file_path, "r") as info_file:
            info_text = info_file.read()
    else:
        info_text = f"No information available for {chosen_shape}."

    config.info_label.config(text=info_text, font=("Arial", 14), fg="black")

def show_information():
    config.info_label.config(text="", font=("Arial", 12), anchor="center")
    chosen_shape = config.option_var.get()
    info_text = f"{chosen_shape}"
    config.info_label.config(text=info_text, font=("Arial", 18, "bold"), fg="blue")

    display_shape_information(chosen_shape)

    config.image_canvas.delete("all")

    if chosen_shape != "Choose":
        image_path = f"./Images/{chosen_shape}.png"
        if os.path.exists(image_path):
            pil_image = Image.open(image_path)

            canvas_width = config.image_canvas.winfo_width()
            canvas_height = config.image_canvas.winfo_height()
            image_width, image_height = pil_image.size
            scale_factor = min(canvas_width / image_width, canvas_height / image_height)

            new_width = int(image_width * scale_factor)
            new_height = int(image_height * scale_factor)
            pil_image = pil_image.resize((new_width, new_height), Image.ANTIALIAS)

            config.image = ImageTk.PhotoImage(pil_image)

            config.image_canvas.config(width=canvas_width, height=canvas_height)
            config.image_canvas.create_image((canvas_width - new_width) // 2, (canvas_height - new_height) // 2,
                                             anchor=tk.NW, image=config.image)
        else:
            print(f"Image not found: {image_path}")


def on_panel_close():
    config.isopen_info_panel = False
    config.info_window.destroy()
    config.info_panel = None
    config.info_label = None
    config.image_canvas = None
    config.current_selection = ""

def information():
    if not config.isopen_info_panel:
        config.info_window = tk.Toplevel(config.root)

        config.info_window.title("Information Panel")
        config.info_window.geometry("900x1000")

        config.info_window.protocol("WM_DELETE_WINDOW", on_panel_close)

        config.info_panel = tk.Label(config.info_window, text="Choose a shape:")
        config.info_panel.pack(padx=10, pady=10)

        config.option_var = tk.StringVar()
        config.current_selection = ""

        choices = ["Choose", "Point", "Segment", "Line", "Circle", "Polygon"]
        config.option_var.set(choices[0])  # Set the default choice
        config.option_menu = tk.OptionMenu(config.info_window, config.option_var, *choices)
        config.option_menu.pack(padx=10, pady=10)

        show_info_btn = tk.Button(config.info_window, text="Load Info", command=show_information)
        show_info_btn.pack(pady=5)

        config.info_label = tk.Label(config.info_window, text="", font=("Arial", 12), anchor="center")
        config.info_label.pack(padx=10, pady=5)

        config.image_canvas = tk.Canvas(config.info_window, width=300, height=300)
        config.image_canvas.pack()

        config.isopen_info_panel = True

def x():
    for shape in config.shapes:
        if isinstance(shape, Segment):
            if shape.get_label() == '':
                config.shapes.remove(shape)
    update_label()
    update_display()


def convex(label):
    config.null_segments=[]

    config.conv_vx = ""
    x()
    points = []
    shape = find_shape(label)

    for segment in shape.get_segment_list():
        start = segment.get_start()
        end = segment.get_end()
        if start not in points:
            points.append(start)
        if end not in points:
            points.append(end)

    poly = shape.graham_scan(points)
    for edge_poly in poly:
        # draw_shape(edge_poly)
        edge_poly.draw(config.ax)
        config.null_segments.append(edge_poly)

        l=edge_poly.get_start().get_label()
        if l not in config.conv_vx.split(", "):
            if config.conv_vx == "":
                config.conv_vx = l

            else:
                config.conv_vx = f'{config.conv_vx}, {l}'


def triangulation(label):
    config.null_segments = []
    shape = find_shape(label)
    triangles = shape.triangulation()
    for tria in triangles:
        tria.draw(config.ax)
        config.null_segments.append(tria)
        # draw_shape(tria)


def find_shape(label):
    for shape in config.shapes:
        if label == shape.get_label():
            return shape
    return None


def activate():
    config.null_segments = []
    if config.bool_panel_algo:
        update_display()
        config.algorithms_panel.clear_text()

    if not config.calc:
        config.info = tk.Label(config.algorithms_panel.text, text="Information: ", font='Helvetica 25 bold')
        config.info.pack(anchor='w', padx=10)
        config.calc = True

    chosen_algo = config.algo_var.get()
    chosen_shape = config.poly_var.get()

    if chosen_algo == "choose" or chosen_shape == "choose":
        return

    else:
        shape = find_shape(chosen_shape)
        type=''
        if isinstance(shape, Point):
            type = 'Point'
        elif isinstance(shape, Line):
            type = 'Line'
        elif isinstance(shape, Segment):
            type = 'Segment'
        elif isinstance(shape, Circle):
            type = 'Circle'
        elif isinstance(shape, Polygon):
            type = 'Polygon'


        data = ['\n'*35,
                f' Type: {type}\n',
                f' Label: {shape.get_label()}\n'
                ]
        config.algorithms_panel.insert_block(data)

        if isinstance(shape, Point):
            config.algorithms_panel.insert_text(f' Coords: ({shape.get_x():0.3f}, {shape.get_y():0.3f})\n')

        elif isinstance(shape, Circle):
            data = [f' Radius: {shape.get_radius():0.3f}\n',
                    f' Center: ({shape.get_center().get_x():0.3f}, {shape.get_center().get_y():0.3f})\n'
                    ]
            config.algorithms_panel.insert_block(data)

        elif isinstance(shape, Segment) or isinstance(shape, Line):
            data = [f' Start: ({shape.get_start().get_x():0.3f}, {shape.get_start().get_y():0.3f})\n',
                    f' End: ({shape.get_end().get_x():0.3f}, {shape.get_end().get_y():0.3f})\n'
                    ]
            config.algorithms_panel.insert_block(data)

        elif isinstance(shape, Polygon):
            pass


        if chosen_algo == 'Perimeter':
            config.algorithms_panel.insert_text(f' Perimeter: {shape.perimeter()}\n')

        elif chosen_algo == 'Area':
            config.algorithms_panel.insert_text(f' Area: {shape.area()}\n')

        elif chosen_algo == 'Convex-hull':
            convex(chosen_shape)
            config.algorithms_panel.insert_text(f' Convex: {config.conv_vx}\n')

        elif chosen_algo == 'Triangulation':
            triangulation(chosen_shape)

    return


def reset_button(bool=True):
    config.null_segments = []

    x()
    if config.algorithms_panel is not None:
        config.algorithms_panel.clear_text()
        if not config.bool_panel_algo:
            config.algorithms_panel.pack_forget()
            config.bool_panel_algo = False


    config.algo_var = None
    config.poly_var = None
    if bool:
        algos()


def algos():
    config.calc = False
    if not config.bool_panel_algo:
        config.algorithms_panel = SidePanel(config.root, False, tk.RIGHT, True)
        config.algorithms_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
        config.bool_panel_algo = True

        tk.Label(config.algorithms_panel.text, text="Algorithms ", bg="white",
                 font='Helvetica 18 bold underline').pack(anchor='w', fill=tk.BOTH)

        # Add menu, text, and button
        menu_label = tk.Label(config.algorithms_panel.text, text="Choose an algorithm:", font='Helvetica 20 bold')
        menu_label.pack(anchor='center', pady=20)

        config.algo_var = tk.StringVar()
        config.algo_var.set("choose")  # Set default value

        config.algo_var.trace('w', update_shape_options)

        algos = ["choose", "Perimeter", "Area", "Convex-hull", "Triangulation"]

        menu = tk.OptionMenu(config.algorithms_panel.text, config.algo_var, *algos)
        menu.pack(anchor='center', pady=10)

        choice_label = tk.Label(config.algorithms_panel.text, text="Choose Shape:", font='Helvetica 20 bold')
        choice_label.pack(anchor='center', pady=20)

        config.poly_var = tk.StringVar()
        config.poly_var.set("choose")  # Set default value

        labels=["choose"]
        for shape in config.shapes:
            labels.append(shape.get_label())

        config.menu = None
        l = tk.OptionMenu(config.algorithms_panel.text, config.poly_var, *labels)
        l.pack(anchor='center', pady=10)
        config.menu = l

        calculate_button = tk.Button(config.algorithms_panel.text, text="Calculate", command=activate, font='Helvetica 15 bold')
        calculate_button.pack(anchor='center', pady=60)

        reset_butto = tk.Button (config.algorithms_panel.text, text="reset", command=reset_button,
                                     font='Helvetica 10')
        reset_butto.pack(anchor='center', pady=5)

        left_line = tk.Frame(config.algorithms_panel, bg="black", width=2)
        left_line.place(x=0, y=0, relheight=1)

        right_line = tk.Frame(config.algorithms_panel, bg="black", width=2)
        right_line.place(relx=1, y=0, relheight=1, anchor=tk.NE)

    else:
        config.algorithms_panel.pack_forget()
        config.bool_panel_algo = False


def update_shape_options(*args):
    selected_algo = config.algo_var.get()
    labels = []
    if selected_algo == "Convex-hull" or selected_algo == "Triangulation":
        for shape in config.shapes:
            if isinstance(shape, Polygon):
                labels.append(shape.get_label())

    else:
        for shape in config.shapes:
            labels.append(shape.get_label())


    config.menu['menu'].delete(0, 'end')
    # config.menu = tk.OptionMenu(config.algorithms_panel.text, config.algo_var, *labels)
    for option in labels:
        config.menu["menu"].add_command(label=option, command=lambda opt=option: config.poly_var.set(opt))


def shape_clicked(x, y):
    if x is None or y is None:
        return
    threshold = 0.5
    for shape in config.shapes:
        if isinstance(shape, Point):
            try:
                if np.abs(x - shape.get_x()) <= threshold and np.abs(y - shape.get_y()) <= threshold:
                    return shape
            except TypeError:
                pass

        elif isinstance(shape, Circle):
            center = shape.get_center()

            distance = np.sqrt((x - center.get_x()) ** 2 + (y - center.get_y()) ** 2)
            if np.abs(distance - shape.radius) <= threshold:
                return shape

        elif isinstance(shape, Line):
            m, b = shape.m_b()
            if m==None:
                line_y=b

            elif b==None:
                line_y = m

            else:
                line_y = m * x + b

            if np.abs(y - line_y) <= threshold:
                return shape

        elif isinstance(shape, Segment):
            # start = shape.get_start()
            # end = shape.get_end()
            # if start.get_x() < end.get_x():
            #     if x>end.get_x() or x<start.get_x():
            #         return None
            # elif start.get_x() > end.get_x():
            #     if x<end.get_x() or x>start.get_x():
            #         return None

            m, b = shape.m_b()
            if m == None:
                segment_y = b

            elif b == None:
                segment_y = m

            else:
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

def find_widget_by_shape(shape):
    for widget in config.label_widgets:
        equality = widget.cget("text")
        pattern = r'\((.*?)\)'
        matches = re.findall(pattern, equality)
        label = matches[0]
        if label == shape.get_label():
            return widget

def on_key(event):
    if event.key == 'ctrl+z' or event.key == 'ctrl+Z':
        undo()

    elif event.key == 'ctrl+y' or event.key == 'ctrl+Y':
        redo()

    elif event.key == 'delete':
        delete_by_label(config.last_shape.get_label())

def on_press(event):
    if event.button == 1:  # Left mouse button
        config.selected_shape = shape_clicked(event.xdata, event.ydata)


        if config.selected_shape is not None:
            config.start_drag_x, config.start_drag_y = event.xdata, event.ydata

            if config.last_shape not in config.shapes:
                config.last_shape=None

            if config.last_shape is not None:
                w = find_widget_by_shape(config.last_shape)
                if w is not None:
                    w.configure(fg='black')
                update_display()

            curr_widget = None
            for widget in config.label_widgets:
                equality = widget.cget("text")
                pattern = r'\((.*?)\)'
                matches = re.findall(pattern, equality)
                label = matches[0]
                if label==config.selected_shape.get_label():
                    curr_widget = widget


            config.selected_shape.set_color('cyan')
            curr_widget.configure(fg='cyan')
            config.last_widget = curr_widget
            config.last_shape = config.selected_shape

            plt.draw()

        else:
            if config.last_shape is not None:
                w = find_widget_by_shape(config.last_shape)
                if w is not None:
                    w.configure(fg='black')
                update_display()

    elif event.button == 3:
        config.selected_shape = shape_clicked(event.xdata, event.ydata)
        if isinstance(config.selected_shape, Point):
            config.start_drag_x, config.start_drag_y = event.xdata, event.ydata
            if config.set_shape == 0:
                open_insert_window(config.selected_shape)


def on_release(event):
    if config.selected_shape is not None:
        config.selected_shape = None
        config.start_drag_x, config.start_drag_y = None, None

    # if config.last_shape is not None and config.last_widget is not None:
    #     config.last_shape.set_color('cyan')
    #     w = find_widget_by_shape(config.last_shape)
    #     if w is not None:
    #
    #         w.configure(fg='cyan')


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


def set_shape_color(event):
    update_display()
    clicked_label = event.widget



    if config.last_shape is not None and config.last_widget is not None:
        w = find_widget_by_shape(config.last_shape)
        if w is not None:
            w.configure(fg='black')

    equality = clicked_label.cget("text")

    pattern = r'\((.*?)\)'
    matches = re.findall(pattern, equality)
    label = matches[0]

    shape = get_shape_by_label(label)
    shape.set_color('cyan')
    clicked_label.configure(fg='cyan')
    config.last_widget = clicked_label
    config.last_shape = shape
    plt.draw()


def hide(event):
    clicked_label = event.widget
    equality = clicked_label.cget("text")
    # label = re.match("\((\\w+)\)", equality).groups()[0]
    pattern = r'\((.*?)\)'
    matches = re.findall(pattern, equality)
    label = matches[0]
    shape = get_shape_by_label(label)

    if isinstance(shape, Point):
        if shape.is_hidden():
            shape.set_hidden(False)
        else:
            shape.set_hidden(True)
        # circle = shape.is_circle_part()
        # line = shape.is_line_part()
        # segment = shape.is_segment_part()
        # if circle:
        #     if shape.is_hidden():
        #         circle.set_hidden(False)
        #         shape.set_hidden(False)
        #
        #     else:
        #         circle.set_hidden(True)
        #         shape.set_hidden(True)
        #
        # if line:
        #     if shape.is_hidden():
        #         line.get_start().set_hidden(False)
        #         line.get_end().set_hidden(False)
        #         line.set_hidden(False)
        #
        #     else:
        #         line.get_start().set_hidden(True)
        #         line.get_end().set_hidden(True)
        #         line.set_hidden(True)
        #
        # if segment:
        #     if shape.is_hidden():
        #         segment.get_start().set_hidden(False)
        #         segment.get_end().set_hidden(False)
        #         segment.set_hidden(False)
        #
        #     else:
        #         segment.get_start().set_hidden(True)
        #         segment.get_end().set_hidden(True)
        #         segment.set_hidden(True)
        #
        # elif not line and not circle and not segment:
        #     if shape.is_hidden():
        #         shape.set_hidden(False)
        #     else:
        #         shape.set_hidden(True)

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

            config.curr_polygon = Polygon([], '')
            config.polygon_x, config.polygon_y = event.xdata, event.ydata
            config.first_point_polygon = Point(event.xdata, event.ydata, next(config.label_generator))
            config.curr_polygon.set_label(config.first_point_polygon.get_label())
            config.last_point_polygon = config.first_point_polygon
            plt.title("Click left click to draw the end segment point")
            plt.draw()

        elif shape_clicked(event.xdata, event.ydata) == config.first_point_polygon:
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

            config.curr_polygon.set_label(config.first_point_polygon.get_label())
            config.shapes.append(config.curr_polygon)

            command = {"type": 'draw', "shape": config.curr_polygon}
            config.undo_stack.insert(len(config.undo_stack), command)

            config.ax.figure.canvas.mpl_disconnect(config.cid)
            config.first_point_polygon = None
            config.last_point_polygon = None
            config.curr_polygon = None
            config.polygon_x, config.polygon_y = [None] * 2
            # if config.algorithms_panel is not None:
            reset_button(False)
            plt.title("")
            plt.draw()

        else:
            # Second click sets the end point
            p1 = config.last_point_polygon
            p2 = Point(event.xdata, event.ydata, next(config.label_generator))
            segment = Segment(p1, p2, next(config.label_generator))

            config.curr_polygon.set_label(p2.get_label())
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
            p=shape.is_polygon_part()
            if p:
                for segment in p.get_segment_list():
                    start = segment.get_start()
                    end = segment.get_end()
                    if start in config.shapes:
                        config.shapes.remove(start)
                    if end in config.shapes:
                        config.shapes.remove(end)

                    config.shapes.remove(segment)


                config.shapes.remove(p)
                update_display()
                update_label()
                return



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
            for s in config.shapes:
                if isinstance(s, Polygon):
                    if shape in s.get_segment_list():
                        for segment in s.get_segment_list():
                            start = segment.get_start()
                            end = segment.get_end()
                            if start in config.shapes:
                                config.shapes.remove(start)
                            if end in config.shapes:
                                config.shapes.remove(end)

                            config.shapes.remove(segment)

                        config.shapes.remove(s)
                        update_display()
                        update_label()
                        return

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


    config.last_shapes_list.append(list(config.shapes))
    config.index = len(config.last_shapes_list) - 1
    config.last_pos.append(config.index+1)

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
    for shape in config.null_segments:
        shape.draw(config.ax)

    for shape in config.shapes:
        if not shape.is_hidden():
            shape.draw(config.ax)
    plt.draw()


def update_label():
    global label_text, coords
    for widget in config.label_widgets:
        widget.destroy()
    config.label_widgets = []
    draw = []
    for shape in config.shapes:


        if shape.get_label == '':
            continue
        if shape in draw:
            continue
        draw.append(shape)
        hidden_str = '\u25D9'
        if shape.is_hidden():
            hidden_str = '\u25CB'

        if isinstance(shape, Polygon):
            label_text = f'({shape.get_label()}): Polygon'

        if isinstance(shape, Line):
            m, b = shape.m_b()
            if m==None:
                label_text = f'{hidden_str} ({shape.get_label()}) Line: y = {b}'
            elif b==None:
                label_text = f'{hidden_str} ({shape.get_label()}) Line: x = {m}'
            else:
                label_text = f'{hidden_str} ({shape.get_label()}) Line: y = {m:.3f}x + {b:.3f}'

        elif isinstance(shape, Segment):
            m, b = shape.m_b()
            if m==None:
                label_text = f'{hidden_str} ({shape.get_label()}) Segment: y = {b}'
            elif b==None:
                label_text = f'{hidden_str} ({shape.get_label()}) Segment: x = {m}'
            else:
                label_text = f'{hidden_str} ({shape.get_label()}) Segment: y = {m:.3f}x + {b:.3f} '

        elif isinstance(shape, Point):
            try:
                label_text = f'{hidden_str} ({shape.get_label()}) Point: ({shape.get_x():.3f}, {shape.get_y():.3f})'

            except TypeError:
                pass

        elif isinstance(shape, Circle):
            x = shape.get_center().get_x()
            y = shape.get_center().get_y()
            r = shape.get_radius()

            label_text = f'{hidden_str} ({shape.get_label()}) Circle: (x-{x:.3f})^2 + (y-{y:.3f})^2 = {r ** 2:.3f}'

        config.label_widget = tk.Label(config.side_panel.text, text=label_text, bg='white')
        config.label_widget.pack(anchor='w')
        config.label_widgets.append(config.label_widget)
        config.label_widget.bind("<Button-3>", hide)
        config.label_widget.bind("<Button-1>", set_shape_color)


def reset():
    command = {"type": 'reset', "list": config.shapes}
    config.undo_stack.insert(len(config.undo_stack), command)
    x()
    reset_button()
    config.null_segments = []
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

