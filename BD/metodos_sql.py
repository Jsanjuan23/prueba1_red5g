from ast import Try
import pymysql
from respuesta import msj
from BD.credenciales import HOST, PASSW, USER, BASE

class metodos_sql:
    
    def conectar(self):
        
        try:
            self.cone = pymysql.connect(host=HOST,
                                        user=USER,
                                        passwd=PASSW,
                                        database=BASE,
                                        cursorclass=pymysql.cursors.DictCursor)
            return self.cone.cursor(), True
        except:
            return None, False
   
    def insertar(self, sql):
        
        cur, _ = self.conectar()
        if not _:
            return msj(True, 'Error al conectar con base de datos')
        cur.execute(sql)
        self.cone.commit()
        self.cone.close()
        return msj(mensaje='Registro exitoso!')
                    
    def consulta(self, sql):
        """
        Metodo para consutar datos usando la sentencia SQL suministrada y retornando un dicccionario con
        estrucra fija para la respuesta 
        param: SQL => str
        return:  dict
        """
        cur, _ = self.conectar()
        if not _:
            return msj(True, 'Error al conectar con base de datos')
        try:
      
            cur.execute(sql)
            res = cur.fetchall()
            self.cone.close()
            return msj(data=res)
        except:
            return msj(True, "Ha habido un error en la consulta")
        
    def actualiza(self, sql):
        
        cur, _ = self.conectar()
        if not _:
            return msj(True, 'Error al conectar con base de datos')
        try:
            cur.execute(sql)
            self.cone.commit()
            self.cone.close()
            return msj(mensaje="Registro actualizado")
        
        except:
            return msj(True, "Error al actualizar el registro")
        
    def eliminar(self,sql):
        
        cur, _ = self.conectar()
        if not _:
            return msj(True, 'Error al conectar con base de datos')
        try:
            cur.execute(sql)
            self.cone.commit()
            self.cone.close()
            return msj(mensaje="Registro eliminado")
        
        except:
            return msj(True, "Error al eliminar el registro")