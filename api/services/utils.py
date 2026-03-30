def paginate(items, page=1, page_size=10):
    if not items:
        return {"items": [], "total": 0, "page": page, "page_size": page_size}
    
    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    paginated_items = items[start:end]
    
    return {
        "items": paginated_items,      # ← keep full dicts here
        "total": total,
        "page": page,
        "page_size": page_size,
        "has_more": end < total
    }