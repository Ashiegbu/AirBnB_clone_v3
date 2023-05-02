#!/usr/bin/python3
"""reviews routes module"""
from api.v1.views import app_views
from api.v1.views import *
from flask import jsonify, make_response, abort, request
from models import storage

model = "Review"
parent_model = "Place"


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=["GET"])
def retrieve_reviews(place_id):
    """[GET] Retrieves a list of all City objects linked to a place"""
    return retrieve_models(parent_model, place_id, "reviews")


@app_views.route("/reviews/<review_id>", methods=["GET"])
def retrieve_review(review_id):
    """[GET] Retrieves a list of all City objects"""
    return retrieve_model(model, review_id)


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def del_review(review_id):
    """[DELETE] - deletes a review object with specified id"""
    return del_model(model, review_id)


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=["POST"])
def create_review(place_id):
    """[POST] - adds a review object"""
    required_data = {"text", "user_id"}
    return create_model(model, parent_model, place_id, required_data)


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def update_review(review_id):
    """[PUT] - updates a review object"""
    auto_data = ["id", "created_at", "updated_at", "user_id", "place_id"]
    return update_model(model, review_id, auto_data)
