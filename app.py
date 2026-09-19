# Flask cria o site, request busca informações da internet
from flask import Flask, render_template, request, flash, redirect, session, jsonify, g

# Serve para criptografar as senhas dos usuários
from werkzeug.security import generate_password_hash, check_password_hash 
from livros import busca_livros
from datetime import timedelta
import sqlite3  # Mexe no banco de dados
import requests
import os
import time


app = Flask(__name__)
app.config['SECRET_KEY'] = '8840bf70c075d619b5335aff78220c097c12674ffdaa05bdc81c30bba3979fcc'
app.config['DATABASE'] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'banco_de_dados',
    'biblioteca.db'
)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

# Função para conectar ao banco de dados
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


# Função para fechar conexão
@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    
    if db is not None:
        db.close()  

# Rota para a página inicial
@app.route("/")
def pagina_inicial():
    if 'id' in session:
        db = get_db()

        usuario = db.execute('SELECT * FROM usuarios WHERE id = ?', (session['id'],)).fetchone()

        if usuario:
            return render_template("home.html", email=usuario['email'])
        
    return render_template("home.html")


# Rota que espera dados enviados do formulário
@app.route("/acesso", methods=['POST'])
def acesso():
    email = request.form.get('email')
    senha = request.form.get('senha')
    lembrar_senha = request.form.get('lembrar_senha')
    
    if not email or not senha:
        flash("Preencha o email e a senha.")
        return redirect('/login')
    
    db = get_db()
    usuario = db.execute('SELECT * FROM usuarios WHERE email = ?', (email,)).fetchone()
    
    if usuario and check_password_hash(usuario['senha'], senha):
        session['id'] = usuario['id']
        
        if lembrar_senha == 'sim':
            session.permanent = True
        else:
            session.permanent = False
        return redirect('/home')
    else:
        flash('nome e/ou senha inválidos, tente novamente! ')
        return redirect('/login')
    

# Rota para o formulário de cadastro
@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")


# Rota que processa o formúlario do cadastro
@app.route("/cadastrando", methods=['POST'])
def cadastrando():
    nome_usuario = request.form.get('nome_usuario')
    email = request.form.get('email')
    senha = request.form.get('senha')
    confirmar_senha = request.form.get('confirmar_senha')

    if not nome_usuario or not email or not senha or not confirmar_senha:
        flash("Preencha todos os campos.")
        return redirect('/cadastro')
    
    if len(senha) < 6:
        flash("A senha deve ter pelo menos 6 caracteres.")
        return redirect('/cadastro')
    
    if confirmar_senha != senha:
        flash("As senhas não coincidem.")
        return redirect('/cadastro')

    hash_senha = generate_password_hash(senha)
    db = get_db()

    usuario_existente = db.execute('SELECT id FROM usuarios WHERE email = ?', (email,)).fetchone()
    if usuario_existente:
        flash("Este email já está cadastrado.")
        return redirect('/cadastro')

    cursor = db.execute(
        '''INSERT INTO usuarios(nome_usuario, email, senha) VALUES (?, ?, ?)''', (nome_usuario, email, hash_senha))

    db.commit()

    flash(f'Seja bem vindo a biblioteca, {nome_usuario}!!')
    session['id'] = cursor.lastrowid

    return redirect('/home')


# Rota para saber se o usuário está logado
@app.route("/home")
def home():
    if 'id' in session:
        id_usuario = session["id"]
        db = get_db()
        usuario = db.execute('SELECT * FROM usuarios WHERE id = ?', (id_usuario,)).fetchone()
        if usuario:
            email = usuario['email']
        else:
            return redirect('/')
        return render_template('home.html', email=email)
    else:
        flash('acesso restrito!!')
        return redirect('/')


# Rota que envia os livros para o HTML 
@app.route("/livros")
def pagina_livros():
    if 'id' not in session:
        flash("Você precisa estar logado para acessar os livros.")
        return redirect('/login')

    db = get_db()

    usuario = db.execute('SELECT * FROM usuarios WHERE id = ?', (session['id'],)).fetchone()

    livros = busca_livros(db)

    return render_template("livros.html", livros=livros, email=usuario['email'])


