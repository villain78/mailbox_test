from flask import Flask
from config import CONFIG

base_path = ''
config_name = ''


def register_blueprint(app, base_path):
    app.register_blueprint("chucexinxi", url_prefix="{}echo".format(base_path))


def create_app():
    app = Flask(__name__)
    app.config.from_object(CONFIG[config_name])
    CONFIG[config_name].init_app(app)
    # api = init_api_handler(**CONFIG)
    # app.config.from_object(api)
    register_blueprint(app, base_path)
    return app


app = create_app()
