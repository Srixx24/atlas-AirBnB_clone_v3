#!/usr/bin/python3
"""
Index file
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def obj_stats():
    """Gets the stats for each object"""
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(stats)
