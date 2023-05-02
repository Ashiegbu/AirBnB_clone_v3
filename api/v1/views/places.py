#!/usr/bin/python3
"""places routes module"""
from api.v1.views import app_views
from api.v1.views import *
from flask import jsonify, make_response, abort, request
from models import storage

model = "Place"
parent_model = "City"


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=["GET"])
def retrieve_places(city_id):
    """[GET] Retrieves a list of all place objects linked to a city"""
    return retrieve_models(parent_model, city_id, "places")


@app_views.route("/places/<place_id>", methods=["GET"])
def retrieve_place(place_id):
    """[GET] Retrieves a list of all place objects"""
    return retrieve_model(model, place_id)


@app_views.route("/places/<place_id>", methods=["DELETE"])
def del_place(place_id):
    """[DELETE] - deletes a place object with specified id"""
    return del_model(model, place_id)


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=["POST"])
def create_place(city_id):
    """[POST] - adds a place object"""
    required_data = {"name", "user_id"}
    return create_model(model, parent_model, city_id, required_data)


@app_views.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id):
    """[PUT] - updates a place object"""
    auto_data = ["id", "created_at", "updated_at", "user_id", "city_id"]
    return update_model(model, place_id, auto_data)


@app_views.route("/places_search", strict_slashes=False,
                 methods=["POST"])
def search_places():
    """ retrieves all Place objects depending of the JSON in the body
     of the request"""
    data = request.get_json(force=True, silent=True)
    if data is None:
        abort(400, 'Not a JSON')

    ok = {"states", "cities"}
    places = []
    if not len(data) or all([len(v) == 0 for k, v in data.items() if k in ok]):
        places = storage.all("Place").values()

    if len(data.get("states", [])):
        states = [storage.get("State", id) for id in data["states"]]
        [[[places.append(place) for place in city.places]
         for city in state.cities] for state in states if state]

    if len(data.get("cities", [])):
        cities = [storage.get("City", id) for id in data["cities"]]
        [[places.append(place) for place in city.places]
         for city in cities if city]

    places = list(set(places))
    if len(data.get("amenities", [])):
        amenities = [storage.get("Amenity", id) for id in data["amenities"]]
        places = [place for place in places
                  if all([a in place.amenities for a in amenities])]

    return jsonify([place.to_dict() for place in places])
