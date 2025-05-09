import csv

class CSVParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_user_data(self):
        """Reads user data from the CSV file and returns a list of dictionaries."""
        try:
            with open(self.file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                users = [row for row in reader]
                return users
        except FileNotFoundError:
            raise Exception(f"File not found: {self.file_path}")
        except Exception as e:
            raise Exception(f"Error reading CSV file: {e}")