# Função para buscar Capa do livro no API
def busca_capa(titulo, autor, isbn=None):
    url = "https://openlibrary.org/search.json"
    
    titulos_alternativos = {
        "O investidor inteligente": "The Intelligent Investor"
    }

    try:
        # Busca pelo ISBN temporariamente desativada
        if isbn:
            isbn = isbn.replace("-", "").replace(" ", "")

            parametros = {
                "isbn": isbn,
                "fields": "cover_i,edition_key",
                "limit": 5
            }

            resposta = requests.get(
                url,
                params=parametros,
                timeout=30
            )

            resposta.raise_for_status()

            dados = resposta.json()
            
            print(">>> RESULTADO BUSCA ISBN:")
            print(dados)

            for livro in dados.get("docs", []):

                cover_id = livro.get("cover_i")

                if cover_id:
                    return f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"

        titulo_busca = titulos_alternativos.get(titulo, titulo)
        
        print(">>> TITULO ORIGINAL:", titulo)
        print(">>> TITULO USADO NA BUSCA:", titulo_busca)

        # Tenta título + autor
        parametros = {
            "q": f"{titulo_busca} {autor}",
            "fields": "cover_i",
            "limit": 10
        }

        resposta = requests.get(
            url,
            params=parametros,
            timeout=30
        )

        resposta.raise_for_status()

        dados = resposta.json()

        print(">>> RESULTADOS BUSCA TÍTULO + AUTOR:")
        print(dados.get("docs", []))

        for livro in dados.get("docs", []):
            cover_id = livro.get("cover_i")

            if cover_id:
                return f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"

        # Tenta somente pelo título
        parametros = {
            "title": titulo,
            "fields": "cover_i,edition_key",
            "limit": 10
        }

        resposta = requests.get(
            url,
            params=parametros,
            timeout=30
        )

        resposta.raise_for_status()

        dados = resposta.json()

        print(">>> RESULTADOS BUSCA SOMENTE TÍTULO:")
        print(dados.get("docs", []))

        for livro in dados.get("docs", []):

            cover_id = livro.get("cover_i")

            if cover_id:
                return f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"

            edition_keys = livro.get("edition_key", [])

            for edition_key in edition_keys:

                url_edicao = f"https://openlibrary.org/books/{edition_key}.json"

                try:
                    resposta_edicao = requests.get(
                        url_edicao,
                        timeout=30
                    )

                    resposta_edicao.raise_for_status()

                    dados_edicao = resposta_edicao.json()
                    print(">>> DADOS DA EDIÇÃO:", dados_edicao)

                    titulo_edicao = dados_edicao.get("title", "").lower()
                    titulo_original = titulo.lower()

                    if titulo_original not in titulo_edicao and titulo_edicao not in titulo_original:
                        print(">>> EDIÇÃO IGNORADA:", dados_edicao.get("title"))
                        continue
                    
                    if dados_edicao.get("covers"):
                        cover_id = dados_edicao["covers"][0]

                        return f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"

                except requests.RequestException:
                    continue

            work_key = livro.get("key")

            if work_key:
                url_obra = f"https://openlibrary.org{work_key}.json"

                try:
                    resposta_obra = requests.get(
                        url_obra,
                        timeout=30
                    )

                    resposta_obra.raise_for_status()

                    dados_obra = resposta_obra.json()

                    if dados_obra.get("covers"):
                        cover_id = dados_obra["covers"][0]

                        return f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"

                except requests.RequestException:
                    continue
    except requests.RequestException as erro:
            print("ERRO AO BUSCAR CAPA:", erro)
            return None

