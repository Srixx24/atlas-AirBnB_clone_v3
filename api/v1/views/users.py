#!/usr/bin/python3
"""
Handles all default RESTFul API actions
for users objects
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """Gets list of all user objects"""
    users = storage.all(User)
    user_list = [user.to_dict() for user in users.values()]
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def one_user(user_id):
    """Gets the user object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def user_delete(user_id):
    """Deletes a user object"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def user_create():
    """Creates a user object"""

    if not request.json:
        abort(400, 'Not a JSON')

    new_user = request.get_json()
    if 'name' not in new_user:
        abort(400, 'Missing name')

    user = User(**new_user)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def user_update(user_id):
    """Updates a user object"""
    user = storage.get(User, user_id)
    ignored_keys = ["id", "email", "created_at", "updated_at"]
    if user is None:
        abort(404)
    new_user = request.get_json()
    if not new_user:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in new_user.items():
        if key not in ignored_keys:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
