from flask import Flask
from flask_cors import CORS

from .utils.log import setup_logger
from .utils.configReader import getConfig

from .controllers import *

'''
    Creating / Configuring the Flask app
'''

# Configuration settings
config = getConfig()
logger = setup_logger('mainlog')

# Flask app
app = Flask(__name__)

# App Configurations
cors = CORS(app)

# Controllers
