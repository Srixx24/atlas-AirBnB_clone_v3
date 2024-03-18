#!/usr/bin/python3
"""
Handles all default RESTFul API actions
for places objects
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_places():
    """Gets list of all place objects"""
    boop


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def one_place():
    """Gets the place object"""
    boop


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def place_delete():
    """Deletes a place object"""
    boop


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def place_create():
    """Creates a place object"""
    boop


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def place_update():
    """Updates a place object"""
    boop
