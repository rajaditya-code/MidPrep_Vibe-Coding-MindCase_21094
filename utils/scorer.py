from datetime import datetime
import dateparser

def calculate_score(data):
    score = 0
    org = data.get("organization", "").lower()
    
    # 1. Organization Weight
    if "iit" in org or "iiser" in org: score += 20
    elif "csir" in org or "icar" in org: score += 15
    elif "zoho" in org or "infosys" in org: score += 10

    # 2. Urgency Weight (Ending Soon)
    if data.get("deadline"):
        dt = dateparser.parse(data["deadline"], settings={'DATE_ORDER': 'DMY'})
        if dt:
            days_left = (dt - datetime.now()).days
            if 0 <= days_left <= 3: score += 50
            elif 3 < days_left <= 7: score += 30

    # 3. Hot Topics
    if "ai" in data.get("tags", []): score += 10

    return score