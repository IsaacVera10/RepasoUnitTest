import unittest
from flask import Flask
import app

class TestMensajeriaApp(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_obtener_contactos_exitoso(self):
        """
        Caso de prueba exitoso para la función obtener_contactos.
        Debe devolver una lista de contactos en formato HTML.
        """
        response = self.app.get('/mensajeria/contactos?mialias=cpaz')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "lmunoz: Luisa<br>mgrau: Miguel")

    def test_enviar_mensaje_error_usuario_no_encontrado(self):
        """
        Caso de prueba de error para la función enviar_mensaje.
        Debe devolver un mensaje de error si el usuario emisor no está registrado.
        """
        response = self.app.get('/mensajeria/enviar?mialias=usuario1&aliasdestino=cpaz&texto=Hola')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Usuario no encontrado", response.data.decode())

    def test_enviar_mensaje_error_destino_no_encontrado(self):
        """
        Caso de prueba de error para la función enviar_mensaje.
        Debe devolver un mensaje de error si el usuario receptor no está registrado.
        """
        response = self.app.get('/mensajeria/enviar?mialias=cpaz&aliasdestino=usuario2&texto=Hola')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Usuario no encontrado", response.data.decode())

    def test_obtener_mensajes_recibidos_error_usuario_no_encontrado(self):
        """
        Caso de prueba de error para la función obtener_recibidos.
        Debe devolver un mensaje de error si el usuario no está registrado.
        """
        response = self.app.get('/mensajeria/recibidos?mialias=usuario1')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Usuario no encontrado", response.data.decode())

if __name__ == '__main__':
    unittest.main()
