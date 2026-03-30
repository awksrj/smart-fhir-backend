import requests
from .base_adapter import BaseAdapter

BASE_URL = "http://localhost:8080/fhir"

class HAPIAdapter(BaseAdapter):

    def fetch_patients(self, name=None):
        params = {"_count": 10}
        if name:
            params["name"] = name

        response = requests.get(f"{BASE_URL}/Patient", params=params)
        response.raise_for_status()
        return response.json()

    def fetch_observations(self, patient_id=None):
        params = {"_count": 50}

        # For dashboard, always fetch all observations (ignore patient_id filter)
        if patient_id and patient_id != "None":   # safety
            params["subject"] = f"Patient/{patient_id}"

        response = requests.get(f"{BASE_URL}/Observation", params=params)
        response.raise_for_status()

        data = response.json()

        count = len(data.get('entry', []))
        print(f"[DEBUG] HAPI returned {count} observations (patient_id filter: {patient_id})")

        return data

    def normalize_patient(self, data):
        return data.get("entry", [])

    def normalize_observation(self, data):
        return data.get("entry", [])
    