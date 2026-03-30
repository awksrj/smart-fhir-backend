import requests
from .base_adapter import BaseAdapter

BASE_URL = "https://r4.smarthealthit.org"

class SmartAdapter(BaseAdapter):

    def fetch_patients(self, name=None):
        params = {"_count": 10}
        if name:
            params["name"] = name

        response = requests.get(f"{BASE_URL}/Patient", params=params)
        response.raise_for_status()
        return response.json()

    def fetch_observations(self, patient_id):
        params = {"subject": f"Patient/{patient_id}"}

        response = requests.get(f"{BASE_URL}/Observation", params=params)
        response.raise_for_status()
        return response.json()

    def normalize_patient(self, data):
        return data.get("entry", [])

    def normalize_observation(self, data):
        return data.get("entry", [])