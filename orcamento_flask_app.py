from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_FILE = 'orcamento_web.db'

def inicializar_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS categoria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            limite REAL
        )''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS lancamento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            tipo TEXT NOT NULL,
            valor REAL NOT NULL,
            categoria_id INTEGER,
            descricao TEXT,
            FOREIGN KEY (categoria_id) REFERENCES categoria(id)
        )''')
        conn.commit()

@app.route('/')
def index():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM categoria')
        categorias = cursor.fetchall()
    return render_template('index.html', categorias=categorias)

@app.route('/adicionar_categoria', methods=['POST'])
def adicionar_categoria():
    nome = request.form['nome']
    limite = request.form['limite'] or None
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO categoria (nome, limite) VALUES (?, ?)', (nome, limite))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/adicionar_lancamento', methods=['POST'])
def adicionar_lancamento():
    data = request.form['data']
    tipo = request.form['tipo']
    valor = float(request.form['valor'])
    categoria_id = int(request.form['categoria_id'])
    descricao = request.form['descricao']
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO lancamento (data, tipo, valor, categoria_id, descricao)
                          VALUES (?, ?, ?, ?, ?)''',
                       (data, tipo, valor, categoria_id, descricao))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/relatorio')
def relatorio():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.nome, l.tipo, SUM(l.valor), c.limite
            FROM lancamento l
            JOIN categoria c ON l.categoria_id = c.id
            GROUP BY c.nome, l.tipo
        ''')
        resumo = cursor.fetchall()

        cursor.execute('SELECT tipo, SUM(valor) FROM lancamento GROUP BY tipo')
        totais = dict(cursor.fetchall())
        saldo = totais.get('receita', 0) - totais.get('despesa', 0)

    return render_template('relatorio.html', resumo=resumo, saldo=saldo)

if __name__ == '__main__':
    inicializar_db()
    app.run(debug=True)
