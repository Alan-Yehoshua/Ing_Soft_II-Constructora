from .database import get_supabase_client

class EmpleadoModel:
    def __init__(self):
        self.supabase = get_supabase_client()

    def obtener_empleados(self):
        response = self.supabase.rpc("get_empleados").execute()
        return response.data
    #POSIBLES CAMBIOS
    def agregar_empleados(self, obra_data):
        self.supabase.table("empleados").insert(obra_data).execute()
    #POSIBLES CAMBIOS
    def actualizar_empleados(self, id_empleado, empleado_data):
        self.supabase.table("empleados").update(empleado_data).eq("id_obra", id_empleado).execute()
    #POSIBLES CAMBIOS
    def eliminar_empleados(self, id_empleado):
        self.supabase.table("empleados").delete().eq("id_empleado", id_empleado).execute()
    #POSIBLES CAMBIOS        
    def obtener_Obras(self):
        response = self.supabase.table("obra").select("nombre").execute()
        return response.data
    #POSIBLES CAMBIOS    
    def obtener_id_obra(self, name):
        response = (self.supabase.table("obra").select("id_obra").eq("nombre", name).execute())
        return response.data[0]["id_obra"]
        