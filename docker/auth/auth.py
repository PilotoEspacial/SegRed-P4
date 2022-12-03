#!/usr/bin/env python3

from flask import jsonify, Flask, request
from flask_restful import Resource, Api, abort
import uuid, os, hashlib
from time import ctime
from datetime import datetime, timedelta

app = Flask(__name__)
api = Api(app)

'Global variables'

IP_HOST = "10.0.2.3"
PORT = 5000

TOKENS_DICT = {}
EXP_TOKEN = {}
USERS_PATH = "users/"
MINUTES = 5
KEY = "195DAED626537B32D3CC7CE988ADDE5F4A000F36D13473B7D46C4E53E57F8E61"

def verify_token(token, username):
	try:
            data = jwt.decode(token, KEY, algorithms=['HS256'])
            exp = datetime.fromtimestamp(data['exp'])

            if exp < datetime.utcnow():
                print('Token expired')
                raise jwt.ExpiredSignatureError

            if data['username'] != username:
                print('Usuario no coincide con el token')
                raise jwt.InvalidTokenError
            
            return True
        
        except jwt.ExpiredSignatureError:
            return False
        
        except jwt.InvalidTokenError:
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
        time = str(ctime())
        salt = time.replace(':','/')
        
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
            un = json_data['username']
            pw = json_data['password']
        except KeyError:
            abort(400, message="Arguments must be 'username' and 'password'")
        except:
            abort(400, message="Wrong format of the file")
        else:
        #Comprobamos si el usuario esta registrado
            if (self.check_credentials(un,pw)):
                #Probamos si tiene un token asociado, si no se genera
                try:
                    token = TOKENS_DICT[un]
                except KeyError:
                    token = generate_access_token()
                    TOKENS_DICT[un] = token
                    return jsonify(access_token=token)
                #Si lo tiene, comprobamos su fecha de caducidad, si ha expirado, los eliminamos de ambos json y generamos unos nuevos
                if verify_token(token,un):
                    return jsonify(access_token=TOKENS_DICT[un])
                
                else:
                    del(TOKENS_DICT[un])
                    token = generate_access_token(username)
                    TOKENS_DICT[un] = token
                    return jsonify(access_token=token)
            else:
                abort(401, message="Error, user or password incorrect")



api.add_resource(Login, '/login')
api.add_resource(SignUp, '/signup')

if __name__ == '__main__':
    check_directories()
    app.run(debug=True, host=IP_HOST, port=PORT)
