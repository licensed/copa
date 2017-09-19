from flask import Flask
from flask_sqlalchemy import SQLAlchemy as conn
from os import path

APP_DIR = path.abspath(path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + APP_DIR + "/database.sqlite"
SECRET_KEY = b'9d236d8464e74cedb4c8d7042cd8bb16'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = SECRET_KEY

db = conn(app)


from bolao.views import bolao
app.register_blueprint(bolao)
#app.run(threaded=True)
db.create_all()
