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
from models import db, User, People, Planets, Vehicles, Favorites

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

@app.route('/users', methods=['GET'])        
def handle_hello():
    try:
        users = User.query.all()
        new_user=[]
        for user in users:
            new_user.append(user.serialize())
        return jsonify(new_user), 200
    except  Exception as e:
        return jsonify({"error": str(e)})
@app.route('/people', methods=['GET'])
def get_people():
    try:
        characters = People.query.all()
        new_characters_list = []
        for character in characters:
            new_characters_list.append(character.serialize())  # es serialize porque en esa función definimos en el archivo models.py cuales son los datos que va a llamar de todos los que trae json
        return jsonify(new_characters_list), 200
    except Exception as e:
        return jsonify({"error": str(e)})    

@app.route('/people/<int:people_id>', methods=['GET'])
def get_character(people_id):       # acá debo colocar adentro de la función que es a lo que quiero llamar más adelante, lo que viene siendo lo mismo a lo que comparo con el _id
        try:
            characters = People.query.all()
            new_character_list = []
            for character in characters:
                new_character_list.append(character.serialize())
            for one_character in new_character_list:
                if one_character["id"] == people_id:
                    return jsonify(one_character), 200
        except Exception as e:
            return jsonify({"error": str(e)})
@app.route('/planets', methods=['GET'])
def get_planets():
    try:
        planets = Planets.query.all()
        new_planets_list=[]
        for planet in planets:
            new_planets_list.append(planet.serialize())
        return jsonify(new_planets_list), 200
    except Exception as e:
        return jsonify({"error": str(e)})
@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
        try:
            planets = Planets.query.all()
            new_planets_list = []
            for planet in planets:
                new_planets_list.append(planet.serialize())
            for one_planet in new_planets_list:
                if one_planet["id"] == planet_id:
                    return jsonify(one_planet), 200
        except Exception as e:
            return jsonify({"error": str(e)})
@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    try:
        vehicles = Vehicles.query.all()
        new_vehicles_list = []
        for vehicle in vehicles:
            new_vehicles_list.append(vehicle.serialize())
        return jsonify(new_vehicles_list), 200
    except Exception as e:
        return jsonify({"error": str(e)})
@app.route('/vehicle/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    try:
        vehicles = Vehicles.query.all()
        new_vehicles = []
        for vehicle in vehicles:
            new_vehicles.append(vehicle.serialize())
        for one_vehicle in new_vehicles:
            if one_vehicle["id"] == vehicle_id:
                return jsonify(one_vehicle), 200
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/users/favorites', methods=['GET'])         
def favorites():
    try:
        get_favorites = Favorites.query.all()
        new_favorites = []
        for favorite in get_favorites:
            new_favorites.append(favorite.serialize())
        return jsonify(new_favorites)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/favorite/planet/<int:favorite_id>', methods=['POST'])      
def add_planets(favorite_id):
    try:
        favorite = Favorites.query.get_or_404(favorite_id)      # se obtiene el objeto de Favorites con el id dado (si existe lo obtiene, si no 404)

        planet_id = request.json.get('planet_id')                              # se obtiene la data de planet en formato json

        if Planets.query.filter_by(id=planet_id).first()in favorite.planets:
            return jsonify({"error": "This planes is already in favorites list"}), 400       # se verifica que el planeta no esté en favoritos, en caso de estar se arroja error
        
        planet = Planets.query.get_or_404(planet_id)            # se hace la solicitud del objeto de Planets correspondiente al id dado

        favorite.favorite_planets.append(planet)
        db.session.commit()                                     # se agrega el planeta a los favoritos del usuario


        
        return jsonify({"done": "favorite planet has been added"}),200
    except Exception as e:
        return jsonify({"error": str(e)})  


    
            

@app.route('/favorite/<int:people_id>', methods=['POST'])       # por ende no puedo probar este tampoco
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

# @app.route('/favorite/vehicle/<int:planet_id')
# def get_favorite_vehicle():
#     favorite_v={
#         "msg": "true"
#     }
#     return jsonify(favorite_v)
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
