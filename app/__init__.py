from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder
from flask_restful import Api
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__)
api = Api(app)
app.config.from_object(Config)
app.debug = True
app.config['SECRET_KEY'] = str(os.environ.get("APP_SECRET"))
app.config['JWT_SECRET_KEY'] = str(os.environ.get("JWT_SECRET"))
jwt = JWTManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

seeder = FlaskSeeder()
seeder.init_app(app, db)

from app.model import todo, user
from app import routes
