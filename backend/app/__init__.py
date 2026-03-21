from flask import Flask
from .extensions import init_extensions
from .routes import api_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    init_extensions(app)

    app.register_blueprint(api_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)