import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from auth import Auth
from orchestration import Orchestration
from log_parser import LogParser
from predictive_analytics import PredictiveAnalytics
from chatbot import SaaSFlowChatBot

class UserOnboardingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User Onboarding and Offboarding Tool")
        self.auth = Auth()
        self.logged_in_user = None

        # Initialize predictive analytics and chatbot
        self.analytics = PredictiveAnalytics('user_data.csv')
        self.analytics.train_model()
        self.chatbot = SaaSFlowChatBot()
        self.chatbot.train_bot()

        self.show_login_screen()

    def show_login_screen(self):
        """Display the login screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Login", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Username:").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Login", command=self.login).pack(pady=10)

    def login(self):
        """Handle user login."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            role = self.auth.authenticate_user(username, password)
            self.logged_in_user = {"username": username, "role": role}
            self.show_main_dashboard()
        except Exception as e:
            messagebox.showerror("Login Failed", str(e))

    def show_main_dashboard(self):
        """Display the main dashboard."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"Welcome, {self.logged_in_user['username']}!", font=("Arial", 16)).pack(pady=10)

        if self.logged_in_user["role"] == "Admin":
            tk.Button(self.root, text="Onboard Users", command=self.onboard_users).pack(pady=5)
            tk.Button(self.root, text="Offboard Users", command=self.offboard_users).pack(pady=5)
            tk.Button(self.root, text="View Logs", command=self.view_logs).pack(pady=5)
            tk.Button(self.root, text="Chat with SaaSFlowBot", command=self.chatbot_interaction).pack(pady=5)
            tk.Button(self.root, text="Show Predictions", command=self.show_predictions).pack(pady=5)
            tk.Button(self.root, text="Settings", command=self.open_settings).pack(pady=5)
            tk.Button(self.root, text="Security Licenses", command=self.open_license_settings).pack(pady=10)
        else:
            tk.Label(self.root, text="Limited Access: Manager Role", font=("Arial", 12)).pack(pady=10)

        tk.Button(self.root, text="Logout", command=self.show_login_screen).pack(pady=10)

    def onboard_users(self):
        """Handle user onboarding with additional options."""
        # Select database system
        db_window = tk.Toplevel(self.root)
        db_window.title("Select Database System")

        tk.Label(db_window, text="Choose Database System:", font=("Arial", 12)).pack(pady=10)
        db_choice = tk.StringVar(value="SQLite")
        tk.Radiobutton(db_window, text="SQLite", variable=db_choice, value="SQLite").pack(anchor="w")
        tk.Radiobutton(db_window, text="MySQL", variable=db_choice, value="MySQL").pack(anchor="w")
        tk.Radiobutton(db_window, text="PostgreSQL", variable=db_choice, value="PostgreSQL").pack(anchor="w")

        def proceed_with_db():
            db_system = db_choice.get()
            db_window.destroy()

            # Select CSV file
            csv_file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
            if not csv_file:
                messagebox.showerror("Error", "No CSV file selected.")
                return

            # Select Google credentials
            google_credentials = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
            if not google_credentials:
                messagebox.showerror("Error", "No Google credentials file selected.")
                return

            # Input Slack token
            slack_token = tk.simpledialog.askstring("Slack Token", "Enter your Slack API token:")
            if not slack_token:
                messagebox.showerror("Error", "No Slack token provided.")
                return

            # Input Zoom API credentials
            zoom_api_key = tk.simpledialog.askstring("Zoom API Key", "Enter your Zoom API key:")
            if not zoom_api_key:
                messagebox.showerror("Error", "No Zoom API key provided.")
                return

            zoom_api_secret = tk.simpledialog.askstring("Zoom API Secret", "Enter your Zoom API secret:")
            if not zoom_api_secret:
                messagebox.showerror("Error", "No Zoom API secret provided.")
                return

            # Select SaaS applications
            saas_window = tk.Toplevel(self.root)
            saas_window.title("Select SaaS Applications")

            tk.Label(saas_window, text="Choose SaaS Applications:", font=("Arial", 12)).pack(pady=10)
            google_var = tk.BooleanVar(value=True)
            slack_var = tk.BooleanVar(value=True)
            zoom_var = tk.BooleanVar(value=True)

            tk.Checkbutton(saas_window, text="Google Workspace", variable=google_var).pack(anchor="w")
            tk.Checkbutton(saas_window, text="Slack", variable=slack_var).pack(anchor="w")
            tk.Checkbutton(saas_window, text="Zoom", variable=zoom_var).pack(anchor="w")

            def proceed_with_saas():
                saas_window.destroy()

                # Confirm onboarding actions
                confirm = messagebox.askyesno("Confirm Onboarding", "Proceed with onboarding users?")
                if not confirm:
                    return

                # Execute onboarding
                smtp_config = {
                    "server": "smtp.example.com",
                    "port": 587,
                    "user": "your-email@example.com",
                    "password": "your-email-password"
                }

                slack_webhook_url = "https://hooks.slack.com/services/your/webhook/url"

                try:
                    orchestrator = Orchestration(
                        csv_file=csv_file,
                        google_credentials=google_credentials,
                        slack_token=slack_token,
                        zoom_api_key=zoom_api_key,
                        zoom_api_secret=zoom_api_secret,
                        smtp_config=smtp_config,
                        slack_webhook_url=slack_webhook_url
                    )

                    report = orchestrator.onboard_users()
                    messagebox.showinfo("Success", "Onboarding completed. Check logs for details.")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred during onboarding: {e}")

            tk.Button(saas_window, text="Proceed", command=proceed_with_saas).pack(pady=10)

        tk.Button(db_window, text="Proceed", command=proceed_with_db).pack(pady=10)

    def offboard_users(self):
        """Handle user offboarding."""
        messagebox.showinfo("Offboard Users", "Offboarding users feature coming soon!")

    def view_logs(self):
        """Display logs in a new window."""
        log_parser = LogParser()
        logs = log_parser.fetch_logs()

        log_window = tk.Toplevel(self.root)
        log_window.title("Logs")

        tk.Label(log_window, text="Logs", font=("Arial", 16)).pack(pady=10)

        text_area = tk.Text(log_window, wrap=tk.WORD, width=80, height=20)
        text_area.pack(pady=10)

        for log in logs:
            text_area.insert(tk.END, f"ID: {log[0]} | Email: {log[1]} | Action: {log[2]} | Status: {log[3]} | Error: {log[4]} | Timestamp: {log[5]}\n")

        tk.Button(log_window, text="Close", command=log_window.destroy).pack(pady=10)

    def chatbot_interaction(self):
        """Handle chatbot interaction."""
        user_input = tk.simpledialog.askstring("Chat with SaaSFlowBot", "Ask SaaSFlowBot:")
        if user_input:
            response = self.chatbot.get_response(user_input)
            messagebox.showinfo("SaaSFlowBot", response)

    def show_predictions(self):
        """Display predictive analytics results."""
        user_data = {}  # Collect user data from GUI inputs (to be implemented)
        predictions = self.analytics.predict(user_data)
        messagebox.showinfo("Predictions", f"Predictions: {predictions}")

    def open_settings(self):
        """Open the settings menu for admin configuration."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Admin Settings")

        tk.Label(settings_window, text="SMTP Server:").grid(row=0, column=0, padx=10, pady=5)
        smtp_entry = tk.Entry(settings_window)
        smtp_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(settings_window, text="SMTP Port:").grid(row=1, column=0, padx=10, pady=5)
        port_entry = tk.Entry(settings_window)
        port_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(settings_window, text="Admin Email:").grid(row=2, column=0, padx=10, pady=5)
        email_entry = tk.Entry(settings_window)
        email_entry.grid(row=2, column=1, padx=10, pady=5)

        def save_settings():
            smtp_server = smtp_entry.get()
            smtp_port = port_entry.get()
            admin_email = email_entry.get()
            print(f"Settings saved: SMTP Server={smtp_server}, Port={smtp_port}, Admin Email={admin_email}")
            settings_window.destroy()

        save_button = tk.Button(settings_window, text="Save", command=save_settings)
        save_button.grid(row=3, column=0, columnspan=2, pady=10)

    def open_license_settings(self):
        """Open the security licenses menu."""
        license_window = tk.Toplevel(self.root)
        license_window.title("Security Licenses")

        tk.Label(license_window, text="Add Security License:").grid(row=0, column=0, padx=10, pady=5)
        license_entry = tk.Entry(license_window)
        license_entry.grid(row=0, column=1, padx=10, pady=5)

        def save_license():
            license_key = license_entry.get()
            print(f"License added: {license_key}")
            license_window.destroy()

        save_button = tk.Button(license_window, text="Add License", command=save_license)
        save_button.grid(row=1, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = UserOnboardingApp(root)
    root.mainloop()
