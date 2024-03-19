#!/usr/bin/python3
"""
Handles all default RESTFul API actions
for cities objects
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities(state_id):
    """Gets list of all state objests"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = state.cities
    cities_list = []
    for city in cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)

@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def one_city(city_id):
    """
    Gets the state object by state id or 404
    error if not linked to any state
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def city_delete(city_id):
    """Deletes a city object"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def city_create(state_id):
    """Creates a city object"""
    state = storage.get("State", state_id)
    if request.content_type != 'application/json':
        abort(
            400,
            description="Invalid Content-Type.Expects 'application/json'"
        )
    if state is None:
        abort(404)

    if not request.json:
        abort(400, 'Not a JSON')

    cities = request.get_json()
    if 'name' not in cities:
        abort(400, 'Missing name')

    cities['state_id'] = state_id
    new_city = City(**cities)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def city_update(city_id):
    """Updates a city object"""
    city = storage.get("City", city_id)
    ignored_keys = ["id", "state_id", "created_at", "updated_at"]
    if city is None:
        abort(404)
    new_city = request.get_json()
    if not new_city:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in new_city.items():
        if key not in ignored_keys:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
