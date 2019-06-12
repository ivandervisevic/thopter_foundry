from flask import Flask
from flask_bootstrap import Bootstrap
from server.config import Config

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)

from server import routes