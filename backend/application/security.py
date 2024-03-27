from flask_security import SQLAlchemyUserDatastore
from .db import db, User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
