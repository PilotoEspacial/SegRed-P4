#!/usr/bin/env python3

import uuid, os, hashlib, json
from flask import jsonify, Flask, request
from flask_restful import Resource, Api, abort
from time import ctime
from datetime import datetime, timedelta

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'SegRed-P3'

''' Global variables '''
IP_HOST = "10.0.1.4"
PORT = 5000

IP_AUTH = "10.0.2.3"
IP_FILES = "10.0.2.4"

__version__ = 'v2.3.69-alpha'
USERS_PATH = "users/"
TOKENS_DICT = {}
EXP_TOKEN = {}
MINUTES = 5

''' Global functions '''

def check_authorization_header(user_id):
    ''' Check if token is correct '''
    auth_header = request.headers.get('Authorization')
    header = auth_header.split(" ")

    if header[0] != "token":
        abort(400, message="Authorization header must be: token <user-auth-token>")

    token = header[1]
        
    if token in EXP_TOKEN:
        try:
            if TOKENS_DICT[user_id]==token:
                if (datetime.strptime(EXP_TOKEN[token], '%H:%M') > datetime.strptime(datetime.now().strftime('%H,%M'),'%H,%M')):
                    return True
                else:
                    del(EXP_TOKEN[token])
                    del(TOKENS_DICT[user_id])
        except KeyError:
            abort(404, message="The user " + user_id + " is not registered in the system")

    return False

''' Classes '''
class Version(Resource):
    ''' Version class '''    
    def get(self):
        ''' Return software version '''
        return {'version' : __version__}

class SignUp(Resource):
    ''' SignUp class '''

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