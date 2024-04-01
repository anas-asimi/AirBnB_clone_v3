#!/usr/bin/python3
"""
Flask index
"""

import json
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {"amenities": Amenity, "cities": City, "places": Place,
           "reviews": Review, "states": State, "users": User}


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ return status """
    response = {"status": "OK"}
    return json.dumps(response, sort_keys=True, indent=2)


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ return status """
    response = {}
    for clss in classes:
        response[clss] = storage.count(classes[clss])
    return json.dumps(response, sort_keys=True, indent=2)
