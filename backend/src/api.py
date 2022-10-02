import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_all_drinks():
    drinks = Drink.query.all()
    return jsonify({
        "success": True,
        'drinks': [drink.short() for drink in drinks] 
    })


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_details():
    try:
        drinks = Drink.query.all()
        return jsonify({
            "success": True,
            'drinks': [drink.long() for drink in drinks] 
        })
    except:
        abort(422)
    

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks", methods=["POST"])
@requires_auth('post:drinks')
def add_new_drink():
    body = request.get_json()
    if 'title' and 'recipe' not in body:
        abort(422)
    
    my_recipe = body['recipe']
    if isinstance(my_recipe, dict):
        my_recipe = [my_recipe]
    try:
        drink_title = body['title']
        drink_recipe = json.dumps(my_recipe)
        new_drink = Drink(title=drink_title, recipe=drink_recipe)
        new_drink.insert()
    except:
        abort(400)
    return jsonify({
        'success': True,
        'drinks': [new_drink.long()]
    }), 200


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks/<int:drink_id>", methods=["PATCH"])
@requires_auth('patch:drinks')
def modify_drink(drink_id):
    body = request.get_json()

    try:
        thedrink = Drink.query.filter(Drink.id == drink_id).one_or_none()

        if thedrink is None:
            abort(404)

        if "title" in body:
            thedrink.title = body['title']

        thedrink.update()

        return jsonify({"success": True, 'drinks': [thedrink.long()]})

    except:
        abort(400)
'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks/<int:drink_id>", methods=["DELETE"])
@requires_auth('delete:drinks')
def delete_drink(drink_id):
    try:
        thedrink = Drink.query.filter(Drink.id == drink_id).one_or_none()

        if thedrink is None:
            abort(404)

        thedrink.delete()
        return jsonify(
            {
                "success": True,
                "delete": drink_id,
            }
        )

    except:
        abort(422)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False, 
        "error": 400, 
        "message": "bad request"
    }), 400

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False, 
        "error": 405, 
        "message": "method not allowed"
    }), 405,

@app.errorhandler(500)
def Server_error_occurred(error):
    return  jsonify({
        "success": False, 
        "error": 500, 
        "message": "Internal Server Error"
    }),500
'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource not found"
    }), 404

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def invalid_token(error):
    response = jsonify(error.error)
    response.status_code = error.status_code
    return response
