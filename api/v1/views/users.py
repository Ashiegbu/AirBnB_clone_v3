#!/usr/bin/python3
"""Users routes module"""
from api.v1.views import app_views
from api.v1.views import *
from flask import jsonify, make_response, abort, request
from models import storage

model = "User"


@app_views.route("/users", strict_slashes=False, methods=["GET"])
@app_views.route("/users/<user_id>", strict_slashes=False, methods=["GET"])
def retrieve_users(user_id=None):
    """[GET] Retrieves a user or list of users"""
    if not user_id:
        usrs = [usr.to_dict() for usr in storage.all(model).values()]
        return jsonify(usrs)
    return retrieve_model(model, user_id)


@app_views.route("/users/<user_id>", methods=["DELETE"])
def del_user(user_id):
    """[DELETE] - deletes a user object with specified id"""
    return del_model(model, user_id)


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def create_user():
    """[POST] - adds a user object"""
    required_data = {"email", "password"}
    return create_model(model, None, None, required_data)


@app_views.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    """[PUT] - updates a user object"""
    auto_data = ["id", "created_at", "updated_at", "email"]
    return update_model(model, user_id, auto_data)
