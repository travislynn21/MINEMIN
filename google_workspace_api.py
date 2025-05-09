from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

class GoogleWorkspaceAPI:
    def __init__(self, credentials_file):
        self.credentials_file = credentials_file
        self.service = self._authenticate()

    def _authenticate(self):
        """Authenticate with Google Workspace using a service account."""
        try:
            credentials = Credentials.from_service_account_file(
                self.credentials_file,
                scopes=[
                    'https://www.googleapis.com/auth/admin.directory.user',
                    'https://www.googleapis.com/auth/admin.directory.group'
                ]
            )
            service = build('admin', 'directory_v1', credentials=credentials)
            return service
        except Exception as e:
            raise Exception(f"Error authenticating with Google Workspace: {e}")

    def create_user(self, user_data):
        """Create a user in Google Workspace."""
        try:
            user_body = {
                "name": {
                    "givenName": user_data["First Name"],
                    "familyName": user_data["Last Name"]
                },
                "password": "TemporaryPassword123",  # Replace with a secure method
                "primaryEmail": user_data["Email Address"]
            }
            self.service.users().insert(body=user_body).execute()
            return {"status": "success", "email": user_data["Email Address"]}
        except Exception as e:
            return {"status": "failure", "email": user_data["Email Address"], "error": str(e)}

    def delete_user(self, email):
        """Delete a user in Google Workspace."""
        try:
            self.service.users().delete(userKey=email).execute()
            return {"status": "success", "email": email}
        except Exception as e:
            return {"status": "failure", "email": email, "error": str(e)}
