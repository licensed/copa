from werkzeug.security import generate_password_hash as genpass
from flask_login import UserMixin
from datetime import datetime
from bolao import db
from sqlalchemy.orm import relationship


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
    posicao = db.Column(db.Integer, default=0)

    def __init__(self, sigla, nome, posicao=0):
        self.sigla = sigla
        self.nome = nome
        self.posicao = posicao

    def __repr__(self):
        return self.sigla


class Partida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    local = db.Column(db.String(50))
    time1_id = db.Column(db.Integer, db.ForeignKey('time.id'))
    time1 = db.relationship('Time', foreign_keys='Partida.time1_id')
    time2_id = db.Column(db.Integer, db.ForeignKey('time.id'))
    time2 = db.relationship('Time', foreign_keys='Partida.time2_id')
    placar_time1 = db.Column(db.Integer)
    placar_time2 = db.Column(db.Integer)

    def __init__(self, local, time1, time2, placar_time1=None, placar_time2=None):
        self.local = local
        self.time1_id = time1
        self.time2_id = time2
        self.placar_time1 = placar_time1
        self.placar_time2 = placar_time2

#    def __repr__(self):
#        return u"%s: %s X %s" % (self.id, self.time1, self.time2)


class Aposta(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('login.id'))
    usuario = db.relationship('Login', foreign_keys=usuario_id)
    partida_id = db.Column(db.Integer, db.ForeignKey('partida.id'))
    partida = db.relationship('Partida', foreign_keys=partida_id)
    placar_time1 = db.Column(db.Integer)
    placar_time2 = db.Column(db.Integer)
    pontuacao = db.Column(db.Integer, default=0)
    __table_args__ = (db.UniqueConstraint('usuario_id', 'partida_id',
                                          name='aposta'),)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
#    def __repr__(self):
#        return "Apostas {}".format(self.id)
