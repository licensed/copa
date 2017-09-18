from flask_sqlalchemy import SQLAlchemy as conn
from werkzeug.security import generate_password_hash as genpass
from flask_login import UserMixin
from datetime import datetime


db = conn()


class Login(UserMixin, db.Model):

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(80))
    is_admin = db.Column(db.Boolean(), default=False)
    sign_date = db.Column(db.DateTime, default=datetime.utcnow())

    aposta_id = db.relationship("Aposta", backref="login", lazy="dynamic")

    def __init__(self, username, email, name, password):
        self.username = username
        self.email = email
        self.name = name
        self.password = genpass(password)

    def __repr__(self):
        return "Login {}".format(self.username)


class Time(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sigla = db.Column(db.String(3), unique=True)
    nome = db.Column(db.String(80))
    posicao = db.Column(db.Integer)

    def __repr__(self):
        return self.nome


class Partida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    local = db.Column(db.String(50))
    time1_id = db.Column(db.Integer, db.ForeignKey('time.id'))
    time1 = db.relationship('Time', foreign_keys=time1_id)
    time2_id = db.Column(db.Integer, db.ForeignKey('time.id'))
    time2 = db.relationship('Time', foreign_keys=time2_id)
    placar_time1 = db.Column(db.Integer)
    placar_time2 = db.Column(db.Integer)

    def __repr__(self):
        return u"%s: %s X %s" % (self.id, self.time1, self.time2)


class Aposta(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('login.id'))
    usuario = db.relationship('Login', foreign_keys=usuario_id)
    partida_id = db.Column(db.Integer, db.ForeignKey('partida.id'))
    partida = db.relationship('Partida', foreign_keys=partida_id)
    placar_time1 = db.Column(db.Integer)
    placar_time2 = db.Column(db.Integer)
    hora = db.Column(db.DateTime(), default=datetime.now())
    edicao = db.Column(db.DateTime())
    pontuacao = db.Column(db.Integer, default=0)
    __table_args__ = (db.UniqueConstraint('usuario_id', 'partida_id',
                                          name='aposta'),)

    def __repr__(self):
        return "Apostas {}".format(self.id)
