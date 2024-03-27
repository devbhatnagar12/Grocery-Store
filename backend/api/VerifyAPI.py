from flask_restful import Resource, reqparse
from flask_security import current_user, auth_required
from flask import jsonify


auth_parser = reqparse.RequestParser()
auth_parser.add_argument("email", type=str, required=True, help="Email is required")
auth_parser.add_argument("role", type=str, required=True, help="Role is required")

class VerifyAPI(Resource):
    @auth_required('token')
    def post(self):
        data = auth_parser.parse_args()
        
        # check if the token, email and role are matching
        if current_user.email == data.get("email") and current_user.roles[0].name == data.get("role"):
            return jsonify({"message": "Token is valid"})
        else:
            return jsonify({"message": "Token is invalid"}), 400

