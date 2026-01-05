from supabase import create_client, Client

def get_supabase_client() -> Client:
    url = "https://qlsmhahdkovvqfauntde.supabase.co"
    key = "APIKEY"

    return create_client(url, key)
