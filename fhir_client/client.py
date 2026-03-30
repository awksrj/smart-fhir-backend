from fhir_client.adapters.hapi_adapter import HAPIAdapter
from fhir_client.adapters.smart_adapter import SmartAdapter
class FHIRClient:

    def __init__(self, server="hapi"):
        if server == "hapi":
            self.adapter = HAPIAdapter()
        elif server == "smart":
            self.adapter = SmartAdapter()
        else:
            raise ValueError("Unsupported FHIR server")

    def get_patients(self, name=None):
        raw = self.adapter.fetch_patients(name)
        return self.adapter.normalize_patient(raw)

    def get_observations(self,patient_id=None):
        raw = self.adapter.fetch_observations(patient_id)
        return self.adapter.normalize_observation(raw)
    
