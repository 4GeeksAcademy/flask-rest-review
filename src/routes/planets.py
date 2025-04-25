# Blueprint en Flask es una forma de organizar y reutilizar rutas o vistas.
# Permite separar la logica de defirentes partes de tu app en archivos o modulos distintos.
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError

from models import db, Planet

# Definimos el blueprint para agrupar todas las rutas de planetas
bp = Blueprint('planets', __name__, url_prefix='/planets')


@bp.route('/', methods=["GET"])
def get_all_planets():
    # Recorremos todos los planetas de la base de datos
    # query.all() -> select * from planet
    planets = Planet.query.all()
    # Serializamos la lista de planetas para enviarlas en un formato JSON
    return jsonify([planet.serialize() for planet in planets]), 200


@bp.route('/<int:planet_id>', methods=["GET"])
def get_planet(planet_id):
    # query.get_or_404() -> select * from planet where id = 'planet_id'
    planet = Planet.query.get_or_404(planet_id)
    return jsonify(planet.serialize()), 200


@bp.route('/', methods=["POST"])
def create_planet():
    data = request.json
    new_planet = Planet(
        name=data.get('name'),
        climate=data.get('climate'),
        terrain=data.get('terrain'),
        population=data.get('population'),
    )

    # Añadimos el nuevo planeta a la sesion y guardamos en la base de datos
    db.session.add(new_planet)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "El planeta ya existe"}), 409

    return jsonify(new_planet.serialize()), 201


@bp.route('/<int:planet_id>', methods=["PUT"])
def update_planet(planet_id):
    planet = Planet.query.get_or_404(planet_id)
    data = request.json

    # Actualizamos solo los campos que llegan en la solicitud (si no llegan, se mantiene el valor actual)
    planet.name = data.get('name', planet.name)
    planet.climate = data.get('climate', planet.climate)
    planet.terrain = data.get('terrain', planet.terrain)
    planet.population = data.get('population', planet.population)

    db.session.commit()

    return jsonify(planet.serialize()), 200


@bp.route('/<int:planet_id>', methods=["DELETE"])
def delete_planet(planet_id):
    planet = Planet.query.get_or_404(planet_id)
    db.session.delete(planet)
    db.session.commit()
    return '', 204
