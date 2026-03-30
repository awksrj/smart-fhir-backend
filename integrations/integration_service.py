from integrations.registry import get_plugin
from api.services.observation_service import get_observations
from api.services.patient_service import get_patients
from data_pipeline.transformer import transform   # still needed for patients

def export_plugin_data(plugin_name: str, server: str = "hapi"):
    plugin = get_plugin(plugin_name)
    if not plugin:
        raise ValueError(f"Plugin {plugin_name} not found.")

    # Fetch patients and build map
    patients_list = get_patients(server=server)
    
    # Ensure we have transformed patient list
    if isinstance(patients_list, dict) and "items" in patients_list:
        patients_list = patients_list.get("items", [])
    
    patient_map = {p.get("id"): p for p in patients_list 
                   if isinstance(p, dict) and p.get("id")}

    # Get normalized observations from data_pipeline
    observations = get_observations(server)

    print(f"[DEBUG] Patients in map: {len(patient_map)}, Observations: {len(observations)}")

    # Pass normalized data to domain-specific plugin
    return plugin.execute(observations, {"patients": patient_map})


# def export_research(server: str = "hapi"):
#     return export_plugin_data("research", server)


def export_dashboard(server: str = "hapi"):
    return export_plugin_data("dashboard", server)

