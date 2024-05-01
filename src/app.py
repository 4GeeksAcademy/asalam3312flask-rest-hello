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
from models import db, User, Characters, Planets, Vehicles, Favorites

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
@app.route('/characters', methods=['GET'])
def get_characters():
    try:
        characters = Characters.query.all()
        new_characters_list = []
        for character in characters:
            new_characters_list.append(character.serialize())  # es serialize porque en esa función definimos en el archivo models.py cuales son los datos que va a llamar de todos los que trae json
        return jsonify(new_characters_list), 200
    except Exception as e:
        return jsonify({"error": str(e)})    

@app.route('/characters/<int:characters_id>', methods=['GET'])
def get_character(characters_id):       # acá debo colocar adentro de la función que es a lo que quiero llamar más adelante, lo que viene siendo lo mismo a lo que comparo con el _id
        try:
            characters = Characters.query.all()
            new_character_list = []
            for character in characters:
                new_character_list.append(character.serialize())
            for one_character in new_character_list:
                if one_character["id"] == characters_id:
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


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):                             # lo que tiene esta función como argumento es lo que me permitirá modificar el <int:planet_id>
    try:
        user_id = request.json.get("user_id")  # se hace una petición en formato json para obtener la información respecto a user_id
        
        if user_id is None:
            return jsonify({"msg": "missing 'user_id' in request JSON"}), 400
        if not planet_id or not user_id: 
            return jsonify({"msg": "to create a new favorite planet user_id and planets_id are requiered"}), 400
        
        new_favorite_planet = Favorites(user_id = user_id, planet_id=planet_id)  # se crea una nueva variable que contenga las igualdades de significancia entre el planets_id de models.py y el de acá (app.py) y de la misma manera con los users, donde el primero es el de models y el segundo el de app.py
        
        db.session.add(new_favorite_planet)     # se añade new_favorites en el clon
        db.session.commit()                    # se guarda en la base de datos original

        return jsonify({"done": "Favorite planet has been added succsesfully"}), 201        # unicamente es necesrio pasar en el postman el id del planeta en el URL y el user_id:<int:user_id> en el body
    
    except Exception as e:
        return jsonify(str(e)), 500
            

@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):
    try:
        user_id = request.json.get("user_id")       # petición de información user_id contenida en el body
        
        if not user_id or not character_id:
            return jsonify({"msg": "to create a favorite chatacter, user_id and character_id are requiered"}), 400      # manejo de errores
        
        new_favorite_character = Favorites(user_id=user_id, character_id=character_id)      # variable que crea dentro de Favorites una equivalencia entre valores de models.py y app.py
        
        db.session.add(new_favorite_character)      # se añade la función de equivalencias en el clon
        db.session.commit()                        # se guarda primero en el clon y luego en la base de datos
        
        return jsonify({"done": "Favorite character has been added succesfully"}), 201
    except Exception as e:
        return jsonify(str(e)), 500

@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['POST'])
def add_favorite_vehicle(vehicle_id):
    try:
        user_id= request.json.get("user_id")

        if not user_id or not vehicle_id:
            return jsonify({"msg": "to add a favorite vehicle, user_id and vehicle_id are requiered"}), 400
        
        new_favorite_vehicle = Favorites(user_id=user_id, vehicle_id=vehicle_id)

        db.session.add(new_favorite_vehicle)
        db.session.commit()

        return jsonify({"done": "Favorite vehicle has been submited succesfully"}),201
    except Exception as e:
        return jsonify(str(e)), 500   


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    try:
        user_id = request.json.get("user_id")       # se solicita un usuario especifico del cual se va a eliminar el favorito                                               
        if not user_id:
            return jsonify({"msg": "the 'user_id' is missing from the request"}), 400    # si no existe 400
        
        favorite_planet = Favorites.query.filter_by(user_id=user_id, planet_id=planet_id).first()       # en se manda una petición que hace filtrado en Favorites, el filtrado busca que haya equivalencia entre user_id y planet_id
        
        if favorite_planet is None:
            return jsonify({"msg": "the favorite planet with given user_id and planet_id does not exist"}), 404     # si no hay planeta registrado a ese usuario 404 not found

        db.session.delete(favorite_planet)      #  se hace un borrado de lo obtenido con favorite planet y se guarda en el clon
        db.session.commit()                     # guardado en base de datos

        return jsonify({"done": "the favorite planet has been deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    try:
        user_id = request.json.get("user_id")

        if not user_id:
            return jsonify({"msg": "the 'user_id' is missing from the request"}), 400
        
        favorite_character = Favorites.query.filter_by(user_id=user_id, character_id=character_id).first()
        
        if favorite_character is None:
            return jsonify({"msg": "the favorite character with given user_id and character_id does not exist"}), 404
        
        db.session.delete(favorite_character)
        db.session.commit()
        
        return jsonify({"done": "the favorite character has been deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    

@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    try:
        user_id = request.json.get("user_id")
        if not user_id:
            return jsonify({"msg": "the 'user_id' is missing from the request"}), 400
        
        favorite_vehicle = Favorites.query.filter_by(user_id=user_id, vehicle_id=vehicle_id).first()
        
        if favorite_vehicle is None:
            return jsonify({"msg": "the favorite vehicle with given user_id and vehicle_id does not exist"}), 404

        db.session.delete(favorite_vehicle)
        db.session.commit()

        return jsonify({"done": "the favorite vehicle has been deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
