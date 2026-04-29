import tkinter as tk
from tkinter import messagebox

BG = "#EAECF0"
CARD_BG = "#FFFFFF"
ACCENT = "#1A3A5C"
TEXT_SEC = "#6E6E73"
BORDER = "#C8C8CC"
SUCCESS = "#34C759"
FONT = "Arial"


class BallotScreen:
    def __init__(self, parent, db, user):
        self.window = tk.Toplevel(parent)
        self.db = db
        self.user = user

        self.window.title("Ballot")
        self.window.geometry("450x500")

        self.selected = tk.IntVar(value=0)
        self.rows = {}

        self.setup_ui()

    def setup_ui(self):
        self.candidates = self.db.get_all_candidates()

        for c in self.candidates:
            self.row(c)

        tk.Button(self.window, text="Submit",
                  bg=SUCCESS, fg="white",
                  command=self.submit).pack(pady=10)

    def row(self, c):
        cid = c.get_candidate_id()

        frame = tk.Frame(self.window, bg=CARD_BG,
                         highlightthickness=1,
                         highlightbackground=BORDER)
        frame.pack(fill="x", pady=5)

        tk.Radiobutton(frame, variable=self.selected,
                       value=cid,
                       bg=CARD_BG).pack(side="left")

        text = f"{c.get_name()} - {c.get_party()}"

        tk.Label(frame, text=text,
                 bg=CARD_BG).pack(side="left")

    def submit(self):
        cid = self.selected.get()

        if cid == 0:
            messagebox.showwarning("Warning", "Select candidate")
            return

        c = next((x for x in self.candidates
                  if x.get_candidate_id() == cid), None)

        if c is None:
            return

        self.db.cast_vote(self.user.get_tc_no(), cid, c.get_position())
        messagebox.showinfo("Success", "Vote saved")
        self.window.destroy()