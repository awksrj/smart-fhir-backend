from integrations.base_plugin import BasePlugin
from data_pipeline.utils import calculate_age
from collections import defaultdict

class DashboardPlugin(BasePlugin):
    """
    Dashboard plugin for patient overview.
    Takes normalized observations and produces UI-ready dashboard data.
    """

    def execute(self, observations, config=None):
        if config is None:
            config = {}

        patient_map = config.get("patients", {})
        dashboard_data = []

        print(f"[DEBUG] Total observations received: {len(observations)}")
        print(f"[DEBUG] Patient map has {len(patient_map)} patients")

        for obs in observations:
            if not isinstance(obs, dict):
                continue

            patient_id = obs.get("patient_id")
            if not patient_id:
                print(f"[DEBUG] Skipped observation: missing patient_id")
                continue

            patient = patient_map.get(patient_id)
            if not patient:
                print(f"[DEBUG] Skipped observation: patient {patient_id} not found")
                continue

            # Domain-specific: Extract numeric components for dashboard
            components = self.extract_numeric_components(obs)
            if not components:
                print(f"[DEBUG] Skipped observation: no numeric components")
                continue

            dashboard_data.append({
                "patient_id": self.anonymize(patient_id),
                "age": calculate_age(patient.get("birthDate")),
                "observation_type": obs.get("code", "unknown"),
                "components": components,
                "date": obs.get("date")
            })

        # Generate summary statistics (dashboard-specific)
        summary = self.generate_summary(dashboard_data)

        return {
            "dashboard": "patient_overview",
            "total_patients": len(set(d["patient_id"] for d in dashboard_data)),
            "total_observations": len(dashboard_data),
            "summary": summary,
            "dataset": dashboard_data
        }

    def extract_numeric_components(self, obs):
        """Dashboard-specific extraction from normalized components."""
        result = {}

        for comp in obs.get("components", []):
            if isinstance(comp, dict):
                code = comp.get("code")
                value = comp.get("value")
                unit = comp.get("unit")
                if code and value is not None:
                    result[code] = {"value": value, "unit": unit}

        return result if result else None

    def anonymize(self, patient_id):
        return f"anon_{hash(patient_id) % 10000}"

    def generate_summary(self, data):
        """Creates summary statistics for dashboard."""
        obs_totals = defaultdict(list)
        patient_counts = defaultdict(int)

        for record in data:
            patient_counts[record["patient_id"]] += 1
            for key, comp in record["components"].items():
                if isinstance(comp, dict) and "value" in comp:
                    obs_totals[key].append(comp["value"])
                elif key == "value":
                    obs_totals[key].append(comp)

        avg_values = {k: sum(v)/len(v) if v else None for k, v in obs_totals.items()}

        return {
            "avg_values_by_type": avg_values,
            "observations_per_patient": dict(patient_counts)
        }

