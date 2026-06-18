from dotenv import load_dotenv

load_dotenv(override=False)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from yacut.settings import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from yacut import views, api_views, error_handlers
