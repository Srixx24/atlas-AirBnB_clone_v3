#!/usr/bin/python3
"""
Handles all default RESTFul API actions
for states objects
"""
from flask import jsonify, request, abort
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def all_states():
    """Gets list of all state objests"""
    states = storage.all("State").values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def one_state(state_id):
    """
    Gets the state object by state id or 404
    error if not linked to any state
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_json()), 200


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def state_delete(state_id):
    """Deletes a State object by state_id"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_create():
    """Creates a new State object"""
    if not request.json:
        abort(400, 'Not a JSON')

    states = request.get_json()
    if 'name' not in states:
        abort(400, 'Missing name')
    
    new_state = State(**states)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def state_update(state_id):
    """Updates a State object by state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if not request.json:
        abort(400, 'Not a JSON')

    new_state = request.json
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in new_state.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
