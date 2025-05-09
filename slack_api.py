import requests

class SlackAPI:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://slack.com/api"

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def create_user(self, user_data):
        """Invite a user to a Slack workspace."""
        try:
            url = f"{self.base_url}/users.admin.invite"
            payload = {
                "email": user_data["Email Address"],
                "real_name": f"{user_data['First Name']} {user_data['Last Name']}",
                "resend": True
            }
            response = requests.post(url, json=payload, headers=self._headers())
            if response.status_code == 200 and response.json().get("ok"):
                return {"status": "success", "email": user_data["Email Address"]}
            else:
                return {"status": "failure", "email": user_data["Email Address"], "error": response.json().get("error")}
        except Exception as e:
            return {"status": "failure", "email": user_data["Email Address"], "error": str(e)}

    def deactivate_user(self, email):
        """Deactivate a user in Slack."""
        try:
            # Slack API does not directly support deactivating users via API.
            # This would require admin intervention or a third-party tool.
            return {"status": "failure", "email": email, "error": "Deactivation not supported via API"}
        except Exception as e:
            return {"status": "failure", "email": email, "error": str(e)}
