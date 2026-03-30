from fhir_client.client import FHIRClient
from data_pipeline.transformer import transform
from api.cache import cache_manager as cache
from api.services.utils import paginate


def get_patients(name=None, page=1, page_size=5, server="hapi"):
    cache_key = f"{server}:patients:{name}:{page}:{page_size}"

    if cache.exists(cache_key):
        return cache.get(cache_key)

    client = FHIRClient(server)

    # Step 1: Fetch from FHIR
    data = client.get_patients(name)

    # Step 2: Transform
    transformed = transform("Patient", data)

    # Step 3: Additional filtering
    if name:
        transformed = [
            p for p in transformed
            if p["name"] and name.lower() in p["name"].lower()
        ]

    # Step 4: Pagination
    result = paginate(transformed, page, page_size)

    # Step 5: Cache
    cache.set(cache_key, result)

    return result