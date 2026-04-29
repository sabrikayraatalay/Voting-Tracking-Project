import tkinter as tk
from tkinter import messagebox, ttk
from gui.DashboardScreen import DashboardScreen

# ── Design Tokens ─────────────────────────────────────────────────────────────
BG         = "#EAECF0"
CARD_BG    = "#FFFFFF"
ACCENT     = "#1A3A5C"
ACCENT_LIT = "#2E5F8A"
TEXT_PRI   = "#1C1C1E"
TEXT_SEC   = "#6E6E73"
BORDER     = "#C8C8CC"
FONT       = "Helvetica Neue"
# ─────────────────────────────────────────────────────────────────────────────


def make_button(parent, text, command, bg, hover_bg, fg="white", pad_y=13):
    """
    macOS-safe clickable button built from a Label.
    tk.Button ignores bg on macOS Aqua theme; tk.Label does not.
    """
    btn = tk.Label(parent, text=text,
                   font=(FONT, 13, "bold"),
                   bg=bg, fg=fg,
                   cursor="hand2",
                   pady=pad_y)
    btn.pack(fill="x")
    btn.bind("<Button-1>", lambda e: command())
    btn.bind("<Enter>",    lambda e: btn.configure(bg=hover_bg))
    btn.bind("<Leave>",    lambda e: btn.configure(bg=bg))
    return btn


class LoginScreen:
    def __init__(self, root, db_manager):
        self.root = root
        self.db   = db_manager

        self.root.title("Election System — Login")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        # Set geometry BEFORE building UI — avoids macOS layout collapse
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        w, h = 400, 500
        self.root.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

        self.setup_ui()

    def setup_ui(self):
        # ── Hero strip ────────────────────────────────────────────────────
        hero = tk.Frame(self.root, bg=ACCENT)
        hero.pack(fill="x", side="top")

        tk.Label(hero, text="🗳",
                 font=(FONT, 36), bg=ACCENT, fg="white"
                 ).pack(pady=(24, 4))
        tk.Label(hero, text="Election System",
                 font=(FONT, 17, "bold"), bg=ACCENT, fg="white"
                 ).pack()
        tk.Label(hero, text="Secure Voting Platform",
                 font=(FONT, 10), bg=ACCENT, fg="#A8C0D8"
                 ).pack(pady=(2, 22))

        # ── Form area ─────────────────────────────────────────────────────
        form = tk.Frame(self.root, bg=BG)
        form.pack(fill="x", padx=36, pady=28)

        # TC Number
        tk.Label(form, text="TC Identity Number",
                 font=(FONT, 11, "bold"), bg=BG, fg=TEXT_SEC,
                 anchor="w").pack(fill="x")

        tc_wrap = tk.Frame(form, bg=CARD_BG,
                           highlightthickness=1,
                           highlightbackground=BORDER,
                           highlightcolor=ACCENT)
        tc_wrap.pack(fill="x", pady=(4, 16))
        self.tc_entry = tk.Entry(tc_wrap,
                                 font=(FONT, 13), bg=CARD_BG, fg=TEXT_PRI,
                                 bd=0, relief="flat", insertbackground=ACCENT)
        self.tc_entry.pack(fill="x", padx=12, pady=10)
        self.tc_entry.bind("<FocusIn>",  lambda e: tc_wrap.configure(highlightbackground=ACCENT))
        self.tc_entry.bind("<FocusOut>", lambda e: tc_wrap.configure(highlightbackground=BORDER))
        self.tc_entry.bind("<Return>",   lambda e: self.pass_entry.focus_set())

        # Password
        tk.Label(form, text="Password",
                 font=(FONT, 11, "bold"), bg=BG, fg=TEXT_SEC,
                 anchor="w").pack(fill="x")

        pw_wrap = tk.Frame(form, bg=CARD_BG,
                           highlightthickness=1,
                           highlightbackground=BORDER,
                           highlightcolor=ACCENT)
        pw_wrap.pack(fill="x", pady=(4, 24))
        self.pass_entry = tk.Entry(pw_wrap, show="•",
                                   font=(FONT, 13), bg=CARD_BG, fg=TEXT_PRI,
                                   bd=0, relief="flat", insertbackground=ACCENT)
        self.pass_entry.pack(fill="x", padx=12, pady=10)
        self.pass_entry.bind("<FocusIn>",  lambda e: pw_wrap.configure(highlightbackground=ACCENT))
        self.pass_entry.bind("<FocusOut>", lambda e: pw_wrap.configure(highlightbackground=BORDER))
        self.pass_entry.bind("<Return>",   lambda e: self.attempt_login())

        # Sign In — Label-based button (macOS-safe)
        make_button(form, "Sign In  →", self.attempt_login,
                    bg=ACCENT, hover_bg=ACCENT_LIT)

        tk.Label(form, text="Authorised personnel only",
                 font=(FONT, 9), bg=BG, fg=TEXT_SEC
                 ).pack(pady=(14, 0))

    # ── Backend (unchanged) ───────────────────────────────────────────────────

    def attempt_login(self):
        tc       = self.tc_entry.get().strip()
        password = self.pass_entry.get().strip()

        if not tc or not password:
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return

        user = self.db.authenticate_user(tc, password)

        if user:
            self.root.destroy()
            self.open_dashboard(user)
        else:
            messagebox.showerror("Error", "Invalid TC Number or Password.")

    def open_dashboard(self, user):
        dashboard_root = tk.Tk()
        DashboardScreen(dashboard_root, self.db, user)
        dashboard_root.mainloop()
