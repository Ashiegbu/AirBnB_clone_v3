#!/usr/bin/python3
"""Amenities routes module"""
from api.v1.views import app_views
from api.v1.views import *
from models import storage
from flask import jsonify, make_response, abort, request


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def amenities(amenity_id=None):
    """[GET] Retrieves a list of all Amenity objects"""
    if not amenity_id:
        objs = [obj.to_dict() for obj in storage.all('Amenity').values()]
        return jsonify(objs)
    return retrieve_model('Amenity', amenity_id)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_amenity(amenity_id):
    """[DELETE] - deletes a amenity object with specified id"""
    return del_model('Amenity', amenity_id)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    """[POST] - adds a amenity object"""
    data = {'name'}
    return create_model('Amenity', None, None, data)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    """[PUT] - updates a amenity object"""
    auto_data = ['id', 'created_at', 'updated_at']
    return update_model('Amenity', amenity_id, auto_data)
