#!/usr/bin/python3
"""
Flask index
"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """ return status """
    response = {"status": "OK"}
    return jsonify(response)
