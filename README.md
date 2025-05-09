# SaaSFlow

## Overview
This tool automates the onboarding and offboarding of users across multiple SaaS applications, including Google Workspace, Slack, and Zoom. It provides a graphical user interface (GUI) for ease of use and supports database integration for logging and reporting.

## Features
- **Onboarding**: Automatically creates user accounts, assigns attributes, adds users to groups/channels, and assigns licenses.
- **Offboarding**: Deletes or deactivates user accounts.
- **Database Integration**: Logs all actions and stores user data for auditing.
- **Custom Workflows**: Supports department-specific workflows for onboarding and offboarding.
- **Notifications**: Sends email and Slack notifications for onboarding/offboarding status.
- **Log Viewer**: Allows admins to view logs with filters.
- **GUI**: User-friendly interface for system administrators.

## Requirements
- Python 3.8+
- Required Python libraries (install via `pip install -r requirements.txt`):
  - `google-api-python-client`
  - `google-auth`
  - `requests`
  - `tkinter`
  - `sqlite3`

## Setup

### 1. Google Workspace Service Account
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Navigate to **IAM & Admin > Service Accounts**.
4. Create a new service account and assign the "Admin SDK Directory API" role.
5. Generate a JSON key and download it.

### 2. Slack API Token
1. Create a Slack app in your workspace.
2. Enable the necessary permissions (e.g., `users:read`, `users:write`).
3. Generate an API token.

### 3. Zoom API Key and Secret
1. Create a Zoom app in the Zoom App Marketplace.
2. Generate the API credentials (key and secret).

### 4. SMTP Configuration
Provide the SMTP server details for sending email notifications:
- Server: `smtp.gmail.com`
- Port: `587`
- User: Your email address
- Password: Your email password or app-specific password

### 5. Install Dependencies
Run the following command to install the required Python libraries:
```bash
pip install google-api-python-client google-auth requests
```

## Usage

### Running the Application
1. Execute the GUI application:
   ```bash
   python gui.py
   ```
2. Log in using the test admin credentials:
   - Username: `admin`
   - Password: `admin123`
3. Use the GUI to:
   - Onboard users by selecting the test CSV file (`test_users.csv`).
   - Provide the required credentials (Google Workspace JSON, Slack token, Zoom API key/secret).
   - Select SaaS applications and confirm actions.

### Testing
A sample CSV file (`test_users.csv`) is included for testing. It contains the following fields:
- First Name
- Last Name
- Email Address
- Department
- Role
- Custom Attributes

## File Structure
- `auth.py`: Handles user authentication and role-based access control.
- `csv_parser.py`: Parses user data from CSV files.
- `database.py`: Manages database integration and logging.
- `google_workspace_api.py`: Interacts with the Google Workspace API.
- `gui.py`: Provides the graphical user interface.
- `log_parser.py`: Fetches and displays logs.
- `notifications.py`: Sends email and Slack notifications.
- `orchestration.py`: Coordinates onboarding and offboarding workflows.
- `reporting.py`: Generates reports.
- `slack_api.py`: Interacts with the Slack API.
- `zoom_api.py`: Interacts with the Zoom API.
- `workflows.py`: Manages custom workflows.
- `test_users.csv`: Sample CSV file for testing.

## License
This project is licensed under the MIT License.
