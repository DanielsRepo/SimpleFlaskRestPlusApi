import os

from werkzeug.contrib.fixers import ProxyFix
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api
from flask_migrate import Migrate
from dotenv import load_dotenv


load_dotenv()

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    app.config["DEBUG"] = os.environ["DEBUG"]
    app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
    app.config["RESTPLUS_MASK_SWAGGER"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    user = os.environ["POSTGRES_USER"]
    pwd = os.environ["POSTGRES_PASSWORD"]
    host = os.environ["POSTGRES_HOST"]
    port = os.environ["POSTGRES_PORT"]
    db_name = os.environ["POSTGRES_DB"]

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db_name}"

    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    #     os.path.abspath(os.path.dirname(__file__)), "app.db"
    # )

    from .models import User

    db.init_app(app)
    with app.app_context():
        db.create_all()

    migrate = Migrate(app, db)

    api = Api(
        app=app,
        title="Engineer Test Assignment",
        description="Simple Flask-Restplus API that gives opportunity to \
                    manage data loaded from Random User Generator",
    )

    from .views import user_api

    api.add_namespace(user_api, path="/api/users")

    return app
