import tkinter as tk
from tkinter import messagebox
from models.Candidate import Candidate

BG = "#EAECF0"
FONT = "Arial"


class AddCandidateScreen:
    def __init__(self, parent, db):
        self.window = tk.Toplevel(parent)
        self.db = db

        self.window.title("Add Candidate")
        self.window.geometry("400x350")

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.window, text="Name").pack()
        self.name = tk.Entry(self.window)
        self.name.pack()

        tk.Label(self.window, text="Party").pack()
        self.party = tk.Entry(self.window)
        self.party.pack()

        tk.Button(self.window, text="Save",
                  command=self.save).pack(pady=10)

    def save(self):
        name = self.name.get()
        party = self.party.get()

        if not name or not party:
            messagebox.showwarning("Error", "Fill fields")
            return

        c = Candidate(None, name, party, "President")
        self.db.add_candidate(c)

        messagebox.showinfo("OK", "Saved")
        self.window.destroy()