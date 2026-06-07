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

    def get_all_steps(self):
        """Fetch all brew steps."""
        try:
            resp = requests.get(f"{self.base_url}/step2/", timeout=2)
            if resp.status_code == 200:
                return resp.json()
            return []
        except Exception as e:
            logging.error(f"Error fetching steps: {e}")
            return []

