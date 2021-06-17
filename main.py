from common.config import setup_config

app, db = setup_config('dev')

if __name__ == '__main__':
    app.run()

