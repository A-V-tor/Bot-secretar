import os
from src.webapp.wsgi import app

check_environment = os.getenv('FLASK_ENV')
debug_mode = False if check_environment == 'production' else True

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=debug_mode)
