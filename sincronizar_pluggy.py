import os
from datetime import datetime

from orcamento_flask_app import inicializar_db, sincronizar_pluggy_transacoes


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, 'logs')
LOG_PATH = os.path.join(LOG_DIR, 'pluggy_sync.log')


def registrar_log(mensagem):
    os.makedirs(LOG_DIR, exist_ok=True)
    agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_PATH, 'a', encoding='utf-8') as arquivo:
        arquivo.write(f'[{agora}] {mensagem}\n')


def main():
    os.chdir(BASE_DIR)
    try:
        inicializar_db()
        total = sincronizar_pluggy_transacoes()
        registrar_log(f'Sincronizacao concluida. {total} transacoes verificadas.')
        print(f'Sincronizacao concluida. {total} transacoes verificadas.')
    except Exception as exc:
        registrar_log(f'Erro na sincronizacao: {exc}')
        raise


if __name__ == '__main__':
    main()
