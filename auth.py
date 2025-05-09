import sqlite3
import hashlib

class Auth:
    def __init__(self, db_path="onboarding_tool.db"):
        self.db_path = db_path
        self._initialize_auth_table()

    def _initialize_auth_table(self):
        """Initialize the authentication table."""
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')
        connection.commit()
        connection.close()

    def register_user(self, username, password, role):
        """Register a new user with a hashed password."""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (username, password_hash, role)
                VALUES (?, ?, ?)
            ''', (username, password_hash, role))
            connection.commit()
        except sqlite3.IntegrityError:
            raise Exception("Username already exists.")
        finally:
            connection.close()

    def authenticate_user(self, username, password):
        """Authenticate a user by verifying the password."""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute('''
            SELECT role FROM users WHERE username = ? AND password_hash = ?
        ''', (username, password_hash))
        result = cursor.fetchone()
        connection.close()
        if result:
            return result[0]  # Return the role
        else:
            raise Exception("Invalid username or password.")

if __name__ == "__main__":
    auth = Auth()
    try:
        auth.register_user(username="admin", password="admin123", role="Admin")
        print("Test admin user created successfully.")
    except Exception as e:
        print(f"Error creating test admin user: {e}")
