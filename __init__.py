from flask import Flask
from blueprints.main.models import init_db


def create_app():
    app = Flask(__name__)

    app.config['TEMPLATES_AUTO_RELOAD'] = True

    init_db(app)

    from blueprints.main.views import main

    app.register_blueprint(main, url_prefix='/')

    return app


if __name__ == '__main__':
    create_app().run(debug=True)
