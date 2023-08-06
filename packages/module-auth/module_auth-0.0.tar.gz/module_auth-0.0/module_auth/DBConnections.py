# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 23:10:52 2022

@author: anugrahshrivastava
"""
""" Update History
Sr.		  UpdatedOn		        UpdatedBy		                       Desc
1		20/Dec/2022		   Anugrah Shrivastava	         Added method to prepare SP execute queries

"""
from Encryption import Encryptor
import re

def get_connectionstring(choice: int = 1, path: str = 'enc_db_config.txt') -> str:
    '''
    Returns connection string based on the channel provided

    Parameters
    ----------
    path : str, optional
        path and filename of the encrypted config file. The default is 'enc_db_config.txt'
    choice : int, optional
        choice of channel. 1 is for SourcePros, 2 for SourceAbled. The default is 1.

    Returns
    -------
    str
        Connection String.

    '''
    db_config = read_config(path)
    if choice == 2:
        section = db_config[1].strip().split('\n')
    else:
        section = db_config[0].strip().split('\n')
    DRIVER = 'SQL Server'
    SERVER = section[0].split('=')[1].strip()
    DATABASE = section[1].split('=')[1].strip()
    UID = section[2].split('=')[1].strip()
    PWD = section[3].split('=')[1].strip()

    CONNECTION_STRING = 'DRIVER={'+DRIVER+'}; SERVER='+SERVER+';DATABASE='+DATABASE+';UID='+UID+';PWD='+ PWD
    return CONNECTION_STRING


def read_config(path: str = '') -> str:
    '''
    Reads the encrypted config file for db and return the decrypted text

    Parameters
    ----------
    path : str, optional
        path and file name of the config file. The default is ''.

    Returns
    -------
    str
        Decrypted text.

    '''
    encryptor=Encryptor()
    loaded_key=encryptor.key_load('mykey.key')
    decrypted = encryptor.file_decrypt(loaded_key, path).decode("utf-8")
    return re.split(r'#', decrypted)
    
    
def prepare_stored_procedure_query(SP_name: str, **args) -> str:
    '''
    generates and sql query to execute SP based on the dynamic parameters provided

    Parameters
    ----------
    SP_name : str
        Name of the Stored procedure.
    **args : TYPE
        dynamic arguments.

    Returns
    -------
    str
        SP executionn query.

    '''
    sql = 'EXEC '+SP_name + ' '
    if len(args) == 0:
        return sql
    params = []
    for key,value in args.items():
        if value:
            if type(value) is str:
                params.append('@'+str(key)+" = '"+str(value.replace("'","''"))+"'")
            else:
                params.append('@'+str(key)+" = "+str(value))
    sql = sql + ', '.join(params)
    return sql