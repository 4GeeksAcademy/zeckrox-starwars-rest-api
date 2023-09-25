from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password
            # do not serialize the password, its a security breach
        }
    
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False )
    gender = db.Column(db.String(10))
    birth_year = db.Column(db.String(10), nullable=False )
    hair_color = db.Column(db.String(20))
    skin_color = db.Column(db.String(20), nullable=False )
    eye_color = db.Column(db.String(20) )
    height = db.Column(db.Integer, nullable=False )
    mass = db.Column(db.Integer, nullable=False )

    def __repr__(self):
        return self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "height": self.height,
            "mass": self.mass
        }
    
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True )
    name = db.Column(db.String, nullable=False, unique=True )
    terrain = db.Column(db.String, nullable=False )
    climate = db.Column(db.String, nullable=False )
    population = db.Column(db.Integer, nullable=False )
    gravity = db.Column(db.String, nullable=False )
    diameter = db.Column(db.String, nullable=False )

    def __repr__(self):
        return self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain,
            "climate": self.climate,
            "population": self.population,
            "gravity": self.gravity,
            "diameter": self.diameter
        }
    
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False )
    user = db.relationship("User")
    people_id = db.Column(db.Integer, db.ForeignKey("people.id") )
    people = db.relationship("People")
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id") )
    planet = db.relationship("Planet")

    def __repr__(self):
        return f"User {self.user_id} favorites"

    def serialize(self):
        return {
            "user_id": self.user_id,
            "people_id": self.people_id if self.people else None,
            "people": self.people.name if self.people else None,
            "planet_id": self.planet_id if self.planet else None,
            "planet": self.planet.name if self.planet else None
        }