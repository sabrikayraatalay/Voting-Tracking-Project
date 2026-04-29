import tkinter as tk
from tkinter import messagebox, ttk
from models.Candidate import Candidate

# ── Design Tokens ─────────────────────────────────────────────────────────────
BG         = "#F0F2F5"
CARD_BG    = "#FFFFFF"
ACCENT     = "#1A3A5C"
GOLD       = "#C8963E"
GOLD_LIT   = "#B8852E"
TEXT_PRI   = "#1C1C1E"
TEXT_SEC   = "#6E6E73"
BORDER     = "#D1D1D6"
BORDER_DIM = "#E5E5EA"
FONT       = "Helvetica Neue"
# ─────────────────────────────────────────────────────────────────────────────


def _center(win, w, h):
    win.update_idletasks()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    win.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")


class AddCandidateScreen:
    def __init__(self, parent, db_manager):
        self.window = tk.Toplevel(parent)
        self.db     = db_manager

        self.window.title("Admin — Add Candidate")
        self.window.configure(bg=BG)
        self.window.resizable(False, False)
        _center(self.window, 420, 540)
        self.window.grab_set()
        self.setup_ui()

    def setup_ui(self):
        # ── Header ────────────────────────────────────────────────────────
        header = tk.Frame(self.window, bg=GOLD)
        header.pack(fill="x")

        tk.Label(header, text="➕  Register New Candidate",
                 font=(FONT, 14, "bold"), bg=GOLD, fg="white").pack(pady=(18, 2))
        tk.Label(header, text="Complete all required fields below",
                 font=(FONT, 10), bg=GOLD, fg="#FFF0D6").pack(pady=(0, 18))

        # ── Form ──────────────────────────────────────────────────────────
        form = tk.Frame(self.window, bg=BG)
        form.pack(fill="both", expand=True, padx=32, pady=24)

        # ── Candidate Name ────────────────────────────────────────────────
        tk.Label(form, text="Candidate Name  *",
                 font=(FONT, 11, "bold"), bg=BG, fg=TEXT_SEC,
                 anchor="w").pack(fill="x")
        name_wrap = tk.Frame(form, bg=CARD_BG,
                             highlightthickness=1,
                             highlightbackground=BORDER,
                             highlightcolor=ACCENT)
        name_wrap.pack(fill="x", pady=(4, 16))
        self.name_entry = tk.Entry(name_wrap,
                                   font=(FONT, 13), bg=CARD_BG, fg=TEXT_PRI,
                                   bd=0, relief="flat", insertbackground=ACCENT)
        self.name_entry.pack(fill="x", padx=14, pady=10)
        self.name_entry.bind("<FocusIn>",  lambda e: name_wrap.configure(highlightbackground=ACCENT))
        self.name_entry.bind("<FocusOut>", lambda e: name_wrap.configure(highlightbackground=BORDER))

        # ── Party ─────────────────────────────────────────────────────────
        tk.Label(form, text="Political Party  *",
                 font=(FONT, 11, "bold"), bg=BG, fg=TEXT_SEC,
                 anchor="w").pack(fill="x")
        party_wrap = tk.Frame(form, bg=CARD_BG,
                              highlightthickness=1,
                              highlightbackground=BORDER,
                              highlightcolor=ACCENT)
        party_wrap.pack(fill="x", pady=(4, 16))
        self.party_entry = tk.Entry(party_wrap,
                                    font=(FONT, 13), bg=CARD_BG, fg=TEXT_PRI,
                                    bd=0, relief="flat", insertbackground=ACCENT)
        self.party_entry.pack(fill="x", padx=14, pady=10)
        self.party_entry.bind("<FocusIn>",  lambda e: party_wrap.configure(highlightbackground=ACCENT))
        self.party_entry.bind("<FocusOut>", lambda e: party_wrap.configure(highlightbackground=BORDER))

        # ── Position Combobox ─────────────────────────────────────────────
        tk.Label(form, text="Position",
                 font=(FONT, 11, "bold"), bg=BG, fg=TEXT_SEC,
                 anchor="w").pack(fill="x")
        cb_wrap = tk.Frame(form, bg=CARD_BG,
                           highlightthickness=1,
                           highlightbackground=BORDER,
                           highlightcolor=ACCENT)
        cb_wrap.pack(fill="x", pady=(4, 16))

        self.position_cb = ttk.Combobox(cb_wrap,
                                        values=["President", "Mayor"],
                                        state="readonly",
                                        font=(FONT, 12))
        self.position_cb.set("President")
        self.position_cb.pack(fill="x", padx=10, pady=8)
        self.position_cb.bind("<<ComboboxSelected>>", self.on_position_change)

        # ── City ──────────────────────────────────────────────────────────
        tk.Label(form, text="City  (required for Mayors)",
                 font=(FONT, 11, "bold"), bg=BG, fg=TEXT_SEC,
                 anchor="w").pack(fill="x")
        self.city_wrap = tk.Frame(form, bg=CARD_BG,
                                  highlightthickness=1,
                                  highlightbackground=BORDER_DIM,
                                  highlightcolor=ACCENT)
        self.city_wrap.pack(fill="x", pady=(4, 0))
        self.city_entry = tk.Entry(self.city_wrap,
                                   font=(FONT, 13), bg=CARD_BG, fg=TEXT_PRI,
                                   bd=0, relief="flat", insertbackground=ACCENT,
                                   state="disabled",
                                   disabledbackground=CARD_BG,
                                   disabledforeground="#AEAEB2")
        self.city_entry.pack(fill="x", padx=14, pady=10)
        self.city_entry.bind("<FocusIn>",  lambda e: self.city_wrap.configure(highlightbackground=ACCENT))
        self.city_entry.bind("<FocusOut>", lambda e: self.city_wrap.configure(highlightbackground=BORDER))

        # ── Save button ───────────────────────────────────────────────────
        btn_outer = tk.Frame(self.window, bg=BG)
        btn_outer.pack(fill="x", padx=32, pady=(18, 24))

        save = tk.Button(btn_outer, text="  💾   Save Candidate",
                         command=self.save_candidate,
                         font=(FONT, 13, "bold"),
                         bg=GOLD, fg="white",
                         activebackground=GOLD_LIT, activeforeground="white",
                         relief="flat", bd=0,
                         cursor="hand2", pady=13)
        save.pack(fill="x")
        save.bind("<Enter>", lambda e: save.configure(bg=GOLD_LIT))
        save.bind("<Leave>", lambda e: save.configure(bg=GOLD))

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
