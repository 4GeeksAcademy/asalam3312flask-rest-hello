from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), unique=False, nullable=False)
    last_name = db.Column(db.String(50), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "name": self.name,
            "last_name": self.last_name
            # do not serialize the password, its a security breach
        }
    
# favorites_planets = db.Table('favorites_planets', 
#     db.Column('favorite_id', db.Integer, db.Foreignkey('favorites_id'), pimary_key=True),
#     db.Column('planet_id', db.Integer, db.Foreignkey('planets.id'), primary_key = True))

favorites_planets = db.Table('favorites_planets',
    db.Column('favorite_id', db.Integer, db.ForeignKey('favorites.id'), primary_key=True),
    db.Column('planet_id', db.Integer, db.ForeignKey('planets.id'), primary_key=True)
)


# class Favorites(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     user = db.relationship(User)
#     planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
#     planets = db.relationship('Planets', secondary=favorites_planets, backref=db.backref('favorites', lazy='dynamic'))

#     def __repr__(self):
#         return '<Favorites %r>' % self.id

#     def serialize(self):
#         return {
#             "id": self.id,
#             "user_id": self.user_id,        #  Es mejor no serializar "user" como tal porque es un objeto complejo, para lograr que sea funcional basta con el id de user
#             # do not serialize the password, its a security breach
#         }
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)                                                        # La relación entre esta tabla con User

    # El backref en la relación
    favorite_planets = db.relationship('Planets', secondary = favorites_planets, lazy = 'subquery',
        backref=db.backref('favorite_entries', lazy=True))

    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
        }



class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    hair_color = db.Column(db.String(40), unique=False, nullable=False)
    eye_color = db.Column(db.String(40), unique=False, nullable=False)
    skin_color = db.Column(db.String(50), unique=False, nullable=False)
    gender = db.Column(db.String(50), unique=False, nullable=False)
    favorites_id = db.Column(db.Integer, db.ForeignKey('favorites.id'))
    favorites = db.relationship(Favorites)
 
    def __character_repr__(self):
        return '<People %r' % self.id
    
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "skin_color": self.skin_color,
            "gender": self.gender
        }
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    gravity = db.Column(db.String(80), unique=False, nullable=True)
    population = db.Column(db.Integer, unique=False, nullable=True)
    climate = db.Column(db.String(80), unique=False, nullable=True)
    diameter = db.Column(db.Integer, unique=False, nullable=True)    
    favorites_id = db.Column(db.Integer, db.ForeignKey('favorites.id'))
    favorites = db.relationship(Favorites)
    def __repr__(self):
        return '<Planets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "diameter": self.diameter
            # do not serialize the password, its a security breach
        }

class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    model = db.Column(db.String(80), unique=False, nullable=True)
    passengers = db.Column(db.Integer, unique=False, nullable=True)
    cost_in_credits = db.Column(db.String(80), unique=False, nullable=True)
    crew = db.Column(db.Integer, unique=False, nullable=True)
    length = db.Column(db.Integer, unique=False, nullable=True)
    favorites_id = db.Column(db.Integer, db.ForeignKey('favorites.id'))
    favorites = db.relationship(Favorites) 

    def __repr__(self):
        return '<Vehicles %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "passengers": self.passengers,
            "cost_in_credits": self.cost_in_credits,
            "crew": self.crew,
            "length": self.length
            # do not serialize the password, its a security breach
        }
