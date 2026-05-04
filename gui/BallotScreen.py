import tkinter as tk
from tkinter import messagebox


class BallotScreen:
    def __init__(self, parent, db, user, election_type):
        self.window = tk.Toplevel(parent)
        self.db = db
        self.user = user
        self.election_type = election_type

        self.window.title(f"Voting: {election_type}")
        self.window.geometry("500x600")
        self.window.configure(bg="#F4F7F9")

        # Ekranı ortala
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        w, h = 500, 600
        self.window.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

        # Modal yap: Bu pencere kapanmadan arkadaki dashboard'a tıklanamasın
        self.window.transient(parent)
        self.window.grab_set()

        self.setup_ui()

    def setup_ui(self):
        # Başlık
        tk.Label(self.window, text=f"{self.election_type} Ballot",
                 font=("Arial", 18, "bold"), bg="#F4F7F9", fg="#1A3A5C").pack(pady=20)

        # Aday Listesi Alanı
        list_frame = tk.Frame(self.window, bg="#F4F7F9")
        list_frame.pack(fill="both", expand=True, padx=30)

        # Sadece ilgili seçim türündeki ve (belediye ise) ilgili şehirdeki adayları getir
        all_candidates = self.db.get_all_candidates()

        filtered_candidates = [
            c for c in all_candidates
            if c.get_position() == self.election_type and
               (self.election_type == "President" or c.get_city() == self.user.get_city())
        ]

        if not filtered_candidates:
            tk.Label(list_frame, text="No candidates found for your region.",
                     bg="#F4F7F9", font=("Arial", 11, "italic")).pack(pady=20)

        self.var = tk.IntVar()  # Seçilen adayın ID'sini tutmak için
        self.var.set(0)  # Başlangıçta hiçbir aday seçili olmasın

        # Adayları Radiobutton (tekli seçim) olarak listele
        for c in filtered_candidates:
            rb = tk.Radiobutton(list_frame,
                                text=f"{c.get_name()} ({c.get_party()})",
                                variable=self.var,
                                value=c.get_candidate_id(),
                                font=("Arial", 12),
                                bg="#F4F7F9",
                                cursor="hand2",
                                pady=10)
            rb.pack(anchor="w")

        # OY VER BUTONU
        vote_btn = tk.Button(self.window, text="CONFIRM & CAST VOTE",
                             bg="#2C6B4F", fg="white", font=("Arial", 12, "bold"),
                             command=self.cast_vote_action, pady=15, cursor="hand2")
        vote_btn.pack(fill="x", padx=50, pady=30)

    def cast_vote_action(self):
        candidate_id = self.var.get()

        # Eğer hiç seçim yapılmadıysa uyar ve işlemi durdur
        if candidate_id == 0:
            messagebox.showwarning("Warning", "Please select a candidate before confirming!")
            return

        # Son onay
        if messagebox.askyesno("Final Confirm", "Are you sure? You cannot change your vote later!"):

            # Veritabanında oyu kaydet
            success = self.db.cast_vote(self.user.get_tc_no(), candidate_id, self.election_type)

            if success:
                messagebox.showinfo("Success", "Your vote has been cast securely!")

                # KRİTİK NOKTA: Kullanıcının aktif oturumdaki oy durumunu
                # SADECE işlem başarıyla veritabanına işlendiyse güncelle.
                if self.election_type == "President":
                    self.user.mark_voted_president()
                else:
                    self.user.mark_voted_mayor()

                self.window.destroy()  # Pencereyi kapat (Dashboard otomatik güncellenecek)
            else:
                messagebox.showerror("Error", "Something went wrong while saving your vote.")