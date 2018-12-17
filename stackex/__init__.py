from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#import requests

app = Flask(__name__)
app.config['SECRET_KEY']='yek_terces'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from stackex import routes