import tkinter as tk
from tkinter import messagebox
from gui.DashboardScreen import DashboardScreen

# ── Design Tokens ─────────────────────────────────────────────────────────────
BG         = "#F0F2F5"
CARD_BG    = "#FFFFFF"
ACCENT     = "#1A3A5C"
ACCENT_LIT = "#2E5F8A"
TEXT_PRI   = "#1C1C1E"
TEXT_SEC   = "#6E6E73"
BORDER     = "#D1D1D6"
FONT       = "Helvetica Neue"
# ─────────────────────────────────────────────────────────────────────────────


def _center(win, w, h):
    win.update_idletasks()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    win.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")


def _make_entry(parent, show=None):
    """Bordered entry widget that works reliably on macOS."""
    wrap = tk.Frame(parent, bg=CARD_BG,
                    highlightthickness=1,
                    highlightbackground=BORDER,
                    highlightcolor=ACCENT)
    wrap.pack(fill="x", pady=(4, 16))
    entry = tk.Entry(wrap, show=show,
                     font=(FONT, 13),
                     bg=CARD_BG, fg=TEXT_PRI,
                     bd=0, relief="flat",
                     insertbackground=ACCENT)
    entry.pack(fill="x", padx=14, pady=10)
    # Focus glow
    entry.bind("<FocusIn>",  lambda e: wrap.configure(highlightbackground=ACCENT))
    entry.bind("<FocusOut>", lambda e: wrap.configure(highlightbackground=BORDER))
    return entry, wrap


class LoginScreen:
    def __init__(self, root, db_manager):
        self.root = root
        self.db   = db_manager

        self.root.title("Election System — Login")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        _center(self.root, 400, 510)
        self.setup_ui()

    def setup_ui(self):
        # ── Hero ──────────────────────────────────────────────────────────
        hero = tk.Frame(self.root, bg=ACCENT)
        hero.pack(fill="x")

        tk.Label(hero, text="🗳",
                 font=(FONT, 34), bg=ACCENT, fg="white").pack(pady=(22, 4))
        tk.Label(hero, text="Election System",
                 font=(FONT, 16, "bold"), bg=ACCENT, fg="white").pack()
        tk.Label(hero, text="Secure Voting Platform",
                 font=(FONT, 10), bg=ACCENT, fg="#A8C0D8").pack(pady=(2, 22))

        # ── Form ──────────────────────────────────────────────────────────
        form = tk.Frame(self.root, bg=BG)
        form.pack(fill="both", expand=True, padx=36, pady=28)

        tk.Label(form, text="TC Identity Number",
                 font=(FONT, 11, "bold"), bg=BG, fg=TEXT_SEC,
                 anchor="w").pack(fill="x")
        self.tc_entry, _ = _make_entry(form)
        self.tc_entry.bind("<Return>", lambda e: self.pass_entry.focus_set())

        tk.Label(form, text="Password",
                 font=(FONT, 11, "bold"), bg=BG, fg=TEXT_SEC,
                 anchor="w").pack(fill="x")
        self.pass_entry, _ = _make_entry(form, show="•")
        self.pass_entry.bind("<Return>", lambda e: self.attempt_login())

        # Sign In button
        btn = tk.Button(form, text="Sign In  →",
                        command=self.attempt_login,
                        font=(FONT, 13, "bold"),
                        bg=ACCENT, fg="white",
                        activebackground=ACCENT_LIT, activeforeground="white",
                        relief="flat", bd=0,
                        cursor="hand2", pady=13)
        btn.pack(fill="x", pady=(6, 0))
        btn.bind("<Enter>", lambda e: btn.configure(bg=ACCENT_LIT))
        btn.bind("<Leave>", lambda e: btn.configure(bg=ACCENT))

        tk.Label(form, text="Authorised personnel only",
                 font=(FONT, 9), bg=BG, fg=TEXT_SEC).pack(pady=(14, 0))

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
