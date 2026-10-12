"""Pomodoro timer with a Color Hunt palette and an anti-aliased segmented ring.

Palette: #364F6B (background) · #3FC1C9 (teal) · #F5F5F5 (text) · #FC5185 (pink)
"""

import math
import sys
import time
import tkinter as tk

# ----------------------------------------------------------------- palette
BG = "#364F6B"  # dark blue — main background
CARD = "#2A3F57"  # derived darker shade — buttons / track
CARD2 = "#3FC1C9"  # teal — hover
TEXT = "#F5F5F5"  # near-white — primary text
MUTED = "#3FC1C9"  # teal — secondary text
TRACK = "#2A3F57"  # derived darker shade — inactive ring segments

MODES = {
    "work": {"label": "Focus", "color": "#FC5185", "hover": "#FF7AA3", "minutes": 25},
    "short": {
        "label": "Short Break",
        "color": "#3FC1C9",
        "hover": "#6BD4DB",
        "minutes": 5,
    },
    "long": {
        "label": "Long Break",
        "color": "#F5F5F5",
        "hover": "#FFFFFF",
        "minutes": 15,
    },
}

FAM = {"darwin": "Helvetica Neue", "win32": "Segoe UI"}.get(sys.platform, "DejaVu Sans")

# ---------------------------------------------------------------- geometry
SIZE = 300
PAD = 26
RING = SIZE / 2 - PAD
THICK = 18
SEGMENTS = 60
HALF_DEG = 2.4  # half angular width of a tick (deg)
SUPERSAMPLE = 3  # K × K subsamples per pixel

# ---------------------------------------------------------------- behaviour
TICK_MS = 50  # UI refresh interval in milliseconds
ROUNDS_PER_CYCLE = 4  # work sessions before a long break
DOTS_PER_CYCLE = 4  # dots drawn under the ring
SECONDS_PER_MINUTE = 60
MIN_DURATION = 1
MAX_DURATION = 120
EPSILON = 1e-6

# --------- type alias: (base_rgb, [(segment_index, weight), ...])
Pixel = tuple[tuple[float, float, float], tuple[tuple[int, float], ...]]


def _hex_to_rgb(h: str) -> tuple[int, int, int]:
    """Convert a hex colour string like '#364F6B' to an (R, G, B) tuple."""
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _precompute_coverage() -> list[Pixel]:
    """For each output pixel: (base_rgb, [(seg_idx, weight), …]).

    base_rgb is the pixel colour when nothing is filled (BG/TRACK blend).
    seg_list gives how much of the pixel is covered by each segment's tick.
    """
    cx = cy = SIZE / 2
    r_in = RING - THICK / 2
    r_out = RING + THICK / 2
    r_in_sq, r_out_sq = r_in * r_in, r_out * r_out

    K = SUPERSAMPLE
    inv_K = 1.0 / K
    inv_total = 1.0 / (K * K)
    seg_deg = 360.0 / SEGMENTS
    two_half = 2.0 * HALF_DEG
    margin = 0.75  # max distance from pixel centre to a subsample, +slack

    bg_rgb = _hex_to_rgb(BG)
    track_rgb = _hex_to_rgb(TRACK)
    bg_base: tuple[float, float, float] = (
        float(bg_rgb[0]),
        float(bg_rgb[1]),
        float(bg_rgb[2]),
    )

    coverage: list[Pixel] = []

    for py in range(SIZE):
        for px in range(SIZE):
            dx_c = px + 0.5 - cx
            dy_c = py + 0.5 - cy
            r_c = math.sqrt(dx_c * dx_c + dy_c * dy_c)

            # Fast path: the pixel is entirely outside the ring.
            if r_c < r_in - margin or r_c > r_out + margin:
                coverage.append((bg_base, ()))
                continue

            seg_acc: dict[int, int] = {}
            bg_count = 0
            for sy in range(K):
                fy = py + (sy + 0.5) * inv_K
                dy = fy - cy
                dy2 = dy * dy
                for sx in range(K):
                    fx = px + (sx + 0.5) * inv_K
                    dx = fx - cx
                    r2 = dx * dx + dy2
                    if r2 < r_in_sq or r2 > r_out_sq:
                        bg_count += 1
                        continue
                    # angle: 0 at 12 o'clock, increases clockwise
                    t = (math.degrees(math.atan2(dy, dx)) + 90.0) % 360.0
                    # shift so tick i spans [i*6, i*6 + 2*half]
                    u = (t + HALF_DEG) % 360.0
                    q = int(u / seg_deg)
                    if (u - q * seg_deg) <= two_half:
                        s = q % SEGMENTS
                        seg_acc[s] = seg_acc.get(s, 0) + 1
                    else:
                        bg_count += 1

            bg_w = bg_count * inv_total
            ring_w = 1.0 - bg_w
            base: tuple[float, float, float] = (
                bg_rgb[0] * bg_w + track_rgb[0] * ring_w,
                bg_rgb[1] * bg_w + track_rgb[1] * ring_w,
                bg_rgb[2] * bg_w + track_rgb[2] * ring_w,
            )
            seg_list: tuple[tuple[int, float], ...] = tuple(
                (s, c * inv_total) for s, c in seg_acc.items()
            )
            coverage.append((base, seg_list))

    return coverage


