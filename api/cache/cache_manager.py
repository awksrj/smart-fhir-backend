import time

cache_store = {}

def set(key, value, ttl=60):
    cache_store[key] = {
        "value": value,
        "expiry": time.time() + ttl
    }

def get(key):
    item = cache_store.get(key)
    if not item:
        return None

    if time.time() > item["expiry"]:
        del cache_store[key]
        return None

    return item["value"]

def exists(key):
    return get(key) is not None