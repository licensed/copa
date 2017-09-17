from datetime import datetime
from os import path

from flask import (Flask, flash, g, redirect, render_template, request,
                   session, url_for)
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
from flaskext.markdown import Markdown
from models import Login, Aposta, Time, Partida, db
from sqlalchemy import exc
from werkzeug.security import check_password_hash as chpass

app = Flask(__name__)
app.config.from_pyfile("config.py")
login_manager = LoginManager()
login_manager.init_app(app)
Markdown(app)
login_manager.login_view = "login"
db.init_app(app)


@app.template_filter('truncate_chars')
def truncate_chars(s):
    return s[:500]


@login_manager.user_loader
def user_loader(user_id):
    return Login.query.get(int(user_id))


@app.before_request
def before_request():
    db.create_all()


@app.errorhandler(404)
def errorhandler(e):
    return redirect(url_for("login"))


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


@app.route("/", methods=["POST", "GET"])
@login_required
def index():
    if request.method == "POST":
        fname = request.form["name"]

        aposta = Aposta(id=fname, usuario_id=current_user.id)
        db.session.add(aposta)
        db.session.commit()
        return redirect(url_for("result"))

    return render_template("index.html")


@app.route("/result", methods=["POST", "GET"])
@login_required
def result():
    aposta = Aposta.query.all()
    return render_template("result.html", result=aposta,
                            user=current_user.username)


@app.route("/public", methods=["POST", "GET"])
def public():
    aposta = Aposta.query.all()
    return render_template("public.html", result=aposta)


@app.route("/public/<int:aposta_id>", methods=["POST", "GET"])
def aposta(aposta_id):
    aposta = Aposta.query.filter_by(id=aposta_id).first()
    return render_template("post.html", result=aposta)


@app.route("/times", methods=["POST", "GET"])
@login_required
# Sigla Nome Posicao
def times():
    if request.method == "POST":
        nome = request.form["nome"]
        sigla = request.form["sigla"]
        time = Time(nome=nome, sigla=sigla)
        db.session.add(time)
        db.session.commit()
        return redirect(url_for("times"))
    else:
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


@app.route("/partidas", methods=["POST", "GET"])
@login_required
# Local Time1 Time2 placar_time1 placar_time2
def partidas():
    partidas = Partida.query.all()
    return render_template("partidas.html", result=partidas)


@app.route("/apostas", methods=["POST", "GET"])
@login_required
#
def apostas():
    apostas = Aposta.query.all()
    for x in apostas:
        print(x.partida_id)
    return render_template("apostas.html", result=apostas)


@app.route("/partida_add", methods=["POST", "GET"])
@login_required
def partida_add():
    times = Time.query.all()
    if request.method == "POST":
        local = request.form.get('local')
        time1 = request.form.get('time1')
        time2 = request.form.get('time2')
        placar_time1 = request.form.get('placar_time1')
        placar_time2 = request.form.get('placar_time2')
        partida = Partida(local=local, time1_id=time1, time2_id=time2, placar_time1=placar_time1, placar_time2=placar_time2)
        db.session.add(partida)
        db.session.commit()
        return redirect(url_for("partidas"))
    else:
        return render_template("partida_add.html", times=times)


@app.route("/aposta_add/<int:partida_id>")
@login_required
#usuario, partida, placar_time1, placar_time2 (hora, edicao, pontuacao)
def aposta_add(partida_id):
    gols_time1 = request.form.get('gols_time1')
    gols_time2 = request.form.get('gols_time2')
    print("else", gols_time1)
    if gols_time1 and gols_time2:
        print("aew", gols_time1)
        aposta = Aposta(usuario=current_user, partida_id=partida_id, placar_time1=gols_time1, placar_time2=gols_time2)
        db.session.add(aposta)
        db.session.commit()
    return redirect(url_for("apostas"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You are now Logged Out !")
    return redirect(url_for("login"))


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


if __name__ == '__main__':
    app.run()
