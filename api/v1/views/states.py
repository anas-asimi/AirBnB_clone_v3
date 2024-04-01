#!/usr/bin/python3
"""
Flask index
"""

from flask import abort, request
from werkzeug.exceptions import BadRequest
import json
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """ Retrieves the list of all State """
    all_states = storage.all('State')
    all_states = list(state.to_dict() for state in all_states.values())
    return json.dumps(all_states, sort_keys=True, indent=2)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states_get(state_id):
    """ Retrieves a State """
    state = storage.get('State', state_id)
    if state:
        return json.dumps(state.to_dict(), sort_keys=True, indent=2)
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def states_delete(state_id):
    """ Deletes a State """
    state = storage.get('State', state_id)
    cities = storage.all(City)
    if state:
        for city in cities.values():
            if city.state_id == state.id:
                storage.delete(city)
        storage.delete(state)
        storage.save()
        return json.dumps({})
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def states_post():
    """ Creates a State """
    try:
        state_dict = request.get_json()
        state = State(name=state_dict['name'])
        storage.new(state)
        storage.save()
        return json.dumps(state.to_dict(), sort_keys=True, indent=2), 201
    except Exception as ex:
        if isinstance(ex, KeyError):
            abort(400, 'Missing name')
        if isinstance(ex, BadRequest):
            abort(400, 'Not a JSON')
        abort(400, 'Uknown error')


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def states_update(state_id):
    """ Updates a State """
    try:
        state = storage.get('State', state_id)
        if state is None:
            raise ValueError()
        state_dict = request.get_json()
        state_dict.pop('id', None)
        state_dict.pop('created_at', None)
        state_dict.pop('updated_at', None)
        for key, value in state_dict.items():
            setattr(state, key, value)
        storage.save()
        return json.dumps(state.to_dict(), sort_keys=True, indent=2), 200
    except Exception as ex:
        if isinstance(ex, ValueError):
            abort(404)
        if isinstance(ex, BadRequest):
            abort(400, 'Not a JSON')
        print(ex)
        abort(400, 'Uknown error')
