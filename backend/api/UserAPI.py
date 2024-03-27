from flask_restful import Resource, fields, marshal_with, reqparse
from flask import current_app as app, jsonify, request
from flask_security import current_user, auth_required
from application.validation import NotGivenError, NotFoundError
from application.db import db, User, Approval
from application.helpers import ApprovalType
from werkzeug.security import generate_password_hash
from application.security import user_datastore
from application.access import acs_user_all

user_fields = {
    "id": fields.Integer,
    "email": fields.String,
    "active": fields.Boolean,
    "role": fields.String(attribute=lambda x: x.roles[0].name if x.roles else None)
}

user_post_parser = reqparse.RequestParser()
user_post_parser.add_argument("email", type=str, required=True, help="Email is required")
user_post_parser.add_argument("password", type=str, required=True, help="Password is required")
user_post_parser.add_argument("role", type=str, required=True, help="Role is required")

user_put_parser = reqparse.RequestParser()
user_put_parser.add_argument("password", type=str, required=True, help="Password is required")

def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        raise NotFoundError(status_code=404, message="User not found")
    if not user.active:
        raise NotFoundError(status_code=404, message="User is inactive")
    return user

class UserAPI(Resource):
    @auth_required('token')
    @marshal_with(user_fields)
    def get(self):
        id = request.args.get("id")
        filters_provided = {}
        if id:
            filters_provided["id"] = id
        if filters_provided:
            users = User.query.filter_by(**filters_provided).all()
            if not users:
                raise NotFoundError(status_code=404, message="User not found")
            return users
        
        users = acs_user_all()
        return users, 200

    @auth_required('token')
    def put(self):
        args = user_put_parser.parse_args()
        password = args.get("password")
        
        user = get_user(current_user.id)
        
        user.password = generate_password_hash(password)
        db.session.commit()
        return jsonify({"message": "Password changed successfully!!"})

    @auth_required('token')
    def delete(self, user_id):
        user = get_user(user_id)
        
        db.session.delete(user)
        db.session.commit()
        return 200
        
    def post(self):
        args = user_post_parser.parse_args()
        email = args.get("email")
        password = args.get("password")
        role = args.get("role")
        
        existing_user = User.query.filter(User.email == email).first()
        if existing_user:
            raise NotFoundError(status_code=409, message="User already exists")
        
        with app.app_context():
            user = user_datastore.create_user(email=email, password=generate_password_hash(password), roles=[role], active=role != 'manager')
            db.session.flush()
            if role == 'manager':
                approval = Approval(requester_id=user.id, description=ApprovalType.CREATE_MANAGER.value)
                db.session.add(approval)
            db.session.commit()
        return {"message": "successfully registered!!"}, 201