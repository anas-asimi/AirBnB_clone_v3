#!/usr/bin/python3
"""
Flask API
"""

from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def close_storage(exception):
    """ after each request, this method calls storage.close() """
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """ return Not found """
    response = {"error": "Not found"}
    return jsonify(response), 404


if __name__ == '__main__':
    HBNB_API_HOST = getenv("HBNB_API_HOST")
    HBNB_API_PORT = getenv("HBNB_API_PORT")
    app.run(
        host=HBNB_API_HOST or '0.0.0.0',
        port=HBNB_API_PORT or '5000', threaded=True)
