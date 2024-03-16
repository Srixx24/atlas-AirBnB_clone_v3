#!/usr/bin/python3
"""
Starts a Flask application
"""
from flask import Flask, Blueprint, jsonify
app = Flask(__name__)


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'OK'})

app.register_blueprint(app_views)


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
