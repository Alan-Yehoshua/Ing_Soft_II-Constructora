from .database import get_supabase_client

class MaterialModel:
    def __init__(self):
        self.supabase = get_supabase_client()

    def obtener_materiales(self):
        response = self.supabase.rpc("get_materiales").execute()
        return response.data

    def agregar_material(self, material_data):
        self.supabase.table("material").insert(material_data).execute()

    def actualizar_material(self, id_material, material_data):
        self.supabase.table("material").update(material_data).eq("id_material", id_material).execute()

    def eliminar_material(self, id_material):
        self.supabase.table("material").delete().eq("id_material", id_material).execute()
    
    def obtener_proveedores(self):
        response = self.supabase.table("proveedor").select("nombre").execute()
        return response.data
    
    def obtener_id_proveedor(self, name):
        response = (self.supabase.table("proveedor").select("id_proveedor").eq("nombre", name).execute())
        return response.data[0]["id_proveedor"]

    def obtener_tel_proveedor(self, name):
        response = (self.supabase.table("proveedor").select("telefono").eq("nombre", name).execute())
        return response.data[0]["telefono"]