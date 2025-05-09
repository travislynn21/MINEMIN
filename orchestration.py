from csv_parser import CSVParser
from google_workspace_api import GoogleWorkspaceAPI
from slack_api import SlackAPI
from zoom_api import ZoomAPI
from database import Database
from workflows import Workflows
from notifications import Notifications

class Orchestration:
    def __init__(self, csv_file, google_credentials, slack_token, zoom_api_key, zoom_api_secret, smtp_config, slack_webhook_url):
        self.csv_parser = CSVParser(csv_file)
        self.google_api = GoogleWorkspaceAPI(google_credentials)
        self.slack_api = SlackAPI(slack_token)
        self.zoom_api = ZoomAPI(zoom_api_key, zoom_api_secret)
        self.database = Database()
        self.workflows = Workflows()
        self.notifications = Notifications(
            smtp_server=smtp_config['server'],
            smtp_port=smtp_config['port'],
            smtp_user=smtp_config['user'],
            smtp_password=smtp_config['password'],
            slack_webhook_url=slack_webhook_url
        )

    def onboard_users(self):
        """Onboard users by creating accounts in all SaaS applications based on workflows."""
        users = self.csv_parser.read_user_data()
        report = []

        for user in users:
            self.database.insert_user(user)  # Save user to database

            department = user.get("Department", "General")
            workflow = self.workflows.get_workflow(department, "onboard")

            google_result = slack_result = zoom_result = None

            if "google" in workflow:
                google_result = self.google_api.create_user(user)
                self.database.log_action(user["Email Address"], "onboard_google", google_result["status"], google_result.get("error"))

            if "slack" in workflow:
                slack_result = self.slack_api.create_user(user)
                self.database.log_action(user["Email Address"], "onboard_slack", slack_result["status"], slack_result.get("error"))

            if "zoom" in workflow:
                zoom_result = self.zoom_api.create_user(user)
                self.database.log_action(user["Email Address"], "onboard_zoom", zoom_result["status"], zoom_result.get("error"))

            # Send notifications
            if google_result and google_result["status"] == "success":
                self.notifications.send_email(
                    recipient=user["Email Address"],
                    subject="Welcome to the Company",
                    body="Your Google Workspace account has been created."
                )

            self.notifications.send_slack_message(
                message=f"Onboarding completed for {user['Email Address']} in department {department}."
            )

            report.append({
                "email": user["Email Address"],
                "google": google_result,
                "slack": slack_result,
                "zoom": zoom_result
            })

        return report

    def offboard_users(self):
        """Offboard users by deleting accounts in all SaaS applications based on workflows."""
        users = self.csv_parser.read_user_data()
        report = []

        for user in users:
            department = user.get("Department", "General")
            workflow = self.workflows.get_workflow(department, "offboard")

            google_result = slack_result = zoom_result = None

            if "google" in workflow:
                google_result = self.google_api.delete_user(user["Email Address"])
                self.database.log_action(user["Email Address"], "offboard_google", google_result["status"], google_result.get("error"))

            if "slack" in workflow:
                slack_result = self.slack_api.deactivate_user(user["Email Address"])
                self.database.log_action(user["Email Address"], "offboard_slack", slack_result["status"], slack_result.get("error"))

            if "zoom" in workflow:
                zoom_result = self.zoom_api.delete_user(user["Email Address"])
                self.database.log_action(user["Email Address"], "offboard_zoom", zoom_result["status"], zoom_result.get("error"))

            # Send notifications
            if google_result and google_result["status"] == "success":
                self.notifications.send_email(
                    recipient=user["Email Address"],
                    subject="Account Deactivation",
                    body="Your Google Workspace account has been deactivated."
                )

            self.notifications.send_slack_message(
                message=f"Offboarding completed for {user['Email Address']} in department {department}."
            )

            report.append({
                "email": user["Email Address"],
                "google": google_result,
                "slack": slack_result,
                "zoom": zoom_result
            })

        return report
