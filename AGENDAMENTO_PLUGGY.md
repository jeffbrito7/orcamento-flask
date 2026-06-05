# Agendamento da sincronizacao Pluggy

Use este script para buscar novas compras automaticamente e deixar as transacoes pendentes na tela `Integracoes Bancarias`.

## Teste manual

No PowerShell:

```powershell
cd "C:\Users\CPU JEFF\Documents\GitHub\orcamento-flask"

"C:\Users\CPU JEFF\AppData\Local\Programs\Python\Python39\python.exe" "C:\Users\CPU JEFF\Documents\GitHub\orcamento-flask\sincronizar_pluggy.py"
```

Se estiver tudo certo, o terminal mostra a quantidade de transacoes verificadas e grava um log em:

```text
C:\Users\CPU JEFF\Documents\GitHub\orcamento-flask\logs\pluggy_sync.log
```

## Criar tarefa de hora em hora

Execute o PowerShell como Administrador e rode:

```powershell
schtasks /Create /TN "Orcamento Flask - Sincronizar Pluggy" /SC HOURLY /MO 1 /TR "`"C:\Users\CPU JEFF\AppData\Local\Programs\Python\Python39\python.exe`" `"C:\Users\CPU JEFF\Documents\GitHub\orcamento-flask\sincronizar_pluggy.py`"" /ST 08:00 /F
```

Depois disso, o Windows executa a sincronizacao a cada 1 hora.

## Rodar agora pelo Agendador

```powershell
schtasks /Run /TN "Orcamento Flask - Sincronizar Pluggy"
```

## Remover o agendamento

```powershell
schtasks /Delete /TN "Orcamento Flask - Sincronizar Pluggy" /F
```

## Observacoes

- A rotina apenas sincroniza as transacoes da Pluggy.
- Ela nao cria lancamentos automaticamente.
- Transacoes com categoria ja relacionada ficam disponiveis para importacao.
- Transacoes sem relacionamento ficam pendentes ate o usuario configurar a categoria.
- As credenciais podem continuar na tela `Configuracoes`; variaveis de ambiente continuam tendo prioridade quando existirem.
