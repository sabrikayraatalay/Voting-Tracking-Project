import tkinter as tk
from tkinter import ttk


class ResultScreen:
    def __init__(self, parent, db_manager):
        self.window = tk.Toplevel(parent)
        self.db = db_manager

        self.window.title("Election Results")
        self.window.geometry("500x400")
        self.window.configure(bg="#EAECF0")

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.window, text="Current Live Results", font=("Arial", 16, "bold"), bg="#EAECF0").pack(pady=15)

        # Tablo oluşturma (Treeview)
        columns = ("Name", "Party", "Position", "Votes")
        self.tree = ttk.Treeview(self.window, columns=columns, show="headings", height=12)

        self.tree.heading("Name", text="Candidate Name")
        self.tree.heading("Party", text="Party")
        self.tree.heading("Position", text="Position")
        self.tree.heading("Votes", text="Votes")

        self.tree.column("Name", width=150)
        self.tree.column("Party", width=100)
        self.tree.column("Position", width=100)
        self.tree.column("Votes", width=80, anchor="center")

        self.tree.pack(pady=10, padx=20, fill="x")

        self.load_results()

    def load_results(self):
        candidates = self.db.get_all_candidates()

        # Oyları büyükten küçüğe sıralayalım ki daha şık dursun
        candidates.sort(key=lambda c: c.get_vote_count(), reverse=True)

        for c in candidates:
            self.tree.insert("", "end", values=(c.get_name(), c.get_party(), c.get_position(), c.get_vote_count()))