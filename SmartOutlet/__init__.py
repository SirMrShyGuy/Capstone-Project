from flask import Flask

app = Flask(__name__)

from SmartOutlet import routes
