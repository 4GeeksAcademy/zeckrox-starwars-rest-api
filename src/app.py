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
from models import db, User, Planet, People, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints

@app.route("/")# Aquí definimos el primer path de la API: GET /
def sitemap():
    return generate_sitemap(app)

#PEOPLE

#GET ALL CHARACTERS
@app.route("/people", methods=["GET"])
def get_people():
    try:
        all_people = People.query.all()
        return [character.serialize() for character in all_people]
    
    except ValueError as err:
        return {"message": "failed to retrieve planet " + err}, 500

#GET A CHARACTER BY ID
@app.route("/people/<int:people_id>", methods=["GET"])
def get_people_id(people_id):
    try:
        selected_people = People.query.get(people_id) or None
        if selected_people == None:
            return {"message": f"Character with id {people_id} does not exist"}, 400
        else:
            return selected_people.serialize()
        
    except ValueError as err:
        return {"message": "failed to retrieve people " + err}, 500

#POST A CHARACTER
@app.route("/people", methods=["POST"])
def post_people():
    try:
        body = request.get_json()

        name = body.get("name", None)
        gender = body.get ("gender", None)
        birth_year = body.get ("birth_year", None)
        hair_color = body.get ("hair_color", None)
        skin_color = body.get ("skin_color", None)
        eye_color = body.get ("eye_color", None)
        height = body.get ("height", None)
        mass = body.get ("mass", None)
        
        people_required_info = (name, birth_year, skin_color, height, mass)
        for key in people_required_info:
            if key == None: return {"message": "Some field is missing in request body"}, 400
        
        new_people = People( name=name, gender=gender, birth_year=birth_year, hair_color=hair_color, skin_color=skin_color, eye_color=eye_color, height=height, mass=mass )
        db.session.add(new_people)
        db.session.commit()
        return new_people.serialize(), 200
    
    except ValueError as err:
        return {"message": "failed to retrieve planet " + err}, 500
    
#DELETE A CHARACTER
@app.route("/people/<int:people_id>", methods=["DELETE"])
def delete_people(people_id):
    try:
        selected_people = People.query.get(people_id) or None
        if selected_people == None:
            return {"message": f"Planet with id {people_id} does not exist"}, 400
        else:
            db.session.delete(selected_people)
            db.session.commit()
            return {"message": f"{selected_people.serialize()['name']} has been deleted"}, 200
        
    except ValueError as err:
        return {"message": "failed to retrieve people " + err}, 500


#PLANETS

#GET ALL PLANETS
@app.route("/planets", methods=["GET"])
def get_planets():
    try:
        all_planets = Planet.query.all()
        return [planet.serialize() for planet in all_planets]
    
    except ValueError as err:
        return {"message": "failed to retrieve planet " + err}, 500

#GET A SPECIFIC PLANET BY ID
@app.route("/planets/<int:planet_id>", methods=["GET"])
def get_planet_id(planet_id):
    try:
        selected_planet = Planet.query.get(planet_id) or None
        if selected_planet == None:
            return {"message": f"Planet with id {planet_id} does not exist"}, 400
        else:
            return selected_planet.serialize()
        
    except ValueError as err:
        return {"message": "failed to retrieve planet " + err}, 500

#POST A PLANET
@app.route("/planets", methods=["POST"])
def post_planet():
    try:
        body = request.get_json()
        
        name = body.get("name", None)
        terrain = body.get ("terrain", None)
        climate = body.get ("climate", None)
        population = body.get ("population", None)
        gravity = body.get ("gravity", None)
        diameter = body.get ("diameter", None)

        planet_required_info = (name, terrain, climate, population, gravity, diameter)
        for key in planet_required_info:
            if key == None: return {"message": "Some field is missing in request body"}, 400
        
        new_planet = Planet( name=name, terrain=terrain, climate=climate, population=population, gravity=gravity, diameter=diameter )
        db.session.add(new_planet)
        db.session.commit()
        return new_planet.serialize(), 200
    
    except ValueError as err:
        return {"message": "failed to retrieve planet " + err}, 500

#DELETE A PLANET
@app.route("/planets/<int:planet_id>", methods=["DELETE"])
def delete_planet(planet_id):
    try:
        selected_planet = Planet.query.get(planet_id) or None
        if selected_planet == None:
            return {"message": f"Planet with id {planet_id} does not exist"}, 400
        else:
            db.session.delete(selected_planet)
            db.session.commit()
            return {"message": f"{selected_planet.serialize()['name']} has been deleted"}, 200
        
    except ValueError as err:
        return {"message": "failed to retrieve people " + err}, 500


