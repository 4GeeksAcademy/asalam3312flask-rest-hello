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
from models import db, User, People, Planets, Vehicles

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
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_people():
    characters = People.query.all()
    new_characters_list = []
    for character in characters:
         new_characters_list.append(character.serialize())  # es .serialize porque allá definimos qcuales son los datos que va a llamar de todos los que trae json
    return jsonify(new_characters_list), 200
    

@app.route('/people/<int:people_id>', methods=['GET'])
def get_character(people_id):       # acá debo colocar adentro de la función que es a lo que quiero llamar más adelante
        characters = People.query.all()
        new_character_list = []
        for character in characters:
            new_character_list.append(character.serialize())
        for one_character in new_character_list:
            if one_character["id"] == people_id:
                return jsonify(one_character), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    new_planets_list=[]
    for planet in planets:
        new_planets_list.append(planet.serialize())
    return jsonify(new_planets_list), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
        planets = Planets.query.all()
        new_planets_list = []
        for planet in planets:
            new_planets_list.append(planet.serialize())
        for one_planet in new_planets_list:
            if one_planet["id"] == planet_id:
                return jsonify(one_planet), 200

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    reponse_vehicles_body={
        "msg": "This is the vehicles info in /vehicles response"
    }
    return jsonify(reponse_vehicles_body)

@app.route('/vehicle/<int:id>', methods=['GET'])
def get_vehicle():
    one_vehicle = {
         "msg": "i'm just one vehicle"
    }

    return jsonify(one_vehicle)

@app.route('/users/favorites', methods=['GET'])
def favorites():
    users_favites={
        "msg": "the favorites"
    }
    return jsonify(users_favites)

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_planets():
    favorite_planets={
         "msg": "no favrites by now"
    }
    return jsonify(favorite_planets)

@app.route('/favorite/<int:people_id>', methods=['POST'])
def add_people(): 
     favorite_people={
          "msg": "no favorites by now"
     }
     return jsonify(favorite_people)

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet():
    delete={
        "msg": "done"
    }
    return jsonify(delete)

@app.route('/favorite/people/<int:people_id>')
def delete_people():
    delete_p={
        "msg": "done"
    }
    return jsonify(delete_p)
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
