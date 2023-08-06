# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 07:13:35 2023

@author: anugrahshrivastava
"""

from flask import Flask, make_response, request
from auth_model import auth_model
from flask_cors import CORS

app = Flask(__name__)
api = CORS(app)
app.config['JSON_SORT_KEYS'] = False
auth = auth_model()


@app.route('/api/test')
def test():
    return 'Authentication'

@app.route('/api/auth', methods=['GET'])
def authenticate_client():
    if(request.method == 'GET'):
        ClientKey = request.headers.get('ClientKey')
        ClientSecret = request.headers.get('ClientSecret')
        if ClientKey and ClientSecret:
            df = auth.auth_client(ClientKey, ClientSecret)
            if df.empty:
                return make_response({'Message':'Client Not Verified'}, 401)
            else:
                return make_response({'Message':'Client data verified', 
                                      'Access Token':auth.generate_token(str(df['clientkeyid'][0]), df['clientname'][0])}, 200)
        else:
            return make_response({'Message':'Invalid Inputs'}, 401)
    
if __name__ == '__main__':
    
    app.run( port = 5003 , threaded=True, debug=True, use_reloader = False)