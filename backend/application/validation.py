from werkzeug.exceptions import HTTPException
from flask import make_response, jsonify
import json


class NotFoundError(HTTPException):
    def __init__(self, status_code, message=None):
        if status_code == 409 and not message:
            message = "already exists"
        if status_code == 404 and not message:
            message = "NOT FOUND"
        self.response = make_response(jsonify(message=message), status_code)
        self.response.headers['Content-Type'] = 'application/json'


class NotGivenError(HTTPException):
    def __init__(self, status_code, error_code, message):
        data = {"error_code": error_code, "message": message}
        self.response = make_response(json.dumps(data), status_code)
        self.response.headers['Content-Type'] = 'application/json'

class SchemaValidationError(HTTPException):
    def __init__(self, status_code, error_code, message):
        data = {"error_code": error_code, "message": message}
        self.response = make_response(json.dumps(data), status_code)
        self.response.headers['Content-Type'] = 'application/json'

        
class PropertyExistError(HTTPException):
    def __init__(self, status_code, message):
        data = {"message": message}
        self.response = make_response(json.dumps(data), status_code)
        self.response.headers['Content-Type'] = 'application/json'


class BusinessValidationError(HTTPException):
    def __init__(self, status_code, error_code, message):
        data = {"error_code": error_code, "message": message}
        self.response = make_response(json.dumps(data), status_code)
        self.response.headers['Content-Type'] = 'application/json'