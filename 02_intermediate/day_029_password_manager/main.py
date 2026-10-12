"""Password Manager (Day 29).

A small Tkinter app that generates secure passwords,
stores them in a JSON file, and lets you search saved entries.
"""

import json
import secrets
import string
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

# --- Paths -----------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data.json"

# --- Password generation ---------------------------------------------------
LETTERS = string.ascii_letters
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()-_=+"
PASSWORD_ALPHABET = LETTERS + DIGITS + SYMBOLS
PASSWORD_LENGTH = 16

# --- Theme -----------------------------------------------------------------
BG = "#1f2937"
CARD = "#374151"
FIELD = "#4b5563"
TEXT = "#f9fafb"
MUTED = "#9ca3af"
ACCENT = "#10b981"
ACCENT_HOVER = "#34d399"

FONT_FAMILY = "Segoe UI"
WINDOW_W = 420
WINDOW_H = 460
PAD = 24
FIELD_IPADY = 8


# --- Helpers ---------------------------------------------------------------


def generate_password(length: int = PASSWORD_LENGTH) -> str:
    """Return a cryptographically secure random password."""
    return "".join(secrets.choice(PASSWORD_ALPHABET) for _ in range(length))


def load_data(path: Path) -> dict[str, dict[str, str]]:
    """Return the saved password data, or an empty dict if none exists."""
    if not path.exists():
        return {}
    try:
        with path.open(encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}


def save_data(path: Path, data: dict[str, dict[str, str]]) -> None:
    """Write the given data to the JSON file, pretty-printed."""
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def center_window(window: tk.Tk, width: int, height: int) -> None:
    """Place the window at the centre of the screen."""
    window.update_idletasks()
    x = (window.winfo_screenwidth() - width) // 2
    y = (window.winfo_screenheight() - height) // 3
    window.geometry(f"{width}x{height}+{x}+{y}")


# --- Application -----------------------------------------------------------


