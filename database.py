import sqlite3
from models.Voter import Voter
from models.Admin import Admin
from models.Candidate import Candidate
from models.Election import Election
from models.Party import Party


class DatabaseManager:
    def __init__(self, db_name="election_data.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.setup_tables()
        self.create_default_admin()

    def setup_tables(self):
        # 1. KULLANICILAR (Oy sütunları kaldırıldı, sadece kimlik bilgileri)
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS users
                            (
                                tc_no
                                TEXT
                                PRIMARY
                                KEY,
                                name
                                TEXT
                                NOT
                                NULL,
                                password
                                TEXT
                                NOT
                                NULL,
                                city
                                TEXT
                                NOT
                                NULL,
                                role
                                TEXT
                                DEFAULT
                                'voter'
                            )
                            ''')

        # 2. SEÇİMLER (YENİ)
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS elections
                            (
                                id
                                INTEGER
                                PRIMARY
                                KEY
                                AUTOINCREMENT,
                                title
                                TEXT
                                NOT
                                NULL,
                                status
                                TEXT
                                DEFAULT
                                'Active'
                            )
                            ''')

        # 3. KULLANICI OYLARI (YENİ - Kim hangi seçimde oy verdi?)
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS user_votes
                            (
                                tc_no
                                TEXT,
                                election_id
                                INTEGER,
                                has_voted_president
                                BOOLEAN
                                DEFAULT
                                0,
                                has_voted_mayor
                                BOOLEAN
                                DEFAULT
                                0,
                                PRIMARY
                                KEY
                            (
                                tc_no,
                                election_id
                            )
                                )
                            ''')

        # 4. ADAYLAR (Artık bir seçime bağlılar)
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS candidates
                            (
                                id
                                INTEGER
                                PRIMARY
                                KEY
                                AUTOINCREMENT,
                                election_id
                                INTEGER
                                NOT
                                NULL,
                                name
                                TEXT
                                NOT
                                NULL,
                                party
                                TEXT
                                NOT
                                NULL,
                                position
                                TEXT
                                NOT
                                NULL,
                                city
                                TEXT,
                                vote_count
                                INTEGER
                                DEFAULT
                                0
                            )
                            ''')

        # 5. PARTİLER
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS parties
                            (
                                id
                                INTEGER
                                PRIMARY
                                KEY
                                AUTOINCREMENT,
                                name
                                TEXT
                                NOT
                                NULL,
                                abbreviation
                                TEXT
                                NOT
                                NULL
                            )
                            ''')
        self.conn.commit()

        # Eğer hiç seçim yoksa varsayılan bir tane başlat
        self.cursor.execute("SELECT COUNT(*) FROM elections")
        if self.cursor.fetchone()[0] == 0:
            self.create_election("2026 General Elections")

    def create_default_admin(self):
        self.cursor.execute('''
                            INSERT
                            OR IGNORE INTO users (tc_no, name, password, city, role)
            VALUES ('12345678901', 'System Admin', 'admin123', 'Istanbul', 'admin')
                            ''')
        self.conn.commit()

    # --- SEÇİM (ELECTION) YÖNETİMİ ---
    def create_election(self, title):
        """Mevcut aktif seçimi bitirir ve yeni bir seçim başlatır."""
        self.cursor.execute("UPDATE elections SET status = 'Completed' WHERE status = 'Active'")
        self.cursor.execute("INSERT INTO elections (title, status) VALUES (?, 'Active')", (title,))
        self.conn.commit()

    def get_active_election(self):
        """Aktif seçimin ID, Başlık ve Durum bilgisini sözlük olarak döndürür."""
        self.cursor.execute("SELECT id, title, status FROM elections WHERE status = 'Active' ORDER BY id DESC LIMIT 1")
        row = self.cursor.fetchone()
        return {"id": row[0], "title": row[1], "status": row[2]} if row else None

    def end_election(self):
        """Aktif olan seçimi sonlandırır."""
        self.cursor.execute("UPDATE elections SET status = 'Completed' WHERE status = 'Active'")
        self.conn.commit()

    def is_election_active(self):
        return self.get_active_election() is not None

    def get_current_election_data(self):
        active = self.get_active_election()
        title = active["title"] if active else "No Active Election"
        election = Election(title)
        if active:
            election.set_candidates(self.get_all_candidates(active["id"]))
        return election

    # --- ADAY İŞLEMLERİ ---
    def add_candidate(self, candidate_obj):
        active = self.get_active_election()
        if not active: return False
        try:
            self.cursor.execute('''
                                INSERT INTO candidates (election_id, name, party, position, city, vote_count)
                                VALUES (?, ?, ?, ?, ?, 0)
                                ''', (active["id"], candidate_obj.get_name(), candidate_obj.get_party(),
                                      candidate_obj.get_position(), candidate_obj.get_city()))
            self.conn.commit()
            return True
        except:
            return False

    def get_all_candidates(self, election_id=None):
        """Parametre verilmezse sadece aktif seçimin adaylarını getirir."""
        if election_id is None:
            active = self.get_active_election()
            if not active: return []
            election_id = active["id"]

        self.cursor.execute("SELECT id, name, party, position, city, vote_count FROM candidates WHERE election_id = ?",
                            (election_id,))
        rows = self.cursor.fetchall()
        candidate_list = []
        for row in rows:
            c = Candidate(row[0], row[1], row[2], row[3], row[4])
            c._Candidate__vote_count = row[5]
            candidate_list.append(c)
        return candidate_list

    def update_candidate(self, c_id, name, party, position, city):
        try:
            self.cursor.execute('''
                                UPDATE candidates
                                SET name     = ?,
                                    party    = ?,
                                    position = ?,
                                    city     = ?
                                WHERE id = ?
                                ''', (name, party, position, city, c_id))
            self.conn.commit()
            return True
        except:
            return False

    def delete_candidate(self, candidate_id):
        try:
            self.cursor.execute("DELETE FROM candidates WHERE id = ?", (candidate_id,))
            self.conn.commit()
            return True
        except:
            return False

    # --- KULLANICI VE OY İŞLEMLERİ ---
    def authenticate_user(self, tc_no, password):
        self.cursor.execute("SELECT * FROM users WHERE tc_no = ? AND password = ?", (tc_no, password))
        row = self.cursor.fetchone()
        if row:
            user = Admin(row[0], row[1], row[2], row[3]) if row[4] == 'admin' else Voter(row[0], row[1], row[2], row[3])

            # YENİ MANTIK: Kullanıcının *aktif seçimde* oy kullanıp kullanmadığını kontrol et
            active = self.get_active_election()
            if active:
                self.cursor.execute(
                    "SELECT has_voted_president, has_voted_mayor FROM user_votes WHERE tc_no = ? AND election_id = ?",
                    (tc_no, active["id"]))
                vote_row = self.cursor.fetchone()
                if vote_row:
                    if vote_row[0]: user.mark_voted_president()
                    if vote_row[1]: user.mark_voted_mayor()
            return user
        return None

    def register_user(self, user_obj):
        try:
            self.cursor.execute('''
                                INSERT INTO users (tc_no, name, password, city, role)
                                VALUES (?, ?, ?, ?, 'voter')
                                ''', (user_obj.get_tc_no(), user_obj.get_name(), user_obj.get_password(),
                                      user_obj.get_city()))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def cast_vote(self, tc_no, candidate_id, election_type):
        active = self.get_active_election()
        if not active: return False
        try:
            self.cursor.execute("UPDATE candidates SET vote_count = vote_count + 1 WHERE id = ?", (candidate_id,))

            # Kullanıcı bu seçim için user_votes tablosunda var mı? Yoksa oluştur.
            self.cursor.execute("SELECT * FROM user_votes WHERE tc_no = ? AND election_id = ?", (tc_no, active["id"]))
            if not self.cursor.fetchone():
                self.cursor.execute(
                    "INSERT INTO user_votes (tc_no, election_id, has_voted_president, has_voted_mayor) VALUES (?, ?, 0, 0)",
                    (tc_no, active["id"]))

            # Oy durumunu güncelle
            col = "has_voted_president" if election_type == "President" else "has_voted_mayor"
            self.cursor.execute(f"UPDATE user_votes SET {col} = 1 WHERE tc_no = ? AND election_id = ?",
                                (tc_no, active["id"]))
            self.conn.commit()
            return True
        except:
            return False

    # --- PARTİ İŞLEMLERİ ---
    def add_party(self, party_obj):
        try:
            self.cursor.execute("INSERT INTO parties (name, abbreviation) VALUES (?, ?)",
                                (party_obj.get_name(), party_obj.get_abbreviation()))
            self.conn.commit()
            return True
        except:
            return False

    def get_all_parties(self):
        self.cursor.execute("SELECT * FROM parties")
        rows = self.cursor.fetchall()
        return [Party(row[0], row[1], row[2]) for row in rows]