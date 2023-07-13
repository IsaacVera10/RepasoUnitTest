from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

class Usuario:
    def __init__(self, alias, nombre, contactos):
        self.alias = alias
        self.nombre = nombre
        self.contactos = contactos
        self.mensajes_recibidos = []

    def recibidos(self):
        return self.mensajes_recibidos

    def enviarmensaje(self, alias_destino, texto):
        mensaje = Mensaje(self.alias, alias_destino, texto)
        self.mensajes_recibidos.append(mensaje)

class Mensaje:
    def __init__(self, alias_remitente, alias_destino, texto):
        self.alias_remitente = alias_remitente
        self.alias_destino = alias_destino
        self.fecha = None
        self.texto = texto

BD = []
BD.append(Usuario("cpaz", "Christian", ["lmunoz", "mgrau"]))
BD.append(Usuario("lmunoz", "Luisa", ["mgrau"]))
BD.append(Usuario("mgrau", "Miguel", ["cpaz"]))

@app.route('/mensajeria/contactos', methods=['GET'])
def obtener_contactos():
    mialias = request.args.get('mialias')
    for usuario in BD:
        if usuario.alias == mialias:
            contactos = usuario.contactos
            nombres_contactos = []
            for contacto in contactos:
                for u in BD:
                    if u.alias == contacto:
                        nombres_contactos.append(f"{contacto}: {u.nombre}")
                        break
            return '<br>'.join(nombres_contactos)
    return "Usuario no encontrado"

@app.route('/mensajeria/enviar', methods=['GET'])
def enviar_mensaje():
    mialias = request.args.get('mialias')
    aliasdestino = request.args.get('aliasdestino')
    texto = request.args.get('texto')
    remitente = next((usuario for usuario in BD if usuario.alias == mialias), None)
    destinatario = next((usuario for usuario in BD if usuario.alias == aliasdestino), None)
    if remitente and destinatario:
        mensaje = Mensaje(remitente.alias, destinatario.alias, texto)
        destinatario.mensajes_recibidos.append(mensaje)
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        mensaje.fecha = fecha_actual
        return f"Mensaje enviado en {fecha_actual}"
    return "Usuario no encontrado"

@app.route('/mensajeria/recibidos', methods=['GET'])
def obtener_recibidos():
    mialias = request.args.get('mialias')
    for usuario in BD:
        if usuario.alias == mialias:
            recibidos = usuario.recibidos()
            mensajes = []
            for mensaje in recibidos:
                remitente = next((usuario for usuario in BD if usuario.alias == mensaje.alias_remitente), None)
                if remitente:
                    fecha = mensaje.fecha
                    mensaje_formatado = f"{remitente.nombre} te escribió '{mensaje.texto}' el {fecha}."
                    mensajes.append(mensaje_formatado)
            return '<br>'.join(mensajes)
    return "Usuario no encontrado"

if __name__ == '__main__':
    app.run()
