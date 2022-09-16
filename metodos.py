import hashlib
import jwt
import time
from respuesta import msj
from BD.metodos_sql import metodos_sql

class principal(metodos_sql):
    
    def crear_usuario(self, datos):
       
       passw_encrip = self.conv_pass(datos['clave'])
       sql = f"INSERT INTO PERSONAS (nombre, direccion, telefono, fecha, correo, clave) VALUES ('{datos['nombre']}','{datos['direccion']}','{datos['telefono']}','{datos['fecha']}','{datos['correo']}','{passw_encrip}')"
       res = self.insertar(sql)
       return res
        
    def conv_pass(self, passw):
        hash = hashlib.new('sha256')
        hash.update(passw.encode())
        hash_passw = hash.hexdigest()
        return hash_passw
        
    def login_usuario(self, datos):
        passw_encrip = self.conv_pass(datos['clave'])
        sql = f"SELECT id_persona FROM PERSONAS WHERE correo='{datos['correo']}' AND clave='{passw_encrip}';"
        res = self.consulta(sql)
        
        if len(res['data']) > 0:
            token = self.gen_token(passw_encrip)
            resul = self.guardar_token(token, res['data'][0]['id_persona'])
            return resul
        return msj(True,mensaje="Alguno de los datos son incorrectos")
            
    def gen_token(self, passw):
        fecha = time.strftime('%d%m%Y%H%M%S')
        token = f"{fecha}{passw}"
        encode = jwt.encode({"token":token},"secret", algorithm="HS256")
        return encode
    
    def guardar_token(self, token, id):
        sql = f"UPDATE PERSONAS SET token='{token}' WHERE id_persona={id};"
        res = self.actualizar(sql)
        if res['error']:
             return msj(True, "Incoveniente al momento de guardar el tokens")
        return token 
     
    def crear_noticia(self, datos):
        val = self.validar_token(datos['token'])
        if not val['data'] :
            return msj(True, mensaje="El token no fue encontrado")
        if val['data'][0]['id_persona'] == int(datos['id_persona']):
            
            sql = f"INSERT INTO NOTICIAS (id_persona, titulo, descripcion) VALUES ({val['data'][0]['id_persona']},'{datos['titulo']}','{datos['descripcion']}' )"
            res = self.insertar(sql)
            return res
        return msj(True, mensaje="No es posible agregar a este noticia.")
    
    def bus_noticia(self, datos):
        val = self.validar_token(datos['token'])
        if not val['data'] :
            return msj(True, mensaje="El token no fue encontrado")
 
        if val['data'][0]['id_persona'] == int(datos['id_persona']):
            sql = f"SELECT * FROM NOTICIAS WHERE id_persona='{datos['id_persona']}'"
            res = self.consulta(sql)
            
            if len(res['data'])>0 :
                return res
            return msj(True, "Este usuario no tiene noticias registrada.")
        
        return msj(True, mensaje="No es posible mostrarle las noticias de ese usuario")
    
    def actualizar_noticia(self,datos):
        
        val = self.validar_token(datos['token'])
        if not val['data'] :
            return msj(True, mensaje="El token no fue encontrado")
        
        res = self.validar_noticia(val['data'][0]['id_persona'],datos['id_noticia'])
        if not res:
            sql = f"UPDATE NOTICIAS SET titulo='{datos['titulo']}', descripcion='{datos['descripcion']}' WHERE id_noticia={datos['id_noticia']}"
            resul = self.actualizar(sql)
            return resul
        return res
        
        
    def validar_noticia(self,id_usuario, id_noticia):
        sql = f"SELECT id_persona FROM NOTICIAS WHERE id_noticia={id_noticia}"
        res = self.consulta(sql)
        if not res['data']:
            return msj(True, mensaje="La noticia en donde quiere realizar la operación no existe.")
        if id_usuario == res['data'][0]['id_persona'] :
            return False
        return msj(True, mensaje="No es posible realizar esta operación.")
        
    
            
    def eli_noticia(self, datos):
        val = self.validar_token(datos['token'])
        if not val['data']:
            return msj(True, mensaje="El token no fue encontrado")
        res = self.validar_noticia(val['data'][0]['id_persona'], datos['id_noticia'])
        if not res:            
            sql = f"DELETE FROM NOTICIAS WHERE id_noticia={datos['id_noticia']}"
            res = self.eliminar(sql)
            return res
        return res
    
    def validar_token(self,token):
        sql = f"SELECT id_persona FROM PERSONAS WHERE token='{token}';"
        res = self.consulta(sql)
        return res
    
    def crear_comentarios(self, datos):
        val = self.validar_token(datos['token'])
        if not val['data']:
            return msj(True, mensaje="El token no fue encontrado")
        res = self.validar_noticia(val['data'][0]['id_persona'], datos['id_noticia'])
        if not res:            
            sql = f"INSERT INTO COMENTARIOS(id_noticia,descripcion) VALUES ({datos['id_noticia']},'{datos['descripcion']}')"
            res = self.insertar(sql)
            return res
        return res