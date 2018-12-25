from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import configparser
import os

#Work with config.ini
config_file = "config.ini"

exist = os.path.isfile(config_file)
config = configparser.ConfigParser()
print(1)

if not exist:
    print(2)
    print("Config file is not found")
    config["DEFAULT"] = {"SECRET_KEY": "we_dont_have_secrets", 
    "SQLALCHEMY_DATABASE_URI": 'sqlite:///site.db'}
    with open(config_file ,"w") as configfile:
        config.write(configfile)
    print("Cofig file was created")
    print("Please change secret key")

config.read(config_file)
default_config = config["DEFAULT"]

app = Flask(__name__)
app.config['SECRET_KEY']=default_config['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = default_config['SQLALCHEMY_DATABASE_URI']
db = SQLAlchemy(app)

from stackex import routes