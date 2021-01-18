from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
import configparser
import os

# Work with config.ini
config_file = "config.ini"

exist = os.path.isfile(config_file)
config = configparser.ConfigParser()

if not exist:
    print("Config file is not found")
    config["DEFAULT"] = {"SECRET_KEY": "we_dont_have_secrets",
                         "SQLALCHEMY_DATABASE_URI": 'sqlite:///site.db'}
    with open(config_file, "w") as configfile:
        config.write(configfile)
    print("Config file was created")
    print("Please change secret key")

config.read(config_file)
default_config = config["DEFAULT"]

app = Flask(__name__)
app.config['SECRET_KEY'] = default_config['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = default_config[
    'SQLALCHEMY_DATABASE_URI']
db = SQLAlchemy(app)
moment = Moment(app)


@app.before_first_request
def create_tables():
    db.create_all()


# this import is intentionally put here to avoid circular reference 
from stackex import routes
