SQLALCHEMY_DATABASE_URI = 'sqlite:///base.sqlite3'

CACHE_TYPE = "RedisCache"
CACHE_REDIS_URL = "redis://localhost:6379/0"
CACHE_DEFAULT_TIMEOUT = 300
DEB0UG = False

# Upload Files Conf
UPLOAD_FOLDER = 'static/export/'
EMAIL_TEMPLATE = 'templates/'
PDF_FOLDER = 'static/pdf/'

# Celery
CELERY_BROKER_URL = "redis://localhost:6379/1"
CELERY_RESULT_BACKEND = "redis://localhost:6379/2"

# JWT TOKEN EXPIRATION
JWT_ACCESS_TOKEN_EXPIRES = 3600
JWT_IDENTITY_CLAIM = 'email'


SECRET_KEY =  "ccb24cc3-0cde-470b-b493-b809b56d8e74"
SECURITY_PASSWORD_SALT = "27a3d914-e9b2-4fc1-a1ba-f3f8bfc446d6"
DEBUG = True
WTF_CSRF_ENABLED = False
SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'