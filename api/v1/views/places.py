#!/usr/bin/python3
"""
Handles all default RESTFul API actions
for places objects
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_places(city_id):
    """Gets list of all place objects"""
    city = storage.get(City, city_id,)
    if not city:
        abort(404)
    if not city.place_id:
        return jsonify([])
    places = [place.to_dict() for place in city.place]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def one_place(place_id):
    """Gets the place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def place_delete(place_id):
    """Deletes a place object"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def place_create():
    """Creates a place object"""
    if not request.json:
        abort(400, 'Not a JSON')

    places = request.get_json()
    if 'name' not in places:
        abort(400, 'Missing name')

    new_place = Place(**places)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def place_update(place_id):
    """Updates a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if not request.json:
        abort(400, 'Not a JSON')

    new_place = request.get_json()
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in new_place.items():
        if key not in ignore_keys:
            setattr(place, key, value)
        storage.save()
        return jsonify(place.to_dict()), 200