#USERS

#GET ALL USERS
@app.route("/users", methods=["GET"])
def get_users():
    try:
        all_users = User.query.all()
        return [user.serialize() for user in all_users]

    except ValueError as err:
        return {"message": "failed to retrieve planet " + err}, 500

#GET USER BY ID 
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user_id(user_id):
    try:
        selected_user = User.query.get(user_id) or None
        if selected_user == None:
            return {"message": f"User with id {user_id} does not exist"}
        else:
            return selected_user.serialize()
    
    except ValueError as err:
        return {"message": "failed to retrieve user " + err}, 500


#FAVORITES

#GET ALL FAVORITES FROM USER
@app.route("/users/<int:user_id>/favorites", methods=["GET"])
def get_favorites(user_id):
    try:
        user_favorites = Favorite.query.filter(Favorite.user_id == user_id)
        return [favorite.serialize() for favorite in user_favorites]
        
    except ValueError as err:
        return {"message": "failed to retrieve user " + err}, 500
    
#FAVORITE PLANET

#POST A FAVORITE PLANET FOR AN USER
@app.route("/users/<int:user_id>/favorites/planet/<int:planet_id>", methods=["POST"])
def post_favorite_planet(user_id, planet_id):   
    try:
        planet = Planet.query.get(planet_id)
        same_planet = Favorite.query.filter(Favorite.planet_id == planet_id, Favorite.user_id == user_id)
        same_planet = [planet.serialize() for planet in same_planet]
        if same_planet:
            return {"message": f"{same_planet[0]['planet']} is already on favorites"}
        elif not planet:
            return {"message": f"People with ID:{planet_id} doesn't exist"}
        else:
            new_favorite = Favorite( user_id=user_id, planet_id=planet_id, planet=planet )
            db.session.add(new_favorite)
            db.session.commit()
            return new_favorite.serialize() , 200
    
    except ValueError as err:
        return {"message": "failed to retrieve planet " + err}, 500

#DELETE A FAVORITE PLANET FOR AN USER
@app.route("/users/<int:user_id>/favorites/planet/<int:planet_id>", methods=["DELETE"])
def delete_favorites_planet(user_id, planet_id):
    try:
        selected_favorite = Favorite.query.filter(Favorite.user_id == user_id, Favorite.planet_id == planet_id)
        for favorite in selected_favorite:
            db.session.delete(favorite)
        db.session.commit()

        user_favorites = Favorite.query.filter(Favorite.user_id == user_id)
        return [favorite.serialize() for favorite in user_favorites]
        
    except ValueError as err:
        return {"message": "failed to retrieve user " + err}, 500
    

#FAVORITE CHARACTER

#POST A FAVORITE CHARACTER FOR AN USER
@app.route("/users/<int:user_id>/favorites/people/<int:people_id>", methods=["POST"])
def post_favorite_people(user_id, people_id):
    try:
        character = People.query.get(people_id)
        same_character = Favorite.query.filter(Favorite.people_id == people_id, Favorite.user_id == user_id)
        same_character = [people.serialize() for people in same_character]
        if same_character:
            return {"message": f"{same_character[0]['people']} is already on favorites"}
        elif not character:
            return {"message": f"People with ID:{people_id} doesn't exist"}
        else:
            new_favorite = Favorite( user_id=user_id, people_id=people_id, people=character )
            db.session.add(new_favorite)
            db.session.commit()
            return new_favorite.serialize() , 200
    
    except ValueError as err:
        return {"message": "failed to retrieve planet " + err}, 500

#DELETE A FAVORITE CHARACTER FOR AN USER
@app.route("/users/<int:user_id>/favorites/people/<int:people_id>", methods=["DELETE"])
def delete_favorites_people(user_id, people_id):
    try:
        selected_favorite = Favorite.query.filter(Favorite.user_id == user_id, Favorite.people_id == people_id)
        for favorite in selected_favorite:
            db.session.delete(favorite)
        db.session.commit()

        user_favorites = Favorite.query.filter(Favorite.user_id == user_id)
        return [favorite.serialize() for favorite in user_favorites]
        
    except ValueError as err:
        return {"message": "failed to retrieve user " + err}, 500


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
