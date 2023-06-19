#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

# need to install with: pipenv install flask-restful
# from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

migrate = Migrate(app, db)

db.init_app(app)

# resful stuff... need to go back to models and refer back to to_dict
# api = Api(app)

# class Animals(Resource):
#     def get(self):
#         animal = [animal.to_dict() for animal in Animal.query.all()]
#         return make_response(jsonify(animal), 200)
# api.add_resource(Animals, '/animal')

# class AnimalById(Resource):
#     def get(self, id):
#         if animal:= Animal.query.get(id):
#             return make_response(animal.to_dict(), 200)
#         else:
#             raise Exception('cant do that lol')
# api.add_resource(AnimalById, '/animal/<int:id>')

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    # animal = Animal.query.get(id)
    # animal = Animal.query.filter_by(id=id).first_or_404()
    # animal = Animal.query.filter(Animal.id==id).first_or_404()
    # if animal:= Animal.query.get(id):
    if animal:= db.session.get(Animal, id):
        response_body = f"""
            <ul>ID: {animal.id}</ul>
            <ul>Name: {animal.name}</ul>
            <ul>Species: {animal.species}</ul>
            <ul>Zookeeper: {animal.zookeeper.name}</ul>
            <ul>Enclosure: {animal.enclosure.environment}</ul>
        """
        return make_response(response_body, 200)
    else:
        response_body = f"""
            <ul>404 Not Found any animals with id {id}</ul>
        """
        return make_response(response_body, 404)

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    if zk:= db.session.get(Zookeeper, id):
        response_body = f"""
            <ul>ID: {zk.id}</ul>
            <ul>Name: {zk.name}</ul>
            <ul>Birthday: {zk.birthday}</ul>
        """
        animal_names = [animal.name for animal in zk.animals]
        for name in animal_names:
            response_body += f"<ul>Animal: {name}</ul>"
            
        return make_response(response_body, 200)
    else:
        response_body = f"""
            <ul>404 Not Found any zookeepers with id {id}</ul>
        """
        return make_response(response_body, 404)

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    if enc:= db.session.get(Enclosure, id):
        response_body = f"""
            <ul>ID: {enc.id}</ul>
            <ul>Environment: {enc.environment}</ul>
            <ul>Open to Visitors: {enc.open_to_visitors}</ul>
        """
        animal_names = [animal.name for animal in enc.animals]
        for name in animal_names:
            response_body += f"<ul>Animal: {name}</ul>"
            
        return make_response(response_body, 200)
    else:
        response_body = f"""
            <ul>404 Not Found any zookeepers with id {id}</ul>
        """
        return make_response(response_body, 404)


if __name__ == '__main__':
    app.run(port=5555, debug=True)