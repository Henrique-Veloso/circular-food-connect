from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from servicos import *
import os

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'web'))
app = Flask(__name__, template_folder=template_dir)
app.secret_key = 'super_secret_key_cfc_2025'

USUARIO_ATIVO = None

def obter_usuario_logado():
    return session.get('usuario_ativo', None)

def requer_perfil(tipo: str):
    def decorator(f):
        def decorated_function(*args, **kwargs):
            usuario = obter_usuario_logado()
            if not usuario or usuario.get('tipo') != tipo:
                return redirect(url_for('login_page', erro="Acesso restrito."))
            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__ 
        return decorated_function
    return decorator

@app.route('/')
def index():
    return redirect(url_for('login_page'))

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('loginUsuario.html')

@app.route('/cadastro', methods=['GET'])
def cadastro_page():
    return render_template('cadastrarUsuario.html')

@app.route('/ofertas/listagem', methods=['GET'])
def listagem_ofertas_page():
    if not obter_usuario_logado():
        return redirect(url_for('login_page'))
    return render_template('listaDeProdutos.html', usuario=obter_usuario_logado())

@app.route('/ofertas/cadastro', methods=['GET'])
@requer_perfil('Gerador')
def cadastro_oferta_page():
    return render_template('cadastrarProduto.html', usuario=obter_usuario_logado())

@app.route('/historico', methods=['GET'])
def historico_page():
    if not obter_usuario_logado():
        return redirect(url_for('login_page'))
    return render_template('historicoDeCompras.html', usuario=obter_usuario_logado())

@app.route('/api/login', methods=['POST'])
def api_login():
    credencial = request.form.get('credencial') 
    usuario = obter_usuario_por_credencial(credencial)
    if usuario:
        session['usuario_ativo'] = usuario
        if usuario.get('tipo') == 'Gerador':
            return redirect(url_for('listagem_ofertas_page')) 
        elif usuario.get('tipo') == 'Receptor':
            return redirect(url_for('listagem_ofertas_page')) 
    return render_template('loginUsuario.html', erro="Credencial inválida. Tente novamente.")

@app.route('/api/logout', methods=['GET'])
def api_logout():
    session.pop('usuario_ativo', None)
    return redirect(url_for('login_page'))

@app.route('/api/cadastro_usuario', methods=['POST'])
def api_cadastro_usuario():
    try:
        nome = request.form['nome']
        tipo = request.form['tipo']
        cidade = request.form['cidade']
        criar_usuario_servico(nome, tipo, cidade)
        return redirect(url_for('login_page', sucesso="Cadastro realizado com sucesso!"))
    except Exception as e:
        return render_template('cadastrarUsuario.html', erro=f"Erro no cadastro: {str(e)}")

@app.route('/api/ofertas/ativas', methods=['GET'])
def api_listar_ofertas():
    ofertas = obter_todas_ofertas_ativas()
    return jsonify(ofertas)

@app.route('/api/historico/<user_id>/<user_tipo>', methods=['GET'])
def api_historico_transacoes(user_id, user_tipo):
    if not obter_usuario_logado() or obter_usuario_logado()['id'] != user_id:
        return jsonify({"erro": "Não autorizado"}), 403
    historico = obter_historico_transacoes(user_id, user_tipo)
    return jsonify(historico)

if __name__ == '__main__':
    app.static_folder = os.path.join(template_dir, 'css') 
    app.run(debug=True)