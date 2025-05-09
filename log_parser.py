import sqlite3

class LogParser:
    def __init__(self, db_path="onboarding_tool.db"):
        self.db_path = db_path

    def fetch_logs(self, email=None, action=None, status=None, start_date=None, end_date=None):
        """Fetch logs from the database with optional filters."""
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        query = "SELECT * FROM logs WHERE 1=1"
        params = []

        if email:
            query += " AND email = ?"
            params.append(email)

        if action:
            query += " AND action = ?"
            params.append(action)

        if status:
            query += " AND status = ?"
            params.append(status)

        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date)

        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date)

        cursor.execute(query, params)
        logs = cursor.fetchall()
        connection.close()

        return logs

    def display_logs(self, logs):
        """Display logs in a readable format."""
        for log in logs:
            print(f"ID: {log[0]} | Email: {log[1]} | Action: {log[2]} | Status: {log[3]} | Error: {log[4]} | Timestamp: {log[5]}")
