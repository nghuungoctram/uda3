from cmd import IDENTCHARS
import os
from flask import Flask, request, jsonify, abort
import json
from flask_cors import CORS
from .database.models import setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


# GET ALL DRINKS
@app.route('/drinks', methods=['GET'])
def get_drinks_method():
    return jsonify(
        success=True,
        drinks=[drink.short() for drink in (Drink.query.all())]
    ), 200


# GET DETAIL DRINKS
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail_method():
    return jsonify(
        success=True,
        drinks=[drink.long() for drink in (Drink.query.all())]
    ), 200


# ADD NEW DRINK
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_new_drink_method():
    body = request.get_json()

    if ((body.get('title', None)) is None & (body.get('recipe', None)) is None):
        abort(400, 'TITLE OR/AND RECIPE is none')

    newDrink = Drink(title=body.get('title', None),
                     recipe=json.dumps(body.get('recipe', None)))
    newDrink.insert()

    return jsonify({
        'success': True,
        'drinks': [newDrink.long() for newDrink in (Drink.query.all())],
    }), 200


# UPDATE DRINK BY ID
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink_by_id_method(id):
    drink = Drink.query.filter(Drink.id == id).one_or_more()
    body = request.get_json()

    if drink is None:
        abort(404, 'Drink not found')

    else:
        drink = Drink(title=body.get('title', None),
                      recipe=json.dumps(body.get('recipe', None)))
        drink.update()

    return jsonify({
        'success': True,
        'drinks': [drink.long() for drink in (
            Drink.query.filter_by(title=body.get('title', None)).all())]
    }), 200


# DELETE DRINK
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink_using_id_method(id):
    if ((Drink.query.get(id=id)) is None):
        abort(404, 'Drink not found')
    else:
        try:
            (Drink.query.filter_by(id=id).first()).delete()
        except:
            abort(400, 'got Bad request error')

    return jsonify(
        success=True,
        delete=id
    ), 200


# Error Handling
@app.errorhandler(400)
def bad_request_error(er):
    return jsonify({
        'success': False,
        'error': 'Bad Request',
        "message": "got Bad request error"
    }), 400


@app.errorhandler(404)
def page_not_found_error(er):
    return jsonify({
        "success": False,
        'error': 404,
        "message": "Page Not Found or File Not Found"
    }), 404


@app.errorhandler(405)
def invalid_method_error(er):
    return jsonify({
        "success": False,
        'error': 405,
        "message": "method not allowed!"
    }), 405


@app.errorhandler(422)
def unprocessable_entity_error(er):
    return jsonify({
        "success": False,
        'error': 422,
        "message": "Unprocessable entity error"
    }), 422


@app.errorhandler(500)
def server_error(er):
    return jsonify({
        "success": False,
        "error": 500,
        "message": 'Internal Server Error/Temporary Error'
    }), 500


@app.errorhandler(AuthError)
def authen_got_fail(er):
    return jsonify({
        "success": False,
        "error": er.status_code,
        "message": "Authentification is not successful" + er.error['description']
    }), 401
