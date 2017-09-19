import json, requests
from flask import request, jsonify, Blueprint, abort, flash, redirect, url_for, render_template
from flask.views import MethodView
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
from bolao import db, app
from bolao.models import Time, Login, Aposta, Partida
from sqlalchemy import exc
from werkzeug.security import check_password_hash as chpass
from datetime import datetime

bolao = Blueprint('bolao', __name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def user_loader(user_id):
    return Login.query.get(int(user_id))


@app.route("/", methods=["POST", "GET"])
@login_required
def index():
    users = Login.query.all()
    return render_template("index.html", users=users)


@app.route("/sign", methods=["GET", "POST"])
def sign():
    if request.method == "POST":
        if not request.form["username"]:
            flash("Enter with a Username")
        elif not request.form["email"]:
            flash("Enter with a Email")
        elif not request.form["name"]:
            flash("Enter with a Name")
        elif not request.form["password"]:
            flash("Enter with a Password")
        else:
            try:
                user = Login(request.form["username"],
                             request.form["email"],
                             request.form["name"],
                             request.form["password"])
                db.session.add(user)
                db.session.commit()
                flash("User Sign")
                return redirect(url_for("login"))
            except exc.IntegrityError:
                flash("This Username Or Email Alredy Exists")
                return redirect(url_for("login"))

    return render_template("sign.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        log_user = Login.query.filter_by(username=request.form["username"]).first()
        if log_user:
            if log_user.username == request.form["username"] and (
            chpass(log_user.password, request.form["password"]) == True):
                login_user(log_user)
                return redirect(url_for("index"))

        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You are now Logged Out !")
    return redirect(url_for("login"))


class TimeView(MethodView):
    #decorators = [login_required]

    def get(self, id=None, page=1):
        if not id:
            times = Time.query.paginate(page, 10).items
            res = {}
            for time in times:
                res[time.id] = {
                    'sigla': time.sigla,
                    'nome': time.nome,
                    'posicao': time.posicao,
                }
        else:
            time = Time.query.filter_by(id=id).first()
            if not time:
                abort(404)
            res = {
                'sigla': time.sigla,
                'nome': time.nome,
                'posicao': time.posicao,
            }
        return jsonify(res)

    def post(self):
        sigla = request.form.get('sigla')
        nome = request.form.get('nome')
        posicao = request.form.get('posicao')
        time = Time(sigla, nome, posicao)
        db.session.add(time)
        db.session.commit()
        return jsonify({time.id: {
            'sigla': time.sigla,
            'nome': time.nome,
            'posicao': time.posicao,
        }})

    def put(self, id=None):
        if not id:
            pass
        else:
            time = Time.query.filter_by(id=id).first()
            sigla = request.json['sigla'] or time.sigla
            nome = request.json['nome'] or time.nome
            posicao = request.json['posicao'] or time.posicao
            time.sigla = sigla
            time.nome = nome
            time.posicao = posicao
            db.session.commit()
        return self.get()

    def delete(self, id):
        time = Time.query.filter_by(id=id).first()
        db.session.delete(time)
        db.session.commit()
        return self.get()


class PartidaView(MethodView):
    #decorators = [login_required]

    def get(self, id=None, page=1):
        if not id:
            partidas = Partida.query.paginate(page, 10).items
            res = {}
            for partida in partidas:
                res[partida.id] = {
                    'local': partida.local,
                    'time1': partida.time1,
                    'time2': partida.time2,
                    'placar_time1': partida.placar_time1,
                    'placar_time2': partida.placar_time2,
                }
        else:
            partida = Partida.query.filter_by(id=id).first()
            if not partida:
                abort(404)
            res = {
                'local': partida.local,
                'time1': json.dumps(partida.time1),
                'time2': json.dumps(partida.time2),
                'placar_time1': partida.placar_time1,
                'placar_time2': partida.placar_time2,
            }
        return jsonify(res)

    def post(self):
        local = request.form.get('local')
        time1 = request.form.get('time1')
        time2 = request.form.get('time2')
        local_time1 = request.form.get('local_time1')
        local_time2 = request.form.get('local_time2')
        partida = Partida(local, time1, time2, local_time1, local_time2)
        db.session.add(partida)
        db.session.commit()
        return jsonify({partida.id: {
                'local': partida.local,
                'time1': partida.time1,
                'time2': partida.time2,
                'placar_time1': partida.placar_time1,
                'placar_time2': partida.placar_time2,
        }})

    def put(self, id=None):
        if not id:
            pass
        else:
            partida = Partida.query.filter_by(id=id).first()
            local = request.json['local'] or partida.local
            time1 = request.json['time1'] or partida.time1
            time2 = request.json['time2'] or partida.time2
            placar_time1 = request.json['placar_time1'] or partida.placar_time1
            placar_time2 = request.json['time1'] or partida.placar_time2
            partida.local = local
            partida.time1 = time1
            partida.time2 = time2
            partida.placar_time1 = placar_time1
            partida.placar_time2 = placar_time2
            db.session.commit()
        return self.get()

    def delete(self, id):
        partida = Partida.query.filter_by(id=id).first()
        db.session.delete(partida)
        db.session.commit()
        return self.get()


class ApostaView(MethodView):

    def get(self, id=None, page=1):

        if not id:
            apostas = Aposta.query.paginate(page, 10).items
        else:
            apostas = Aposta.query.filter_by(usuario_id=id).paginate(page, 10).items
        if not apostas:
            abort(404)
        res = {}
        for aposta in apostas:
            res[aposta.id] = {
                'usuario': aposta.usuario,
                'partida': aposta.partida,
                'placar_time1': aposta.placar_time1,
                'placar_time2': aposta.placar_time2,
                'hora': aposta.hora,
                'edicao': aposta.edicao,
                'pontuacao': aposta.pontuacao,
            }
        return jsonify(res)

    def post(self):
        gols_time1 = request.json.get('gols_time1')
        gols_time2 = request.json.get('gols_time2')
        pontuacao = request.json.get('pontuacao')
        partida = request.json.get('partida')
        if gols_time1 and gols_time2:
            aposta = Aposta(usuario=current_user, partida_id=partida,
                            placar_time1=gols_time1, placar_time2=gols_time2,
                            pontuacao=pontuacao)
            db.session.add(aposta)
            db.session.commit()
        return jsonify({aposta.id: {
            'usuario': aposta.usuario,
            'partida': aposta.partida,
            'placar_time1': aposta.placar_time1,
            'placar_time2': aposta.placar_time2,
            'hora': aposta.hora,
            'edicao': aposta.edicao,
            'pontuacao': aposta.pontuacao,
        }})

    def put(self, id):
        aposta = Aposta.query.filter_by(id=id).first()
        placar_time1 = request.form.get('placar_time1') or aposta.placar_time1
        placar_time2 = request.form.get('placar_time2') or aposta.placar_time2
        pontuacao = request.form.get('pontuacao') or aposta.pontuacao
        edicao = datetime.now()
        aposta.placar_time1 = placar_time1
        aposta.placar_time2 = placar_time2
        aposta.pontuacao = pontuacao
        aposta.edicao = edicao
        db.session.commit()
        return jsonify(aposta)

    def delete(self, id):
        db.session.query(Time).filter_by(id=id).delete()
        db.session.commit()
        return "DELETADO"


time_view = TimeView.as_view('time_view')
app.add_url_rule(
    '/time/', view_func=time_view, methods=['GET', 'POST']
)
app.add_url_rule(
    '/time/<int:id>', view_func=time_view, methods=['GET', 'PUT', 'DELETE']
)

partida_view = PartidaView.as_view('partida_view')
app.add_url_rule(
    '/partida/', view_func=partida_view, methods=['GET', 'POST']
)
app.add_url_rule(
    '/partida/<int:id>', view_func=partida_view, methods=['GET', 'PUT', 'DELETE']
)

aposta_view = ApostaView.as_view('aposta_view')
app.add_url_rule(
    '/aposta/', view_func=aposta_view, methods=['GET', 'POST']
)
app.add_url_rule(
    '/aposta/<int:id>', view_func=aposta_view, methods=['GET', 'PUT', 'DELETE']
)

@app.route("/times", methods=["POST", "GET"])
@login_required
# Sigla Nome Posicao
def times():
    times = Time.query.all()
    return render_template("times.html", result=times)

@app.route("/time_add", methods=["POST", "GET"])
@login_required
def time_add():
    if request.method == "POST":
        nome = request.form["nome"]
        sigla = request.form["sigla"]
        time = Time(nome=nome, sigla=sigla)
        db.session.add(time)
        db.session.commit()
        return redirect(url_for("times"))
    else:
        return render_template("time_add.html")


@app.route("/time_update/<int:id>", methods=["POST", "GET"])
@login_required
def time_update(id):
    time = Time.query.filter_by(id=id).first()
    if request.method == "POST":
        time.sigla = request.form["sigla"]
        time.nome = request.form["nome"]
        db.session.commit()
        return redirect(url_for("times"))

    return render_template("time_update.html", time=time)


@app.route("/time_delete/<int:id>")
@login_required
def time_delete(id):
    db.session.query(Time).filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for("times"))