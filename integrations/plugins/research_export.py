from integrations.base_plugin import BasePlugin
from data_pipeline.utils import calculate_age

class ResearchExportPlugin(BasePlugin):
    """
    Research plugin for exporting patient observations for research.
    Supports:
      - Top-level numeric 'value' (seeded BP, labs)
      - Component-level numeric values (LOINC-coded)
      - Anonymized patient IDs
    """

    def execute(self, observations, config=None):
        if config is None:
            config = {}

        patient_map = config.get("patients", {})
        dataset = []

        print(f"[DEBUG] Total observations received: {len(observations)}")

        for obs in observations:
            patient_id = obs.get("patient_id")
            if not patient_id:
                print("[DEBUG] Skipped observation: missing patient_id")
                continue

            patient = patient_map.get(patient_id)
            if not patient:
                print(f"[DEBUG] Skipped observation: patient {patient_id} not in patient_map")
                continue

            # Extract all numeric components, including top-level value
            obs_data = self.extract_numeric_components(obs)
            if not obs_data:
                print(f"[DEBUG] Skipped observation: no numeric components")
                continue

            dataset.append({
                "patient_id": self.anonymize(patient_id),
                "age": calculate_age(patient.get("birthDate")),
                "observation_type": obs.get("code", "unknown"),
                "components": obs_data,
                "date": obs.get("date")
            })

        print(f"[DEBUG] Total dataset entries: {len(dataset)}")
        return {
            "study": "general_patient_observations",
            "record_count": len(dataset),
            "dataset": dataset
        }

    def extract_numeric_components(self, obs):
        """
        Extract all numeric values from an observation:
          - Top-level 'valueQuantity' or 'value'
          - Components array
        """
        result = {}

        # Top-level valueQuantity (FHIR standard)
        if "valueQuantity" in obs and "value" in obs["valueQuantity"]:
            result["value"] = obs["valueQuantity"]["value"]
            result["unit"] = obs["valueQuantity"].get("unit")

        # Top-level 'value' (seeded observations)
        elif "value" in obs:
            result["value"] = obs["value"]

        # Components array (e.g., systolic/diastolic)
        for comp in obs.get("components", []):
            code = comp.get("code", {}).get("coding", [{}])[0].get("code", "unknown")
            value = comp.get("valueQuantity", {}).get("value")
            unit = comp.get("valueQuantity", {}).get("unit")
            if value is not None:
                result[code] = {"value": value, "unit": unit}

        return result if result else None

    def anonymize(self, patient_id):
        """Return a consistent anonymized patient ID"""
        return f"anon_{hash(patient_id) % 10000}"