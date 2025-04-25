# Blueprint en Flask es una forma de organizar y reutilizar rutas o vistas.
# Permite separar la logica de defirentes partes de tu app en archivos o modulos distintos.
from flask import Blueprint, request, jsonify

from models import db, Film

# Definimos el blueprint para agrupar todas las rutas de peliculas
bp = Blueprint('films', __name__, url_prefix='/films')


@bp.route('/', methods=["GET"])
def get_all_films():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@bp.route('/<int:film_id>', methods=["GET"])
def get_film(film_id):
    return ""


@bp.route('/', methods=["POST"])
def create_film():
    return ""


@bp.route('/<int:film_id>', methods=["PUT"])
def update_film(film_id):
    return ""


@bp.route('/<int:film_id>', methods=["DELETE"])
def delete_film(film_id):
    return ""
