class Reporting:
    @staticmethod
    def generate_report(report_data, output_file="report.txt"):
        """Generate a report of success/failure for each action."""
        try:
            with open(output_file, mode='w', encoding='utf-8') as file:
                for entry in report_data:
                    file.write(f"Email: {entry['email']}\n")
                    file.write(f"  Google Workspace: {entry['google']['status']}\n")
                    if 'error' in entry['google']:
                        file.write(f"    Error: {entry['google']['error']}\n")
                    file.write(f"  Slack: {entry['slack']['status']}\n")
                    if 'error' in entry['slack']:
                        file.write(f"    Error: {entry['slack']['error']}\n")
                    file.write(f"  Zoom: {entry['zoom']['status']}\n")
                    if 'error' in entry['zoom']:
                        file.write(f"    Error: {entry['zoom']['error']}\n")
                    file.write("\n")
            print(f"Report generated: {output_file}")
        except Exception as e:
            print(f"Error generating report: {e}")
