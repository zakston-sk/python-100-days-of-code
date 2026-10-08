"""Miles to Kilometers Converter (Day 27).

A small Tkinter app that converts miles to kilometers as you type.
"""

import tkinter as tk
from tkinter import ttk

# ---------- Theme ----------
BG = "#f3f4f6"
CARD = "#ffffff"
TEXT = "#111827"
MUTED = "#6b7280"
ACCENT = "#2563eb"
BORDER = "#d1d5db"
ERROR = "#dc2626"
RESULT_BG = "#eff6ff"
RESULT_BORDER = "#bfdbfe"

KM_PER_MILE = 1.609344
FONT_FAMILY = "Segoe UI"

WINDOW_WIDTH = 460
WINDOW_HEIGHT = 500


def center_window(window: tk.Tk, width: int, height: int) -> None:
    """Place the window at the centre of the screen."""
    window.update_idletasks()
    x = (window.winfo_screenwidth() - width) // 2
    y = (window.winfo_screenheight() - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def build_styles(root: tk.Tk) -> None:
    """Configure the ttk styles used throughout the app."""
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure("TLabel", background=CARD, foreground=TEXT)
    style.configure(
        "Title.TLabel",
        font=(FONT_FAMILY, 20, "bold"),
        background=CARD,
        foreground=TEXT,
    )
    style.configure(
        "Subtitle.TLabel",
        font=(FONT_FAMILY, 10),
        background=CARD,
        foreground=MUTED,
    )
    style.configure(
        "Field.TLabel",
        font=(FONT_FAMILY, 10, "bold"),
        background=CARD,
        foreground=TEXT,
    )
    style.configure(
        "Big.TEntry",
        padding=10,
        fieldbackground="white",
        foreground=TEXT,
    )
    style.configure(
        "Secondary.TButton",
        font=(FONT_FAMILY, 10),
        padding=(12, 8),
        background="#e5e7eb",
        foreground=TEXT,
        borderwidth=0,
    )
    style.map("Secondary.TButton", background=[("active", "#d1d5db")])
    style.configure("TSeparator", background=BORDER)


def main() -> None:
    """Run the Miles to Kilometers converter."""
    root = tk.Tk()
    root.title("Miles to Kilometers Converter")
    root.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
    root.configure(bg=BG)

    build_styles(root)

    # ---------- Layout ----------
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    card = tk.Frame(
        root,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1,
    )
    card.grid(row=0, column=0, sticky="nsew", padx=24, pady=24)
    card.columnconfigure(0, weight=1)

    # Header
    ttk.Label(card, text="Miles to Kilometers", style="Title.TLabel").grid(
        row=0, column=0, sticky="w", padx=24, pady=(24, 4)
    )
    ttk.Label(
        card,
        text="Type a distance in miles to convert it instantly.",
        style="Subtitle.TLabel",
    ).grid(row=1, column=0, sticky="w", padx=24, pady=(0, 16))

    ttk.Separator(card, orient="horizontal").grid(
        row=2, column=0, sticky="ew", padx=24, pady=(0, 20)
    )

    # ---------- State ----------
    miles_var = tk.StringVar()
    result_var = tk.StringVar(value="—")
    error_var = tk.StringVar()

    def convert(*_args) -> None:
        """Update the result whenever the input changes."""
        text = miles_var.get().strip()

        if not text:
            result_var.set("—")
            error_var.set("")
            return

        try:
            miles = float(text)
        except ValueError:
            result_var.set("—")
            error_var.set("Please enter a valid number.")
            return

        if miles < 0:
            result_var.set("—")
            error_var.set("Distance cannot be negative.")
            return

        km = miles * KM_PER_MILE
        result_var.set(f"{km:,.3f} km")
        error_var.set("")

    def clear() -> None:
        """Clear the input and focus the entry."""
        miles_var.set("")
        miles_entry.focus_set()

    miles_var.trace_add("write", convert)

    # ---------- Input ----------
    ttk.Label(card, text="Miles", style="Field.TLabel").grid(
        row=3, column=0, sticky="w", padx=24
    )

    miles_entry = ttk.Entry(
        card,
        textvariable=miles_var,
        style="Big.TEntry",
        justify="right",
        font=(FONT_FAMILY, 16),
    )
    miles_entry.grid(row=4, column=0, sticky="ew", padx=24, pady=(6, 4))
    miles_entry.focus_set()

    tk.Label(
        card,
        textvariable=error_var,
        font=(FONT_FAMILY, 9),
        bg=CARD,
        fg=ERROR,
        anchor="w",
    ).grid(row=5, column=0, sticky="ew", padx=24)

    # ---------- Result ----------
    result_frame = tk.Frame(
        card,
        bg=RESULT_BG,
        highlightbackground=RESULT_BORDER,
        highlightthickness=1,
    )
    result_frame.grid(row=6, column=0, sticky="ew", padx=24, pady=(16, 12))
    result_frame.columnconfigure(0, weight=1)

    tk.Label(
        result_frame,
        text="Kilometers",
        font=(FONT_FAMILY, 10, "bold"),
        bg=RESULT_BG,
        fg=MUTED,
    ).grid(row=0, column=0, sticky="w", padx=16, pady=(12, 0))

    tk.Label(
        result_frame,
        textvariable=result_var,
        font=(FONT_FAMILY, 24, "bold"),
        bg=RESULT_BG,
        fg=ACCENT,
    ).grid(row=1, column=0, sticky="w", padx=16, pady=(0, 12))

    # ---------- Clear button ----------
    ttk.Button(
        card,
        text="Clear",
        style="Secondary.TButton",
        command=clear,
    ).grid(row=7, column=0, sticky="e", padx=24, pady=(0, 16))

    # Footer
    tk.Label(
        card,
        text=f"1 mile = {KM_PER_MILE} kilometers",
        font=(FONT_FAMILY, 9),
        bg=CARD,
        fg=MUTED,
    ).grid(row=8, column=0, sticky="w", padx=24, pady=(0, 20))

    # ---------- Bindings ----------
    root.bind("<Escape>", lambda _event: clear())

    center_window(root, WINDOW_WIDTH, WINDOW_HEIGHT)
    root.mainloop()


if __name__ == "__main__":
    main()
