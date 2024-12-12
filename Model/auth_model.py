from supabase import create_client, Client

def get_supabase_client() -> Client:
    url = ""
    key = ""
    return create_client(url, key)

class AuthModel:
    def __init__(self):
        self.supabase = get_supabase_client()

    def verify_credentials(self, username: str, password: str):
        response = self.supabase.from_("empleados").select("*").eq("username", username).eq("password", password).execute()
        return response.data

    def is_admin(self, user_data):
        return user_data.get('puesto') == "Administrador"
