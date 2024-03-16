#!/usr/bin/python3
"""
Starts a Flask application
"""
import os
from flask import Flask, Blueprint, jsonify
from api.v1.views import app_views
from models import storage
app = Flask(__name__)


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
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


app.register_blueprint(app_views)


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
