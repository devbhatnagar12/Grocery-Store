from flask import request
from flask_restful import fields, marshal_with, reqparse, Resource
from flask import jsonify
from flask_security import current_user, auth_required, roles_accepted
from application.validation import NotGivenError, NotFoundError
from application.db import db, Section, User, Approval
from application.helpers import ApprovalType
from application.access import acs_section_all


section_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "creator_id": fields.Integer,
    "active": fields.String,
    "products": fields.List(fields.Nested({
        "id": fields.Integer,
        "name": fields.String,
        "description": fields.String,
        "price": fields.Float,
        "section_id": fields.Integer,
        "unit": fields.String,
        "stock": fields.Integer,
        "created_at": fields.DateTime,
        "expired_at": fields.DateTime,
    }))

}

section_parse = reqparse.RequestParser()
section_parse.add_argument("name", type=str, required=True, help="Name is required")

def get_section(section_id):
    sec = Section.query.filter_by(id=section_id).first()
    if not sec:
        raise NotFoundError(status_code=404, message="Section not found")
    return sec

class SectionAPI(Resource):
    @auth_required('token')
    @marshal_with(section_fields)
    def get(self):
        section_id = request.args.get("section_id")
        active = request.args.get("active")
        name = request.args.get("name")
        filters_provided = {}
        if active:
            filters_provided["active"] = active == 'true'
        if section_id:
            filters_provided["id"] = section_id
        if name:
            filters_provided["name"] = name
        if filters_provided:
            sections = Section.query.filter_by(**filters_provided).all()
            if not sections:
                raise NotFoundError(status_code=404, message="Section not found")
            return sections
        
        sections = acs_section_all()
        return sections

    
    @auth_required('token')
    @roles_accepted('manager', 'admin')
    @marshal_with(section_fields)
    def post(self):
        args = section_parse.parse_args()
        name = args.get("name")

        sec = Section.query.filter_by(name=name).first()
        role = current_user.roles[0].name

        if sec:
            if sec.active:
                raise NotGivenError(
                    status_code=400,
                    error_code="SECTION002",
                    message="Section already exists",
                )
            elif role == 'manager':
                raise NotGivenError(
                    status_code=400,
                    error_code="SECTION003",
                    message="Section exists but is not active, wait for admin's approval",
                )
            elif role == 'admin':
                sec.active = True
                db.session.commit()
                return sec

        active = role == 'admin'
        sec = Section(name=name, creator_id=current_user.id, active=active)
        db.session.add(sec)
        db.session.flush()

        if role == 'manager':
            print("manager making a request for section creation", sec.id)
            print(sec)
            approval = Approval(requester_id=current_user.id, description=ApprovalType.CREATE_SECTION.value, section_id=sec.id)
            db.session.add(approval)

        db.session.commit()
        return sec

    @auth_required('token')
    @roles_accepted('manager', 'admin')
    def delete(self, section_id):
        
        sec = get_section(section_id)

        role = current_user.roles[0].name

        if role == 'manager':
            # check if any approval request already exists or not
            approval = Approval.query.filter_by(requester_id=current_user.id, section_id=sec.id, description=ApprovalType.DELETE_SECTION.value, status="pending").first()
            if approval:
                raise NotGivenError(
                    status_code=400,
                    error_code="SECTION003",
                    message="Section delete request already exists",
                )
            approval = Approval(requester_id=current_user.id, description=ApprovalType.DELETE_SECTION.value, section_id = sec.id)

            db.session.add(approval)
            db.session.commit()
            return jsonify({"message": "Section delete request made successfully!! Please wait for admin approval"})
        elif role == 'admin':
            db.session.delete(sec)
            db.session.commit()
            return jsonify({"message": "Section deleted successfully!!"})
        
    
    @auth_required('token')
    @roles_accepted('admin')
    @marshal_with(section_fields)
    def put(self, section_id):
        args = section_parse.parse_args()
        name = args.get("name")
        sec = get_section(section_id)
        
        name_exists = Section.query.filter_by(name=name).first()
        if name_exists:
            raise NotGivenError(
                status_code=400,
                error_code="SECTION002",
                message="Section already exists",
            )
        sec.name = name
        db.session.commit()
        return sec