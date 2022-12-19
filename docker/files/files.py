#!/usr/bin/env python3

import os,json
from flask import jsonify, Flask, request
from flask_restful import Resource, Api, abort, reqparse
import requests


app = Flask(__name__)
api = Api(app)

'''Global variables'''
IP_HOST = "10.0.2.4"
PORT = 5000

KEY = "195DAED626537B32D3CC7CE988ADDE5F4A000F36D13473B7D46C4E53E57F8E61"

AUTH_SERVER = "http://auth:5000/"
TOKENS_DICT = {}
USERS_PATH = "users"

create_user = reqparse.RequestParser()
create_user.add_argument('username', type=str, help="Username required", required=True)


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

class User(Resource):
    ''' User class '''
    def get(self, user_id, doc_id):
        ''' Process GET request '''
        token = check_authorization_header()
        response = requests.get(AUTH_SERVER + "checking", {"username" : user_id, "token" : token}, verify=False)
        
        print("\nAuth response: ", response.status_code)
        
        if (response.status_code == 200):
            if not os.path.exists(USERS_PATH + "/" + user_id + "/" + doc_id + ".json"):
                ###AQUIIIIIII
                abort(404, message="The file does not exist")
            else:
                json_file_name = USERS_PATH + "/" + user_id + "/" + doc_id + ".json"
                with open(json_file_name) as json_file:
                    data = json.load(json_file) 
                return data
        else:
            abort(401, message="Token is not correct "+ str(response.status_code))
    
    def post(self, user_id, doc_id):
        ''' Process POST request '''

        token = check_authorization_header()
        response = requests.get(AUTH_SERVER + "checking", {"username" : user_id, "token" : token}, verify=False)
        print("\nAuth response: ", response.status_code)

        if (response.status_code == 200):
            
            if not os.path.exists(USERS_PATH + "/" + user_id):
                os.mkdir(USERS_PATH+ "/" +user_id)
            
            if os.path.exists( USERS_PATH + "/" + user_id + "/" + doc_id + ".json" ):
                abort(405, message="The file already exists")
            else:
                try:
                    json_data = request.get_json(force=True)
                    #doc_content = json_data['doc_content']
                except KeyError:
                    abort(400, message="Argument must be 'doc_content'")
                except:
                    abort(400, message="Wrong format of the file")
                else:
                    
                    json_file_name = USERS_PATH + "/" + user_id + "/" + doc_id + ".json"
                    json_string = json.dumps(json_data)
                    
                    with open(json_file_name, 'w') as outfile:
                        outfile.write(json_string)

                    outfile.close()

                    file_size = os.stat(json_file_name)

                    return jsonify(size=file_size.st_size)
        else:
            abort(401, message="Token is not correct")
        
    def put(self, user_id, doc_id):
        ''' Process PUT request '''
        token = check_authorization_header()
        response = requests.get(AUTH_SERVER + "checking", {"username" : user_id, "token" : token}, verify=False)
        print("\nAuth response: ", response.status_code)
        if (response.status_code == 200):
            # Delete json file
            if not os.path.exists(USERS_PATH + "/" + user_id + "/" + doc_id + ".json"):
                abort(404, message="The file does not exists")
            else:
                # Create new json file
                try:
                    json_data = request.get_json(force=True)
                    #doc_content = json_data['doc_content']
                    print("doc_contect: ",json_data)
                except KeyError:
                    abort(400, message="Argument must be 'doc_content'")
                except:
                    abort(400, message="Wrong format of the file")
                else:
                    json_file_name = USERS_PATH + "/" + user_id + "/" + doc_id + ".json"

                    os.remove(json_file_name)
                    json_string = json.dumps(json_data)
                    with open(json_file_name, 'w') as outfile:
                        outfile.write(json_string)

                    file_size = os.stat(json_file_name)

                    return jsonify(size=file_size.st_size)
        else:
            abort(401, message=response.reason)
    
    def delete(self, user_id, doc_id):
        ''' Process DELETE request '''
        token = check_authorization_header()
        response = requests.get(AUTH_SERVER + "checking", {"username" : user_id, "token" : token}, verify=False)
        print("\nAuth response: ", response.status_code)

        if (response.status_code == 200):
            if not os.path.exists(USERS_PATH + "/" + user_id + "/" + doc_id + ".json"):
                abort(404, message="The file does not exits")
            else:
                json_file_name = USERS_PATH + "/" + user_id + "/" + doc_id + ".json"
                os.remove(json_file_name)
                
                return jsonify({})
        else:
            abort(401, message="Token is not correct")

class AllDocs(Resource):
    ''' AllDocs class '''
    def get(self, user_id):

        ''' Process GET request '''
        token = check_authorization_header()
        response = requests.get(AUTH_SERVER + "checking", {"username" : user_id, "token" : token}, verify=False)

        print("\nAuth response: ", response.status_code)

        if (response.status_code == 200):
            all_docks = {}
            path = os.listdir(USERS_PATH + "/" + user_id)
            for files in path:
                with open(USERS_PATH + "/" + user_id + "/" + files) as content:
                    all_docks[files.strip(".json")] = json.load(content)
            return jsonify(all_docks)
        else :
            abort(response.status_code, message="Token is not correct")


class UserDIR(Resource):

    '''UserDIR'''
    def post(self):
        
        username = request.args.get('username')
        print("Username: ",str(username))
        os.mkdir(username)

        return {}, 200


api.add_resource(User, '/<user_id>/<doc_id>')
api.add_resource(AllDocs, '/<user_id>/_all_docs')
api.add_resource(UserDIR, '/space')

if __name__ == '__main__':

    if not os.path.exists(USERS_PATH):
        os.mkdir(USERS_PATH)

    app.run(debug=True, host=IP_HOST, port=PORT)
