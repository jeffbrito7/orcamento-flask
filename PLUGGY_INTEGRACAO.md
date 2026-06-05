# Integracao Pluggy

Esta integracao sincroniza as despesas do cartao de credito conectado no Pluggy para uma tela de conferencia antes de criar os lancamentos financeiros.

## Tela de configuracao

O sistema possui a tela `Configuracoes`, no menu principal, para cadastrar:

- Client ID
- Client Secret
- Item ID
- Final do cartao
- Forma de pagamento criada automaticamente
- Pagador usado na divisao automatica

O `Client Secret` nao aparece novamente depois de salvo. Para trocar, preencha o campo outra vez.

## Variaveis de ambiente opcionais

Voce tambem pode configurar pelo PowerShell antes de subir o sistema. Variaveis de ambiente tem prioridade sobre a tela:

```powershell
$env:PLUGGY_CLIENT_ID="cole-o-client-id-da-sua-aplicacao"
$env:PLUGGY_CLIENT_SECRET="cole-o-client-secret-da-sua-aplicacao"
$env:PLUGGY_ITEM_ID="cole-o-item-id-ja-conectado"
$env:PLUGGY_CARD_LAST4="4512"
$env:PLUGGY_FORMA_PAGAMENTO_NOME="Cartao de credito Itau 4512"
$env:PLUGGY_PAGADOR_DIVISAO="Juliana e Jefferson"
```

Em producao, prefira manter credenciais sensiveis no ambiente do servidor.

## Como usar

1. Suba o sistema.
2. Acesse `Integracoes Bancarias` no menu Movimento.
3. Clique em `Sincronizar Pluggy`.
4. Confira as categorias recebidas em portugues.
5. Relacione cada categoria recebida com uma categoria ja existente no sistema.
6. Marque `Dividir automaticamente` nas categorias que devem entrar na divisao por pagadores.
7. Selecione as transacoes conferidas e clique em `Importar selecionadas`.

## Sincronizacao automatica

Para buscar novas compras de hora em hora sem depender do botao da tela, use o guia:

```text
AGENDAMENTO_PLUGGY.md
```

Essa rotina apenas sincroniza a Pluggy e deixa as transacoes pendentes para conferencia/importacao. Ela nao cria lancamentos automaticamente.

## Como o sistema evita duplicidade

Cada transacao do Pluggy e salva com o id original em `pluggy_transacao`. Quando uma despesa e importada para `lancamento`, o sistema grava tambem `pluggy_transaction_id`. Em novas sincronizacoes, a despesa nao sera criada novamente.

## Categorias

O Pluggy pode retornar categorias em ingles. O sistema traduz as principais categorias para portugues e deixa o relacionamento pendente quando ainda nao houver categoria do sistema vinculada.

O sistema nao cria categorias novas automaticamente. A ideia e manter seu cadastro de categorias como fonte principal e apenas relacionar o que vem da integracao.

## Divisao por pagadores

Quando uma categoria estiver marcada como `Dividir automaticamente`, o lancamento importado recebe o pagador configurado em `PLUGGY_PAGADOR_DIVISAO`. O formato `Juliana e Jefferson` continua compatível com o relatorio de divisao por pagadores, que divide igualmente pelo `e`.

## Referencias oficiais

- Autenticacao Pluggy: https://docs.pluggy.ai/docs/authentication
- API de transacoes: https://docs.pluggy.ai/docs/transactions
- API de contas: https://docs.pluggy.ai/reference/accounts-list
