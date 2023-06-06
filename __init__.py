import os

from flask import Flask, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    app.config['UPLOAD_FOLDER'] = 'portfolio/static/images/'
    app.config['MAX_CONTENT_PATH'] = 3*1000*1000
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def home():
        return render_template('home.html')
    
    @app.route('/byon')
    def byon():
        return render_template('byon.html')
    
    @app.route('/converter')
    def converter():
        return render_template('converter.html')
    
    from . import converter
    app.register_blueprint(converter.bp)

    from . import byon
    app.register_blueprint(byon.bp)

    from . import wetube
    app.register_blueprint(wetube.bp)
    
    from . import db
    db.init_app(app)

    return app
