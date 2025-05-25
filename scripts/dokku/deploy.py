import os
import subprocess

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
os.environ.setdefault('IS_DOKKU', 'True')


pull_res = subprocess.run(['git', 'pull', 'origin', 'main'])

if pull_res.returncode == 0:
    check_db_res = subprocess.run(
        ['dokku', 'postgres:exists', 'bot-secretar'],
        capture_output=True,
        text=True,
    )
    if check_db_res.returncode == 1:
        if 'does not exist' in check_db_res.stderr:
            # первичное развертование, нужно настроить сервис
            subprocess.run(['dokku', 'apps:create', 'bot-secretar'])
            subprocess.run(['dokku', 'postgres:create', 'bot_secretar'])
            subprocess.run(['dokku', 'postgres:link', 'bot_secretar', 'bot-secretar'])

            config_res = subprocess.run(
                ['dokku', 'config', 'bot-secretar'],
                capture_output=True,
                text=True,
            )
            if config_res.returncode == 0 and config_res.stdout:
                config_lines = config_res.stdout.splitlines()
                env_vars = {}
                for line in config_lines:
                    # Пропустить пустые строки и строки без двоеточия
                    if line.strip() and ':' in line:
                        key, value = line.split(':', 1)
                        env_vars[key.strip()] = value.strip()

                database_url = env_vars.get('DATABASE_URL')
                if database_url:
                    # добавление префикса драйвера бд
                    driver = env_vars.get('DB_DRIVER') or 'postgresql+psycopg2'
                    database_url = database_url.split(':', 1)[1]
                    set_db_res = subprocess.run(
                        [
                            'dokku',
                            'config:set',
                            'bot-secretar',
                            f'DATABASE_URL={driver}:{database_url}',
                            'IS_DOKKU=True',
                        ],
                        capture_output=True,
                        text=True,
                    )
                    print('Переменная бд установлена')

                    subprocess.run(
                        ['dokku', 'ports:set', 'bot-secretar', 'http:80:5000'],
                        capture_output=True,
                        text=True,
                    )

                    ip_address = subprocess.check_output("hostname -i | awk '{print $2}'", shell=True).decode().strip()
                    host = os.getenv('HOST') or ip_address
                    subprocess.run(
                        ['dokku', 'domains:add', 'bot-secretar', host],
                        capture_output=True,
                        text=True,
                    )

                    cert_res = subprocess.run(
                        [
                            'dokku',
                            'certs:add',
                            'bot-secretar',
                            'nginx/localhost.crt',
                            'nginx/localhost.key',
                        ],
                        capture_output=True,
                        text=True,
                    )
                    print('Порты и хосты установлены')

if pull_res.returncode == 0:
    push_res = subprocess.run(['git', 'push', '-f', 'dokku', 'main'], capture_output=True, text=True)
    print('stdout (git push):', push_res.stdout)
    print('stderr (git push):', push_res.stderr)

    if push_res.returncode == 0:
        print('<< Сервис обновлен >>')
    else:
        print('Push failed.')

else:
    print('Pull failed, push was not attempted.')
