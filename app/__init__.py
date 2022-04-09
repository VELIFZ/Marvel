from flask import Flask
from config import Config

from .blueprints.auth.routes import auth
from .blueprints.api.routes import api

app = Flask(__name__)

app.config.from_object(Config)

app.register_blueprint(auth)
app.register_blueprint(api)

from . import routes
from . import models