import logging
import logging.handlers
from flask import Flask
from models.db import db


def make_app(config='config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config)

    # LOGGING CONSTANTS
    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler = logging.handlers.RotatingFileHandler(
        app.config['APP_LOG_FILE'], maxBytes=1024 * 1024 * 100, backupCount=20)
    handler.setFormatter(formatter)
    handler.setLevel(app.config['APP_LOG_LEVEL'])
    app.logger.addHandler(handler)
    app.logger.setLevel(app.config['APP_LOG_LEVEL'])

    db.init_app(app)

    return app


if __name__ == "__main__":
    app = make_app('config.py')
    app.run(host='0.0.0.0', port=5000)
