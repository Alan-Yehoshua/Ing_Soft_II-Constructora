from .database import get_supabase_client

class ClienteModel:
    def __init__(self):
        self.supabase = get_supabase_client()

    def obtener_clientes(self):
        response = self.supabase.table("cliente").select("*").execute()
        return response.data

    def agregar_cliente(self, cliente_data):
        self.supabase.table("cliente").insert(cliente_data).execute()

    def actualizar_cliente(self, id_cliente, cliente_data):
        self.supabase.table("cliente").update(cliente_data).eq("id_cliente", id_cliente).execute()

    def eliminar_cliente(self, id_cliente):
        self.supabase.table("cliente").delete().eq("id_cliente", id_cliente).execute()
        