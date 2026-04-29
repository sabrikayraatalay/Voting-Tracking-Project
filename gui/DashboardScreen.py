import tkinter as tk
from tkinter import messagebox
from models.Admin import Admin
from gui.BallotScreen import BallotScreen
from gui.AddCandidateScreen import AddCandidateScreen

BG = "#EAECF0"
CARD_BG = "#FFFFFF"
ACCENT = "#1A3A5C"
ACCENT_LIT = "#2E5F8A"
GOLD = "#C8963E"
GOLD_LIT = "#B8852E"
GREEN = "#2C6B4F"
GREEN_LIT = "#235940"
TEXT_SEC = "#6E6E73"
BORDER = "#C8C8CC"
SUCCESS = "#34C759"
FONT = "Arial"


def make_button(parent, text, command, bg, hover_bg):
    btn = tk.Label(parent, text=text,
                   font=(FONT, 12),
                   bg=bg, fg="white",
                   cursor="hand2",
                   padx=18, pady=10)
    btn.pack(fill="x", pady=6, padx=18)
    btn.bind("<Button-1>", lambda e: command())
    btn.bind("<Enter>", lambda e: btn.configure(bg=hover_bg))
    btn.bind("<Leave>", lambda e: btn.configure(bg=bg))


class DashboardScreen:
    def __init__(self, root, db_manager, user):
        self.root = root
        self.db = db_manager
        self.user = user

        self.root.title("Dashboard")
        self.root.configure(bg=BG)

        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        root.geometry(f"600x450+{(sw-600)//2}+{(sh-450)//2}")

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root,
                 text=f"Welcome {self.user.get_name()}",
                 font=(FONT, 16, "bold"),
                 bg=BG).pack(pady=20)

        make_button(self.root, "Vote",
                    self.open_ballot, ACCENT, ACCENT_LIT)

        if isinstance(self.user, Admin):
            make_button(self.root, "Add Candidate",
                        self.add_candidate, GOLD, GOLD_LIT)

            make_button(self.root, "View Results",
                        self.show_results, GREEN, GREEN_LIT)

    def open_ballot(self):
        BallotScreen(self.root, self.db, self.user)

    def add_candidate(self):
        AddCandidateScreen(self.root, self.db)

    def show_results(self):
        candidates = self.db.get_all_candidates()

        if not candidates:
            messagebox.showinfo("Results", "No votes yet.")
            return

        text = ""
        for c in candidates:
            text += f"{c.get_name()} - {c.get_vote_count()}\n"

        messagebox.showinfo("Results", text)