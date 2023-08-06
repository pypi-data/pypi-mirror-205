# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 02:57:27 2023

@author: anugrahshrivastava
"""

from datetime import datetime, timedelta
import jwt
from flask import make_response, request
from functools import wraps
import pandas as pd
from DBConnections import get_connectionstring, prepare_stored_procedure_query
import pypyodbc
from Response import Response
import re
import os

response = Response()

class auth_model():
    
  
    
    def auth_client(self, client_key: str, client_secret: str):
        '''
        Verifies the existence of client ky and client secret combination in the DB.
        Returns row if found.

        Parameters
        ----------
        client_key : str
            DESCRIPTION.
        client_secret : str
            DESCRIPTION.

        Returns
        -------
        df : TYPE
            DESCRIPTION.

        '''
        try:
            CONNECTION_STRING = get_connectionstring(1)
            conn = pypyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            sql = prepare_stored_procedure_query('Usp_AI_VerifyClient',
                                                 ClientKey = client_key, ClientSecret = client_secret)
            cursor.execute(sql)
            df= pd.DataFrame.from_records(cursor, columns = [i[0] for i in cursor.description])
            
        except Exception as e:
            response.add_error('Client Authentication', str(e), severity='Critical')
        finally:
            conn.close()
            return df
        
    
    def token_auth(self):
        '''
        Decorator function to authenticate all API endpoints 

        Returns
        -------
        TYPE
            DESCRIPTION.

        '''
        def inner1(func):
            @wraps(func)
            def inner2(*args):
                '''
                Checks the authentication and validity of the access token

                Parameters
                ----------
                *args : dynamic
                    arguments passed to the inner function call.

                Returns
                -------
                TYPE
                    DESCRIPTION.

                '''
                try:
                    access_token = request.headers.get('authorization')
                    if not access_token:
                        response.add_error('Authentication', 'Missing Token')

                        return make_response({'message':'You are unauthorized'}, 401)
                    if re.match("^Bearer *([^ ]+) *$", access_token, flags=0):
                        token = access_token.split(" ")[1]
                    else:
                        return make_response({'message':'Invalid Token'}, 401)

                except Exception as e:
                    response.add_error('Authentication', str(e))

                    return make_response({'message':'You are unauthorized'}, 401)
                
                try:    
                    decoded = jwt.decode(token, os.environ['SECRET_KEY'],algorithms="HS512")
                except jwt.ExpiredSignatureError as e:
                    response.add_error('Decode','token '+ token +' '+ str(e))
                    return make_response({'message':str(e)}, 401)
                # except jwt.InvalidTokenError as e:
                #     print(e)
                #     return make_response({'message':'You are unauthorized'}, 401)
                except Exception as e:
                    response.add_error('Decode','token '+ token +' '+ str(e))
                    return make_response({'message':'You are unauthorized'}, 401)
                
                try:
                    payload = decoded['payload']
                    if payload['verified']:
                        print('ok')
                        return func(*args)
                    else:
                        return make_response({'message':'You are unauthorized'}, 401)
            
                except Exception as e:
                    response.add_error('Verify', str(e))
                    return make_response({'message':'You are unauthorized'}, 401)
            
            return inner2
        return inner1
    
    def generate_token(self, ClientID: str, ClientName: str):
        '''
        Generates a JWT token

        Parameters
        ----------
        ClientID : str
            Client ID to add in payload.
        ClientName : str
            Client Name to add in payload.

        Returns
        -------
        encoded : TYPE
            JWT Token.

        '''
        exp = int((datetime.now() + timedelta(days=1)).timestamp())
        payload = {
            "payload":{
                "ClientID":ClientID,
                "ClientName":ClientName,
                "verified":True
                },
            "exp":exp
            }
        encoded = jwt.encode(payload, os.environ['SECRET_KEY'],algorithm="HS512")
        return encoded

    