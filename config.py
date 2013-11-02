import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_RECORD_QUERIES = True


SQLALCHEMY_DATABASE_URI = 'mysql://root:y23684429@localhost/yahoo'

UPLOAD_FOLDER = os.path.join(basedir, 'images')
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

