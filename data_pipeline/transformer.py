from data_pipeline.mappers import patient_mapper, observation_mapper

def transform(resource_type, entries):
    """Safely unwrap FHIR Bundle entries and transform resources."""
    if not entries:
        print(f"[DEBUG Transformer] Empty input for {resource_type}")
        return []

    resources = []

    # Handle full Bundle (most common case from HAPI)
    if isinstance(entries, dict) and "entry" in entries:
        for entry in entries.get("entry", []):
            if isinstance(entry, dict):
                if "resource" in entry:
                    resource = entry["resource"]
                    if isinstance(resource, dict):
                        resources.append(resource)
                elif resource_type in str(entry.get("resourceType", "")):  # fallback
                    resources.append(entry)
        print(f"[DEBUG Transformer] Extracted {len(resources)} {resource_type} resources from Bundle")
    
    # Handle list of entries or resources
    elif isinstance(entries, list):
        for item in entries:
            if isinstance(item, dict):
                if "resource" in item:
                    resources.append(item["resource"])
                else:
                    resources.append(item)
        print(f"[DEBUG Transformer] Processed list with {len(resources)} items")

    else:
        resources = [entries] if isinstance(entries, dict) else []

    # Apply the correct mapper
    if resource_type == "Patient":
        return [patient_mapper.transform(r) for r in resources if isinstance(r, dict)]
    
    elif resource_type == "Observation":
        transformed = []
        for r in resources:
            if isinstance(r, dict):
                mapped = observation_mapper.transform(r)
                transformed.append(mapped)
        print(f"[DEBUG Transformer] Successfully transformed {len(transformed)} Observations")
        return transformed

    return []