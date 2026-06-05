# Plano multiusuario

Objetivo: cada novo usuario deve receber uma base vazia e poder personalizar categorias, pagadores, formas de pagamento, configuracoes, lancamentos e conciliacoes sem enxergar dados de outros usuarios.

## Estado atual

O sistema possui login, cadastro publico em `/cadastro` e isolamento por `usuario_id` nas tabelas de negocio. Novos usuarios entram com a base vazia para configurar seus proprios cadastros.

Tabelas que precisam ser isoladas:

- `categoria`
- `pagador`
- `forma_pagamento`
- `cartao_fatura`
- `configuracao_sistema`
- `lancamento`
- `pluggy_categoria_mapeamento`
- `pluggy_transacao`
- `plano_contas`
- `tipo_operacao_contabil`
- `lancamento_contabil`

## Estrategia recomendada

Usar multi-tenancy por coluna:

- Adicionar `usuario_id NUMBER NOT NULL` nas tabelas de negocio.
- Criar foreign key para `usuario(id)`.
- Migrar dados atuais para o usuario admin existente.
- Todas as consultas, inserts, updates e deletes devem filtrar pelo `usuario_id` da sessao.
- Todas as validacoes de relacionamento precisam verificar se o registro pertence ao usuario logado.

Essa abordagem permite rodar todos os usuarios no mesmo banco, com isolamento logico por aplicacao.

## Cadastro de novos usuarios

Depois da migracao:

1. Criar rota `/cadastro`.
2. Criar usuario com senha hash.
3. Entrar automaticamente ou redirecionar para login.
4. Nao copiar cadastros padrao, para manter a base em branco.
5. Mostrar uma tela inicial de onboarding com atalhos para:
   - Categorias
   - Pagadores
   - Formas de pagamento
   - Configuracoes bancarias
   - Importacao/conciliacao

## Regras obrigatorias de seguranca

- Nunca consultar tabela de negocio sem `usuario_id`.
- Nunca editar/excluir registro sem conferir `usuario_id`.
- Nao usar credenciais Pluggy globais entre usuarios.
- Cada usuario deve ter suas proprias configuracoes em `configuracao_sistema`.
- Relatorios, faturas e importacoes devem respeitar somente dados do usuario logado.

## Ordem de implementacao

1. Criar migracao de schema adicionando `usuario_id`. Concluido.
2. Migrar dados existentes para o primeiro usuario existente. Concluido.
3. Adaptar helpers centrais, como configuracao e validacoes. Concluido.
4. Adaptar cadastros base: categorias, pagadores, formas. Concluido.
5. Adaptar lancamentos e faturas. Concluido.
6. Adaptar relatorios principais e fechamento. Concluido.
7. Adaptar Pluggy/importacoes/conciliador. Concluido.
8. Criar cadastro de usuario. Concluido.
9. Criar testes manuais com dois usuarios:
   - Usuario A cria dados.
   - Usuario B entra e ve base vazia.
   - Usuario B nao consegue acessar URLs de IDs do Usuario A.

## Criterio de pronto

O sistema so deve aceitar usuarios externos quando dois usuarios diferentes puderem usar todas as rotas principais sem compartilhar nenhum dado.
