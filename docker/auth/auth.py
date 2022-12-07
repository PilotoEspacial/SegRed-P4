#!/usr/bin/env python3

from flask import jsonify, Flask, request
from flask_restful import Resource, Api, abort, reqparse
import os, hashlib, uuid
from datetime import datetime, timedelta
import requests
import jwt

app = Flask(__name__)
api = Api(app)

'Global variables'

IP_HOST = "10.0.2.3"
FILE_SERVER = "http://10.0.2.4:5000/space"
PORT = 5000

TOKENS_DICT = {}
USERS_PATH = "users/"
MINUTES = 5
KEY = "195DAED626537B32D3CC7CE988ADDE5F4A000F36D13473B7D46C4E53E57F8E61"


token_check_args = reqparse.RequestParser()
token_check_args.add_argument('username', type=str, help="Username required", required=True)
token_check_args.add_argument('token', type=str, help="Token required", required=True)

'''Global classes'''

def verify_user(username):
    for user in TOKENS_DICT.keys():
        if username == user:
            return True
        else:
            return False

def verify_token(username, token):

        try:
            payload = jwt.decode(token, KEY, algorithms=['HS256'])
            date_expired = datetime.fromtimestamp(payload['exp'])
            #print("Payload: ", payload)
            #print("Expired: ", date_expired)

            if date_expired < datetime.utcnow():
                print('Token expired')
                raise jwt.ExpiredSignatureError

            if payload['username'] != username:
                print('Usuario no coincide con el token')
                raise jwt.InvalidTokenError
            
            return True
        except jwt.ExpiredSignatureError as err:
            abort(401, message="Token is not correct")
            #print("Error:", err)
            #return False
        
        except jwt.InvalidTokenError as err:
            print("Error:", err)
            return False

def check_directories():
    ''' Check if users directory and shadow file '''
    if not os.path.isdir(USERS_PATH):
        os.mkdir(USERS_PATH)
    try:
        shadow_file = open('.shadow', 'r')
        shadow_file.close()
    except FileNotFoundError:
        os.system("touch .shadow")

def encrypt_password(salt, password):
    ''' Encrypt password using SHA256 algorithm'''
    return hashlib.sha256(salt.encode('utf-8') + password.encode('utf-8')).hexdigest()

    
def generate_access_token(username):
    ''' Generate random token for a new user '''
    exp = datetime.utcnow() + timedelta(minutes=MINUTES)
    token = jwt.encode({'username': username, 'exp': exp},KEY, algorithm='HS256')
    
    return token

''' Login class '''
class SignUp(Resource):
    ''' SignUp class '''
    def create_directory(self, username):
        ''' Create directory of user if does not exists '''
        if not os.path.isdir(USERS_PATH + username):
            try:
                os.mkdir(USERS_PATH + username)
            except Exception:
                abort(400, message="Error creating username space")

    def register_user(self, username, password):
        ''' Register new user in shadow file '''
        shadow_file = open('.shadow', 'a')
        credentials = ""
        
        salt = str(uuid.uuid4())
        
        if (os.stat(".shadow").st_size != 0):
            credentials = "\n"

        credentials += username + ":" + salt + ":" + encrypt_password(salt,password)
        shadow_file.writelines(credentials)
        shadow_file.close()

    ''' Check if username already exists '''
    def check_username(self, username):

        shadow_file = open('.shadow', 'r')
        lines = shadow_file.readlines()
        shadow_file.close()

        for line in lines:
            if (line.split(":")[0] == username):
                return True
        
        return False

    def post(self):
        ''' Process POST request '''
        try:
            json_data = request.get_json(force=True)            
            username = json_data['username']
            password = json_data['password']
        except KeyError:
            abort(400, message="Arguments must be 'username' and 'password'")
        except:
            abort(400, message="Wrong format of the file")
        else:
            if (self.check_username(username)):
                abort(409, message="Error, username {} already exists.".format(username))
            else:
                self.register_user(username, password)
                self.create_directory(username)

                token = generate_access_token(username)
                TOKENS_DICT[username] = token
                return jsonify(token)

class Login(Resource):
    ''' Login class '''
    def check_credentials(self, username, password):
        ''' Check if credentials are correct '''   
        shadow_file = open('.shadow', 'r')
        lines = shadow_file.readlines()
        shadow_file.close()
        
        for line in lines:
            credentials = line.split(":")
            if (credentials[0] == username and credentials[2].strip() == encrypt_password(credentials[1],password)):
                return True

        return False

    def post(self):
        ''' Process POST request '''
        try:
            json_data = request.get_json(force=True)            
            username = json_data['username']
            password = json_data['password']
        except KeyError:
            abort(400, message="Arguments must be 'username' and 'password'")
        except:
            abort(400, message="Wrong format of the file")
        else:
        #Comprobamos si el usuario esta registrado
            if (self.check_credentials(username,password)):
                #Probamos si tiene un token asociado, si no se genera
                try:
                    token = TOKENS_DICT[username]
                except KeyError:
                    token = generate_access_token()
                    TOKENS_DICT[username] = token
                    return jsonify(access_token=token)
                #Si lo tiene, comprobamos su fecha de caducidad, si ha expirado, los eliminamos de ambos json y generamos unos nuevos
                if verify_token(username, token):
                    return jsonify(access_token=TOKENS_DICT[username])
                
                else:
                    del(TOKENS_DICT[username])
                    token = generate_access_token(username)
                    TOKENS_DICT[username] = token
                    return jsonify(access_token=token)
            else:
                abort(401, message="Error, user or password incorrect")

class Authorize(Resource):

    def get(self):
        
        username = request.args.get('username')
        token = request.args.get('token')
        if verify_user(username):
            if verify_token(username, token):
                return {}, 200 # Token matches
            else:
                return {"Error": 401, "message": "Wrong token"}
        else:
            abort(401, message = "User not found")

api.add_resource(Login, '/login')
api.add_resource(SignUp, '/signup')
api.add_resource(Authorize, '/checking')

if __name__ == '__main__':
    check_directories()
    app.run(debug=True, host=IP_HOST, port=PORT)