class PasswordManager:
    """Tkinter GUI for generating, storing, and searching passwords."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Password Manager")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.data = load_data(DATA_FILE)

        self.website_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self._build()
        self._bind_keys()
        center_window(root, WINDOW_W, WINDOW_H)

    # ---------------------------------------------------------------- layout
    def _build(self) -> None:
        """Create all widgets and lay them out on the grid."""
        self.root.columnconfigure(0, weight=1)

        card = tk.Frame(self.root, bg=BG, padx=PAD, pady=PAD)
        card.grid(row=0, column=0, sticky="nsew")
        card.columnconfigure(0, weight=1)

        tk.Label(
            card,
            text="Password Manager",
            font=(FONT_FAMILY, 20, "bold"),
            bg=BG,
            fg=TEXT,
        ).grid(row=0, column=0, sticky="w")

        tk.Label(
            card,
            text="Generate strong passwords and keep them safe.",
            font=(FONT_FAMILY, 10),
            bg=BG,
            fg=MUTED,
        ).grid(row=1, column=0, sticky="w", pady=(0, 18))

        self._add_label(card, row=2, text="Website")
        self._add_entry(card, row=3, var=self.website_var)

        self._add_label(card, row=4, text="Email / Username", top=10)
        self._add_entry(card, row=5, var=self.email_var)

        self._add_label(card, row=6, text="Password", top=10)
        self._add_password_row(card, row=7)

        self._add_action_buttons(card, row=8)

    def _add_label(
        self, parent: tk.Widget, *, row: int, text: str, top: int = 0
    ) -> None:
        """Add a small uppercase field label."""
        tk.Label(
            parent,
            text=text,
            font=(FONT_FAMILY, 10, "bold"),
            bg=BG,
            fg=MUTED,
        ).grid(row=row, column=0, sticky="w", pady=(top, 3))

    def _add_entry(self, parent: tk.Widget, *, row: int, var: tk.StringVar) -> tk.Entry:
        """Add a flat-styled text field bound to the given variable."""
        entry = tk.Entry(
            parent,
            textvariable=var,
            font=(FONT_FAMILY, 12),
            bg=FIELD,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            bd=0,
        )
        entry.grid(row=row, column=0, sticky="ew", ipady=FIELD_IPADY)
        return entry

    def _add_password_row(self, parent: tk.Widget, *, row: int) -> None:
        """Add the password field plus the 'Generate' button next to it."""
        row_frame = tk.Frame(parent, bg=BG)
        row_frame.grid(row=row, column=0, sticky="ew")
        row_frame.columnconfigure(0, weight=1)

        entry = tk.Entry(
            row_frame,
            textvariable=self.password_var,
            font=(FONT_FAMILY, 12),
            bg=FIELD,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            bd=0,
        )
        entry.grid(row=0, column=0, sticky="ew", ipady=FIELD_IPADY)

        self._make_button(
            row_frame,
            text="Generate",
            command=self._generate,
            bg=ACCENT,
            hover=ACCENT_HOVER,
            fg=BG,
        ).grid(row=0, column=1, padx=(8, 0), sticky="e")

    def _add_action_buttons(self, parent: tk.Widget, *, row: int) -> None:
        """Add the Copy / Save / Search row."""
        actions = tk.Frame(parent, bg=BG)
        actions.grid(row=row, column=0, sticky="ew", pady=(22, 0))
        for col in range(3):
            actions.columnconfigure(col, weight=1)

        self._make_button(
            actions, text="Copy", command=self._copy, bg=CARD, hover=FIELD
        ).grid(row=0, column=0, sticky="ew", padx=(0, 4))

        self._make_button(
            actions,
            text="Save",
            command=self._save,
            bg=ACCENT,
            hover=ACCENT_HOVER,
            fg=BG,
        ).grid(row=0, column=1, sticky="ew", padx=4)

        self._make_button(
            actions, text="Search", command=self._search, bg=CARD, hover=FIELD
        ).grid(row=0, column=2, sticky="ew", padx=(4, 0))

    @staticmethod
    def _make_button(
        parent: tk.Widget,
        *,
        text: str,
        command,
        bg: str,
        hover: str,
        fg: str = TEXT,
    ) -> tk.Button:
        """Return a flat-styled button with consistent padding."""
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=(FONT_FAMILY, 10, "bold"),
            bg=bg,
            fg=fg,
            activebackground=hover,
            activeforeground=fg,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=12,
            pady=8,
        )

    # ---------------------------------------------------------------- actions
    def _generate(self) -> None:
        """Fill the password field with a fresh secure password."""
        self.password_var.set(generate_password())

    def _copy(self) -> None:
        """Copy the current password to the system clipboard."""
        password = self.password_var.get()
        if not password:
            messagebox.showinfo("Nothing to copy", "Generate a password first.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard.")

    def _save(self) -> None:
        """Validate the form and store the entry in the JSON file."""
        website = self.website_var.get().strip()
        email = self.email_var.get().strip()
        password = self.password_var.get().strip()

        if not website or not email or not password:
            messagebox.showwarning("Missing fields", "Please fill in all fields.")
            return

        self.data[website] = {"email": email, "password": password}
        save_data(DATA_FILE, self.data)

        self.website_var.set("")
        self.password_var.set("")
        messagebox.showinfo("Saved", f"Entry for '{website}' saved.")

    def _search(self) -> None:
        """Look up a website and fill the form with its saved data."""
        website = self.website_var.get().strip()
        if not website:
            messagebox.showinfo("Search", "Type a website name first.")
            return

        entry = self.data.get(website)
        if not entry:
            messagebox.showinfo("Not found", f"No entry for '{website}'.")
            return

        self.email_var.set(entry["email"])
        self.password_var.set(entry["password"])

    # ---------------------------------------------------------------- keys
    def _bind_keys(self) -> None:
        """Bind quick keyboard actions."""
        self.root.bind("<Return>", lambda _event: self._save())
        self.root.bind("<Escape>", lambda _event: self.root.destroy())


def main() -> None:
    """Run the Password Manager."""
    root = tk.Tk()
    PasswordManager(root)
    root.mainloop()


if __name__ == "__main__":
    main()
