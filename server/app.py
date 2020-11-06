from flask import Flask
from api.ping_handler import ping_handler
from api.home_handler import home_handler
from api.mentions_handler import mentions_handler
from dotenv import load_dotenv
load_dotenv()
load_dotenv('.env.local')


app = Flask(__name__)


app.register_blueprint(mentions_handler)
