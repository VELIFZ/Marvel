# initial blueprint setup
from flask import Blueprint, jsonify, request, redirect, url_for, flash, render_template
from flask_login import login_required

api = Blueprint('api', __name__, url_prefix = '/api') 

from app.models import db, Marvel

@api.route('/characters', methods=['GET'])
def getCharacters():
    characters = [b.to_dict() for b in Marvel.query.all()]
    return jsonify(characters), 200

@api.route('/book/name/<string:name>', methods=['GET'])
def getBook(name):
    b = Marvel.query.filter_by(name=name.title()).first()
    if b:
        return jsonify(b.to_dict()), 200
    else:
        return jsonify({'Request failed': 'No character with that name.'}), 404

@api.route('/create/character', methods=['POST'])
def createCharacters():
    try:
        data = request.get_json()
        new_char = Marvel(data)
        db.session.add(new_char)
        db.session.commit()
        return jsonify({'Created New Character': new_char.to_dict()}), 201
    except:
        return jsonify({'Create Character Rejected'}), 400

@api.route('/character/update/<string:id>', methods=['PUT'])
def updateCharacter(id):
    try:
        character = Marvel.query.get(id)
        data = request.get_json()
        character.from_dict(data)
        db.session.commit()
        return jsonify({'Updated Character': character.to_dict()}), 200
    except:
        return jsonify({'Request failed': 'invalid body or ID'}), 400

@api.route('/character/remove/<string:id>', methods=['DELETE'])
def removeCharacter(id):
    character = Marvel.query.get(id)
    if not character: 
        return jsonify({'Remove failed': 'No character of that ID in the database.'}), 404
    db.session.delete(character)
    db.session.commit()
    return jsonify({'Removed character': character.to_dict()}), 200
