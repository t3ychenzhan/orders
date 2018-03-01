import logging

from flask import Blueprint, jsonify, request, url_for, make_response
from flask_api import status    # HTTP Status Codes

items = Blueprint('items', __name__)

@items.route('/items', methods=['GET'])
def index():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

@items.route('/items', methods=['POST'])
def create_items():
    """
    Creates an item
    This endpoint will create an item based the data in the body that is posted
    """
    check_content_type('application/json')

    item = Item()

    item.deserialize(request.get_json())
    item.save()
    message = item.serialize()

    return jsonify(message), status.HTTP_201_CREATED
