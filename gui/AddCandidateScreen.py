import tkinter as tk
from tkinter import messagebox, ttk
from models.Candidate import Candidate

CITIES = ["Ankara", "Istanbul", "Izmir", "Bursa", "Antalya", "Adana", "Konya"]


class AddCandidateScreen:
    def __init__(self, parent, db_manager):
        self.window = tk.Toplevel(parent)
        self.db = db_manager

        self.window.title("Admin - Add New Candidate")
        self.window.geometry("400x600")
        self.window.configure(bg="#F4F7F6")

        # Ekranı ortala
        self.window.transient(parent)
        self.window.grab_set()

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.window, text="Add New Candidate", font=("Arial", 16, "bold"),
                 bg="#F4F7F6", fg="#C8963E").pack(pady=20)

        container = tk.Frame(self.window, bg="#F4F7F6")
        container.pack(padx=40, fill="both")

        # 1. İsim
        tk.Label(container, text="Candidate Full Name:", bg="#F4F7F6").pack(anchor="w")
        self.name_entry = tk.Entry(container, font=("Arial", 11))
        self.name_entry.pack(fill="x", pady=(0, 15))

        # 2. Parti (Veritabanından çekilen partiler)
        tk.Label(container, text="Affiliated Party:", bg="#F4F7F6").pack(anchor="w")
        parties = [p.get_name() for p in self.db.get_all_parties()]
        self.party_combo = ttk.Combobox(container, values=parties, state="readonly", font=("Arial", 10))
        if parties: self.party_combo.current(0)
        self.party_combo.pack(fill="x", pady=(0, 15))

        # 3. Pozisyon (President / Mayor)
        tk.Label(container, text="Running For Position:", bg="#F4F7F6").pack(anchor="w")
        self.pos_combo = ttk.Combobox(container, values=["President", "Mayor"], state="readonly", font=("Arial", 10))
        self.pos_combo.set("President")
        self.pos_combo.pack(fill="x", pady=(0, 15))

        # 4. Şehir (Belediye başkanlığı seçilirse önemli)
        tk.Label(container, text="City (Mandatory for Mayor):", bg="#F4F7F6").pack(anchor="w")
        self.city_combo = ttk.Combobox(container, values=CITIES, state="readonly", font=("Arial", 10))
        self.city_combo.set("Ankara")
        self.city_combo.pack(fill="x", pady=(0, 25))

        # Kaydet Butonu
        tk.Button(self.window, text="SAVE CANDIDATE", bg="#2C6B4F", fg="white",
                  font=("Arial", 11, "bold"), command=self.save_candidate, pady=10).pack(fill="x", padx=40)

    def save_candidate(self):
        name = self.name_entry.get().strip()
        party = self.party_combo.get()
        position = self.pos_combo.get()
        city = self.city_combo.get()

        if not name or not party:
            messagebox.showerror("Error", "Please fill name and select a party!")
            return

        # Cumhurbaşkanı adayları için şehri "National" (Tüm Ülke) yapabiliriz
        # ya da seçili şehri bırakabiliriz (görünümde fark etmez ama database temiz kalır)
        final_city = "National" if position == "President" else city

        # ID'yi DB otomatik vereceği için 0 (geçici) gönderiyoruz
        new_candidate = Candidate(0, name, party, position, final_city)

        if self.db.add_candidate(new_candidate):
            messagebox.showinfo("Success", f"{name} has been added as a {position} candidate.")
            self.window.destroy()
        else:
            messagebox.showerror("Error", "Could not add candidate.")