"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from routes import planets, people, films
# from models import Person

app = Flask(__name__)  # Instanciamos la app de Flask
app.url_map.strict_slashes = False

# Extramos de una variable de entorno (.env) la cada de conexion
db_url = os.getenv("DATABASE_URL")

# Realiza una validacion de la db_url
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

# Recomendado para evitar advertencias innecesar de SQLAlchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializamos Flask-Migrate para gestionar las migraciones
MIGRATE = Migrate(app, db)
db.init_app(app)  # Incilizamos la conexion de SQLAlchemy con al app Flask
CORS(app)  # Activar los CORS (https)
setup_admin(app)

# Registrar los "blueprints" de rutas para separar los endpoints en archivos diferentes
app.register_blueprint(planets.bp)
app.register_blueprint(people.bp)
app.register_blueprint(films.bp)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
