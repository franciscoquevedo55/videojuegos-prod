import os
import unittest
from flask import Flask
from models import db
from api.routes import api  # <-- Importar el Blueprint real con tus rutas


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "TEST_DATABASE_URL",
            "sqlite:///:memory:"
        )
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        db.init_app(self.app)
        self.app.register_blueprint(api, url_prefix="/api")

        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_obtener_juegos(self):
        respuesta = self.client.get("/api/juegos")
        self.assertEqual(respuesta.status_code, 200)

    def test_agregar_juego(self):
        datos = {
            "nombre": "Minecraft",
            "descripcion": "Juego de construccion",
            "precio": 599
        }

        respuesta = self.client.post("/api/juegos", json=datos)
        self.assertEqual(respuesta.status_code, 201)

    def test_obtener_juego(self):
        datos = {
            "nombre": "Minecraft",
            "descripcion": "Juego de construccion",
            "precio": 599
        }

        respuesta = self.client.post("/api/juegos", json=datos)
        id_juego = respuesta.json["id"]

        respuesta = self.client.get(f"/api/juegos/{id_juego}")
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json["nombre"], "Minecraft")

    def test_modificar_juego(self):
        datos = {
            "nombre": "Minecraft",
            "descripcion": "Juego de construccion",
            "precio": 599
        }

        respuesta = self.client.post("/api/juegos", json=datos)
        id_juego = respuesta.json["id"]

        datos["nombre"] = "Minecraft actualizado"

        respuesta = self.client.put(f"/api/juegos/{id_juego}", json=datos)
        self.assertEqual(respuesta.status_code, 200)

    def test_eliminar_juego(self):
        datos = {
            "nombre": "Minecraft",
            "descripcion": "Juego de construccion",
            "precio": 599
        }

        respuesta = self.client.post("/api/juegos", json=datos)
        id_juego = respuesta.json["id"]

        respuesta = self.client.delete(f"/api/juegos/{id_juego}")
        self.assertEqual(respuesta.status_code, 204)


if __name__ == "__main__":
    unittest.main()
