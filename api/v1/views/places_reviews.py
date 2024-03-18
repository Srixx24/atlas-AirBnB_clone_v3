#!/usr/bin/python3
"""
Handles all default RESTFul API actions
for reviews of place objects
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews():
    """Gets list of all review objects"""
    boop


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def one_review():
    """Gets the review object"""
    boop


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def review_delete():
    """Deletes a review object"""
    boop


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def review_create():
    """Creates a review object"""
    boop


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def review_update():
    """Updates a review object"""
    boop
