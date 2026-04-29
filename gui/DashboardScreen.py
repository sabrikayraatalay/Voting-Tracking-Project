import tkinter as tk
from tkinter import messagebox
from models.Admin import Admin
from gui.BallotScreen import BallotScreen
from gui.AddCandidateScreen import AddCandidateScreen

# ── Design Tokens ─────────────────────────────────────────────────────────────
BG         = "#EAECF0"
CARD_BG    = "#FFFFFF"
ACCENT     = "#1A3A5C"
ACCENT_LIT = "#2E5F8A"
GOLD       = "#C8963E"
GOLD_LIT   = "#B8852E"
GREEN      = "#2C6B4F"
GREEN_LIT  = "#235940"
TEXT_PRI   = "#1C1C1E"
TEXT_SEC   = "#6E6E73"
BORDER     = "#C8C8CC"
SUCCESS    = "#34C759"
FONT       = "Helvetica Neue"
# ─────────────────────────────────────────────────────────────────────────────


def make_button(parent, text, command, bg, hover_bg, fg="white", pad_y=11):
    btn = tk.Label(parent, text=text,
                   font=(FONT, 12), bg=bg, fg=fg,
                   cursor="hand2", anchor="w",
                   padx=18, pady=pad_y)
    btn.pack(fill="x", pady=6, padx=18)
    btn.bind("<Button-1>", lambda e: command())
    btn.bind("<Enter>",    lambda e: btn.configure(bg=hover_bg))
    btn.bind("<Leave>",    lambda e: btn.configure(bg=bg))
    return btn


def pill(parent, label, voted):
    color  = SUCCESS if voted else "#AEAEB2"
    symbol = "✓" if voted else "–"
    tk.Label(parent,
             text=f"  {symbol}  {label}: {'Voted' if voted else 'Not Voted'}  ",
             font=(FONT, 10, "bold"), bg=color, fg="white",
             padx=6, pady=4
             ).pack(side="left", padx=(0, 8))


def section_card(parent, title, icon, bar_color):
    outer = tk.Frame(parent, bg=BG)
    outer.pack(fill="x", padx=28, pady=(0, 18))

    bar = tk.Frame(outer, bg=bar_color)
    bar.pack(fill="x")
    tk.Label(bar, text=f"  {icon}   {title}",
             font=(FONT, 11, "bold"), bg=bar_color, fg="white",
             anchor="w").pack(fill="x", padx=8, pady=10)

    body = tk.Frame(outer, bg=CARD_BG,
                    highlightthickness=1,
                    highlightbackground=BORDER)
    body.pack(fill="x")
    return body


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

        # Geometry BEFORE setup_ui
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        w  = 640
        h  = 580 if is_admin else 420
        self.root.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

        self.setup_ui()

    def setup_ui(self):
        self._topbar()
        tk.Frame(self.root, bg=BG, height=18).pack()
        self.create_voting_panel()
        if isinstance(self.user, Admin):
            self.create_admin_panel()
        tk.Frame(self.root, bg=BG, height=18).pack()

    def _topbar(self):
        bar = tk.Frame(self.root, bg=ACCENT)
        bar.pack(fill="x")

        left = tk.Frame(bar, bg=ACCENT)
        left.pack(side="left", padx=24, pady=16)
        tk.Label(left, text=f"Welcome, {self.user.get_name()}",
                 font=(FONT, 15, "bold"), bg=ACCENT, fg="white",
                 anchor="w").pack(anchor="w")
        role = "Administrator" if isinstance(self.user, Admin) else "Registered Voter"
        tk.Label(left, text=role,
                 font=(FONT, 10), bg=ACCENT, fg="#A8C0D8",
                 anchor="w").pack(anchor="w")

        right = tk.Frame(bar, bg=ACCENT)
        right.pack(side="right", padx=24, pady=20)
        tk.Label(right, text="  🔴  LIVE  ",
                 font=(FONT, 10, "bold"), bg=GOLD, fg="white",
                 padx=6, pady=4).pack()

    # ── Voter panel ───────────────────────────────────────────────────────────

    def create_voting_panel(self):
        body = section_card(self.root, "Voting Booth", "🗳", ACCENT)

        tk.Label(body, text="Cast your official vote for each open position.",
                 font=(FONT, 11), bg=CARD_BG, fg=TEXT_SEC,
                 wraplength=520, justify="left", anchor="w"
                 ).pack(fill="x", padx=18, pady=(14, 10))

        pills_row = tk.Frame(body, bg=CARD_BG)
        pills_row.pack(anchor="w", padx=18, pady=(0, 14))
        pill(pills_row, "President", self.user.get_has_voted_president())
        pill(pills_row, "Mayor",     self.user.get_has_voted_mayor())

        make_button(body, "📋   Open Ballot & Cast Vote",
                    self.open_ballot_window, ACCENT, ACCENT_LIT)
        tk.Frame(body, bg=CARD_BG, height=10).pack()

    def open_ballot_window(self):
        BallotScreen(self.root, self.db, self.user)

    # ── Admin panel ───────────────────────────────────────────────────────────

    def create_admin_panel(self):
        body = section_card(self.root, "Admin Control Centre", "⚙️", GOLD)

        tk.Label(body, text="Manage candidates and monitor live election results.",
                 font=(FONT, 11), bg=CARD_BG, fg=TEXT_SEC,
                 wraplength=520, justify="left", anchor="w"
                 ).pack(fill="x", padx=18, pady=(14, 10))

        make_button(body, "➕   Add New Candidate",
                    self.open_add_candidate_window, GOLD, GOLD_LIT)
        make_button(body, "📊   View Election Results",
                    self.show_results, GREEN, GREEN_LIT)
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
