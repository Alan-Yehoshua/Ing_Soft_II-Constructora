from supabase import create_client, Client

def get_supabase_client() -> Client:
    url = "https://qlsmhahdkovvqfauntde.supabase.co"
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFsc21oYWhka292dnFmYXVudGRlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjYwNjcxMjIsImV4cCI6MjA0MTY0MzEyMn0.K-LSXODTvSbvFqu6hnJWYiP8KDmm959LZB5xYQl6aPI"
    return create_client(url, key)

class AuthModel:
    def __init__(self):
        self.supabase = get_supabase_client()

    def verify_credentials(self, username: str, password: str):
        response = self.supabase.from_("empleados").select("*").eq("username", username).eq("password", password).execute()
        return response.data

    def is_admin(self, user_data):
        return user_data.get('puesto') == "Administrador"