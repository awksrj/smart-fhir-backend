from datetime import datetime

def calculate_age(birth_date):
    """
    Calculate age from birth date (YYYY-MM-DD).
    """
    if not birth_date:
        return None

    birth = datetime.strptime(birth_date, "%Y-%m-%d")
    today = datetime.today()
    return today.year - birth.year