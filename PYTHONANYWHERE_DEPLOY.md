# Deploy no PythonAnywhere

Este projeto usa PostgreSQL via `psycopg2`. Para publicar no PythonAnywhere, use um PostgreSQL acessivel pela aplicacao e configure as credenciais por variaveis de ambiente.

Para abrir o sistema para usuarios externos, primeiro conclua a etapa de isolamento multiusuario descrita em `MULTIUSUARIO.md`.

## Variaveis de ambiente de producao

Configure no ambiente do PythonAnywhere:

```bash
export APP_ENV=production
export APP_VERSION=v1.0
export SECRET_KEY="uma-chave-grande-gerada-com-secrets-token-hex"
export DATABASE_URL="postgresql://usuario:senha@host:5432/orcamento"
export ORCAMENTO_ADMIN_USER=""
export ORCAMENTO_ADMIN_PASSWORD=""
```

Como alternativa ao `DATABASE_URL`, configure `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER` e `POSTGRES_PASSWORD`.

## WSGI

O arquivo `wsgi.py` ja expoe:

```python
application = app
```

No Web tab do PythonAnywhere, aponte o WSGI para importar este projeto. O conteudo equivalente no arquivo WSGI do PythonAnywhere fica assim:

```python
import os
import sys

project_home = '/home/SEU_USUARIO/orcamento-flask'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from wsgi import application
```

## Virtualenv

Crie um virtualenv com a mesma versao Python escolhida na aba Web e instale:

```bash
cd ~/orcamento-flask
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Depois informe o caminho do virtualenv na aba Web do PythonAnywhere.

## Checklist antes de publicar

- `APP_ENV=production`.
- `SECRET_KEY` definida por variavel de ambiente.
- Debug desligado.
- Usuario de banco restrito.
- Backup automatico do banco.
- Isolamento por usuario implementado e testado.
- Pagina de cadastro publico so liberada depois do isolamento.
- Logs revisados no PythonAnywhere apos o primeiro reload.
