from fhir_client.client import FHIRClient
from data_pipeline.transformer import transform
from api.services.utils import paginate

def get_observations(patient_id=None, server="hapi", page=1, page_size=5):
    client = FHIRClient(server)

    print("[DEBUG] Fetching observations from FHIR server...")
    
    # Force fetch ALL observations (ignore patient_id for dashboard)
    data = client.get_observations(patient_id=None)   # explicitly None

    observations = transform("Observation", data)
    print(f"[DEBUG] Transformed observations: {len(observations)}")

    print(f"[DEBUG] Observations after any processing: {len(observations)}")

    if observations:
        print("[DEBUG] Sample transformed observations (first 3):")
        for i, obs in enumerate(observations[:3]):
            print(f"   {i+1}. patient_id={obs.get('patient_id')!r} | code={obs.get('code')!r} | components={len(obs.get('components', []))}")
    else:
        print("[DEBUG] No observations after transformation!")

    return paginate(observations, page, page_size)


