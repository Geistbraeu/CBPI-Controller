import requests
import logging

class CBPIService:
    def __init__(self, base_url="http://beerpi:8000"):
        self.base_url = base_url
        self.kettles = {}  # name -> dict

    def refresh(self):
        """Fetch all kettles."""
        try:
            resp = requests.get(f"{self.base_url}/kettle/", timeout=2)
            if resp.status_code == 200:
                k_data = resp.json().get('data', [])
                self.kettles = {k['name']: k for k in k_data if 'name' in k}
                return True
            logging.error(f"API Error (kettles): {resp.status_code}")
            return False
        except Exception as e:
            logging.error(f"Error fetching kettles: {e}")
            return False

    def get_kettle(self, name):
        return self.kettles.get(name)

    def get_active_step(self):
        """Fetch the active brew step."""
        try:
            resp = requests.get(f"{self.base_url}/step2/", timeout=2)
            if resp.status_code == 200:
                steps = resp.json()
                # Find step with status "A"
                for step in steps:
                    if step.get('status') == 'A':
                        return step
            return None
        except Exception as e:
            logging.error(f"Error fetching active step: {e}")
            return None

