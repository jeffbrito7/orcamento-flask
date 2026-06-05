# Cloudflare Tunnel para o Orcamento Flask

Este guia coloca o sistema na internet sem abrir porta no roteador. A aplicacao Flask continua rodando localmente em `127.0.0.1:8000`, e o `cloudflared` faz a ponte segura ate a Cloudflare.

## 1. Subir o sistema localmente com Waitress

No PowerShell:

```powershell
cd "C:\Users\CPU JEFF\Documents\GitHub\orcamento-flask"

$env:POSTGRES_HOST="localhost"
$env:POSTGRES_PORT="5432"
$env:POSTGRES_DB="orcamento"
$env:POSTGRES_USER="postgres"
$env:POSTGRES_PASSWORD="sua-senha"
$env:SECRET_KEY="troque-por-uma-chave-grande-e-unica"
$env:APP_VERSION="v1.0"
$env:ORCAMENTO_ADMIN_USER=""
$env:ORCAMENTO_ADMIN_PASSWORD=""

"C:\Users\CPU JEFF\AppData\Local\Programs\Python\Python39\python.exe" -m waitress --host=127.0.0.1 --port=8000 wsgi:app
```

Acesse no proprio computador:

```text
http://127.0.0.1:8000
```

Crie o primeiro acesso pela rota `/cadastro`. Se preferir criar um usuario inicial automaticamente, configure `ORCAMENTO_ADMIN_USER` e `ORCAMENTO_ADMIN_PASSWORD` com valores fortes apenas durante a primeira inicializacao.

## 2. Teste rapido com URL temporaria

Use este caminho para validar com alguem de fora da sua rede:

Se o comando `cloudflared` nao existir no PowerShell, instale primeiro pelo guia oficial de downloads da Cloudflare:

```text
https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/downloads/
```

```powershell
cloudflared tunnel --url http://localhost:8000
```

O terminal vai mostrar uma URL aleatoria em `trycloudflare.com`. Essa URL e temporaria e serve apenas para testes.

## 3. Publicacao com subdominio fixo

Use este caminho quando quiser algo como `orcamento.seudominio.com`.

1. Entre no painel Cloudflare One.
2. Va em `Networks > Connectors > Cloudflare Tunnels`.
3. Clique em `Create a tunnel`.
4. Escolha o conector `Cloudflared`.
5. Dê um nome, por exemplo `orcamento-testes`.
6. Instale e execute o comando que a Cloudflare gerar para o Windows.
7. Em `Published applications`, configure:
   - Subdomain: `orcamento`
   - Domain: seu dominio na Cloudflare
   - Type: `HTTP`
   - URL: `localhost:8000`
8. Salve.

Depois disso, mantenha dois processos ativos no servidor:

- Waitress rodando o Flask em `127.0.0.1:8000`.
- Cloudflared rodando o tunnel.

## 4. Checklist antes de entregar para usuarios externos

- Criar o primeiro usuario pelo `/cadastro`.
- Usar uma `SECRET_KEY` grande e unica.
- Manter `FLASK_DEBUG=false`.
- Nao publicar a porta do PostgreSQL diretamente na internet.
- Fazer backup do PostgreSQL.
- Testar login, lancamentos, importacao e relatorios antes de compartilhar o link.
- Preferir uma politica do Cloudflare Access quando quiser limitar quem pode abrir o sistema.

## Referencias oficiais

- Flask recomenda usar servidor WSGI em producao: https://flask.palletsprojects.com/en/stable/deploying/
- Downloads do cloudflared: https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/downloads/
- Cloudflare Quick Tunnels: https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/do-more-with-tunnels/trycloudflare/
- Cloudflare tunnel gerenciado pelo painel: https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/get-started/create-remote-tunnel/
