def transform(data):
    """General FHIR Observation flattening - produces clean, reusable structure."""
    
    if not isinstance(data, dict):
        return {"patient_id": None, "code": None, "components": [], "date": None}

    # Patient ID
    subject = data.get("subject") or {}
    patient_id = None
    if isinstance(subject, dict):
        ref = subject.get("reference", "")
        if ref:
            patient_id = ref.split("/")[-1]
    elif isinstance(subject, str):
        patient_id = subject.split("/")[-1]

    # Main code (e.g. Blood Pressure panel)
    code = None
    code_obj = data.get("code")
    if isinstance(code_obj, dict):
        coding = code_obj.get("coding", [{}])
        if coding and isinstance(coding[0], dict):
            code = coding[0].get("code")

    # Components (Systolic, Diastolic, etc.)
    components = []
    for comp in data.get("component", []):
        if not isinstance(comp, dict):
            continue
            
        comp_code_obj = comp.get("code", {})
        comp_code = None
        display = None
        if isinstance(comp_code_obj, dict):
            c = comp_code_obj.get("coding", [{}])
            if c and isinstance(c[0], dict):
                comp_code = c[0].get("code")
                display = c[0].get("display")

        value_qty = comp.get("valueQuantity", {})
        value = value_qty.get("value") if isinstance(value_qty, dict) else None
        unit = value_qty.get("unit") if isinstance(value_qty, dict) else None

        if comp_code and value is not None:
            components.append({
                "code": comp_code,
                "display": display,
                "value": value,
                "unit": unit
            })

    date = data.get("effectiveDateTime") or data.get("effectiveInstant")

    return {
        "patient_id": patient_id,
        "code": code,
        "components": components,      # List of dicts - clean and reusable
        "date": date,
        "raw_id": data.get("id")       # Useful for debugging/tracking
    }