#!/usr/bin/python3
"""
Flask index
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ return status """
    response = {"status": "OK"}
    return jsonify(response)


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ return status """
    response = {}
    for clss in classes:
        response[clss] = storage.count(classes[clss])
    return jsonify(response)
