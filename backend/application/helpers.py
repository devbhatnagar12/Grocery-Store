import uuid
from datetime import datetime
from enum import Enum
from flask import jsonify
from application.db import Section
from application.validation import NotFoundError
from application.security import user_datastore
from application.validation import NotFoundError

def check_user_exists_and_active(user_id):
    if user_datastore.find_user(id=user_id, active=True) is None:
        raise NotFoundError(status_code=404, message="User not found or is not active")

def unauthorized_callback():
    response = jsonify({
        'message': 'Unauthorized access. Missing or invalid Authorization header.'
    })
    response.status_code = 401
    return response


def generate_unique_order_id():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]  # Use the current timestamp
    unique_id = str(uuid.uuid4().int)[-6:]  # Use the last 6 digits of a UUID to ensure uniqueness
    order_id = f"{timestamp}-{unique_id}"
    return order_id

class ApprovalType(Enum):
    CREATE_MANAGER = "approve creation of manager"
    CREATE_SECTION = "approve creation of section"
    DELETE_SECTION = "approve deletion of section"


def get_section(section_id):
    sec = Section.query.filter_by(id=section_id).first()
    if not sec:
        raise NotFoundError(status_code=404, message="Section not found")
    return sec