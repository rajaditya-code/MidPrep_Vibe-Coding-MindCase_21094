import os
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY") 

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ ERROR: Supabase keys are missing! Check your .env file.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_data(data):
    try:
        response = supabase.table("opportunities").upsert(
            data, 
            on_conflict="title, link" 
        ).execute()
        return True
        
    except Exception as e:
        print(f"\n❌ SUPABASE REJECTED THE DATA! Reason:")
        print(e)
        print("-" * 40)
        return False