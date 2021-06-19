from common.config import setup_config
from os import environ

app, db = setup_config('dev')

if __name__ == '__main__':
    app.run(host=environ.get('FLASK_RUN_HOST'))
