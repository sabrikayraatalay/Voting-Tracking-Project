import tkinter as tk
from tkinter import messagebox
from models.Party import Party

BG = "#EAECF0"
ACCENT = "#1A3A5C"
FONT = "Arial"


class AddPartyScreen:
    def __init__(self, parent, db):
        self.window = tk.Toplevel(parent)
        self.db = db
        self.window.title("Add New Party")
        self.window.geometry("350x300")
        self.window.configure(bg=BG)

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.window, text="Create New Party", font=(FONT, 14, "bold"), bg=BG).pack(pady=20)

        tk.Label(self.window, text="Party Name:", bg=BG).pack()
        self.name_entry = tk.Entry(self.window)
        self.name_entry.pack(pady=5)

        tk.Label(self.window, text="Abbreviation (e.g. ALP):", bg=BG).pack()
        self.abbr_entry = tk.Entry(self.window)
        self.abbr_entry.pack(pady=5)

        tk.Button(self.window, text="Save Party", bg=ACCENT, fg="white",
                  command=self.save_party).pack(pady=20)

    def save_party(self):
        name = self.name_entry.get().strip()
        abbr = self.abbr_entry.get().strip().upper()

        if name and abbr:
            new_party = Party(None, name, abbr)
            if self.db.add_party(new_party):
                messagebox.showinfo("Success", f"{name} added successfully!")
                self.window.destroy()
            else:
                messagebox.showerror("Error", "Could not save party.")
        else:
            messagebox.showwarning("Warning", "Fill all fields!")