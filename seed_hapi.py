import requests
import random
from datetime import date, timedelta

# Change this to your HAPI server base URL
HAPI_BASE = "http://localhost:8080/fhir"

# Number of synthetic patients to create
NUM_PATIENTS = 5

def create_patient(i):
    patient_data = {
        "resourceType": "Patient",
        "id": f"patient{i}",
        "name": [{"use": "official", "family": f"Test{i}", "given": [f"Patient{i}"]}],
        "gender": random.choice(["male", "female"]),
        "birthDate": (date.today() - timedelta(days=random.randint(20*365, 70*365))).isoformat()
    }
    resp = requests.put(f"{HAPI_BASE}/Patient/patient{i}", json=patient_data)
    if resp.status_code in (200, 201):
        print(f"[INFO] Created patient {patient_data['id']}")
    else:
        print(f"[ERROR] Failed to create patient {patient_data['id']}: {resp.text}")
    return patient_data["id"]

def create_bp_observation(patient_id):
    systolic = random.randint(110, 140)
    diastolic = random.randint(70, 90)
    obs_data = {
        "resourceType": "Observation",
        "status": "final",
        "category": [{"coding":[{"system":"http://terminology.hl7.org/CodeSystem/observation-category","code":"vital-signs"}]}],
        "code": {"coding":[{"system":"http://loinc.org","code":"85354-9","display":"Blood pressure panel"}]},
        "subject": {"reference": f"Patient/{patient_id}"},
        "effectiveDateTime": date.today().isoformat(),
        "component": [
            {"code":{"coding":[{"system":"http://loinc.org","code":"8480-6","display":"Systolic"}]},
             "valueQuantity":{"value": systolic, "unit": "mmHg"}},
            {"code":{"coding":[{"system":"http://loinc.org","code":"8462-4","display":"Diastolic"}]},
             "valueQuantity":{"value": diastolic, "unit": "mmHg"}}
        ]
    }
    resp = requests.post(f"{HAPI_BASE}/Observation", json=obs_data)
    if resp.status_code in (200, 201):
        print(f"[INFO] Created BP observation for {patient_id}: {systolic}/{diastolic} mmHg")
    else:
        print(f"[ERROR] Failed to create observation for {patient_id}: {resp.text}")

def main():
    patient_ids = [create_patient(i) for i in range(1, NUM_PATIENTS+1)]
    for pid in patient_ids:
        # Create multiple BP observations per patient
        for _ in range(2):
            create_bp_observation(pid)

if __name__ == "__main__":
    main()