# Rota que procura livros que não possuem capa
@app.route("/atualizar_capas")
def atualizar_capas():
    print(">>> ENTROU NA ROTA ATUALIZAR_CAPAS")

    db = get_db()

    livros = db.execute("""
        SELECT id, titulo, autor, isbn
        FROM livros
        WHERE capa_url IS NULL OR capa_url = ''
    """).fetchall()

    print(">>> LIVROS SEM CAPA:", len(livros))

    encontrados = 0
    sem_capa = 0

    for livro in livros:

        time.sleep(2)
        
        print(
                ">>> PROCURANDO:",
                livro["titulo"],
                "| AUTOR:",
                livro["autor"],
            )
        capa_url = busca_capa(
            livro["titulo"],
            livro["autor"],
            livro["isbn"]
        )

        print(">>> RESULTADO:", capa_url)

        if capa_url:
            db.execute("""
                UPDATE livros
                SET capa_url = ?
                WHERE id = ?
            """, (
                capa_url,
                livro["id"]
            ))

            encontrados += 1

        else:
            print(
                ">>> SEM CAPA:",
                livro["titulo"],
                "| AUTOR:",
                livro["autor"],
                "| ISBN:",
                livro["isbn"]
            )
            sem_capa += 1

    db.commit()

    print(">>> ENCONTRADAS:", encontrados)
    print(">>> SEM CAPA:", sem_capa)

    return f"""
    <h2>Atualização concluída!</h2>
    <p>{encontrados} capas encontradas.</p>
    <p>{sem_capa} livros continuam sem capa.</p>
    <a href="/livros">Voltar para os livros</a>
    """

    
# Rota que recebe o formulário de livros novos 
@app.route("/cadastrar_livro")
def pagina_cadastrar_livro():
    return render_template("cadastrar_livro.html")


