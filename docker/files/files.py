#!/usr/bin/env python3

import os,json
from flask import jsonify, Flask, request
from flask_restful import Resource, Api, abort
from datetime import datetime
import jwt


app = Flask(__name__)
api = Api(app)

'''Global variables'''
IP_HOST = "10.0.2.4"
PORT = 5000

KEY = "195DAED626537B32D3CC7CE988ADDE5F4A000F36D13473B7D46C4E53E57F8E61"

TOKENS_DICT = {}
USERS_PATH = "users/"


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

def check_authorization_header(user_id):
    ''' Check if token is correct '''
    auth_header = request.headers.get('Authorization')
    header = auth_header.split(" ")

    if header[0] != "token":
        abort(400, message="Authorization header must be: token <user-auth-token>")

    token = header[1]
        
    if verify_token(token, user_id):
        return True
    else:
        abort(404, message="The user " + user_id + " is not registered in the system")


class User(Resource):
    ''' User class '''
    def get(self, user_id, doc_id):
        ''' Process GET request ''' 
        if check_authorization_header(user_id):
            if not os.path.exists(USERS_PATH+user_id+"/"+doc_id+".json"):
                abort(404, message="The file does not exist")
            else:
                json_file_name = USERS_PATH + user_id + "/" + doc_id + ".json"
                with open(json_file_name) as json_file:
                    data = json.load(json_file) 

                return data
        else:
            abort(401, message="Token is not correct")
    
    def post(self, user_id, doc_id):
        ''' Process POST request '''
        if (check_authorization_header(user_id)):
            if os.path.exists(USERS_PATH+user_id+"/"+doc_id+".json"):
                abort(405, message="The file already exists, use put to update")
            else:
                try:
                    json_data = request.get_json(force=True)
                    doc_content = json_data['doc_content']
                except KeyError:
                    abort(400, message="Argument must be 'doc_content'")
                except:
                    abort(400, message="Wrong format of the file")
                else:
                    json_file_name = USERS_PATH + user_id + "/" + doc_id + ".json"

                    json_string = json.dumps(doc_content)
                    with open(json_file_name, 'w') as outfile:
                        outfile.write(json_string)

                    file_size = os.stat(json_file_name)

                    return jsonify(size=file_size.st_size)
        else:
            abort(401, message="Token is not correct")
        
    def put(self, user_id, doc_id):
        ''' Process PUT request '''
        if (check_authorization_header(user_id)):
            # Delete json file
            if not os.path.exists(USERS_PATH+user_id+"/"+doc_id+".json"):
                abort(404, message="The file does not exists")
            else:
                
                # Create new json file
                try:
                    json_data = request.get_json(force=True)
                    doc_content = json_data['doc_content']
                except:
                    abort(400, message="Wrong format of the file")
                else:
                    json_file_name = USERS_PATH + user_id + "/" + doc_id + ".json"
                
                    os.remove(json_file_name)
                    json_string = json.dumps(doc_content)
                    with open(json_file_name, 'w') as outfile:
                        outfile.write(json_string)

                    file_size = os.stat(json_file_name)

                    return jsonify(size=file_size.st_size)
        else:
            abort(401, message="Token is not correct")
    
    def delete(self, user_id, doc_id):
        ''' Process DELETE request '''
        if (check_authorization_header(user_id)):
            if not os.path.exists(USERS_PATH+user_id+"/"+doc_id+".json"):
                abort(404, message="The file does not exits")
            else:
                json_file_name = USERS_PATH + user_id + "/" + doc_id + ".json"
                os.remove(json_file_name)
                return "{}"
        else:
            abort(401, message="Token is not correct")

class AllDocs(Resource):
    ''' AllDocs class '''
    def get(self, user_id):
        ''' Process GET request '''
        if (check_authorization_header(user_id)):
            all_docks = {}
            path = os.listdir(USERS_PATH + user_id)
            for files in path:
                with open(USERS_PATH + user_id+"/"+files) as content:
                    all_docks[files] = json.load(content)
            return jsonify(all_docks)
        else :
            abort(401, message="Token is not correct")


api.add_resource(User, '/<user_id>/<doc_id>')
api.add_resource(AllDocs, '/<user_id>/_all_docs')


if __name__ == '__main__':
    app.run(debug=True, host=IP_HOST, port=PORT)
