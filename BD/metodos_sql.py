import pymysql
from respuesta import msj
from BD.credenciales import HOST, USER, PASSW, BD
class metodos_sql:
    
    def conectar(self):
        
        try:
            self.cone = pymysql.connect(
             host=HOST,
             user=USER,
             passwd=PASSW,
             database=BD,
             cursorclass=pymysql.cursors.DictCursor
            )
            return self.cone.cursor(), True
        except:
            return None, False
        
    
    def insertar(self, sql):
        
        cur,_ = self.conectar()
        if not _ :
            return msj(True,mensaje='Ha habido un problema en la conexión.')
        
        cur.execute(sql)
        self.cone.commit()
        self.cone.close()
        return msj(mensaje="Se ha guardado exitosamente")
    
    def consulta(self, sql):
        cur, _ = self.conectar()
        if not _ :
            return msj(True, mensaje="Ha habido un problema con la conexión.")
        try:
            cur.execute(sql)
            res = cur.fetchall()
            self.cone.close()
            return msj(data=res)
        except:
            return msj(True, mensaje="Ha habido un error en la consulta")
        
    def actualizar(self, sql):
        cur, _ = self.conectar()
        if not _ :
            return msj(True, mensaje="Ha habido un problema con la conexión.")
        try:
            cur.execute(sql)
            self.cone.commit()
            self.cone.close
            return msj(mensaje="Registro actualizado exitosamente")
        except:
            return msj(True,"Error al actualizar el registro")
        
    def eliminar(self, sql):
        cur, _ = self.conectar()
        if not _ :
            return msj(True, mensaje="Ha habido un problema con la conexión.")
        
        try:
            cur.execute(sql)
            self.cone.commit()
            self.cone.close()
            return msj(mensaje="Registro eliminado.")
        
        except:
            return msj(True,"Error al eliminar el registro")
            