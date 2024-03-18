#!/usr/bin/python3
"""
Handles all default RESTFul API actions
for amenities objects
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """Gets list of all amenity objects"""
    amenities = storage.all(Amenity)
    amenities_list = [amenity.to_dict() for amenity in amenities.values()]
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def one_amenity(amenity_id):
    """Gets the amenity object"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_json())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def amenity_delete(amenity_id):
    """Deletes an amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenity_create():
    """Creates an amenity object"""
    if not request.json:
        abort(400, 'Not a JSON')

    new_amenity = request.get_json()
    if 'name' not in new_amenity:
        abort(400, 'Missing name')

    amenity = Amenity(**new_amenity)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def amenity_update(amenity_id):
    """Updates an amenity object"""
    amenity = storage.get('Amenity', amenity_id)
    ignored_keys = ["id", "created_at", "updated_at"]
    if amenity is None:
        abort(404)
    new_city = request.get_json()
    if not new_city:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in new_city.items():
        if key not in ignored_keys:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
