import tkinter as tk
from tkinter import messagebox, ttk
from models.Candidate import Candidate

# ── Design Tokens ─────────────────────────────────────────────────────────────
BG         = "#EAECF0"
CARD_BG    = "#FFFFFF"
ACCENT     = "#1A3A5C"
GOLD       = "#C8963E"
GOLD_LIT   = "#B8852E"
TEXT_PRI   = "#1C1C1E"
TEXT_SEC   = "#6E6E73"
BORDER     = "#C8C8CC"
BORDER_DIM = "#E0E0E5"
FONT       = "Helvetica Neue"
# ─────────────────────────────────────────────────────────────────────────────


class AddCandidateScreen:
    def __init__(self, parent, db_manager):
        self.window = tk.Toplevel(parent)
        self.db     = db_manager

        self.window.title("Admin — Add Candidate")
        self.window.configure(bg=BG)
        self.window.resizable(False, False)

        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        w, h = 420, 540
        self.window.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

        self.window.grab_set()
        self.setup_ui()

    def _field(self, parent, label_text, show=None, disabled=False):
        """Helper: label + bordered entry. Returns (entry, wrap_frame)."""
        tk.Label(parent, text=label_text,
                 font=(FONT, 11, "bold"), bg=BG, fg=TEXT_SEC,
                 anchor="w").pack(fill="x")

        hb = BORDER_DIM if disabled else BORDER
        wrap = tk.Frame(parent, bg=CARD_BG,
                        highlightthickness=1,
                        highlightbackground=hb,
                        highlightcolor=ACCENT)
        wrap.pack(fill="x", pady=(4, 16))

        state = "disabled" if disabled else "normal"
        entry = tk.Entry(wrap, show=show, state=state,
                         font=(FONT, 13), bg=CARD_BG, fg=TEXT_PRI,
                         bd=0, relief="flat", insertbackground=ACCENT,
                         disabledbackground=CARD_BG,
                         disabledforeground="#AEAEB2")
        entry.pack(fill="x", padx=12, pady=10)
        entry.bind("<FocusIn>",  lambda e: wrap.configure(highlightbackground=ACCENT))
        entry.bind("<FocusOut>", lambda e: wrap.configure(highlightbackground=BORDER))
        return entry, wrap

    def setup_ui(self):
        # Header
        header = tk.Frame(self.window, bg=GOLD)
        header.pack(fill="x")
        tk.Label(header, text="➕  Register New Candidate",
                 font=(FONT, 14, "bold"), bg=GOLD, fg="white"
                 ).pack(pady=(18, 2))
        tk.Label(header, text="Complete all required fields below",
                 font=(FONT, 10), bg=GOLD, fg="#FFF0D6"
                 ).pack(pady=(0, 18))

        # Form
        form = tk.Frame(self.window, bg=BG)
        form.pack(fill="x", padx=32, pady=20)

        self.name_entry,  _               = self._field(form, "Candidate Name  *")
        self.party_entry, _               = self._field(form, "Political Party  *")

        # Position combobox
        tk.Label(form, text="Position",
                 font=(FONT, 11, "bold"), bg=BG, fg=TEXT_SEC,
                 anchor="w").pack(fill="x")
        cb_wrap = tk.Frame(form, bg=CARD_BG,
                           highlightthickness=1,
                           highlightbackground=BORDER)
        cb_wrap.pack(fill="x", pady=(4, 16))
        self.position_cb = ttk.Combobox(cb_wrap,
                                        values=["President", "Mayor"],
                                        state="readonly",
                                        font=(FONT, 12))
        self.position_cb.set("President")
        self.position_cb.pack(fill="x", padx=10, pady=8)
        self.position_cb.bind("<<ComboboxSelected>>", self.on_position_change)

        # City
        self.city_entry, self.city_wrap   = self._field(form, "City  (required for Mayors)",
                                                         disabled=True)

        # Save button (Label-based — macOS safe)
        btn_frame = tk.Frame(self.window, bg=BG)
        btn_frame.pack(fill="x", padx=32, pady=(0, 24))

        save = tk.Label(btn_frame, text="  💾   Save Candidate",
                        font=(FONT, 13, "bold"),
                        bg=GOLD, fg="white",
                        cursor="hand2", pady=13)
        save.pack(fill="x")
        save.bind("<Button-1>", lambda e: self.save_candidate())
        save.bind("<Enter>",    lambda e: save.configure(bg=GOLD_LIT))
        save.bind("<Leave>",    lambda e: save.configure(bg=GOLD))

    # ── Backend (unchanged) ───────────────────────────────────────────────────

    def on_position_change(self, event):
        if self.position_cb.get() == "President":
            self.city_entry.delete(0, tk.END)
            self.city_entry.config(state="disabled")
            self.city_wrap.configure(highlightbackground=BORDER_DIM)
        else:
            self.city_entry.config(state="normal")
            self.city_wrap.configure(highlightbackground=BORDER)

    def save_candidate(self):
        name     = self.name_entry.get().strip()
        party    = self.party_entry.get().strip()
        position = self.position_cb.get()
        city     = self.city_entry.get().strip()

        if not name or not party:
            messagebox.showwarning("Warning",
                                   "Name and Party fields cannot be empty!",
                                   parent=self.window)
            return

        if position == "Mayor" and not city:
            messagebox.showwarning("Warning",
                                   "City is mandatory for Mayoral candidates!",
                                   parent=self.window)
            return

        if position == "President":
            city = None

        new_candidate = Candidate(None, name, party, position, city)
        self.db.add_candidate(new_candidate)

        messagebox.showinfo("Success",
                            f"{name} successfully registered as a candidate!",
                            parent=self.window)
        self.window.destroy()
