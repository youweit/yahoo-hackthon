#!flask/bin/python
import os

os.environ['DATABASE_URL'] = 'mysql://root:y23684429@localhost/yahoo'

from app import app

if __name__ == '__main__':
    app.run("0.0.0.0", debug = False, port = 5000)