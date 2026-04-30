import tkinter as tk
from tkinter import messagebox, ttk
from models.Admin import Admin

# Sistem genelindeki şehir listesi (Tutarlılık için)
CITIES = ["Ankara", "Istanbul", "Izmir", "Bursa", "Antalya", "Adana", "Konya"]


class CandidateListScreen:
    def __init__(self, parent, db, user):
        self.window = tk.Toplevel(parent)
        self.db = db
        self.user = user

        self.window.title("Candidate Management System")
        self.window.geometry("750x550")
        self.window.configure(bg="#EAECF0")

        # Ekranı ortala
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        w, h = 750, 550
        self.window.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

        # Dashboard'un üstünde kalsın
        self.window.transient(parent)
        self.window.grab_set()

        self.setup_ui()

    def setup_ui(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        # Üst Panel
        header = tk.Frame(self.window, bg="#1A3A5C", pady=15)
        header.pack(fill="x")
        tk.Label(header, text="Candidate List & Management", font=("Arial", 16, "bold"),
                 fg="white", bg="#1A3A5C").pack()

        # Kaydırma Alanı (Scrollbar)
        main_frame = tk.Frame(self.window, bg="#EAECF0")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        canvas = tk.Canvas(main_frame, bg="#EAECF0", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="#EAECF0")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.load_candidates()

    def load_candidates(self):
        candidates = self.db.get_all_candidates()

        if not candidates:
            tk.Label(self.scrollable_frame, text="No registered candidates found.",
                     font=("Arial", 11, "italic"), bg="#EAECF0").pack(pady=20)
            return

        for c in candidates:
            card = tk.Frame(self.scrollable_frame, bg="white", bd=1, relief="solid", highlightbackground="#C8C8CC")
            card.pack(fill="x", pady=5, padx=10, ipady=10)

            # Bilgiler
            info = f"👤 {c.get_name()}\n🏢 Party: {c.get_party()} | 📍 {c.get_position()} ({c.get_city()})"
            tk.Label(card, text=info, font=("Arial", 11), bg="white", justify="left", anchor="w").pack(side="left",
                                                                                                       padx=15)

            # Sadece Admin Yetkileri
            if isinstance(self.user, Admin):
                btn_frame = tk.Frame(card, bg="white")
                btn_frame.pack(side="right", padx=15)

                # DÜZENLE (Edit) - Hata giderilmiş buton
                tk.Button(btn_frame, text="✏️ Edit", bg="#C8963E", fg="white", font=("Arial", 9, "bold"),
                          command=lambda obj=c: self.open_edit_window(obj), width=8, cursor="hand2").pack(side="left",
                                                                                                          padx=5)

                # SİL (Delete)
                tk.Button(btn_frame, text="🗑️ Delete", bg="#D32F2F", fg="white", font=("Arial", 9, "bold"),
                          command=lambda cid=c.get_candidate_id(): self.delete_confirm(cid), width=8,
                          cursor="hand2").pack(side="left", padx=5)

    def delete_confirm(self, cid):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this candidate?"):
            if self.db.delete_candidate(cid):
                messagebox.showinfo("Success", "Candidate deleted.")
                self.setup_ui()

    def open_edit_window(self, candidate):
        edit_win = tk.Toplevel(self.window)
        edit_win.title(f"Edit: {candidate.get_name()}")
        edit_win.geometry("350x450")
        edit_win.configure(bg="white")

        # Alt pencereyi kilitle (Modal)
        edit_win.transient(self.window)
        edit_win.grab_set()

        tk.Label(edit_win, text="Update Candidate", font=("Arial", 12, "bold"), bg="white").pack(pady=15)

        # İsim Girişi
        tk.Label(edit_win, text="Full Name:", bg="white").pack(anchor="w", padx=40)
        name_entry = tk.Entry(edit_win, font=("Arial", 11))
        name_entry.insert(0, candidate.get_name())
        name_entry.pack(fill="x", padx=40, pady=5)

        # Şehir Seçimi
        tk.Label(edit_win, text="City:", bg="white").pack(anchor="w", padx=40)
        city_combo = ttk.Combobox(edit_win, values=CITIES, state="readonly")

        # Hatanın (TclError) çözüldüğü kısım: current() kullanımı
        try:
            current_idx = CITIES.index(candidate.get_city())
            city_combo.current(current_idx)
        except (ValueError, IndexError):
            city_combo.set(candidate.get_city())  # Listedışı ise (National vb.) manuel set

        city_combo.pack(fill="x", padx=40, pady=5)

        def save_changes():
            new_name = name_entry.get().strip()
            new_city = city_combo.get()

            if not new_name:
                messagebox.showerror("Error", "Name is required!")
                return

            # DB Update
            if self.db.update_candidate(candidate.get_candidate_id(), new_name,
                                        candidate.get_party(), candidate.get_position(), new_city):
                messagebox.showinfo("Success", "Candidate updated successfully!")
                edit_win.destroy()
                self.setup_ui()  # Listeyi yenile
            else:
                messagebox.showerror("Error", "Update failed.")

        tk.Button(edit_win, text="SAVE CHANGES", bg="#2C6B4F", fg="white", font=("Arial", 10, "bold"),
                  command=save_changes, pady=10, cursor="hand2").pack(fill="x", padx=40, pady=30)