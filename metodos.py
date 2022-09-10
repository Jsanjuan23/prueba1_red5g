from BD.metodos_sql import metodos_sql
from respuesta import msj
import hashlib
import jwt
import time
class principal(metodos_sql):
    
    def crear_usuario(self,datos):
        passw_encrip = self.conv_passw(datos['clave'])
        sql = f"INSERT INTO PERSONAS (nombre, direccion, telefono, fecha, correo, clave) VALUES ('{datos['nombre']}','{datos['direccion']}','{datos['telefono']}','{datos['fecha']}','{datos['correo']}','{passw_encrip}');"
        resp = self.insertar(sql)
        return resp
    
    def login_usuario(self, datos):
        
        passw_encrip = self.conv_passw(datos['clave'])
        sql = f"SELECT id_persona FROM PERSONAS WHERE correo='{datos['correo']}' AND clave='{passw_encrip}';"
        res = self.consulta(sql)
        if len(res['data']) > 0:
        # se genera el nuevo token de sesion y se guarda
            token = self.gen_token(passw_encrip)
            resul = self.guardar_token(token, res['data'][0]['id_persona'])
            return resul
        return "Algunos de los datos son incorrectos"
        
    def conv_passw(self, passw):
        """
        Metodo para convertir la contraseña del usuario en una contraseña segura
        param: passw => str
        return: hash_passw => str
        """
        hash = hashlib.new('sha256')
        hash.update(passw.encode())
        hash_passw = hash.hexdigest()
        return hash_passw
    
    def gen_token(self, passw):
        """
        Metodo para generar un nuevo token recibe como parametro 
        param: passw => str
        return: token => str
        """
        fecha = time.strftime('%d%m%Y%H%M%S')
        token = f"{fecha}{passw}"
        token = jwt.encode({"token":token}, "secret", algorithm="HS256")
        return token
    
    def guardar_token(self, token, Id):
        """
        Metodo para guardar el token en la base de datos de la platforma
        recibe el token y el id del usuario
        param: token => str
        param: Id => int
        return: => dict
        """

        sql = f"UPDATE PERSONAS SET tokens= '{token}' WHERE id_persona={Id};"
        res = self.actualiza(sql)
        if res['error']:
            return msj(True, "Incoveniente al momento de guardar el tokens")
        return token
    
    def bus_noticias(self, datos):
        
        sql = f"SELECT * FROM NOTICIAS WHERE id_usuario={datos['id_persona']};"
        res = self.consulta(sql)
        if len(res['data']) > 0:
            return res
        return msj(True,"Este usuario no tiene ninguna noticia registrada.")
    
    def crear_noticias(self, datos):

        val = self.validar_token(datos['token'])
        sql = f"INSERT INTO NOTICIAS (id_usuario, titulo, descripcion) VALUES ({val['data'][0]['id_persona']}, '{datos['titulo']}', '{datos['descripcion']}')"
        res = self.insertar(sql)
        return res
        
    def validar_token(self,token):
        
        sql = f"SELECT id_persona FROM PERSONAS WHERE tokens='{token}';"
        res = self.consulta(sql)
        
        if not res['data']:
            return msj(True, "El token no fue encontrado")
        return res
    
    def act_noticias(self, datos):
        
        id_1 = self.validar_token(datos['token'])
        sql = f"SELECT id_usuario FROM NOTICIAS WHERE id_noticia={datos['id_noticia']};"
        id_2 = self.consulta(sql)
        if id_1['data'][0]['id_persona'] == id_2['data'][0]['id_usuario']:
            
            sql = f"""UPDATE NOTICIAS SET titulo='{datos['titulo']}', descripcion='{datos['descripcion']}' 
            WHERE id_noticia={datos['id_noticia']}"""
            res = self.actualiza(sql)
            return res
        return msj(True,"No le es permitido actualizar esta noticia!")
        
    def eli_noticias(self,datos):
        
        id_1 = self.validar_token(datos['token'])
        sql = f"SELECT id_usuario FROM NOTICIAS WHERE id_noticia={datos['id_noticia']};"
        id_2 = self.consulta(sql)
        if id_1['data'][0]['id_persona'] == id_2['data'][0]['id_usuario']:
            sql = f"DELETE FROM NOTICIAS WHERE id_noticia={datos['id_noticia']};"
            res = self.eliminar(sql)
            return res
        return "No le es permitido eliminar esta noticia"
    
    def crear_comentario(self,datos):
        
        id_1 = self.validar_token(datos['token'])
        sql = f"SELECT id_usuario FROM NOTICIAS WHERE id_noticia={datos['id_noticia']};"
        id_2 = self.consulta(sql)
        if not id_2['data']:
            return "No existe esta noticia."
        if id_1['data'][0]['id_persona'] == id_2['data'][0]['id_usuario']:
            sql = f"INSERT INTO comentario VALUES (2,'{datos['comentario']}', {datos['id_noticia']});"
            res = self.insertar(sql)
            return res
        return "No se pudo agregar el comentario "