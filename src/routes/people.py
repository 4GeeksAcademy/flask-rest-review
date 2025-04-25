# Blueprint en Flask es una forma de organizar y reutilizar rutas o vistas.
# Permite separar la logica de defirentes partes de tu app en archivos o modulos distintos.
from flask import Blueprint, request, jsonify

from models import db, People, Planet

# Definimos el blueprint para agrupar todas las rutas de personas
bp = Blueprint('peoples', __name__, url_prefix='/peoples')


@bp.route('/', methods=["GET"])
def get_all_peoples():
    peoples = People.query.all()

    return jsonify([person.serialize() for person in peoples]), 200


@bp.route('/<int:people_id>', methods=["GET"])
def get_people(people_id):
    return ""


@bp.route('/', methods=["POST"])
def create_people():
    data = request.json

    planet_id = data.get('homeworld')
    planet = Planet.query.get(planet_id) if planet_id else None

    new_person = People(
        name=data.get('name'),
        height=data.get('height'),
        mass=data.get('mass'),
        gender=data.get('gender'),
        homeworld=planet
    )

    db.session.add(new_person)
    db.session.commit()

    return jsonify(new_person.serialize()), 200


@bp.route('/<int:people_id>', methods=["PUT"])
def update_people(people_id):
    person = People.query.get_or_404(people_id)
    data = request.json

    person.name = data.get('name', person.name),
    person.height = data.get('height', person.height),
    person.mass = data.get('mass', person.mass),
    person.gender = data.get('gender', person.gender),

    if 'homeworld' in data:
        planet = Planet.query.get(data['homeworld'])
        planet.homeworld = planet

    db.session.commit()

    return jsonify(person.serialize()), 200


@bp.route('/<int:people_id>', methods=["DELETE"])
def delete_people(people_id):
    return ""
