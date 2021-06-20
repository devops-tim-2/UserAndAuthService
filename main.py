from os import environ
from common.config import setup_config

if __name__ == '__main__':
    app = setup_config('dev')
    app.run(host=environ.get('FLASK_RUN_HOST'))
