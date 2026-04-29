import tkinter as tk
from tkinter import messagebox
from models.Admin import Admin
from gui.BallotScreen import BallotScreen
from gui.AddCandidateScreen import AddCandidateScreen

# ── Design Tokens ─────────────────────────────────────────────────────────────
BG         = "#F0F2F5"
CARD_BG    = "#FFFFFF"
ACCENT     = "#1A3A5C"
ACCENT_LIT = "#2E5F8A"
GOLD       = "#C8963E"
GOLD_LIT   = "#B8852E"
GREEN_DARK = "#2C6B4F"
GREEN_LIT  = "#235940"
TEXT_PRI   = "#1C1C1E"
TEXT_SEC   = "#6E6E73"
BORDER     = "#D1D1D6"
SUCCESS    = "#34C759"
FONT       = "Helvetica Neue"
# ─────────────────────────────────────────────────────────────────────────────


def _center(win, w, h):
    win.update_idletasks()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    win.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")


def _section(parent, title, icon, bar_color):
    """Titled white card with coloured header bar."""
    outer = tk.Frame(parent, bg=BG)
    outer.pack(fill="x", padx=28, pady=(0, 18))

    # Coloured header
    bar = tk.Frame(outer, bg=bar_color)
    bar.pack(fill="x")
    tk.Label(bar, text=f"  {icon}   {title}",
             font=(FONT, 11, "bold"), bg=bar_color, fg="white",
             anchor="w").pack(fill="x", padx=8, pady=10)

    # White body
    body = tk.Frame(outer, bg=CARD_BG,
                    highlightthickness=1,
                    highlightbackground=BORDER,
                    highlightcolor=BORDER)
    body.pack(fill="x")
    return body


def _btn(parent, text, command, bg, active_bg, icon=""):
    b = tk.Button(parent, text=f"  {icon}   {text}",
                  command=command,
                  font=(FONT, 12), anchor="w",
                  bg=bg, fg="white",
                  activebackground=active_bg, activeforeground="white",
                  relief="flat", bd=0, cursor="hand2", pady=11)
    b.pack(fill="x", padx=18, pady=6)
    b.bind("<Enter>", lambda e: b.configure(bg=active_bg))
    b.bind("<Leave>", lambda e: b.configure(bg=bg))
    return b


def _pill(parent, label, voted: bool):
    color  = SUCCESS if voted else "#AEAEB2"
    symbol = "✓" if voted else "–"
    tk.Label(parent, text=f"  {symbol}  {label}: {'Voted' if voted else 'Not voted'}  ",
             font=(FONT, 10, "bold"),
             bg=color, fg="white",
             padx=8, pady=4).pack(side="left", padx=(0, 8))


class DashboardScreen:
    def __init__(self, root, db_manager, current_user):
        self.root = root
        self.db   = db_manager
        self.user = current_user

        is_admin   = isinstance(self.user, Admin)
        role_title = "Admin" if is_admin else "Voter"
        self.root.title(f"Election Dashboard — {self.user.get_name()} ({role_title})")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        height = 600 if is_admin else 430
        _center(self.root, 640, height)
        self.setup_ui()

    def setup_ui(self):
        self._build_topbar()
        tk.Frame(self.root, bg=BG, height=18).pack()   # top spacer
        self.create_voting_panel()
        if isinstance(self.user, Admin):
            self.create_admin_panel()
        tk.Frame(self.root, bg=BG, height=18).pack()   # bottom spacer

    # ── Top bar ───────────────────────────────────────────────────────────────

    def _build_topbar(self):
        bar = tk.Frame(self.root, bg=ACCENT)
        bar.pack(fill="x")

        # Left side
        left = tk.Frame(bar, bg=ACCENT)
        left.pack(side="left", padx=24, pady=16)
        tk.Label(left, text=f"Welcome, {self.user.get_name()}",
                 font=(FONT, 15, "bold"), bg=ACCENT, fg="white",
                 anchor="w").pack(anchor="w")
        role = "Administrator" if isinstance(self.user, Admin) else "Registered Voter"
        tk.Label(left, text=role,
                 font=(FONT, 10), bg=ACCENT, fg="#A8C0D8",
                 anchor="w").pack(anchor="w")

        # Right side — LIVE badge
        right = tk.Frame(bar, bg=ACCENT)
        right.pack(side="right", padx=24, pady=20)
        tk.Label(right, text="  🔴  LIVE  ",
                 font=(FONT, 10, "bold"), bg=GOLD, fg="white",
                 padx=6, pady=4).pack()

    # ── Voter panel ───────────────────────────────────────────────────────────

    def create_voting_panel(self):
        body = _section(self.root, "Voting Booth", "🗳", ACCENT)

        tk.Label(body, text="Cast your official vote for each open position.",
                 font=(FONT, 11), bg=CARD_BG, fg=TEXT_SEC,
                 wraplength=520, justify="left",
                 anchor="w").pack(fill="x", padx=18, pady=(14, 10))

        # Status pills
        pills = tk.Frame(body, bg=CARD_BG)
        pills.pack(anchor="w", padx=18, pady=(0, 14))
        _pill(pills, "President", self.user.get_has_voted_president())
        _pill(pills, "Mayor",     self.user.get_has_voted_mayor())

        _btn(body, "Open Ballot & Cast Vote",
             self.open_ballot_window, ACCENT, ACCENT_LIT, icon="📋")

        tk.Frame(body, bg=CARD_BG, height=10).pack()

    def open_ballot_window(self):
        BallotScreen(self.root, self.db, self.user)

    # ── Admin panel ───────────────────────────────────────────────────────────

    def create_admin_panel(self):
        body = _section(self.root, "Admin Control Centre", "⚙️", GOLD)

        tk.Label(body, text="Manage candidates and monitor live election results.",
                 font=(FONT, 11), bg=CARD_BG, fg=TEXT_SEC,
                 wraplength=520, justify="left",
                 anchor="w").pack(fill="x", padx=18, pady=(14, 10))

        _btn(body, "Add New Candidate",
             self.open_add_candidate_window, GOLD, GOLD_LIT, icon="➕")
        _btn(body, "View Election Results",
             self.show_results, GREEN_DARK, GREEN_LIT, icon="📊")

        tk.Frame(body, bg=CARD_BG, height=10).pack()

    def open_add_candidate_window(self):
        AddCandidateScreen(self.root, self.db)

    def show_results(self):
        candidates = self.db.get_all_candidates()
        if not candidates:
            messagebox.showinfo("Results", "No votes cast yet.")
            return

        result_text = "CURRENT ELECTION RESULTS\n" + "─" * 30 + "\n"
        for c in candidates:
            result_text += f"{c.get_name()} ({c.get_party()}): {c.get_vote_count()} votes\n"

        messagebox.showinfo("Election Results", result_text)
