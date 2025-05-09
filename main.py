import argparse
from orchestration import Orchestration
from reporting import Reporting
from auth import Auth
from log_parser import LogParser
from gui import open_settings, open_license_settings

def login():
    print("Welcome to the User Onboarding and Offboarding Tool")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    auth = Auth()
    try:
        role = auth.authenticate_user(username, password)
        print(f"Login successful! Role: {role}")
        return role
    except Exception as e:
        print(f"Login failed: {e}")
        return None

def view_logs():
    log_parser = LogParser()

    print("\nLog Viewer")
    email = input("Filter by email (leave blank for all): ")
    action = input("Filter by action (leave blank for all): ")
    status = input("Filter by status (leave blank for all): ")
    start_date = input("Filter by start date (YYYY-MM-DD, leave blank for all): ")
    end_date = input("Filter by end date (YYYY-MM-DD, leave blank for all): ")

    logs = log_parser.fetch_logs(email=email, action=action, status=status, start_date=start_date, end_date=end_date)
    log_parser.display_logs(logs)

def main():
    role = login()
    if not role:
        return

    if role == "Admin":
        print("Admin access granted. You can onboard, offboard users, view logs, and manage settings.")
        print("1. Onboard Users")
        print("2. Offboard Users")
        print("3. View Logs")
        print("4. Open Settings")
        print("5. Manage Security Licenses")
        choice = input("Enter your choice: ")

        if choice == "1":
            parser = argparse.ArgumentParser(description="Automated User Onboarding and Offboarding Tool")
            parser.add_argument("--csv", required=True, help="Path to the CSV file containing user data")
            parser.add_argument("--google-credentials", required=True, help="Path to the Google Workspace credentials JSON file")
            parser.add_argument("--slack-token", required=True, help="Slack API token")
            parser.add_argument("--zoom-api-key", required=True, help="Zoom API key")
            parser.add_argument("--zoom-api-secret", required=True, help="Zoom API secret")
            parser.add_argument("--action", required=True, choices=["onboard", "offboard"], help="Action to perform: onboard or offboard")
            parser.add_argument("--report", default="report.txt", help="Path to save the report file")

            args = parser.parse_args()

            orchestrator = Orchestration(
                csv_file=args.csv,
                google_credentials=args.google_credentials,
                slack_token=args.slack_token,
                zoom_api_key=args.zoom_api_key,
                zoom_api_secret=args.zoom_api_secret
            )

            if args.action == "onboard":
                report_data = orchestrator.onboard_users()
            elif args.action == "offboard":
                report_data = orchestrator.offboard_users()

            Reporting.generate_report(report_data, output_file=args.report)
        elif choice == "2":
            parser = argparse.ArgumentParser(description="Automated User Onboarding and Offboarding Tool")
            parser.add_argument("--csv", required=True, help="Path to the CSV file containing user data")
            parser.add_argument("--google-credentials", required=True, help="Path to the Google Workspace credentials JSON file")
            parser.add_argument("--slack-token", required=True, help="Slack API token")
            parser.add_argument("--zoom-api-key", required=True, help="Zoom API key")
            parser.add_argument("--zoom-api-secret", required=True, help="Zoom API secret")
            parser.add_argument("--action", required=True, choices=["onboard", "offboard"], help="Action to perform: onboard or offboard")
            parser.add_argument("--report", default="report.txt", help="Path to save the report file")

            args = parser.parse_args()

            orchestrator = Orchestration(
                csv_file=args.csv,
                google_credentials=args.google_credentials,
                slack_token=args.slack_token,
                zoom_api_key=args.zoom_api_key,
                zoom_api_secret=args.zoom_api_secret
            )

            if args.action == "onboard":
                report_data = orchestrator.onboard_users()
            elif args.action == "offboard":
                report_data = orchestrator.offboard_users()

            Reporting.generate_report(report_data, output_file=args.report)
        elif choice == "3":
            view_logs()
        elif choice == "4":
            open_settings()
        elif choice == "5":
            open_license_settings()
        else:
            print("Invalid choice.")
    elif role == "Manager":
        print("Manager access granted. Limited actions available.")
        # Call limited orchestration logic here
    else:
        print("Access denied.")

if __name__ == "__main__":
    main()