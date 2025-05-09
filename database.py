import sqlite3

class Database:
    def __init__(self, db_path="onboarding_tool.db"):
        self.db_path = db_path
        self._initialize_database()

    def _initialize_database(self):
        """Initialize the database with required tables."""
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                department TEXT,
                role TEXT,
                custom_attributes TEXT
            )
        ''')

        # Create logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                action TEXT NOT NULL,
                status TEXT NOT NULL,
                error_message TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create reports table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_data TEXT NOT NULL,
                generated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        connection.commit()
        connection.close()

    def insert_user(self, user_data):
        """Insert a user into the users table."""
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (first_name, last_name, email, department, role, custom_attributes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                user_data["First Name"],
                user_data["Last Name"],
                user_data["Email Address"],
                user_data.get("Department"),
                user_data.get("Role"),
                str(user_data.get("Custom Attributes", ""))
            ))
            connection.commit()
        except sqlite3.IntegrityError:
            pass  # Ignore duplicate entries
        finally:
            connection.close()

    def log_action(self, email, action, status, error_message=None):
        """Log an action to the logs table."""
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO logs (email, action, status, error_message)
            VALUES (?, ?, ?, ?)
        ''', (email, action, status, error_message))
        connection.commit()
        connection.close()

    def save_report(self, report_data):
        """Save a report to the reports table."""
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO reports (report_data)
            VALUES (?)
        ''', (report_data,))
        connection.commit()
        connection.close()
