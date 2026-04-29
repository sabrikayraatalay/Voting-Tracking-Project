import sqlite3
from models.Voter import Voter
from models.Admin import Admin
from models.Candidate import Candidate

class DatabaseManager:
    # Initialize the database connection and create tables if they don't exist
    def __init__(self, db_name="election_data.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.setup_tables()
        self.create_default_admin()

    def setup_tables(self):
        # Create Users table for both Voters and Admins (Inheritance applied in DB logic)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                tc_no TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                password TEXT NOT NULL,
                city TEXT NOT NULL,
                role TEXT DEFAULT 'voter',
                has_voted_president BOOLEAN DEFAULT 0,
                has_voted_mayor BOOLEAN DEFAULT 0
            )
        ''')

        # Create Candidates table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                party TEXT NOT NULL,
                position TEXT NOT NULL,
                city TEXT,
                vote_count INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def create_default_admin(self):
        # Insert a default admin account so you can log in the first time
        # We use IGNORE to prevent errors if the admin already exists
        self.cursor.execute('''
            INSERT OR IGNORE INTO users (tc_no, name, password, city, role)
            VALUES ('12345678901', 'System Admin', 'admin123', 'Istanbul', 'admin')
        ''')
        self.conn.commit()

    # --- USER AUTHENTICATION & REGISTRATION ---

    def register_user(self, user_obj):
        # Check if the user is an Admin or a Voter to assign the correct role
        role = 'admin' if isinstance(user_obj, Admin) else 'voter'

        try:
            self.cursor.execute('''
                INSERT INTO users (tc_no, name, password, city, role)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_obj.get_tc_no(), user_obj.get_name(), user_obj.get_password(), user_obj.get_city(), role))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Returns False if TC number already exists
            return False

    def authenticate_user(self, tc_no, password):
        # Fetch user data based on credentials
        self.cursor.execute("SELECT * FROM users WHERE tc_no = ? AND password = ?", (tc_no, password))
        row = self.cursor.fetchone()

        if row:
            # row: (tc_no, name, password, city, role, voted_pres, voted_mayor)
            if row[4] == 'admin':
                user = Admin(row[0], row[1], row[2], row[3])
            else:
                user = Voter(row[0], row[1], row[2], row[3])

            # Restore voting status
            if row[5]: user.mark_voted_president()
            if row[6]: user.mark_voted_mayor()

            return user
        return None

    # --- CANDIDATE MANAGEMENT ---

    def add_candidate(self, candidate_obj):
        self.cursor.execute('''
            INSERT INTO candidates (name, party, position, city)
            VALUES (?, ?, ?, ?)
        ''', (candidate_obj.get_name(), candidate_obj.get_party(), candidate_obj.get_position(),
              candidate_obj.get_city()))
        self.conn.commit()

    def get_all_candidates(self):
        self.cursor.execute("SELECT * FROM candidates")
        rows = self.cursor.fetchall()

        candidate_list = []
        for row in rows:
            # row: (id, name, party, position, city, vote_count)
            c = Candidate(row[0], row[1], row[2], row[3], row[4])
            # Set the current vote count using a loop directly or a setter if we add one,
            # for now we'll do it safely by calling add_vote multiple times or adding a set_vote_count method in Model
            c._Candidate__vote_count = row[5]  # Direct access for DB recreation (acceptable practice for ORMs)
            candidate_list.append(c)
        return candidate_list

    def delete_candidate(self, candidate_id):
        self.cursor.execute("DELETE FROM candidates WHERE id = ?", (candidate_id,))
        self.conn.commit()

    # --- VOTING LOGIC ---

    def cast_vote(self, tc_no, candidate_id, position):
        # 1. Update Candidate vote count
        self.cursor.execute("UPDATE candidates SET vote_count = vote_count + 1 WHERE id = ?", (candidate_id,))

        # 2. Update User voting status
        if position.lower() == 'president':
            self.cursor.execute("UPDATE users SET has_voted_president = 1 WHERE tc_no = ?", (tc_no,))
        elif position.lower() == 'mayor':
            self.cursor.execute("UPDATE users SET has_voted_mayor = 1 WHERE tc_no = ?", (tc_no,))

        self.conn.commit()

    def close_connection(self):
        # Always good practice to close DB connection when exiting the application
        self.conn.close()