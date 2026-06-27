"""UI theme — Deep Space Observatory aesthetic.

Near-black base layers, electric blue/cyan primary accents,
per-shape-type neon colours, monospace algebra panel.
"""
from __future__ import annotations
import platform

# ── Background layers (darkest → lightest) ────────────────────────────────────
BG_BASE    = "#0b0d15"   # root window / deepest bg
BG_PANEL   = "#10131e"   # side panels
BG_SURFACE = "#161929"   # raised cards / entry rows
BG_HOVER   = "#1e2235"   # hover state
BG_ACTIVE  = "#252b42"   # pressed / active

# ── Borders ───────────────────────────────────────────────────────────────────
BORDER       = "#1e2337"
BORDER_LIGHT = "#252b42"
ACCENT_GLOW  = "#2a3a6a"   # subtle glow border

# ── Text ──────────────────────────────────────────────────────────────────────
TEXT        = "#c8d0f0"    # primary
TEXT_MUTED  = "#5c6488"    # secondary / placeholder
TEXT_DIM    = "#2c3250"    # very dim / structural

# ── Accent colours ────────────────────────────────────────────────────────────
ACCENT_BLUE = "#4d9fff"    # primary action / algebra header
ACCENT_CYAN = "#00d4f7"    # secondary highlights
ACCENT_GOLD = "#ffa94d"    # warm emphasis

# ── Per-shape-type colours ────────────────────────────────────────────────────
SHAPE_COLOR = {
    "Point":   "#ff6b8a",   # rose — warm, stands out
    "Line":    "#4d9fff",   # sky blue
    "Segment": "#00e5a0",   # teal green
    "Circle":  "#c084fc",   # violet
    "Polygon": "#fbbf24",   # amber
}

# ── Matplotlib canvas ─────────────────────────────────────────────────────────
CANVAS_BG   = "#0d1017"
CANVAS_GRID = "#1a1f2e"
CANVAS_AXIS = "#252b42"

# ── Toolbar button groups (bg, hover, active, fg) ────────────────────────────
_G = {
    "file":    ("#0f1e2e", "#162b42", "#1e3d5c", "#4d9fff"),
    "draw":    ("#0e1f18", "#15302a", "#1c4538", "#00e5a0"),
    "edit":    ("#1f0e12", "#32151c", "#451c26", "#ff6b8a"),
    "history": ("#16102a", "#221840", "#2e2055", "#c084fc"),
    "algo":    ("#1f1a0e", "#322a15", "#45391c", "#fbbf24"),
    "info":    ("#0e1c1f", "#152e33", "#1c4048", "#00d4f7"),
}

def group(name: str) -> dict:
    """Return (bg, hover_bg, active_bg, fg) for a toolbar group."""
    bg, hov, act, fg = _G[name]
    return {"bg": bg, "hover": hov, "active": act, "fg": fg}

# ── Fonts (platform-aware) ────────────────────────────────────────────────────
_OS = platform.system()
if _OS == "Darwin":
    FONT_UI        = ("Helvetica Neue", 10)
    FONT_UI_BOLD   = ("Helvetica Neue", 10, "bold")
    FONT_HEADING   = ("Helvetica Neue", 13, "bold")
    FONT_TITLE     = ("Helvetica Neue", 15, "bold")
    FONT_MONO      = ("Menlo", 10)
    FONT_MONO_SM   = ("Menlo", 9)
    FONT_STATUS    = ("Menlo", 9)
elif _OS == "Windows":
    FONT_UI        = ("Segoe UI", 10)
    FONT_UI_BOLD   = ("Segoe UI", 10, "bold")
    FONT_HEADING   = ("Segoe UI", 13, "bold")
    FONT_TITLE     = ("Segoe UI", 15, "bold")
    FONT_MONO      = ("Consolas", 10)
    FONT_MONO_SM   = ("Consolas", 9)
    FONT_STATUS    = ("Consolas", 9)
else:
    FONT_UI        = ("DejaVu Sans", 10)
    FONT_UI_BOLD   = ("DejaVu Sans", 10, "bold")
    FONT_HEADING   = ("DejaVu Sans", 13, "bold")
    FONT_TITLE     = ("DejaVu Sans", 15, "bold")
    FONT_MONO      = ("DejaVu Sans Mono", 10)
    FONT_MONO_SM   = ("DejaVu Sans Mono", 9)
    FONT_STATUS    = ("DejaVu Sans Mono", 9)

# ── Dimensions ────────────────────────────────────────────────────────────────
PANEL_WIDTH    = 248
TOOLBAR_HEIGHT = 44
STATUS_HEIGHT  = 26

# ── Shortcut colour names (used by algo_panel + older code) ──────────────────
ALGO_BTN_BG = "#fbbf24"
EDIT_BTN_BG = "#ff6b8a"


def btn_kw(bg: str, fg: str = TEXT) -> dict:
    """Return kwargs for a tk.Button (used in algo panel)."""
    return {
        "bg": bg, "fg": fg,
        "activebackground": BG_HOVER, "activeforeground": fg,
        "relief": "flat", "padx": 10, "pady": 5,
        "borderwidth": 0, "cursor": "hand2",
        "font": FONT_UI,
    }
