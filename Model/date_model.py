from .database import get_supabase_client

class CitaModel:
    def __init__(self):
        self.supabase = get_supabase_client()

    def obtener_citas(self):
        response = self.supabase.rpc("get_citas").execute()
        return response.data

    def agregar_cita(self, cita_data):
        self.supabase.table("citas").insert(cita_data).execute()

    def actualizar_cita(self, id_cita, cita_data):
        self.supabase.table("citas").update(cita_data).eq("id_citas", id_cita).execute()

    def eliminar_cita(self, id_cita):
        self.supabase.table("citas").delete().eq("id_citas", id_cita).execute()
    
    def obtener_clientes(self):
        response = self.supabase.table("cliente").select("nombre").execute()
        return response.data
    
    def obtener_id_cliente(self, name):
        response = (self.supabase.table("cliente").select("id_cliente").eq("nombre", name).execute())
        return response.data[0]["id_cliente"]

    def obtener_tel_cliente(self, name):
        response = (self.supabase.table("cliente").select("telefono").eq("nombre", name).execute())
        return response.data[0]["telefono"]
    
    def agregar_mensaje(self, msg_data):
        self.supabase.table("mensajes_enviados").insert(msg_data).execute()