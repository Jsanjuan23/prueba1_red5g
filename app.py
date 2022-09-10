from flask import Flask,redirect,url_for,render_template,request
from metodos import principal
from respuesta import msj

app=Flask(__name__)


@app.route('/')
def home():
 
    return "Hola mundo"

@app.route('/registrar', methods=['post'])
def registrar():
    
    datos = request.json
    aut = principal()
    mensaje = aut.crear_usuario(datos)
    return msj(mensaje=mensaje)


@app.route('/login', methods=['post'])
def login():
    
    datos = request.json
    aut = principal()
    mensaje = aut.login_usuario(datos)
    return msj(mensaje=mensaje)

@app.route('/noticias/<int:op>', methods=['post','get'])
def noticias(op):
    
    if op == 1 :
        datos = request.json
        aut = principal()
        mensaje = aut.bus_noticias(datos)
        return mensaje
    if op == 2 : 
        datos = request.json
        aut = principal()
        mensaje = aut.crear_noticias(datos)
        return mensaje
    if op == 3 :
        datos = request.json
        aut = principal()
        mensaje = aut.act_noticias(datos)
        return mensaje
    if op == 4 :
        datos = request.json
        aut = principal()
        mensaje = aut.eli_noticias(datos)
        return mensaje
    return msj(True, mensaje="No ha ingresado una operación válida.")

@app.route('/comentarios', methods=['post'])
def comentario():
    
    datos = request.json
    aut = principal()
    mensaje = aut.crear_comentario(datos)
    return msj(True,mensaje=mensaje)
    
if __name__ == '__main__':
   
    app.run(debug=True)