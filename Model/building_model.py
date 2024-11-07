from .database import get_supabase_client

class ObraModel:
    def __init__(self):
        self.supabase = get_supabase_client()

    def obtener_Obras(self):
        response = self.supabase.rpc("get_obras").execute()
        return response.data

    def agregar_obra(self, obra_data):
        self.supabase.table("obra").insert(obra_data).execute()

    def actualizar_obra(self, id_obra, obra_data):
        self.supabase.table("obra").update(obra_data).eq("id_obra", id_obra).execute()

    def eliminar_obra(self, id_obra):
        self.supabase.table("obra").delete().eq("id_obra", id_obra).execute()
        
    def obtener_clientes(self):
        response = self.supabase.table("cliente").select("nombre").execute()
        return response.data
    
    def obtener_id_cliente(self, name):
        response = (self.supabase.table("cliente").select("id_cliente").eq("nombre", name).execute())
        return response.data[0]["id_cliente"]
        