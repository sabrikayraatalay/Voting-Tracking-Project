import tkinter as tk
from tkinter import messagebox, ttk
from models.Admin import Admin

# Tasarım Sabitleri
BG = "#EAECF0"
SIDEBAR_BG = "#FFFFFF"
HEADER_BG = "#1A3A5C"
ACCENT = "#C8963E"
GREEN = "#2C6B4F"


class PartyListScreen:
    def __init__(self, parent, db, user):
        self.window = tk.Toplevel(parent)
        self.db = db
        self.user = user

        self.window.title("Party & Candidate Management")
        self.window.geometry("900x600")
        self.window.configure(bg=BG)

        # Ekranı ortala
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        w, h = 900, 600
        self.window.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

        self.window.transient(parent)
        self.window.grab_set()

        self.setup_ui()

    def setup_ui(self):
        # Üst Başlık
        header = tk.Frame(self.window, bg=HEADER_BG, pady=15)
        header.pack(fill="x")
        tk.Label(header, text="Political Party Management", font=("Arial", 16, "bold"),
                 fg="white", bg=HEADER_BG).pack()

        # Ana Gövde (İki Panel)
        self.main_container = tk.PanedWindow(self.window, orient="horizontal", bg=BG, sashwidth=4)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # SOL PANEL: Parti Listesi
        self.left_panel = tk.Frame(self.main_container, bg=SIDEBAR_BG, width=400)
        self.main_container.add(self.left_panel)

        tk.Label(self.left_panel, text="Parties", font=("Arial", 12, "bold"), bg=SIDEBAR_BG).pack(pady=10)

        # Scrollable Alan
        canvas = tk.Canvas(self.left_panel, bg=SIDEBAR_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.left_panel, orient="vertical", command=canvas.yview)
        self.party_list_frame = tk.Frame(canvas, bg=SIDEBAR_BG)

        self.party_list_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.party_list_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # SAĞ PANEL: Aday Detayları
        self.right_panel = tk.Frame(self.main_container, bg=BG)
        self.main_container.add(self.right_panel)

        self.candidate_info_label = tk.Label(self.right_panel, text="Select a party to see candidates",
                                             font=("Arial", 11, "italic"), bg=BG, pady=100)
        self.candidate_info_label.pack()

        self.load_parties()

    def load_parties(self):
        # Listeyi temizle
        for widget in self.party_list_frame.winfo_children():
            widget.destroy()

        parties = self.db.get_all_parties()
        if not parties:
            tk.Label(self.party_list_frame, text="No parties found.", bg=SIDEBAR_BG).pack(pady=20)
            return

        for p in parties:
            frame = tk.Frame(self.party_list_frame, bg="white", bd=1, relief="groove")
            frame.pack(fill="x", padx=10, pady=5, ipady=5)

            # Parti Bilgisi (Tıklanabilir)
            lbl_text = f"{p.get_name()} ({p.get_abbreviation()})"
            btn_info = tk.Button(frame, text=lbl_text, font=("Arial", 10, "bold"), anchor="w",
                                 relief="flat", bg="white", cursor="hand2",
                                 command=lambda party=p: self.show_candidates(party))
            btn_info.pack(side="left", fill="x", expand=True, padx=10)

            # Admin Kontrolleri
            if isinstance(self.user, Admin):
                ctrl_frame = tk.Frame(frame, bg="white")
                ctrl_frame.pack(side="right", padx=5)

                tk.Button(ctrl_frame, text="✏️", bg="#F0F0F0",
                          command=lambda party=p: self.edit_party_window(party)).pack(side="left", padx=2)
                tk.Button(ctrl_frame, text="🗑️", bg="#F0F0F0", fg="red",
                          command=lambda party=p: self.delete_party_confirm(party)).pack(side="left", padx=2)

    def show_candidates(self, party):
        # Sağ paneli temizle
        for widget in self.right_panel.winfo_children():
            widget.destroy()

        tk.Label(self.right_panel, text=f"Candidates of {party.get_name()}",
                 font=("Arial", 13, "bold"), bg=BG, pady=15).pack()

        all_candidates = self.db.get_all_candidates()
        party_candidates = [c for c in all_candidates if c.get_party() == party.get_name()]

        if not party_candidates:
            tk.Label(self.right_panel, text="No candidates registered for this party.", bg=BG).pack(pady=50)
            return

        # Aday Listesi Tablosu
        cols = ("Name", "Position", "City")
        tree = ttk.Treeview(self.right_panel, columns=cols, show="headings", height=15)
        tree.heading("Name", text="Candidate Name")
        tree.heading("Position", text="Position")
        tree.heading("City", text="City/Scope")

        tree.column("Name", width=150)
        tree.column("Position", width=100)
        tree.column("City", width=100)

        for c in party_candidates:
            city_display = c.get_city() if c.get_city() else "National"
            tree.insert("", "end", values=(c.get_name(), c.get_position(), city_display))

        tree.pack(fill="both", expand=True, padx=20, pady=10)

    def delete_party_confirm(self, party):
        msg = f"Are you sure you want to delete {party.get_name()}?\nThis will not delete candidates but they will be party-less."
        if messagebox.askyesno("Confirm Delete", msg):
            # database.py içinde delete_party metodun olduğunu varsayıyorum
            if self.db.delete_party(party.get_party_id()):
                messagebox.showinfo("Success", "Party deleted.")
                self.load_parties()

    def edit_party_window(self, party):
        edit_win = tk.Toplevel(self.window)
        edit_win.title("Edit Party")
        edit_win.geometry("300x250")

        tk.Label(edit_win, text="Party Name:").pack(pady=(20, 0))
        name_entry = tk.Entry(edit_win)
        name_entry.insert(0, party.get_name())
        name_entry.pack(pady=5)

        tk.Label(edit_win, text="Abbreviation:").pack()
        abbr_entry = tk.Entry(edit_win)
        abbr_entry.insert(0, party.get_abbreviation())
        abbr_entry.pack(pady=5)

        def save():
            new_name = name_entry.get().strip()
            new_abbr = abbr_entry.get().strip()
            if new_name and new_abbr:
                # database.py içinde update_party metodun olduğunu varsayıyorum
                if self.db.update_party(party.get_party_id(), new_name, new_abbr):
                    messagebox.showinfo("Success", "Party updated!")
                    edit_win.destroy()
                    self.load_parties()
            else:
                messagebox.showerror("Error", "Fields cannot be empty!")

        tk.Button(edit_win, text="Update", bg=GREEN, fg="white", command=save).pack(pady=20)