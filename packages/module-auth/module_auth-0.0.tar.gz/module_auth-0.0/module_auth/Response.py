# -*- coding: utf-8 -*-
#=============================================
# Author: Anugrah Shrivastava
# Create date: Tue May 17 23:20:28 2022
# Description: This file contains a 'Response' class which is used to return a fix structured response for the flask APIs
#              There is also a method to log exceptions in file and database
# =============================================
""" Update History
Sr.		UpdatedOn		         UpdatedBy		                       Desc
1		21/June/2022		Anugrah Shrivastava	          Added method to insert data into database
2       19/Oct/2022         Anugrah Shrivastava           Added Feature for switching channels
3.      14/Dec/2022         Anugrah Shrivastava           Updated API to return years of experience and gap period in response
"""


import datetime
import openpyxl
import pyodbc
from DBConnections import get_connectionstring, prepare_stored_procedure_query

import pypyodbc


class Response:
    
    #constructor
    def __init__(self, channel = 1):
        self.status_code = 200
        self.message = 'Processed Successfully'
        self.connection_string = get_connectionstring(channel)
        self.add_data()
        
    #method to log errors in text file
    def add_error(self,module: str, error_message: str, traceback = '', error_type: str = '', reference_table:str = 'NULL', reference_id: int = 0, severity: str = 'Error'):
        '''
        Log error in a text file

        Parameters
        ----------
        module : str
            Class/Project/Module for which the error occured.
        error_message : str
            Error message.
        traceback : TYPE, optional
            traceback informationn of exception. The default is None.
        error_type : str, optional
            Type/class of exception. The default is None.
        reference_table : str, optional
            Tablename for reference (eg. CandidateMaster). The default is 'NULL'.
        reference_id : int, optional
            Primary key or ID from the reference_table(eg. CandidateID). The default is 0.
        severity : str, optional
            Priority of the error(Critical, Error, Warning, Log). The default is 'Error'

        Returns
        -------
        None.

        '''
        
        try:
            wb = openpyxl.load_workbook('ErrorLog//ErrorLog.xlsx')
            sheet = wb.active
    
            sheet.insert_rows(2)
            for col_idx, cell_val in enumerate([module, error_message, str(traceback), str(error_type), reference_table, str(reference_id), severity, str(datetime.datetime.today())], 1):
                sheet.cell(row=2, column=col_idx, value=cell_val)
            
            # save the changes to the file
            wb.save('ErrorLog//ErrorLog.xlsx')
        except Exception as e:
            print(e)
            self.add_error_to_db(str(e), 'Logging', severity = 'Critical')
        finally:
            wb.close()
        
            self.add_error_to_db(error_message, module, reference_table, reference_id, severity)

    #Add error into database
    def add_error_to_db(self, message: str, module: str = 'NULL', reference_table: str = 'NULL', reference_id: int = 0, severity: str='Error'):
        """
        Inserts/Logs the exception in database.

        Parameters
        ----------
        message : str
            Error Message.
        module : str, optional
            Class/Project/Module for which the error occured. The default is 'NULL'.
        reference_table : str, optional
            Tablename for reference (eg. CandidateMaster). The default is 'NULL'.
        reference_id : int, optional
            Primary key or ID from the reference_table(eg. CandidateID). The default is 0.
        severity : str, optional
            Priority of the error(Critical, Error, Warning, Log). The default is 'Error'.

        Raises
        ------
        Exception
            If the data is not inserted.

        Returns
        -------
        None.

        """
        try:    
            conn = pyodbc.connect(self.connection_string)
            cursor = conn.cursor()
            cursor.execute("""EXEC USP_IU_AI_ExceptionLog
                           @ReferenceTable = ?,
                           @ReferenceID = ?,
                           @ExceptionModule = ?,
                           @ExceptionMessage = ?  ,
                           @ExceptionSeverity = ?
                        """, 
            str(reference_table),
            str(reference_id),
            str(module),
            str(message),
            str(severity)
            )
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            conn.close()
        
    #method to add default values to response data with a fixed format
    def add_data(self, candidate_id: int = 0, name: str = '', email: str = '', contact: str = '', address: dict = {}, education: dict = {}, expr: dict = {}, years_of_experience: int = 0, gap_period: list = [], skills: dict = {}, certificates: dict = {}):
        '''
        Creates a response JSON data

        Parameters
        ----------
        candidate_id : int, optinal
            Candidate ID. The default is 0
        name : str, optional
            Candidate Name. The default is ''.
        email : str, optional
            Candidate email ID. The default is ''.
        contact : str, optional
            Candidate primary contact number. The default is ''.
        address : dict, optional
            Candidate primary location object. The default is {}.
        education : dict, optional
            Candidate education details object. The default is {}.
        expr : dict, optional
            Candidate experience details object. The default is {}.
        years_of_experience: int, optional
            Total years of experience
        gap_period: list
            List of gap period range
        skills : str, optional
            Candidate skills list. The default is ''.
        certificates : dict, optional
            Candidate certificate details object. The default is {}.

        Returns
        -------
        None.

        '''
        self.data = {
            'Candidate ID': candidate_id,
            'Name':name,
            'Email':email,
            'Contact':contact,
            'Location':{
                'ZipCode':'',
                'City':'',
                'State': '',
                'Country': '',
                'Full Street': '',
                'Address':''
                },
            'Education':[{k:v} for k, v in education.items()],
            'Experience':[{k:v} for k, v in expr.items()],
            "Years of Experience" : years_of_experience,
            'Gap Period' : gap_period,
            'Skills':skills,
            'Certificates': certificates
            }
        if address:
            self.data['Location'] = {
                'ZipCode': address['postal_code'],
                'City': address['city'],
                'State': address['region1'],
                'Country': address['country_id'],
                'Full Street': address['full_street'],
                'Address': address['full_address']
                }
    def save_response_in_db(self, jsondata: str, channel: int, parsed_by: str, userid:int =  55, candidate_id: int = 0, file_name: str = ''):
        '''
        This method is used to insert the parsed data into db in a JSON format

        Parameters
        ----------
        jsondata : str
            Response object in the form of JSON.
        channel : int
            Source of database.
        parsed_by : str
            Depends on the endpoint chosen to parse the resume (File/ID/Text).
        userid : int, optional
            User. The default is 55.
        candidate_id : int, optional
            ID of candidate if present. The default is 0.
        file_name : str, optional
            Name of the resume file. The default is ''.

        Returns
        -------
        None.

        '''
        response = Response(channel)
        try:
            CONNECTION_STRING = get_connectionstring(channel)
            conn = pypyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            sql = prepare_stored_procedure_query('Usp_AI_IU_ResumeParserJSONMaster', CandidateID = candidate_id, 
                                                 UserId = userid,
                                                 ParsedBy = parsed_by,
                                                 JSONData = jsondata,
                                                 ResumeName = file_name
                                                 )
            
            cursor.execute(sql)
            
            conn.commit()
        except Exception as e:
            print(e)
            response.add_error('JSON Data Insertion', 'Candidate ID : '+str(candidate_id) + '\n' + str(e))
        finally:
            conn.close()

    
