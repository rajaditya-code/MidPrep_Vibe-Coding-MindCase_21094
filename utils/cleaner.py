import dateparser

def parse_date(date_str):
    if not date_str: return None
    dt = dateparser.parse(date_str, settings={'DATE_ORDER': 'DMY'})
    return dt.strftime("%d-%m-%Y") if dt else None

def detect_type(title):
    t = title.lower()
    if any(w in t for w in ["intern", "internship"]): return "internship"
    if "hackathon" in t: return "hackathon"
    if any(w in t for w in ["jrf", "srf", "project assistant", "fellow"]): return "research"
    return "job"

def detect_location(text):
    t = (text or "").lower()
    return "remote" if any(w in t for w in ["online", "remote", "wfh"]) else "onsite"

def extract_tags(text):
    keywords = ["ai", "ml", "biology", "data", "web", "python", "react", "research", "hardware"]
    return [k for k in keywords if k in (text or "").lower()]