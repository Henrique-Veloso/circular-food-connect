from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from servicos import *
import os
from werkzeug.utils import secure_filename
import time

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'web'))
app = Flask(__name__, template_folder=template_dir)
app.secret_key = 'super_secret_key_cfc_2025'

UPLOAD_FOLDER = os.path.join(template_dir, 'img', 'ofertas')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', usuario=obter_usuario_logado())

@app.route('/login', methods=['GET'])
def login_page():
    sucesso = request.args.get('sucesso')
    erro = request.args.get('erro')
    return render_template('loginUsuario.html', sucesso=sucesso, erro=erro)

@app.route('/cadastro', methods=['GET'])
def cadastro_page():
    return render_template('cadastrarUsuario.html')

@app.route('/ofertas/listagem', methods=['GET'])
def listagem_ofertas_page():
    ofertas = obter_todas_ofertas_ativas()
    return render_template('listaDeProdutos.html', usuario=obter_usuario_logado(), ofertas=ofertas)

@app.route('/ofertas/cadastro', methods=['GET'])
@requer_perfil('Gerador')
def cadastro_oferta_page():
    return render_template('cadastrarProduto.html', usuario=obter_usuario_logado())

@app.route('/ofertas/comprar/<oferta_id>', methods=['GET'])
def comprar_produto_page(oferta_id):
    oferta = obter_oferta_por_id(oferta_id)
    if not oferta or oferta.get('status') != 'Ativa':
        return redirect(url_for('listagem_ofertas_page', erro="Oferta não encontrada ou inativa."))
    gerador = obter_usuario_por_credencial(oferta['gerador_id'])
    
    sucesso = request.args.get('sucesso')
    erro = request.args.get('erro')

    return render_template('comprarProduto.html', 
        usuario=obter_usuario_logado(), 
        oferta=oferta, 
        gerador=gerador,
        oferta_id=oferta_id,
        sucesso=sucesso,
        erro=erro
    )

@app.route('/ofertas/editar/<oferta_id>', methods=['GET'])
@requer_perfil('Gerador')
def editar_produto_page(oferta_id):
    return render_template('edicaoProduto.html', usuario=obter_usuario_logado(), oferta_id=oferta_id)

@app.route('/historico', methods=['GET'])
def historico_page():
    if not obter_usuario_logado():
        return redirect(url_for('login_page'))
    
    usuario = obter_usuario_logado()
    historico = obter_historico_transacoes(usuario['id'], usuario['tipo'])
    
    return render_template('historicoDeCompras.html', usuario=usuario, historico=historico)

@app.route('/api/login', methods=['POST'])
def api_login():
    email = request.form.get('email')
    senha = request.form.get('senha')
    usuario = autenticar_usuario(email, senha)
    if usuario:
        session['usuario_ativo'] = usuario
        return redirect(url_for('listagem_ofertas_page'))
    else:
        return render_template('loginUsuario.html', erro="E-mail ou senha inválidos. Tente novamente.")

@app.route('/api/logout', methods=['GET'])
def api_logout():
    session.pop('usuario_ativo', None)
    return redirect(url_for('index'))

@app.route('/api/cadastro_usuario', methods=['POST'])
def api_cadastro_usuario():
    try:
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        tipo = request.form['tipo']
        cidade = request.form['cidade']
        criar_usuario_servico(nome, tipo, cidade, email, senha) 
        return redirect(url_for('login_page', sucesso="Cadastro realizado com sucesso! Faça seu login."))
    except ValueError as e:
        return render_template('cadastrarUsuario.html', erro=f"Erro no cadastro: {str(e)}")
    except Exception as e:
        return render_template('cadastrarUsuario.html', erro=f"Erro inesperado: {str(e)}")

@app.route('/api/cadastro_oferta', methods=['POST'])
@requer_perfil('Gerador')
def api_cadastro_oferta():
    usuario = obter_usuario_logado()
    if not usuario:
        return redirect(url_for('login_page', erro="Faça login para cadastrar uma oferta."))
    
    caminhos_imagens = []
    files = request.files.getlist('imagens')
    
    for i, file in enumerate(files):
        if i >= 3: 
            break
        if file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            unique_filename = f"{usuario['id']}_{int(time.time())}_{i}_{filename}"
            file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            
            try:
                file.save(file_path)
                caminhos_imagens.append(f"img/ofertas/{unique_filename}")
            except Exception as e:
                return render_template('cadastrarProduto.html', usuario=usuario, erro=f"Erro ao salvar arquivo: {str(e)}")
        elif file.filename != '':
             return render_template('cadastrarProduto.html', usuario=usuario, erro="Formato de arquivo não permitido. Use PNG, JPG ou GIF.")

    try:
        gerador_id = usuario['id']
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        quantidade = request.form['quantidade']
        valor_de_venda = request.form['valor_de_venda']
        cidade = request.form['cidade']
        
        criar_oferta_servico(gerador_id, titulo, descricao, quantidade, valor_de_venda, cidade, caminhos_imagens)
        
        return redirect(url_for('listagem_ofertas_page', sucesso="Oferta publicada com sucesso!"))
    except ValueError as e:
        return render_template('cadastrarProduto.html', usuario=usuario, erro=f"Erro de Validação: {str(e)}")
    except Exception as e:
        return render_template('cadastrarProduto.html', usuario=usuario, erro=f"Erro inesperado: {str(e)}")

@app.route('/api/ofertas/comprar/<oferta_id>', methods=['POST'])
def api_compra_oferta(oferta_id):
    usuario = obter_usuario_logado()
    if not usuario:
        return redirect(url_for('login_page', erro="Você precisa estar logado para finalizar uma compra."))

    if usuario.get('tipo') != 'Receptor':
        return redirect(url_for('comprar_produto_page', oferta_id=oferta_id, erro="Apenas usuários Receptores podem realizar esta transação."))

    try:
        quantidade_str = request.form['quantidade_desejada']
        quantidade_desejada = float(quantidade_str)
        if quantidade_desejada <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")

        comprador_id = usuario['id']
        
        resultado = transacao_compra_servico(oferta_id, comprador_id, quantidade_desejada)
        
        if resultado['status'] == 'Removida':
             return redirect(url_for('listagem_ofertas_page', sucesso=f"Compra de {quantidade_desejada} Kg realizada! Oferta foi esgotada."))
        return redirect(url_for('comprar_produto_page', oferta_id=oferta_id, sucesso=f"Compra de {quantidade_desejada} Kg realizada com sucesso! Restam {resultado['restante']} Kg."))

    except ValueError as e:
        return redirect(url_for('comprar_produto_page', oferta_id=oferta_id, erro=f"Erro de Validação: {str(e)}"))
    except Exception as e:
        return redirect(url_for('comprar_produto_page', oferta_id=oferta_id, erro=f"Erro inesperado no servidor: {str(e)}"))


@app.route('/api/ofertas/ativas', methods=['GET'])
def api_listar_ofertas():
    ofertas = obter_todas_ofertas_ativas()
    return jsonify(ofertas)

if __name__ == '__main__':
    app.static_folder = template_dir
    app.static_url_path = '/static'
    app.run(debug=True)