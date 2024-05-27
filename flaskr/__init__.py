import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='wekju1hrywo9ie33ryufadsl124kjfadsliyfhwe;tj22dslkjfh4weol4fierw44hf5oihljkyu',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/images')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db, auth, shop
    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(shop.bp)

    app.add_url_rule('/', endpoint='index')

    return app