# Rota para cadastro de livros novos 
@app.route("/cadastrar_livro", methods=["POST"])
def cadastrar_livro():

    titulo = request.form.get("titulo")
    autor = request.form.get("autor")
    ano = request.form.get("ano")
    isbn = request.form.get("isbn")
    categoria = request.form.get("categoria")
    qtd = request.form.get("qtd")

    capa_url = busca_capa(titulo, autor, isbn)

    db = get_db()

    db.execute("""
        INSERT INTO livros
        (titulo, autor, ano, isbn, categoria, qtd, capa_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        titulo,
        autor,
        ano,
        isbn,
        categoria,
        qtd,
        capa_url
    ))

    db.commit()

    return redirect("/livros")

# Rota que mostra a página de login
@app.route("/login")
def login():
    return render_template('login.html')


# Rota que apaga os dados da sessão
@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu da sua conta.")
    return redirect('/')


# Rota para pegar os livros que o usuário quer por empréstimo
@app.route("/emprestimo", methods=['POST'])
def emprestimo():
    livro_id = request.form.get('livro_id')
    if not livro_id:
        flash("Livro não informado.")
        return redirect('/livros')
    
    db_livro = get_db() 
    livro = db_livro.execute('SELECT * FROM livros WHERE id = ?', (livro_id,)).fetchone() 
    
    usuario_id = session.get('id')
    if not usuario_id:
        flash("Você precisa estar logado para solicitar um empréstimo.")
        return redirect('/login')
    
    usuario = db_livro.execute('SELECT * FROM usuarios WHERE id = ?',(usuario_id,)).fetchone()
    if not usuario:
        session.clear()
        flash("Usuário não encontrado. Faça login novamente.")
        return redirect('/login')
        
    if livro:
        if livro["qtd"] > 0: 
            db_livro.execute('''
                       INSERT INTO emprestimo(nome_usuario, email, titulo, data_hora_emprestimo, status) VALUES (?, ?, ?, datetime('now'), ?)
                       ''', (usuario["nome_usuario"], usuario["email"], livro["titulo"], "emprestado"))
            
            db_livro.execute('UPDATE livros SET qtd = qtd - 1 WHERE id = ?', (livro_id,))
            
            db_livro.commit()
            flash("Empréstimo realizado com sucesso!")
            return redirect('/livros')
        else:
            flash("Livro indisponível.")
            return redirect('/livros')  
    else:
        flash("Livro não encontrado")
        return redirect('/livros')


# Rota que busca os empréstimos do email logado
@app.route('/meus_emprestimos')
def meus_emprestimos():
    db = get_db()
    usuario_logado = session.get('id')
    
    if not usuario_logado:
        flash("Você precisa estar logado para a devolução de um empréstimo.")
        return redirect('/login')
    
    usuario = db.execute('SELECT * FROM usuarios WHERE id = ?', (usuario_logado,)).fetchone()
    if not usuario:
        session.clear()
        flash("Usuário não encontrado. Faça login novamente.")
        return redirect('/login')
    
    emprestimos = db.execute('SELECT * FROM emprestimo WHERE email = ?',(usuario["email"],)).fetchall()
                    
    return render_template('meus_emprestimos.html', emprestimos=emprestimos, email=usuario['email'])


# Rota da devolução dos empréstimos 
@app.route('/devolucao', methods=['POST'])
def devolucao():
    db = get_db()
    usuario_id = session.get('id')
    if not usuario_id:
        flash("Você precisa estar logado.")
        return redirect('/login')
    
    emprestimo_id = request.form.get('emprestimo_devolucao')
    emprestimo = db.execute('''SELECT * FROM emprestimo WHERE id = ?''',(emprestimo_id,)).fetchone()
    if not emprestimo:
        flash("Empréstimo não encontrado.")
        return redirect('/meus_emprestimos')
    
    usuario = db.execute('SELECT * FROM usuarios WHERE id = ?', (usuario_id,)).fetchone()
    if not usuario:
        session.clear()
        flash("Usuário não encontrado. Faça login novamente.")
        return redirect('/login')
    
    if emprestimo["email"] != usuario["email"]:
        flash("Você não pode devolver este empréstimo")
        return redirect('/meus_emprestimos')
    
    if emprestimo["status"] == "devolvido":
        flash("Este empréstimo já foi devolvido.")
        return redirect('/meus_emprestimos')
    
	
    livro = db.execute('''SELECT * FROM livros WHERE titulo = ?''',(emprestimo["titulo"],)).fetchone()
    if not livro:
        flash("Livro não encontrado.")
        return redirect ('/meus_emprestimos') 
    db.execute(''' UPDATE emprestimo SET data_hora_devolucao = datetime('now'), status = ? WHERE id = ?''', ('devolvido', emprestimo_id,))

    db.execute('UPDATE livros SET qtd = qtd + 1 WHERE id = ?', (livro["id"],))

    db.commit()
    flash("Empréstimo devolvido com sucesso!")
    return redirect('/meus_emprestimos')


# Rota que processa o email para caso de esquecer a senha 
@app.route('/esqueci_senha', methods=['GET', 'POST'])
def esqueci_senha():

    if request.method == 'POST':

        email = request.form.get('email')

        if not email:
            flash("Digite seu email.")
            return redirect('/esqueci_senha')

        db = get_db()

        usuario = db.execute(
            'SELECT * FROM usuarios WHERE email = ?',
            (email,)
        ).fetchone()

        if not usuario:
            flash("Email não encontrado.")
            return redirect('/esqueci_senha')

        session['usuario_reset'] = usuario["id"]

        return render_template('nova_senha.html')

    return render_template("esqueci_senha.html")


# Rota que recebe a nova senha 
@app.route('/nova_senha', methods=['POST'])
def nova_senha():
    usuario_id = session.get('usuario_reset')    
    
    if not usuario_id:
        flash("Solicitação de redefinição de senha inválida.")
        return redirect('/esqueci_senha')
    
    senha = request.form.get('senha')
    confirmar_senha = request.form.get('confirmar_senha')
    
    if len(senha) < 6:
        flash("A senha deve ter pelo menos 6 caracteres.")
        return render_template('nova_senha.html')
    
    if senha != confirmar_senha:
        flash("As senhas não coincidem.")
        return render_template('nova_senha.html')

    hash_senha = generate_password_hash(senha)

    db = get_db()

    db.execute('UPDATE usuarios SET senha = ? WHERE id = ?',(hash_senha, usuario_id))

    db.commit()
    
    session.pop('usuario_reset', None)
    
    flash("Senha alterada com sucesso.")
    return redirect('/login')

# Inicia o servidor 
if __name__ == "__main__":
    app.run(debug=True)