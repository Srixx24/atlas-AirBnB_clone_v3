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
def all_reviews(place_id):
    """Gets list of all review objects"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify([review.to_dict() for review in place.reviews])
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def one_review(review_id):
    """Gets the review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def review_delete(review_id):
    """Deletes a review object"""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def review_create(place_id):
    """Creates a review object"""
    place = storage.get('Place', place_id)
    if request.content_type != 'application/json':
        abort(
            400,
            description="Invalid Content-Type.Expects 'application/json'"
        )
    if place is None:
        abort(404)

    review_data = request.get_json()
    if review_data is None:
        abort(400, 'Not a JSON')

    if 'user_id' not in review_data:
        abort(400, 'Missing user_id')

    user = storage.get('User', review_data['user_id'])
    if user is None:
        abort(404)

    if 'text' not in review_data:
        abort(400, 'Missing text')

    review_data['place_id'] = place_id
    review = Review(**review_data)
    review.save()

    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def review_update(review_id):
    """Updates a review object"""
    review = storage.get(Review, review_id)
    ignore_keys = [
        'id',
        'user_id',
        'place_id',
        'created_at',
        'updated_at'
    ]
    if review is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')

    new_review = request.get_json()
    for key, value in new_review.items():
        if key not in ignore_keys:
            setattr(review, key, value)
        review.save()
    return jsonify(review.to_dict()), 200
