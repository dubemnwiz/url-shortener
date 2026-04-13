import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(env: str | None = None) -> Flask:
    """
    Application factory.

    Parameters
    ----------
    env : str, optional
        One of "development" or "production".  Falls back to the
        FLASK_ENV environment variable, then to "development".
    """
    from config import config_map

    app = Flask(
        __name__,
        # tell Flask to serve files from the top-level static/ folder.
        static_folder=os.path.join(os.path.dirname(__file__), "..", "static"),
        static_url_path="/static",
    )

    # get config from environment variable or default to development
    env = env or os.environ.get("FLASK_ENV", "development")
    app.config.from_object(config_map.get(env, config_map["development"]))

    # binds extensions to app
    db.init_app(app)
    migrate.init_app(app, db)

    # registers url blueprint
    from app.routes import urls_bp
    app.register_blueprint(urls_bp)

    # serve index.html at the root
    from flask import send_from_directory

    @app.route("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    return app
