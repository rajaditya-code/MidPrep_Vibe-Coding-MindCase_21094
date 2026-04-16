import json
import os

# The file where your data will be saved
DATA_FILE = "opportunities_test_data.json"

def _load_existing_data():
    """Helper function to load data or create an empty list if file doesn't exist."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # If the file exists but is corrupted/empty, start fresh
        return []

def insert_data(data):
    """
    Saves data to a local JSON file. 
    Returns True if inserted, False if it was a duplicate.
    """
    existing_data = _load_existing_data()
    
    # 1. Duplicate Prevention (Simulating Supabase UNIQUE constraint)
    # Create a set of all existing links for fast lookup
    existing_links = {item.get('link') for item in existing_data}
    
    if data.get('link') in existing_links:
        # Duplicate found, skip insertion
        return False
        
    # 2. Append new data
    existing_data.append(data)
    
    # 3. Save back to file
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving to local file: {e}")
        return False