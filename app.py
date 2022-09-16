from BD.metodos import principal
from flask import Flask,request

app=Flask(__name__)
@app.route('/')
def home():
    return 'Holaaaa'

@app.route('/registrar', methods=['post'])
def registrar():
    """ recibe todos los campos de tablas persona, excepto id_persona y token"""
    datos = request.json
    aut = principal()
    mensaje = aut.crear_usuario(datos)
    return mensaje

@app.route('/login', methods=['get', 'post'])
def login():
    """ recibe correo y contraseña"""
    datos = request.json
    aut = principal()
    mensaje = aut.login_usuario(datos)
    return mensaje
    
@app.route('/noticias/<int:op>', methods=['get', 'post'])
def noticias(op):
    
    datos = request.json
    aut = principal()
    
    """ CREATE """
    if op == 1 :
        "se recibe token, titulo y descripcion"
        mensaje = aut.crear_noticia(datos)
        return mensaje
    
    """ READ """
    if op == 2 :
        "se recibe token y id_persona"
        mensaje = aut.bus_noticia(datos)
        return mensaje
    
    """ UPDATE """
    if op == 3 :
        "se recibe token, id_noticia, titulo y descripcion"
        mensaje = aut.actualizar_noticia(datos)
        return mensaje
    
    """ DELETE """
    if op == 4 :
        "se recibe token, id_noticia"
        mensaje = aut.eli_noticia(datos)
        return mensaje
    
    return "Se ha recibido una operación no valida "

@app.route('/comentarios', methods=['get', 'post'])
def comentarios():
    
    datos = request.json
    aut = principal()
    mensaje = aut.crear_comentarios(datos)
    return mensaje
    
if __name__ == '__main__':
    app.run(debug=True)