from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    resp = make_response(jsonify(data))
    resp.headers['Content-Type'] = 'application/json'
    return resp

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture["id"] == id:
            return picture
    return {"message": "Resource not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_pictuare = request.json
    if not new_pictuare:
        return {"message": "Invalid input parameter"},
    # code to validate new_pictuare ommited
    try:
        for item in data:
            if item['id'] == new_pictuare['id']:
                return jsonify(Message=f"picture with id {new_pictuare['id']} already present"), 302

        data.append(new_pictuare)
        return jsonify(id=new_pictuare['id'], pictuareInsert=new_pictuare), 201
    except NameError:
        return {"message": "data not defined"}, 500

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    new_pictuare = request.json
    if not new_pictuare:
        return {"message": "Invalid input parameter"},
    # code to validate new_pictuare ommited
    try:
        for item in data:
            if item['id'] == new_pictuare['id']:
               data.remove(new_pictuare)
               data.append(new_pictuare)
               
        state = new_pictuare['event_state'] 
        return jsonify(id=new_pictuare['id'], event_state=state), 200
    except NameError:
        return {"message": "data not defined"}, 500

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for picture in data:
       if picture["id"] == id:
           data.remove(picture)
           return {"message":f"{id}"}, 204
    return {"message": "picture not found"}, 404
