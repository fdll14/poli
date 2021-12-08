import os
from flask import Flask, request
from flask_bcrypt import Bcrypt
from flaskext.mysql import MySQL
from flask_session import Session



app = Flask(__name__)
mysql = MySQL()
app.config['SECRET_KEY'] = 'super secret key'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config['UPLOAD_FOLDER'] = os.path.abspath('app/static/upload/testimoni')

bcrypt = Bcrypt(app)

app.config['MYSQL_DATABASE_USER'] = os.getenv("DB_USER")
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv("DB_PASS")
app.config['MYSQL_DATABASE_DB'] = os.getenv("DB_NAME")
app.config['MYSQL_DATABASE_HOST'] = os.getenv("DB_HOST")
mysql.init_app(app)

from app.controllers import indexcontroller
from app.controllers import botcontroller
from app.controllers import logincontroller
from app.controllers import admincontroller
