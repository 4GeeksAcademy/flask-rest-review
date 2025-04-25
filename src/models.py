from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Creamos una instancia de SQLAlchemy para gestionar la conexion y los modelos de la base de datos.
db = SQLAlchemy()

# Tabla de asociacion para la relacion "muchos a muchos" entre personas (People) y peliculas (Film)
people_films = Table(
    "people_films",
    db.Model.metadata,
    db.Column("people_id", Integer, ForeignKey("people.id"), primary_key=True),
    db.Column("film_id", Integer, ForeignKey("film.id"), primary_key=True)
)

# Tabla de asociacion para la relacion "muchos a muchos" entre planetas (People) y peliculas (Film)
planet_films = Table(
    "planet_films",
    db.Model.metadata,
    db.Column("planet_id", Integer, ForeignKey("planet.id"), primary_key=True),
    db.Column("film_id", Integer, ForeignKey("film.id"), primary_key=True)
)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Planet(db.Model):
    # __tablename__ es un atributo especial que se define en una clase modelo de SQLAlchemy
    # para indicar el nombre de la tabla que tendra esa clase en la base de datos.
    __tablename__ = "planet"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    # Nombre del planeta (unico y obligatorio)
    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    # Clima del planeta (puede estar vacio)
    climate: Mapped[str] = mapped_column(String(50), nullable=True)
    terrain: Mapped[str] = mapped_column(
        String(50), nullable=True)  # Terreno (puede estar vacio)
    population: Mapped[str] = mapped_column(
        String(50), nullable=True)  # Poblacion (puede estar vacio)

    # Relacion "uno a muchos": un planeta tiene muchos residentes (personas (people))
    # People es el nombre de la clase destino
    # back_populates="homeworld" -> Indica que la relacion es bidireccional: en la clase People debe haber una columna
    # homeworld con su propio relationship apuntando de regreso a Planet
    # cascade="all, delete" -> Indica que si eliminas un planeta, automaticamente se eliminaran todos los residentes
    # asociados a ese planete en la base de datos
    residents = relationship(
        "People", back_populates="homeworld", cascade="all, delete")

    # Relacion "muchos a muchos": un planeta aparece en muchas peliculas
    # Film es el nombre de la clase destino
    # secondary=planet_films -> Aqui le dices a SQLAlchemy que la relacion entre Planet y Film es "muchos a muchos"
    # y usa una tabla intermedia llamada 'planet_films'
    # back_populates="planets" -> Indica que la relacion es bidireccional: en la clase Film debe haber una columna
    # planets con su propio relationship apuntando de regreso a Planet
    films = relationship("Film", secondary=planet_films,
                         back_populates="planets")

    def serialize(self):
        # Convierte el objeto planeta en un diccionario para poder enviarlo en formato JSON.
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
            # Lista de IDs de los residentes del planeta (relacion uno-a-muchos)
            "residents": [resident.id for resident in self.residents],
            # Lista de IDs de peliculas en las que aparece el planet (relacion muchos-a-muchos)
            "films": [film.id for film in self.films],
        }


class People(db.Model):
    # __tablename__ es un atributo especial que se define en una clase modelo de SQLAlchemy
    # para indicar el nombre de la tabla que tendra esa clase en la base de datos.
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    # Nombre de la persona (obligatorio)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    height: Mapped[str] = mapped_column(
        String(10), nullable=True)  # Altura (1.68m o "unknown")
    mass: Mapped[str] = mapped_column(
        String(10), nullable=True)  # Peso (68kg o "unknown")
    gender: Mapped[str] = mapped_column(String(10), nullable=True)  # Genero

    # Clave foranea a la talba de planetas para indicar el planeta natal
    planet_id: Mapped[int] = mapped_column(Integer, ForeignKey('planet.id'))

    # Relacion inversa: el planeta natal de la persona
    homeworld = relationship("Planet", back_populates="residents")

    # Relacion "muchos a muchos": un persona aparece en muchas peliculas
    # Film es el nombre de la clase destino
    # secondary=people_films -> Aqui le dices a SQLAlchemy que la relacion entre People y Film es "muchos a muchos"
    # y usa una tabla intermedia llamada 'people_films'
    # back_populates="characters" -> Indica que la relacion es bidireccional: en la clase Film debe haber una columna
    # characters con su propio relationship apuntando de regreso a People
    films = relationship("Film", secondary=people_films,
                         back_populates="characters")

    def serialize(self):
        # Convierte el objeto planeta en un diccionario para poder enviarlo en formato JSON.
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "gender": self.gender,
            "homeworld": self.planet_id,  # Solo el ID del planeta natal
            # Lista de IDs de peliculas en las que aparece la persona (relacion muchos-a-muchos)
            "films": [film.id for film in self.films],
        }


class Film(db.Model):
    # __tablename__ es un atributo especial que se define en una clase modelo de SQLAlchemy
    # para indicar el nombre de la tabla que tendra esa clase en la base de datos.
    __tablename__ = "film"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    # Titulo de la pelicula (unico y obligatorio)
    title: Mapped[str] = mapped_column(
        String(120), nullable=False, unique=True)
    director: Mapped[str] = mapped_column(
        String(120), nullable=True)  # Nombre del director
    release_date: Mapped[str] = mapped_column(
        String(20), nullable=True)  # Fecha de lanzamiento (texto)

    characters = relationship(
        "People", secondary=people_films, back_populates="films")

    planets = relationship(
        "Planet", secondary=planet_films, back_populates="films")

    def serialize(self):
        # Convierte el objeto planeta en un diccionario para poder enviarlo en formato JSON.
        return {
            "id": self.id,
            "title": self.title,
            "director": self.director,
            "release_date": self.release_date,
            # Lista de IDs de personajes que aparecen en la pelicula
            "characters": [character.id for character in self.characters],
            # Lista de IDs de planetas que aparecen en la pelicula
            "planets": [planet.id for planet in self.planets],
        }
