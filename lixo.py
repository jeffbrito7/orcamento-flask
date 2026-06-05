from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import csv
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename

app = Flask(__name__)
DB_FILE = 'orcamento_web.db'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Centralize a conexão
def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    return conn

def inicializar_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categoria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                percentual_orcamento REAL
            )''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pagador (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL
            )''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lancamento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                tipo TEXT NOT NULL,
                valor REAL NOT NULL,
                categoria_id INTEGER,
                descricao TEXT,
                pagador TEXT,
                FOREIGN KEY (categoria_id) REFERENCES categoria(id)
            )''')
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/categorias')
def categorias():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, percentual_orcamento FROM categoria')
    categorias = cursor.fetchall()
    conn.close()
    return render_template('categorias.html', categorias=categorias)

@app.route('/editar_categoria/<int:id>', methods=['GET', 'POST'])
def editar_categoria(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        nome = request.form['nome']
        percentual_orcamento = request.form['percentual_orcamento'] or None
        cursor.execute('UPDATE categoria SET nome = ?, percentual_orcamento = ? WHERE id = ?', (nome, percentual_orcamento, id))
        conn.commit()
        conn.close()
        return redirect(url_for('categorias'))
    else:
        cursor.execute('SELECT * FROM categoria WHERE id = ?', (id,))
        categoria = cursor.fetchone()
        conn.close()
        return render_template('editar_categoria.html', categoria=categoria)

@app.route('/adicionar_categoria', methods=['POST'])
def adicionar_categoria():
    nome = request.form['nome']
    percentual_orcamento = request.form['percentual_orcamento'] or None
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO categoria (nome, percentual_orcamento) VALUES (?, ?)', (nome, percentual_orcamento))
    conn.commit()
    conn.close()
    return redirect(url_for('categorias'))

@app.route('/pagadores')
def pagadores():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pagador')
    pagadores = cursor.fetchall()
    conn.close()
    return render_template('pagadores.html', pagadores=pagadores)

@app.route('/adicionar_pagador', methods=['POST'])
def adicionar_pagador():
    nome = request.form['nome']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO pagador (nome) VALUES (?)', (nome,))
    conn.commit()
    conn.close()
    return redirect(url_for('pagadores'))

@app.route('/lancamentos')
def lancamentos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categoria')
    categorias = cursor.fetchall()
    cursor.execute('SELECT * FROM pagador')
    pagadores = cursor.fetchall()
    cursor.execute('''
        SELECT l.id, l.data, l.tipo, l.valor, l.categoria_id, l.descricao, c.nome, l.pagador
        FROM lancamento l
        JOIN categoria c ON l.categoria_id = c.id
        ORDER BY l.data DESC
    ''')
    lancamentos = cursor.fetchall()
    conn.close()
    return render_template('lancamentos.html', categorias=categorias, pagadores=pagadores, lancamentos=lancamentos)

@app.route('/adicionar_lancamento', methods=['POST'])
def adicionar_lancamento():
    data = request.form['data']
    tipo = request.form['tipo']
    valor_total = float(request.form['valor'])
    categoria_id = int(request.form['categoria_id'])
    pagador = request.form['pagador']
    descricao = request.form['descricao']
    parcelado = request.form.get('parcelado') == 'on'
    parcelas = int(request.form['parcelas']) if parcelado else 1

    conn = get_db_connection()
    cursor = conn.cursor()
    for i in range(parcelas):
        data_parcela = datetime.strptime(data, '%Y-%m-%d') + timedelta(days=30 * i)
        valor_parcela = round(valor_total / parcelas, 2)
        desc = f"{descricao} (Parcela {i+1}/{parcelas})" if parcelado else descricao
        cursor.execute('''
            INSERT INTO lancamento (data, tipo, valor, categoria_id, descricao, pagador)
            VALUES (?, ?, ?, ?, ?, ?)''',
            (data_parcela.strftime('%Y-%m-%d'), tipo, valor_parcela, categoria_id, desc, pagador))
    conn.commit()
    conn.close()
    return redirect(url_for('lancamentos'))

@app.route('/relatorio')
def relatorio():
    competencia = request.args.get('competencia')
    conn = get_db_connection()
    cursor = conn.cursor()
    if competencia:
        cursor.execute('''
            SELECT 
                strftime('%Y-%m', l.data) AS competencia,
                c.nome,
                l.tipo,
                SUM(l.valor),
                c.percentual_orcamento,
                l.pagador
            FROM lancamento l
            JOIN categoria c ON l.categoria_id = c.id
            WHERE strftime('%Y-%m', l.data) = ?
            GROUP BY competencia, c.nome, l.tipo, l.pagador, c.percentual_orcamento
            ORDER BY competencia, c.nome
        ''', (competencia,))
    else:
        cursor.execute('''
            SELECT 
                strftime('%Y-%m', l.data) AS competencia,
                c.nome,
                l.tipo,
                SUM(l.valor),
                c.percentual_orcamento,
                l.pagador
            FROM lancamento l
            JOIN categoria c ON l.categoria_id = c.id
            GROUP BY competencia, c.nome, l.tipo, l.pagador, c.percentual_orcamento
            ORDER BY competencia, c.nome
        ''')
    resumo = cursor.fetchall()
    cursor.execute('SELECT tipo, SUM(valor) FROM lancamento GROUP BY tipo')
    totais = dict(cursor.fetchall())
    receita = totais.get('receita') or 0
    despesa = totais.get('despesa') or 0
    saldo = receita - despesa
    conn.close()
    return render_template('relatorio.html', resumo=resumo, saldo=saldo, competencia=competencia)

@app.route('/relatorio_consolidado')
def relatorio_consolidado():
    competencia = request.args.get('competencia')
    conn = get_db_connection()
    cursor = conn.cursor()
    if competencia:
        cursor.execute('''
            SELECT
                strftime('%Y-%m', l.data) AS competencia,
                c.nome,
                SUM(CASE WHEN l.tipo = 'receita' THEN l.valor ELSE 0 END) AS total_receita,
                SUM(CASE WHEN l.tipo = 'despesa' THEN l.valor ELSE 0 END) AS total_despesa,
                c.percentual_orcamento
            FROM lancamento l
            JOIN categoria c ON l.categoria_id = c.id
            WHERE strftime('%Y-%m', l.data) = ?
            GROUP BY competencia, c.nome, c.percentual_orcamento
            ORDER BY c.nome
        ''', (competencia,))
    else:
        cursor.execute('''
            SELECT
                strftime('%Y-%m', l.data) AS competencia,
                c.nome,
                SUM(CASE WHEN l.tipo = 'receita' THEN l.valor ELSE 0 END) AS total_receita,
                SUM(CASE WHEN l.tipo = 'despesa' THEN l.valor ELSE 0 END) AS total_despesa,
                c.percentual_orcamento
            FROM lancamento l
            JOIN categoria c ON l.categoria_id = c.id
            GROUP BY competencia, c.nome, c.percentual_orcamento
            ORDER BY competencia, c.nome
        ''')

    resumo = cursor.fetchall()
    total_receita = sum(r[2] for r in resumo)
    total_despesa = sum(r[3] for r in resumo)
    conn.close()
    return render_template('relatorio_consolidado.html',
                           resumo=resumo,
                           competencia=competencia,
                           total_receita=total_receita,
                           total_despesa=total_despesa)

@app.route('/excluir_lancamentos', methods=['POST'])
def excluir_lancamentos():
    ids = request.form.getlist('excluir_ids')
    if ids:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.executemany("DELETE FROM lancamento WHERE id = ?", [(i,) for i in ids])
        conn.commit()
        conn.close()
    return redirect('/lancamentos')

@app.route('/importar', methods=['GET', 'POST'])
def importar():
    sucesso = 0
    erros = []
    if request.method == 'POST':
        arquivo = request.files['arquivo']
        if arquivo.filename.endswith('.csv'):
            caminho = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(arquivo.filename))
            arquivo.save(caminho)

            conn = get_db_connection()
            cursor = conn.cursor()

            # Buscar categorias e pagadores existentes
            cursor.execute('SELECT id FROM categoria')
            categorias_existentes = {str(row[0]) for row in cursor.fetchall()}
            cursor.execute('SELECT nome FROM pagador')
            pagadores_existentes = {row[0] for row in cursor.fetchall()}

            with open(caminho, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for i, linha in enumerate(reader, start=2):
                    cat = linha['categoria_id']
                    pag = linha['pagador']
                    if cat not in categorias_existentes:
                        erros.append({'linha': i, 'msg': f"Categoria '{cat}' não cadastrada."})
                        continue
                    if pag not in pagadores_existentes:
                        erros.append({'linha': i, 'msg': f"Pagador '{pag}' não cadastrado."})
                        continue
                    try:
                        cursor.execute('''
                            INSERT INTO lancamento (data, tipo, valor, categoria_id, descricao, pagador)
                            VALUES (?, ?, ?, ?, ?, ?)''',
                            (linha['data'], linha['tipo'], linha['valor'], cat, linha['descricao'], pag))
                        sucesso += 1
                    except Exception as e:
                        erros.append({'linha': i, 'msg': f"Erro ao inserir: {str(e)}"})
            conn.commit()
            conn.close()
            return render_template('importar.html', sucesso=sucesso, erros=erros)
    return render_template('importar.html', sucesso=None, erros=None)

@app.route('/relatorio_planejado')
def relatorio_planejado():
    competencia = request.args.get('competencia')
    conn = get_db_connection()
    cursor = conn.cursor()
    # Total das receitas
    if competencia:
        cursor.execute('SELECT SUM(valor) FROM lancamento WHERE tipo = "receita" AND strftime("%Y-%m", data) = ?', (competencia,))
    else:
        cursor.execute('SELECT SUM(valor) FROM lancamento WHERE tipo = "receita"')
    total_receita = cursor.fetchone()[0] or 0
    # Busca valor gasto por categoria no período
    if competencia:
        cursor.execute('''
            SELECT c.id, c.nome, c.percentual_orcamento, 
                   SUM(CASE WHEN l.tipo="despesa" THEN l.valor ELSE 0 END) as total_gasto
            FROM categoria c
            LEFT JOIN lancamento l ON l.categoria_id = c.id AND strftime("%Y-%m", l.data) = ?
            GROUP BY c.id, c.nome, c.percentual_orcamento
            ORDER BY c.nome
        ''', (competencia,))
    else:
        cursor.execute('''
            SELECT c.id, c.nome, c.percentual_orcamento, 
                   SUM(CASE WHEN l.tipo="despesa" THEN l.valor ELSE 0 END) as total_gasto
            FROM categoria c
            LEFT JOIN lancamento l ON l.categoria_id = c.id
            GROUP BY c.id, c.nome, c.percentual_orcamento
            ORDER BY c.nome
        ''')
    orcamento_categorias = []
    for cid, nome, percentual, gasto in cursor.fetchall():
        valor_planejado = total_receita * (percentual or 0) / 100
        orcamento_categorias.append({
            'categoria': nome,
            'planejado': valor_planejado,
            'realizado': gasto or 0,
            'porcentagem': (gasto / valor_planejado * 100) if valor_planejado else 0
        })
    conn.close()
    return render_template('relatorio_planejado.html', orcamento_categorias=orcamento_categorias, competencia=competencia, total_receita=total_receita)

if __name__ == '__main__':
    inicializar_db()
    app.run(debug=True)
