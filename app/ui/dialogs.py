"""Modal dialog windows — coordinate input and shape info viewer."""
from __future__ import annotations
import os
import tkinter as tk
from PIL import Image, ImageTk
import config
from app.ui import styles


def open_insert_window(point) -> None:
    """Dialog to manually set a point's (x, y) coordinates."""
    from app.canvas.renderer import update_display, update_label

    win = tk.Toplevel()
    win.configure(bg=styles.BG_PANEL)
    config.set_shape = 1
    win.title("Set Point Coordinates")
    win.geometry("280x210")
    win.resizable(False, False)

    # ── header ────────────────────────────────────────────────────────────────
    hdr = tk.Frame(win, bg=styles.BG_BASE)
    hdr.pack(fill=tk.X)
    tk.Label(
        hdr, text=f"  Set Point  ({point.get_label()})",
        bg=styles.BG_BASE, fg=styles.SHAPE_COLOR["Point"],
        font=styles.FONT_UI_BOLD, padx=4, pady=8, anchor="w",
    ).pack(side=tk.LEFT)
    tk.Frame(win, bg=styles.BORDER, height=1).pack(fill=tk.X)

    body = tk.Frame(win, bg=styles.BG_PANEL)
    body.pack(fill=tk.BOTH, expand=True, padx=16, pady=12)

    def _field(label_text: str) -> tk.Entry:
        tk.Label(body, text=label_text, font=styles.FONT_UI,
                 bg=styles.BG_PANEL, fg=styles.TEXT_MUTED, anchor="w").pack(anchor="w")
        e = tk.Entry(
            body,
            bg=styles.BG_SURFACE, fg=styles.TEXT,
            insertbackground=styles.TEXT,
            relief="flat", bd=0,
            font=styles.FONT_MONO,
            highlightthickness=1,
            highlightbackground=styles.BORDER,
            highlightcolor=styles.ACCENT_BLUE,
        )
        e.pack(fill=tk.X, pady=(2, 10), ipady=6)
        return e

    x_entry = _field("X coordinate")
    y_entry = _field("Y coordinate")

    def _submit() -> None:
        try:
            x = float(x_entry.get())
            y = float(y_entry.get())
        except ValueError:
            return
        point.set_p(x, y)
        config.set_shape = 0
        win.destroy()
        update_label()
        update_display()

    def _close() -> None:
        config.set_shape = 0
        win.destroy()

    win.protocol("WM_DELETE_WINDOW", _close)

    tk.Button(
        body, text="Set Point", command=_submit,
        **styles.btn_kw(styles.ACCENT_BLUE, styles.BG_BASE),
    ).pack(fill=tk.X)


def open_info_window() -> None:
    """Open the shape information panel (singleton)."""
    if config.isopen_info_panel:
        return

    win = tk.Toplevel(config.root)
    win.configure(bg=styles.BG_PANEL)
    win.title("Shape Information")
    win.geometry("820x900")
    win.protocol("WM_DELETE_WINDOW", _on_info_close)
    config.info_window    = win
    config.isopen_info_panel = True

    # ── header ────────────────────────────────────────────────────────────────
    hdr = tk.Frame(win, bg=styles.BG_BASE)
    hdr.pack(fill=tk.X)
    tk.Label(
        hdr, text="  Shape Information",
        bg=styles.BG_BASE, fg=styles.ACCENT_BLUE,
        font=styles.FONT_HEADING, padx=4, pady=10, anchor="w",
    ).pack(side=tk.LEFT)
    tk.Frame(win, bg=styles.ACCENT_BLUE, height=1).pack(fill=tk.X)

    body = tk.Frame(win, bg=styles.BG_PANEL)
    body.pack(fill=tk.BOTH, expand=True, padx=20, pady=16)

    # ── shape selector ────────────────────────────────────────────────────────
    tk.Label(body, text="Choose a shape", font=styles.FONT_UI,
             bg=styles.BG_PANEL, fg=styles.TEXT_MUTED, anchor="w").pack(anchor="w")

    config.option_var = tk.StringVar(value="Choose")
    choices = ["Choose", "Point", "Segment", "Line", "Circle", "Polygon"]
    om = tk.OptionMenu(body, config.option_var, *choices)
    om.configure(
        bg=styles.BG_SURFACE, fg=styles.TEXT,
        activebackground=styles.BG_HOVER, activeforeground=styles.TEXT,
        highlightthickness=0, relief="flat", font=styles.FONT_UI,
    )
    om["menu"].configure(
        bg=styles.BG_SURFACE, fg=styles.TEXT,
        activebackground=styles.BG_ACTIVE, activeforeground=styles.TEXT,
        font=styles.FONT_UI,
    )
    om.pack(anchor="w", pady=(4, 12))

    tk.Button(
        body, text="Load Info", command=_show_information,
        **styles.btn_kw(styles.ACCENT_BLUE, styles.BG_BASE),
    ).pack(anchor="w")

    tk.Frame(body, bg=styles.BORDER, height=1).pack(fill=tk.X, pady=12)

    config.info_label = tk.Label(
        body, text="",
        bg=styles.BG_PANEL, fg=styles.TEXT,
        font=styles.FONT_UI, anchor="w", justify="left", wraplength=760,
    )
    config.info_label.pack(anchor="w", pady=(0, 12))

    config.image_canvas = tk.Canvas(
        body, width=400, height=400,
        bg=styles.BG_SURFACE,
        highlightthickness=1,
        highlightbackground=styles.BORDER,
    )
    config.image_canvas.pack(anchor="center", pady=10)


def _on_info_close() -> None:
    config.isopen_info_panel  = False
    config.info_window.destroy()
    config.info_panel         = None
    config.info_label         = None
    config.image_canvas       = None
    config.current_selection  = ""


def _show_information() -> None:
    chosen = config.option_var.get()
    if chosen == "Choose":
        return
    color = styles.SHAPE_COLOR.get(chosen, styles.ACCENT_BLUE)
    config.info_label.config(
        text=chosen, font=styles.FONT_TITLE, fg=color,
    )
    _load_info_text(chosen)
    _load_info_image(chosen)


def _load_info_text(shape_name: str) -> None:
    path = f"./Info/{shape_name}_info.txt"
    text = (open(path).read() if os.path.exists(path)
            else f"No information available for {shape_name}.")
    config.info_label.config(text=text, font=styles.FONT_UI, fg=styles.TEXT)


def _load_info_image(shape_name: str) -> None:
    config.image_canvas.delete("all")
    path = f"./Images/{shape_name}.png"
    if not os.path.exists(path):
        return
    orig  = Image.open(path)
    cw    = config.image_canvas.winfo_width() or 400
    ch    = config.image_canvas.winfo_height() or 400
    scale = min(cw / orig.width, ch / orig.height)
    nw, nh = int(orig.width * scale), int(orig.height * scale)
    config.image = ImageTk.PhotoImage(orig.resize((nw, nh), Image.LANCZOS))
    config.image_canvas.create_image(
        (cw - nw) // 2, (ch - nh) // 2,
        anchor=tk.NW, image=config.image,
    )
