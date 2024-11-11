from .database import get_supabase_client

class BusquedaModel:
    def __init__(self):
        self.supabase = get_supabase_client()
    
    def obtener_Proveedores(self, n):
        response = self.supabase.table("proveedor").\
        select("*").like("nombre", f"{n}%").execute()
        return response.data
    
    def obtener_materiales(self, n):
        response = self.supabase.table("material").\
        select("*").like("nombre", f"{n}%").execute()
        return response.data
    
    def obtener_empleados(self, n):
        response = self.supabase.table("empleados").\
        select("*").like("nombre", f"{n}%").execute()
        return response.data
    
    def obtener_citas(self, n):
        response = self.supabase.table("citas").\
        select("*").like("descripcion", f"{n}%").execute()
        return response.data
    
    def obtener_clientes(self, n):
        response = self.supabase.table("cliente").\
        select("*").like("nombre", f"{n}%").execute()
        return response.data
    
    def obtener_Obras(self, n):
        response = self.supabase.table("obra").\
        select("*").like("nombre", f"{n}%").execute()
        return response.data
    
    def obtener_mensajes(self, n):
        response = self.supabase.table("mensajes_enviados").\
        select("*").like("remitente", f"{n}%").execute()
        return response.data