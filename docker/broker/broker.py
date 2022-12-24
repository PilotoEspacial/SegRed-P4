#!/usr/bin/env python3

import requests
from flask import Flask, jsonify
from flask_restful import Resource, Api, abort, request
import json


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'SegRed-P3'

''' Global variables '''
IP_HOST = "10.0.1.4"
PORT = 5000

CERT_PEM = 'certs/broker.ssl.crt'
KEY_PEM = 'keys/broker.ssl.key'

AUTH = "https://auth:5000"
AUTH_CERT = "certs/auth.ssl.crt"

FILES = "https://files:5000"
FILE_CERT = "certs/files.ssl.crt"

__version__ = 'v2.3.69-alpha'
USERS_PATH = "users/"
TOKENS_DICT = {}
MINUTES = 5

    

def check_authorization_header():
    ''' Check if token is correct '''
    try:
        auth_header = request.headers.get('Authorization')
        header = auth_header.split(" ")

        if header[0] != "token":
            abort(400, message="Authorization header must be: token <user-auth-token>")

        token = header[1]

        return token
        
    except Exception as err:
        print("Error: ", err)

''' Classes '''
class Version(Resource):
    ''' Version class '''    
    def get(self):
        ''' Return software version '''
        return {'version' : __version__}

class SignUp(Resource):
    ''' SignUp class '''
    def post(self):

        json_data = request.get_json(force=True)            
        username = json_data['username']
        password = json_data['password']

        response = requests.post(AUTH + "/signup",json={"username":username, "password": password}, verify=AUTH_CERT, timeout=10)
        print("Auth response: ",response.status_code)

        if(response.status_code == 200):
            return jsonify(access_token = response.json())
        else:
            response_dict = json.loads(response.text)
            abort(response.status_code, message = response_dict["message"])

class Login(Resource):
    '''Login class'''
    def post(self):

        json_data = request.get_json(force=True)            
        username = json_data['username']
        password = json_data['password']

        response = requests.post(AUTH + "/login",json={"username":username, "password": password}, verify=AUTH_CERT, timeout=10)
        print("Auth response: ",response.status_code)

        if(response.status_code == 200):
            return jsonify(response.json())
        else:
            response_dict = json.loads(response.text)
            abort(400, message=response_dict["message"])
class User(Resource):
    ''' User class '''
    def get(self, user_id, doc_id):
        ''' Process GET request ''' 
        token = check_authorization_header()
        response = requests.get(FILES + "/" + user_id + "/" + doc_id, headers={'Authorization':'token ' + token}, verify=FILE_CERT, timeout=10)
    
        if(response.status_code == 200):
            return jsonify(response.json())
        else:
            response_dict = json.loads(response.text)
            abort(response.status_code, message = response_dict["message"])

    def post(self, user_id, doc_id):
        ''' Process POST request '''
        token = check_authorization_header()
        json_data = request.get_json(force=True)
        doc_content = json_data['doc_content']

        response = requests.post(FILES + "/" + user_id + "/" + doc_id, headers={'Authorization':'token '+token}, json=doc_content, verify=FILE_CERT, timeout=10)

        if(response.status_code == 200):
            return jsonify(response.json())
        else:
            response_dict = json.loads(response.text)
            abort(response.status_code, message=response_dict["message"])

    def put(self, user_id, doc_id):
        ''' Process PUT request '''
        token = check_authorization_header()
        json_data = request.get_json(force=True)
        doc_content = json_data['doc_content']

        response = requests.put(FILES + "/" + user_id + "/" + doc_id, headers={'Authorization':'token '+token}, json=doc_content, verify=FILE_CERT, timeout=10)

        if(response.status_code == 200):
            return jsonify(response.json())
        else:
            response_dict = json.loads(response.text)
            abort(response.status_code, message=response_dict["message"])

    
    def delete(self, user_id, doc_id):
        ''' Process DELETE request '''
        
        token = check_authorization_header()
        response = requests.delete(FILES + "/" + user_id + "/" + doc_id, headers={'Authorization':'token '+token}, verify=FILE_CERT, timeout=10)
        print("Auth response: ",response.status_code)

        if(response.status_code == 200):
            return jsonify(response.json())
        else:
            abort(500, message = "Error en Auth Server")


class AllDocs(Resource):
    ''' AllDocs class '''
    def get(self, user_id):
        ''' Process GET AllDocs '''
        token = check_authorization_header()
        response = requests.get(FILES + "/" + user_id + "/_all_docs", headers={'Authorization':'token '+token}, verify=FILE_CERT, timeout=10)
        #print("Auth response: ",response.status_code)

        if(response.status_code == 200):
            return jsonify(response.json())
        else:
            abort(500, message = "Error en Auth Server")


api.add_resource(Version, '/version')
api.add_resource(Login, '/login')
api.add_resource(SignUp, '/signup')
api.add_resource(User, '/<user_id>/<doc_id>')
api.add_resource(AllDocs, '/<user_id>/_all_docs')


if __name__ == '__main__':
    app.run(debug=True, ssl_context=(CERT_PEM,KEY_PEM), host=IP_HOST, port=PORT)
    
#,host=IP_HOST, port=PORT)