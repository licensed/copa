from flask import Flask
from flask_sqlalchemy import SQLAlchemy as conn
from os import path


APP_DIR = path.abspath(path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + APP_DIR + "/database.sqlite"


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = conn(app)


from bolao.views import bolao
app.register_blueprint(bolao)

db.create_all()
