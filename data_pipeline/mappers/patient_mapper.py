def transform(data):
    return {
        "id": data.get("id"),
        "name": data.get("name", [{}])[0].get("text"),
        "birthDate": data.get("birthDate")
    }