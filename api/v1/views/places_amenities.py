#!/usr/bin/python3
"""Places amenities module <relates place and amenities>"""
from api.v1.views import app_views
from api.v1.views import *
from flask import jsonify, make_response, abort, request
from models import storage

model = "Amenity"
parent_model = "Place"


@app_views.route("/places/<place_id>/amenities", strict_slashes=False,
                 methods=["GET"])
def retrieve_amenities(place_id):
    """GET amenities in a place defined by id"""
    return retrieve_models(parent_model, place_id, "amenities")


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=["DELETE", "POST"])
def post_del_amenity(place_id, amenity_id):
    """create or delet amenity linked to a place"""
    if request.method == "DELETE":
        return del_amenity(place_id, amenity_id)
    else:
        return create_amenity(place_id, amenity_id)


def del_amenity(place_id, amenity_id):
    """[DELETE] - delete an amenity"""
    place = storage.get(parent_model, place_id)
    if not place:
        return make_response(jsonify({"error": "Not found"}), 404)
    amenity = storage.get(model, amenity_id)
    if not amenity:
        return make_response(jsonify({"error": "Not found"}), 404)

    if amenity not in place.amenities:
        return make_response(jsonify({"error": "Not found"}), 404)
    place.amenities.remove(amenity)

    storage.save()
    return make_response(jsonify({}), 200)


def create_amenity(place_id, amenity_id):
    """[POST] - create amenity"""
    place = storage.get(parent_model, place_id)
    if not place:
        return make_response(jsonify({"error": "Not found"}), 404)
    amenity = storage.get(model, amenity_id)
    if not amenity:
        return make_response(jsonify({"error": "Not found"}), 404)

    if amenity in place.amenities:
        return make_response(jsonify(amenity.to_dict()), 200)

    place.amenities.append(amenity)

    place.save()
    return make_response(jsonify(amenity.to_dict()), 201)
