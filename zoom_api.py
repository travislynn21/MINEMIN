import requests

class ZoomAPI:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.zoom.us/v2"

    def _headers(self):
        return {
            "Authorization": f"Bearer {self._generate_jwt_token()}",
            "Content-Type": "application/json"
        }

    def _generate_jwt_token(self):
        """Generate a JWT token for Zoom API authentication."""
        import jwt
        import time

        payload = {
            "iss": self.api_key,
            "exp": time.time() + 3600
        }
        token = jwt.encode(payload, self.api_secret, algorithm="HS256")
        return token

    def create_user(self, user_data):
        """Create a user in Zoom."""
        try:
            url = f"{self.base_url}/users"
            payload = {
                "action": "create",
                "user_info": {
                    "email": user_data["Email Address"],
                    "type": 1,
                    "first_name": user_data["First Name"],
                    "last_name": user_data["Last Name"]
                }
            }
            response = requests.post(url, json=payload, headers=self._headers())
            if response.status_code == 201:
                return {"status": "success", "email": user_data["Email Address"]}
            else:
                return {"status": "failure", "email": user_data["Email Address"], "error": response.json().get("message")}
        except Exception as e:
            return {"status": "failure", "email": user_data["Email Address"], "error": str(e)}

    def delete_user(self, email):
        """Delete a user in Zoom."""
        try:
            url = f"{self.base_url}/users/{email}"
            response = requests.delete(url, headers=self._headers())
            if response.status_code == 204:
                return {"status": "success", "email": email}
            else:
                return {"status": "failure", "email": email, "error": response.json().get("message")}
        except Exception as e:
            return {"status": "failure", "email": email, "error": str(e)}
