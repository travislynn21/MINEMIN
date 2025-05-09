class Workflows:
    def __init__(self):
        # Predefined workflows for different roles or departments
        self.workflows = {
            "Engineering": {
                "onboard": ["google", "slack"],
                "offboard": ["google", "slack"]
            },
            "HR": {
                "onboard": ["google", "zoom"],
                "offboard": ["google", "zoom"]
            },
            "Sales": {
                "onboard": ["google", "slack", "zoom"],
                "offboard": ["google", "slack", "zoom"]
            }
        }

    def get_workflow(self, department, action):
        """Retrieve the workflow for a specific department and action."""
        return self.workflows.get(department, {}).get(action, [])
