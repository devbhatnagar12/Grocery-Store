from flask import request
from flask_restful import Resource, fields, marshal_with
from flask_security import roles_required, auth_required
from application.helpers import ApprovalType, get_section, check_user_exists_and_active
from flask import jsonify
from application.db import Approval, db
from application.validation import NotFoundError
from application.security import user_datastore
from application.access import acs_approval_with_status

# Define the fields for the Approval resource
approval_fields = {
    "id": fields.Integer,
    "description": fields.String,
    "requester_id": fields.Integer,
    "section_id": fields.Integer(default=None),
    "status": fields.String,
}

class ApprovalAPI(Resource):
    """
    This class represents the Approval resource. It contains methods for handling
    the HTTP methods GET, PUT, and DELETE.
    """

    @auth_required('token')
    @roles_required('admin')    
    def put(self, id):
        """
        Handles the approval or rejection of a given item identified by its id.

        This method requires authentication and admin role. It checks the current status of the item.
        If the status is already 'approved' or 'rejected', it returns a message indicating that.
        If the status is 'pending', it handles the approval or rejection based on the 'type' parameter in the request.
        If the 'type' is neither 'approve' nor 'reject', or if the status is not recognized, it returns an 'Invalid' message.

        Parameters:
        id (int): The id of the item to be approved or rejected.

        Returns:
        Flask.Response: A JSON response that contains a message about the result of the operation.
        """
        type = request.args.get("type")  # Get the type parameter from the request
        app = self._get_approval(id)  # Get the Approval object

        # Check the current status of the Approval object and handle accordingly
        if app.status in ("rejected", "approved"):
            return jsonify({"message":"Already {0}".format(app.status)})
        elif app.status == "pending":
            if type == "approve":
                return self._handle_approval_types(app)
            elif type == "reject":
                return self._handle_rejection_types(app)
            else:
                return jsonify({"message":"Invalid type"})
        else:
            return jsonify({"message":"Invalid status"}) 
        
    @auth_required('token')
    @roles_required('admin')
    @marshal_with(approval_fields)
    def get(self):
        """
        Handles the GET request for the Approval resource.

        This method requires authentication and admin role. It returns all Approval objects
        if no status parameter is provided in the request. If a status parameter is provided,
        it returns all Approval objects with that status.

        Returns:
        list: A list of Approval objects.
        """
        status = request.args.get("status")  
        if status:
            if status not in ("pending", "approved", "rejected"):
                return jsonify({"message":"Invalid status"})
            apps = acs_approval_with_status(status)
            return apps
        
        apps = Approval.query.all()  
        return apps
    
    @auth_required('token')
    @roles_required('admin')
    def delete(self, id):
        """
        Handles the DELETE request for the Approval resource.

        This method requires authentication and admin role. It deletes the Approval object
        identified by the given id and any associated Section object.

        Parameters:
        id (int): The id of the Approval object to be deleted.

        Returns:
        None
        """
        app = self._get_approval(id)  
        if app.section_id is not None:
            section = get_section(app.section_id) 
            db.session.delete(section)  
        app.status = "rejected"
        
        db.session.commit()  
        return jsonify({"message":"Approval deleted successfully!!"})
        

    def _get_approval(self, approval_id):
        app = Approval.query.filter_by(id=approval_id).first()
        if not app:
            raise NotFoundError(status_code=404, message="Approval not found")
        return app


    def _handle_approval_types(self, app):
        if app.description == ApprovalType.CREATE_MANAGER.value:
            return self._approve_manager(app)
        elif app.description == ApprovalType.CREATE_SECTION.value:
            return self._approve_create_section(app)
        elif app.description == ApprovalType.DELETE_SECTION.value:
            return self._approve_delete_section(app)

    def _approve_manager(self, app):
        user = user_datastore.find_user(id=app.requester_id)
        if not user:
            raise NotFoundError(status_code=404, message="User not found")
        
        user_datastore.activate_user(user)
        app.status = "approved"
        db.session.commit()
        return jsonify({"message":"Manager approved successfully!!"})

    def _approve_create_section(self, app):
        check_user_exists_and_active(app.requester_id)
        section = get_section(app.section_id)
        
        section.active = True
        app.status = "approved"
        db.session.commit()
        return jsonify({"message":"Section create request approved. Section {0} created successfully!!".format(section.name)})

    def _approve_delete_section(self, app):
        check_user_exists_and_active(app.requester_id)
        section = get_section(app.section_id)
        
        db.session.delete(section)
        app.status = "approved"
        db.session.commit()
        return jsonify({"message":"Section delete request approved. Section {0} deleted successfully!!".format(section.name)})
    
    def _handle_rejection_types(self, app):
        if app.description == ApprovalType.CREATE_MANAGER.value:
            return self._reject_manager(app)
        elif app.description == ApprovalType.CREATE_SECTION.value:
            return self._reject_create_section(app)
        elif app.description == ApprovalType.DELETE_SECTION.value:
            return self._reject_delete_section(app)
        
    def _reject_manager(self, app):
        user = user_datastore.find_user(id=app.requester_id)
        if not user:
            raise NotFoundError(status_code=404, message="User not found")
        
        user_datastore.delete_user(user)
        app.status = "rejected"
        db.session.commit()
        return jsonify({"message":"Manager rejected successfully!!"})
    
    def _reject_create_section(self, app):
        check_user_exists_and_active(app.requester_id)
        section = get_section(app.section_id)
        
        db.session.delete(section)
        app.status = "rejected"
        db.session.commit()
        return jsonify({"message":"Section create request rejected. Section {0} deleted successfully!!".format(section.name)})
    
    def _reject_delete_section(self, app):
        check_user_exists_and_active(app.requester_id)
        app.status = "rejected"
        db.session.commit()
        return jsonify({"message":"Section delete request rejected."})



