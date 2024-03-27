from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate
from flask_security import Security
from celery.schedules import crontab



from api.UserAPI import UserAPI
from api.ApprovalAPI import ApprovalAPI
from api.SectionAPI import SectionAPI
from api.ProductAPI import ProductAPI
from api.CartAPI import CartAPI
from api.PurchaseAPI import PurchaseAPI
from api.VerifyAPI import VerifyAPI


from application.db import db
from application.cache import cache
import application.config as config
from application.security import user_datastore
from application.jobs import workers, tasks
from application.helpers import unauthorized_callback
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.config.from_object(config)
security = Security(app, user_datastore)
security.unauthorized_handler(unauthorized_callback)
app.security = security

# Enable Flask Cache
cache.init_app(app)
CORS(app)


# Flask Database Settings
migrate = Migrate(app, db)
db.init_app(app)

# Enable Celery
celery = workers.celery
celery.conf.update(
    broker_url=app.config['CELERY_BROKER_URL'],
    result_backend=app.config['CELERY_RESULT_BACKEND'],
    broker_connection_retry_on_startup=True,
    timezone = "Asia/kolkata",

)
celery.Task = workers.ContextTask
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    print("something supposed to happen")
    sender.add_periodic_task(
        crontab(minute=6, hour = 1), 
        tasks.sendDailyReminder.s(),
        name='send daily reminder'
    )
    # add a monthly report task here
    sender.add_periodic_task(
        crontab(day_of_month=1, month_of_year='*'),
        tasks.monthlyMail.s(),
        name='send monthly report'
    )
    

api = Api(app)
api.init_app(app)


app.app_context().push()

api.add_resource(UserAPI, '/api/user', '/api/user/<int:user_id>')
api.add_resource(ApprovalAPI, '/api/approve/<int:id>', '/api/approvals')
api.add_resource(SectionAPI, '/api/section', '/api/section/<int:section_id>')
api.add_resource(ProductAPI, '/api/product', '/api/product/<int:product_id>')
api.add_resource(CartAPI, '/api/cart', '/api/cart/<int:id>')
api.add_resource(PurchaseAPI, '/api/purchase', '/api/purchase/<string:id>')
api.add_resource(VerifyAPI, '/api/auth/verify')


def init_db():
    user_datastore.find_or_create_role(name="admin", description="User is an admin")
    user_datastore.find_or_create_role(name="manager", description="User is a Manager")
    user_datastore.find_or_create_role(name="user", description="User is an user")
    db.session.commit()
    if not user_datastore.find_user(email="admin@email.com"):
        user_datastore.create_user(
            email="admin@email.com", password=generate_password_hash("admin"), roles=["admin"])
    if not user_datastore.find_user(email="manager@email.com"):
        user_datastore.create_user(
            email="manager@email.com", password=generate_password_hash("manager"), roles=["manager"], active=True)
    if not user_datastore.find_user(email="manager2@email.com"):
        user_datastore.create_user(
            email="manager2@email.com", password=generate_password_hash("manager2"), roles=["manager"], active=True)
    if not user_datastore.find_user(email="user@email.com"):
        user_datastore.create_user(
            email="user@email.com", password=generate_password_hash("user"), roles=["user"])
    if not user_datastore.find_user(email="user2@email.com"):
        user_datastore.create_user(
            email="user2@email.com", password=generate_password_hash("user2"), roles=["user"])
    db.session.commit()

with app.app_context():
    import application.views

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_db()
        app.run(debug=True)


