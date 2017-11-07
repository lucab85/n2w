# app/__init__.py

from flask_api import FlaskAPI
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_httpauth import HTTPBasicAuth
from num2words import num2words
import datetime

# local import
from instance.config import app_config

app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()

def create_app(config_name):
    #app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    return app

@auth.get_password
def get_password(username):
    if username == 'production':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog
    
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)
    
@app.route('/n2w/api/v1.0/get/<int:n>', methods = ['GET'])
@app.route('/n2w/api/v1.0/get/<int:n>/<string(length=2):l>', methods = ['GET'])
def get_n2w(n, l='en'):
	try:
		v = num2words(n, lang=l)
		json = {
			'number': n,
			'text': v, 
			'lang': l,
			'created': datetime.datetime.now(),
		}
		return jsonify( json )
	except NotImplementedError as e:
		return not_found(400)
