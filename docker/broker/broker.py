#!/usr/bin/env python3

import requests
from flask import Flask, jsonify
from flask_restful import Resource, Api, abort


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'SegRed-P3'

''' Global variables '''
IP_HOST = "10.0.1.4"
PORT = 5000

AUTH = "http://auth:5000"
FILES = "files"

__version__ = 'v2.3.69-alpha'
USERS_PATH = "users/"
TOKENS_DICT = {}
MINUTES = 5

''' Classes '''
class Version(Resource):
    ''' Version class '''    
    def get(self):
        ''' Return software version '''
        return {'version' : __version__}

class SignUp(Resource):
    ''' SignUp class '''
    def post(self, username, password):
        response = requests.post(AUTH, {},{"username":username, "password": password}, verify=False)
        print("Auth response: ",response.status_code)

        if(response.status_code == 200):
            return jsonify(access_token = response.json())
        else:
            abort(response.status_code, message = "Error in auth server")

class Login(Resource):
        '''Login class'''

class User(Resource):
    ''' User class '''
    def get(self, user_id, doc_id):
        ''' Process GET request ''' 
    
    def post(self, user_id, doc_id):
        ''' Process POST request '''

    def put(self, user_id, doc_id):
        ''' Process PUT request '''
    
    def delete(self, user_id, doc_id):
        ''' Process DELETE request '''


class AllDocs(Resource):
    ''' AllDocs class '''
    def get(self, user_id):
        ''' Process GET AllDocs '''


api.add_resource(Version, '/version')
api.add_resource(Login, '/login')
api.add_resource(SignUp, '/signup')
api.add_resource(User, '/<user_id>/<doc_id>')
api.add_resource(AllDocs, '/<user_id>/_all_docs')


if __name__ == '__main__':
    app.run(debug=True, host=IP_HOST, port=PORT)