class HoverButton(tk.Button):
    """Flat tk.Button with a hover colour, driven by set_colors()."""

    def __init__(
        self,
        parent: tk.Misc,
        *,
        text: str,
        command,
        bg: str,
        hover: str,
        fg: str,
        big: bool = False,
    ) -> None:
        font = (FAM, 13, "bold") if big else (FAM, 11)
        super().__init__(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=hover,
            activeforeground=fg,
            relief="flat",
            bd=0,
            highlightthickness=0,
            takefocus=0,
            cursor="hand2",
            font=font,
            padx=24 if big else 16,
            pady=12 if big else 10,
        )
        self._normal_bg = bg
        self._hover_bg = hover
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, _event: tk.Event) -> None:
        """Switch to the hover colour."""
        self.config(bg=self._hover_bg)

    def _on_leave(self, _event: tk.Event) -> None:
        """Restore the normal colour."""
        self.config(bg=self._normal_bg)

    def set_colors(self, normal: str, hover: str) -> None:
        """Update both the normal and hover colours."""
        self._normal_bg = normal
        self._hover_bg = hover
        self.config(bg=normal, activebackground=hover)


class Pomodoro:
    """Pomodoro timer application."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("Pomodoro")
        root.configure(bg=BG)
        root.resizable(False, False)

        self.durations: dict[str, int] = {k: v["minutes"] for k, v in MODES.items()}
        self.mode: str = "work"
        self.running: bool = False
        self.completed: int = 0
        self.remaining: float = float(self.durations["work"] * SECONDS_PER_MINUTE)

        self._after_id: str | None = None
        self._deadline: float = 0.0

        # ---------- precompute the ring coverage once, at boot
        self._coverage: list[Pixel] = _precompute_coverage()
        self._bg_rgb: tuple[int, int, int] = _hex_to_rgb(BG)
        self._track_rgb: tuple[int, int, int] = _hex_to_rgb(TRACK)

        # baseline body: every pixel = BG. Copied on every render, then
        # we only overwrite the ring pixels.
        self._empty_body: bytes = bytes(self._bg_rgb) * (SIZE * SIZE)

        self._last_key: tuple[int, int, str] | None = None
        # assigned in _build(); declared here so Pylance knows the real type
        self._ring_photo: tk.PhotoImage

        self._build()
        self._bind_keys()
        self._render()

    # ------------------------------------------------------------- widgets
    def _build(self) -> None:
        """Create all widgets and lay them out."""
        outer = tk.Frame(self.root, bg=BG, padx=30, pady=26)
        outer.pack()

        self.mode_lbl = tk.Label(outer, font=(FAM, 12, "bold"), bg=BG, fg=MUTED)
        self.mode_lbl.pack(pady=(0, 10))

        self.canvas = tk.Canvas(
            outer, width=SIZE, height=SIZE, bg=BG, highlightthickness=0
        )
        self.canvas.pack()

        # placeholder ring — will be replaced by _render_ring
        self._ring_photo = tk.PhotoImage(width=SIZE, height=SIZE)
        self._ring_photo.put(BG, to=(0, 0, SIZE, SIZE))
        self.ring_item = self.canvas.create_image(
            SIZE / 2, SIZE / 2, anchor="center", image=self._ring_photo
        )

        self.time_txt = self.canvas.create_text(
            SIZE / 2, SIZE / 2 - 6, text="25:00", fill=TEXT, font=(FAM, 52, "bold")
        )
        self.sub_txt = self.canvas.create_text(
            SIZE / 2, SIZE / 2 + 42, text="", fill=MUTED, font=(FAM, 11)
        )

        # ---- session dots
        self.dots = tk.Canvas(outer, width=140, height=16, bg=BG, highlightthickness=0)
        self.dots.pack(pady=(14, 0))
        self.dot_ids: list[int] = [
            self.dots.create_oval(
                22 + i * 32 - 5, 3, 22 + i * 32 + 5, 13, outline=TRACK, fill=BG, width=2
            )
            for i in range(DOTS_PER_CYCLE)
        ]

        # ---- buttons
        row = tk.Frame(outer, bg=BG)
        row.pack(pady=(20, 0))

        self.reset_btn = HoverButton(
            row, text="Reset", command=self.reset, bg=CARD, hover=CARD2, fg=TEXT
        )
        self.reset_btn.pack(side="left", padx=5)

        self.start_btn = HoverButton(
            row,
            text="Start",
            command=self.toggle,
            bg=MODES["work"]["color"],
            hover=MODES["work"]["hover"],
            fg=BG,
            big=True,
        )
        self.start_btn.pack(side="left", padx=5)

        self.skip_btn = HoverButton(
            row, text="Skip", command=self.skip, bg=CARD, hover=CARD2, fg=TEXT
        )
        self.skip_btn.pack(side="left", padx=5)

        # ---- settings
        tk.Frame(outer, bg=TRACK, height=1).pack(fill="x", pady=(22, 16))

        srow = tk.Frame(outer, bg=BG)
        srow.pack()
        self.vars: dict[str, tk.IntVar] = {}
        for key, label in (("work", "Focus"), ("short", "Short"), ("long", "Long")):
            cell = tk.Frame(srow, bg=BG)
            cell.pack(side="left", padx=10)
            tk.Label(cell, text=label, bg=BG, fg=MUTED, font=(FAM, 9)).pack()

            var = tk.IntVar(value=self.durations[key])
            var.trace_add("write", lambda *_, k=key: self._duration_changed(k))
            self.vars[key] = var

            tk.Spinbox(
                cell,
                from_=MIN_DURATION,
                to=MAX_DURATION,
                width=3,
                textvariable=var,
                bg=CARD,
                fg=TEXT,
                buttonbackground=CARD,
                relief="flat",
                bd=0,
                justify="center",
                font=(FAM, 12, "bold"),
                takefocus=1,
                highlightthickness=0,
                insertbackground=TEXT,
                activebackground=CARD2,
            ).pack(pady=(3, 0))

    # -------------------------------------------------- anti-aliased ring
    def _render_ring(self, frac: float, color_hex: str) -> None:
        """Redraw the ring image at the given fraction and colour."""
        # Quantise to quarter-segment steps so we don't re-render every tick.
        exact = frac * SEGMENTS
        full = int(exact)
        partial_q = min(4, round((exact - full) * 4))

        key = (full, partial_q, color_hex)
        if key == self._last_key:
            return
        self._last_key = key

        partial = partial_q / 4.0

        cr = _hex_to_rgb(color_hex)
        tr = self._track_rgb
        dr_r = cr[0] - tr[0]
        dr_g = cr[1] - tr[1]
        dr_b = cr[2] - tr[2]

        body = bytearray(self._empty_body)

        for i, (base, seg_list) in enumerate(self._coverage):
            if not seg_list:
                continue
            r, g, b = base
            for s, w in seg_list:
                if s < full:
                    contrib = w
                elif s == full and full < SEGMENTS:
                    contrib = partial * w
                else:
                    continue
                r += dr_r * contrib
                g += dr_g * contrib
                b += dr_b * contrib
            j = i * 3
            body[j] = int(r)
            body[j + 1] = int(g)
            body[j + 2] = int(b)

        # ---- build the Tcl colour-list string for PhotoImage.put ----
        hex_str = body.hex()
        groups = ["#" + hex_str[k : k + 6] for k in range(0, len(hex_str), 6)]
        rows = []
        for y in range(SIZE):
            rows.append("{" + " ".join(groups[y * SIZE : (y + 1) * SIZE]) + "}")
        self._ring_photo.put(" ".join(rows))

    # ------------------------------------------------------------- drawing
    def _render(self) -> None:
        """Refresh every visual element based on the current state."""
        cfg = MODES[self.mode]
        total = self.durations[self.mode] * SECONDS_PER_MINUTE
        elapsed = max(0.0, total - self.remaining)
        frac = min(1.0, elapsed / total) if total else 0.0

        self._render_ring(frac, cfg["color"])

        secs = max(0, int(math.ceil(self.remaining - EPSILON)))
        self.canvas.itemconfig(self.time_txt, text=f"{secs // 60:02d}:{secs % 60:02d}")

        if self.running:
            sub = (
                f"Round {self.completed % ROUNDS_PER_CYCLE + 1} of {ROUNDS_PER_CYCLE}"
                if self.mode == "work"
                else "Break time"
            )
        else:
            sub = "Paused" if self.remaining < total else "Ready"
        self.canvas.itemconfig(self.sub_txt, text=sub)

        self.mode_lbl.config(text=cfg["label"].upper(), fg=cfg["color"])

        filled_dots = (
            DOTS_PER_CYCLE if self.mode == "long" else self.completed % ROUNDS_PER_CYCLE
        )
        for i, dot in enumerate(self.dot_ids):
            on = i < filled_dots
            self.dots.itemconfig(
                dot,
                fill=MODES["work"]["color"] if on else BG,
                outline=MODES["work"]["color"] if on else TRACK,
            )

        self.start_btn.config(text="Pause" if self.running else "Start")
        self.start_btn.set_colors(cfg["color"], cfg["hover"])

    # ------------------------------------------------------------- timer
    def toggle(self) -> None:
        """Start or pause the timer, depending on current state."""
        self.pause() if self.running else self.start()

    def start(self) -> None:
        """Start (or resume) the countdown."""
        if self.running:
            return
        if self.remaining <= 0.05:
            self.remaining = float(self.durations[self.mode] * SECONDS_PER_MINUTE)
        self.running = True
        self._deadline = time.monotonic() + self.remaining
        self._tick()

    def pause(self) -> None:
        """Pause the countdown and keep the remaining time."""
        if not self.running:
            return
        self.running = False
        self._cancel_tick()
        self._render()

    def reset(self) -> None:
        """Reset the current session to its full duration."""
        self.running = False
        self._cancel_tick()
        self.remaining = float(self.durations[self.mode] * SECONDS_PER_MINUTE)
        self._render()

    def skip(self) -> None:
        """Skip the current session and advance to the next one."""
        self.running = False
        self._cancel_tick()
        self._advance(count=False)
        self._render()

    def _cancel_tick(self) -> None:
        """Cancel the pending after() callback, if any."""
        if self._after_id is not None:
            self.root.after_cancel(self._after_id)
            self._after_id = None

    def _tick(self) -> None:
        """Update the remaining time and schedule the next tick."""
        if not self.running:
            return
        self.remaining = self._deadline - time.monotonic()
        if self.remaining <= 0:
            self.remaining = 0.0
            self._render()
            self._finish()
            return
        self._render()
        self._after_id = self.root.after(TICK_MS, self._tick)

    def _finish(self) -> None:
        """Handle the end of a session: bell, advance, re-render."""
        self.running = False
        self._cancel_tick()
        try:
            self.root.bell()
            self.root.lift()
        except tk.TclError:
            pass
        self._advance(count=True)
        self._render()

    def _advance(self, count: bool) -> None:
        """Move to the next session.

        Args:
            count: whether the just-finished work session counts towards
                the long-break cycle.
        """
        if self.mode == "work":
            if count:
                self.completed += 1
                if self.completed % ROUNDS_PER_CYCLE == 0:
                    self._set_mode("long")
                    return
            self._set_mode("short")
        else:
            self._set_mode("work")

    def _set_mode(self, mode: str) -> None:
        """Switch to the given mode and reset the remaining time."""
        self.mode = mode
        self.remaining = float(self.durations[mode] * SECONDS_PER_MINUTE)
        self.running = False
        self._cancel_tick()
        self._last_key = None  # force a re-render

    # ------------------------------------------------------------- settings
    def _duration_changed(self, key: str) -> None:
        """Clamp and apply a new duration coming from a Spinbox."""
        try:
            val = int(self.vars[key].get())
        except (tk.TclError, ValueError):
            return
        val = max(MIN_DURATION, min(MAX_DURATION, val))
        if val != self.vars[key].get():
            self.vars[key].set(val)
        self.durations[key] = val
        if key == self.mode and not self.running:
            self.remaining = float(val * SECONDS_PER_MINUTE)
            self._last_key = None
            self._render()

    # ------------------------------------------------------------- keys
    def _bind_keys(self) -> None:
        """Bind keyboard shortcuts, ignoring them when a Spinbox has focus."""

        def guard(fn):
            def handler(_event: tk.Event) -> None:
                try:
                    if isinstance(self.root.focus_get(), tk.Spinbox):
                        return
                except (KeyError, tk.TclError):
                    pass
                fn()

            return handler

        self.root.bind("<space>", guard(self.toggle))
        self.root.bind("<r>", guard(self.reset))
        self.root.bind("<s>", guard(self.skip))
        self.root.bind("<Escape>", lambda _event: self.root.destroy())


def main() -> None:
    """Create the window, centre it, and run the app."""
    root = tk.Tk()
    Pomodoro(root)
    root.update_idletasks()
    x = (root.winfo_screenwidth() - root.winfo_width()) // 2
    y = (root.winfo_screenheight() - root.winfo_height()) // 3
    root.geometry(f"+{x}+{y}")
    root.mainloop()


if __name__ == "__main__":
    main()
