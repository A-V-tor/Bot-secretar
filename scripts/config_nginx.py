import os
import subprocess

from dotenv import load_dotenv

import nginx

load_dotenv()


def replace_host(host=os.getenv('HOST')):
    """Замена наименования хоста в конфиге nginx."""
    ip_address = subprocess.check_output("hostname -i | awk '{print $2}'", shell=True).decode().strip()

    config = nginx.loadf('nginx/nginx.conf')
    config.children[1].children[2].value = host or ip_address
    nginx.dumpf(config, 'nginx/nginx.conf')


if __name__ == '__main__':
    replace_host()
