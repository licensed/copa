import json
from flask import request, jsonify, Blueprint, abort
from flask.views import MethodView
from bolao import db, app
from bolao.models import Time

bolao = Blueprint('bolao', __name__)


@bolao.route('/')
@bolao.route('/home')
def home():
    return "Welcome to the Catalog Home."


class TimeView(MethodView):

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

    def put(self, id):
        # Update the record for the provided id
        # with the details provided.
        return

    def delete(self, id):
        # Delete the record for the provided id.
        return


time_view = TimeView.as_view('time_view')
app.add_url_rule(
    '/time/', view_func=time_view, methods=['GET', 'POST']
)
app.add_url_rule(
    '/time/<int:id>', view_func=time_view, methods=['GET']
)
