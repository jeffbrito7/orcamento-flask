# Publicacao do Orcamento Flask

Versao atual: `v1.0`.

Para PythonAnywhere, veja `PYTHONANYWHERE_DEPLOY.md`.
Para liberar cadastro de novos usuarios com base em branco, veja `MULTIUSUARIO.md`.

Este projeto nao deve ser publicado usando `python orcamento_flask_app.py` com `debug=True`.
Para usuarios externos, use um servidor WSGI de producao, configure o banco PostgreSQL e coloque
autenticacao antes de abrir o acesso pela internet.

## Opcao recomendada para comecar

Como o projeto agora usa PostgreSQL, o caminho mais simples e previsivel e usar uma VPS ou plataforma
com banco PostgreSQL gerenciado:

- Python 3.9+
- PostgreSQL local ou externo
- Dependencias do `requirements.txt`
- Um servidor WSGI, como Waitress
- Um proxy HTTPS, como Nginx, Apache, IIS ou Cloudflare Tunnel

## Rodando localmente em modo mais proximo de producao

Instale as dependencias:

```powershell
cd "C:\Users\CPU JEFF\Documents\GitHub\orcamento-flask"
"C:\Users\CPU JEFF\AppData\Local\Programs\Python\Python39\python.exe" -m pip install -r requirements.txt
```

Configure as variaveis do PostgreSQL:

```powershell
$env:POSTGRES_HOST="localhost"
$env:POSTGRES_PORT="5432"
$env:POSTGRES_DB="orcamento"
$env:POSTGRES_USER="postgres"
$env:POSTGRES_PASSWORD="sua-senha"
$env:SECRET_KEY="troque-por-uma-chave-grande-e-unica"
$env:APP_VERSION="v1.0"
$env:ORCAMENTO_ADMIN_USER=""
$env:ORCAMENTO_ADMIN_PASSWORD=""
```

Tambem e possivel usar uma URL unica:

```powershell
$env:DATABASE_URL="postgresql://usuario:senha@host:5432/orcamento"
```

Suba com Waitress:

```powershell
"C:\Users\CPU JEFF\AppData\Local\Programs\Python\Python39\python.exe" -m waitress --host=127.0.0.1 --port=8000 wsgi:app
```

No servidor, acesse:

```text
http://127.0.0.1:8000
```

Para acesso externo sem abrir porta no roteador, veja `CLOUDFLARE_TUNNEL.md`.

## Para acesso externo pela internet

Use uma destas abordagens:

1. VPS em nuvem com dominio e HTTPS.
2. Servidor na sua empresa/casa com redirecionamento de porta, firewall e HTTPS.
3. Cloudflare Tunnel ou VPN, evitando expor diretamente uma porta do roteador. Para esta fase de testes, a recomendacao e Cloudflare Tunnel.

## Antes de abrir para usuarios externos

- Criar o primeiro usuario pelo `/cadastro` ou configurar `ORCAMENTO_ADMIN_USER`/`ORCAMENTO_ADMIN_PASSWORD` com valores fortes apenas durante a primeira inicializacao.
- Trocar o `SECRET_KEY`.
- Trocar senha padrao do PostgreSQL e remover credenciais fixas.
- Usar HTTPS.
- Fazer backup automatico do banco.
- Desligar debug em producao.
- Restringir acesso ao PostgreSQL para nao ficar exposto publicamente.
- Criar um usuario PostgreSQL proprio para a aplicacao.
