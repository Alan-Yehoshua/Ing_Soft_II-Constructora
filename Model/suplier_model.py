from .database import get_supabase_client

class ProveedorModel:
    def __init__(self):
        self.supabase = get_supabase_client()

    def obtener_Proveedores(self):
        response = self.supabase.table("proveedor").select("*").execute()
        return response.data

    def agregar_Proveedores(self, proveedor_data):
        self.supabase.table("proveedor").insert(proveedor_data).execute()

    def actualizar_Proveedores(self, id_proveedor, proveedor_data):
        self.supabase.table("proveedor").update(proveedor_data).eq("id_proveedor", id_proveedor).execute()

    def eliminar_Proveedores(self, id_proveedor):
        self.supabase.table("proveedor").delete().eq("id_proveedor", id_proveedor).execute()
        